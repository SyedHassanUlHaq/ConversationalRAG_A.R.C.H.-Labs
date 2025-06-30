from flask import Flask, request, jsonify
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

app = Flask(__name__)

def load_data():
    documents = []
    
    # Load markdown files
    try:
        md_loader = DirectoryLoader("./data", glob="**/*.md", loader_cls=TextLoader)
        documents.extend(md_loader.load())
    except Exception as e:
        print(f"Error loading markdown files: {str(e)}")
    
    # Improved JSON loading
    try:
        # Load each JSON file individually with proper handling
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

# Initialize chain
qa_chain = None
try:
    qa_chain = initialize_chain()
    print("✅ System initialized successfully!")
except Exception as e:
    print(f"❌ Initialization failed: {str(e)}")

@app.route("/chat", methods=["POST"])
def chat():
    if not qa_chain:
        return jsonify({"error": "System not initialized"}), 500
        
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
        
    try:
        result = qa_chain.invoke({"question": user_input})
        return jsonify({
            "response": result["answer"],
            "sources": [doc.metadata["source"] for doc in result["source_documents"]]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)