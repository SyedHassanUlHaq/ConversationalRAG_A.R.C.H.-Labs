import chainlit as cl
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.document_loaders.json_loader import JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate
import json
import os
from dotenv import load_dotenv

load_dotenv()

# --- Customer Support Prompt Template ---
CUSTOMER_SUPPORT_PROMPT = """You are a friendly and professional customer support representative for A.R.C.H. Labs, a software development company. 

IMPORTANT GUIDELINES:
1. Always assume the person you're talking to is a potential or existing client
2. Be helpful, professional, and enthusiastic about A.R.C.H. Labs services
3. NEVER quote specific prices - always direct pricing questions to contact information
4. When asked about pricing, costs, rates, or budget, respond with: "For accurate pricing tailored to your specific project needs, I'd recommend contacting our team directly at ahsantoufiq@archlabs.tech or +923121359857. They can provide detailed quotes based on your requirements."
5. Use the provided context to answer questions about services, technologies, and capabilities
6. If you don't know something specific, direct them to contact the team for detailed information
7. Be conversational and treat them as valued clients
8. Highlight A.R.C.H. Labs' strengths: custom solutions, AI expertise, automation, full-stack capabilities

Context from A.R.C.H. Labs knowledge base:
{context}

Previous conversation:
{chat_history}

Client question: {question}

Customer Support Response:"""

# --- Optimized for Google AI Free Tier ---
def load_data():
    """Load and process company data with free tier optimizations"""
    documents = []
    try:
        md_loader = DirectoryLoader("./data", glob="**/*.md", loader_cls=TextLoader)
        documents.extend(md_loader.load())
    except Exception as e:
        print(f"Error loading markdown files: {str(e)}")
    
    try:
        for json_file in os.listdir("./data"):
            if json_file.endswith(".json"):
                with open(f"./data/{json_file}") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            documents.append(Document(
                                page_content=str(item),
                                metadata={"source": json_file}
                            ))
                    else:
                        documents.append(Document(
                            page_content=str(data),
                            metadata={"source": json_file}
                        ))
    except Exception as e:
        print(f"Error loading JSON files: {str(e)}")
    
    if not documents:
        raise ValueError("No documents were loaded. Check your data files.")
    
    # Optimized chunk size for free tier
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,  # Smaller chunks for better free tier performance
        chunk_overlap=150
    )
    return text_splitter.split_documents(documents)

def initialize_chain():
    """Initialize the RAG chain optimized for Google AI free tier with customer support persona"""
    splits = load_data()
    if not splits:
        raise ValueError("No documents were loaded.")
    
    # Use free tier embedding model
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004"  # Latest free embedding model
    )
    vectorstore = FAISS.from_documents(splits, embeddings)
    
    # Use Gemini Flash for free tier (faster and more efficient)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",  # Optimized for free tier
        temperature=0.7,
        max_output_tokens=1000,  # Reasonable limit for free tier
        top_p=0.9,
        top_k=40,
    )
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key='answer',
        max_token_limit=4000  # Limit memory to stay within free tier
    )
    
    # Create custom prompt template for customer support
    prompt_template = PromptTemplate(
        template=CUSTOMER_SUPPORT_PROMPT,
        input_variables=["context", "chat_history", "question"]
    )
    
    return ConversationalRetrievalChain.from_llm(
        llm,
        retriever=vectorstore.as_retriever(
            search_kwargs={"k": 4}  # Retrieve more context for better support
        ),
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt_template}
    )

# --- Chainlit event handlers ---
@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session with customer support welcome"""
    try:
        await cl.Message(content="🚀 Connecting you with A.R.C.H. Labs support...").send()
        chain = initialize_chain()
        cl.user_session.set("chain", chain)
        
        welcome_msg = """
## 👋 Hello! Welcome to A.R.C.H. Labs Support

I'm here to help you with any questions about our software development services! 

**🏢 A.R.C.H. Labs specializes in:**
- **Custom Web & Mobile Development** (React, Django, cross-platform apps)
- **AI & Machine Learning Solutions** (TensorFlow, PyTorch, LangChain)
- **Process Automation** (Zapier, n8n, UIPath, Power Automate)
- **Cloud Solutions** (AWS, Azure, Google Cloud)
- **API Development & Integrations**
- **SEO & Performance Optimization**

**💬 I can help you with:**
- Information about our services and capabilities
- Technical questions about our expertise
- Project consultation and next steps
- General inquiries about A.R.C.H. Labs

**📞 Ready to discuss your project?**
- **Email:** ahsantoufiq@archlabs.tech
- **Phone/WhatsApp:** +923121359857

**What would you like to know about our services today?** 🚀
        """
        
        await cl.Message(content=welcome_msg).send()
        
    except Exception as e:
        error_msg = f"""
❌ **I apologize, there seems to be a technical issue with our support system.**

**Please contact our team directly for immediate assistance:**
- **Email:** ahsantoufiq@archlabs.tech  
- **Phone/WhatsApp:** +923121359857

**Error details:** {str(e)}

We'll have this resolved shortly. Thank you for your patience!
        """
        await cl.Message(content=error_msg).send()

@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming messages with customer support approach"""
    chain = cl.user_session.get("chain")
    if not chain:
        await cl.Message(content="""
❌ **I apologize, but I need to reconnect to our support system.**

**Please contact our team directly:**
- **Email:** ahsantoufiq@archlabs.tech
- **Phone/WhatsApp:** +923121359857

Or refresh this page to restart our chat support.
        """).send()
        return
    
    try:
        # Show thinking indicator
        async with cl.Step(name="researching") as step:
            step.output = "Looking up information in our knowledge base..."
            
            # Process the question with customer support context
            result = chain.invoke({"question": message.content})
            
            # Extract response and sources
            response = result["answer"]
            sources = [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]
            
            step.output = f"Found relevant information from our documentation"
        
        # Send main response
        await cl.Message(content=response).send()
        
        # Add helpful footer for complex questions
        if any(keyword in message.content.lower() for keyword in ['price', 'cost', 'quote', 'budget', 'timeline', 'estimate']):
            footer_msg = """
---
💡 **Need more specific information?** Our team can provide detailed estimates and timelines tailored to your project.

**Contact us:**
- **Email:** ahsantoufiq@archlabs.tech
- **Phone/WhatsApp:** +923121359857
            """
            await cl.Message(content=footer_msg).send()
            
    except Exception as e:
        error_msg = f"""
❌ **I apologize for the technical difficulty. Let me connect you with our team directly.**

**For immediate assistance:**
- **Email:** ahsantoufiq@archlabs.tech
- **Phone/WhatsApp:** +923121359857

**You can also ask me to try again, or feel free to ask about:**
- Our services and capabilities
- Technical expertise areas
- General company information

What else would you like to know about A.R.C.H. Labs?
        """
        await cl.Message(content=error_msg).send() 