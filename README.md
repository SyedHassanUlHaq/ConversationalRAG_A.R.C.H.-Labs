# Langchain Conversational RAG - Company Portfolio Assistant

A conversational RAG (Retrieval-Augmented Generation) system built with Langchain and Google Gemini AI to answer questions about your company's services, expertise, and information.

## Features

- 🤖 **AI-Powered**: Uses Google Gemini AI for intelligent responses
- 🔍 **RAG System**: Retrieves relevant information from company knowledge base
- 💬 **Conversational**: Maintains conversation context and memory
- 🌐 **Web Interface**: Beautiful Chainlit web interface
- 🔌 **API Support**: REST API endpoints for integration
- 📊 **Multi-format Support**: Handles markdown and JSON data files

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Environment

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Get your Google AI API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

3. Update `.env` with your API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Run the Application

#### Option A: Chainlit Web Interface (Recommended)
```bash
chainlit run chainlit_app.py -w
```

#### Option B: Flask API
```bash
python app.py
```

## Usage

### Web Interface
1. Open your browser to the Chainlit URL (usually `http://localhost:8000`)
2. Start asking questions about the company!

### API Usage
Send POST requests to `http://localhost:5000/chat`:
```json
{
  "message": "What services do you offer?"
}
```

## Data Structure

The system reads from the `data/` folder:
- `about_us.md`: Company information and mission
- `services.md`: Services offered
- `expertise.md`: Technical expertise and capabilities  
- `faqs.json`: Frequently asked questions

## Example Questions

- "What services do you offer?"
- "Tell me about your expertise in cloud computing"
- "What technologies do you use?"
- "What is your company's mission?"
- "Do you provide maintenance services?"

## Technology Stack

- **LangChain**: RAG framework
- **Google Gemini AI**: Language model
- **FAISS**: Vector database for similarity search
- **Chainlit**: Web interface
- **Flask**: REST API
- **Python**: Backend language

## License

This project is for internal company use. 