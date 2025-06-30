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
import json
import os
from dotenv import load_dotenv

load_dotenv()

# --- Data loading and chain initialization (sync, as in app.py) ---
def load_data():
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
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return text_splitter.split_documents(documents)

def initialize_chain():
    splits = load_data()
    if not splits:
        raise ValueError("No documents were loaded.")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(splits, embeddings)
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-latest", temperature=0.7)
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key='answer'
    )
    return ConversationalRetrievalChain.from_llm(
        llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        return_source_documents=True
    )

# --- Chainlit event handlers ---
@cl.on_chat_start
async def on_chat_start():
    chain = initialize_chain()
    cl.user_session.set("chain", chain)
    await cl.Message(content="Hello! I'm your company assistant. Ask me anything about our services, expertise, or company!").send()

@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("chain")
    if not chain:
        await cl.Message(content="System not initialized.").send()
        return
    try:
        result = chain.invoke({"question": message.content})
        sources = [doc.metadata["source"] for doc in result["source_documents"]]
        response = result["answer"]
        await cl.Message(content=response, author="Bot").send()
        if sources:
            await cl.Message(content=f"Sources: {', '.join(sources)}", author="Bot").send()
    except Exception as e:
        await cl.Message(content=f"Error: {str(e)}").send() 