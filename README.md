# 🤖 AdSparkX Customer Support Agent

An intelligent, multi-persona customer support chatbot that adapts responses based on user type and conversation context. Built with Streamlit, HuggingFace, and Google Gemini AI.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

AdSparkX Support Agent is an AI-powered customer support system that provides personalized assistance by:
- **Detecting user personas** (Technical Expert, Frustrated User, Business Executive, General User)
- **Classifying intent** (Login issues, API errors, billing disputes, etc.)
- **Searching knowledge base** for instant answers
- **Using AI agents** when KB doesn't have answers
- **Escalating to humans** when issues are complex or urgent

## ✨ Key Features

### 🎭 Multi-Persona Support
Adapts communication style based on customer type:
- **Technical Expert**: Precise, technical language with code examples
- **Frustrated User**: Empathetic, apologetic, solution-focused
- **Business Executive**: Professional, ROI-focused, business impact
- **General User**: Friendly, clear, jargon-free

### 🧠 Context-Aware Conversations
- Maintains conversation history throughout the session
- Uses context for better persona/intent detection
- Generates coherent multi-turn responses
- Remembers previous issues for follow-up questions

### 📚 Three-Tier Response System
1. **Knowledge Base Search** - Instant answers from structured KB
2. **AI Agent (Gemini)** - Generates responses when KB doesn't have answers
3. **Human Escalation** - Routes complex issues to appropriate teams

### 🚨 Smart Escalation Logic
Automatically escalates when:
- Legal or regulatory threats detected
- Frustrated user with repeated issues
- High-value business matters
- User explicitly requests human agent

## 🏗️ Architecture

```
User Input
    ↓
Persona Detection (HuggingFace)
    ↓
Intent Classification (HuggingFace)
    ↓
Context Update
    ↓
Should Escalate?
    ├── YES → Human Agent Assignment
    └── NO → KB Search
              ├── Found → Adapt Tone → Response
              └── Not Found → AI Agent (Gemini) → Adapt Tone → Response
```

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip
- Git

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/ramanakurva164/persona_agent.git
cd persona_agent
```

2. **Create virtual environment**
```bash
python -m venv personaenv
```

3. **Activate virtual environment**
```bash
# Windows
personaenv\Scripts\activate

# Linux/Mac
source personaenv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Create `.env` file

Create a `.env` file in the root directory:

```plaintext
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# HuggingFace Token (optional - for premium models)
HF_TOKEN=your_huggingface_token_here
```

### 2. Get API Keys

**Gemini API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste into `.env`

**HuggingFace Token (Optional):**
1. Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)
2. Create a new token
3. Copy and paste into `.env`

### 3. Customize Knowledge Base

Edit [`adsparkx_kb.txt`](adsparkx_kb.txt ) to add your own support articles:

```plaintext
---ARTICLE---
Title: Your Article Title
Summary: Brief description of the issue
Steps:
1. First step to resolve
2. Second step to resolve
3. Third step to resolve
Possible causes:
- Cause one
- Cause two
Tags: keyword1, keyword2, keyword3
```

## 🎮 Usage

### Run the Application

```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Chat Interface

1. **Enter your name** in the input field
2. **Ask your question** in the chat input
3. **View the response** with adapted tone and relevant information
4. **Continue the conversation** - the agent remembers context

### Example Interactions

**Technical Expert:**
```
User: "Our API integration is throwing 504 errors on /v1/campaigns endpoint"
Agent: "Root cause analysis: Gateway timeout indicates backend service overload. 
        Execute diagnostic: curl -v https://api.adsparkx.com/health..."
```

**Frustrated User:**
```
User: "I can't login and I need access NOW!"
Agent: "I'm really sorry for the trouble! 😔 Let's get you back in right away:
        1. Click 'Forgot Password' on the login page..."
```

**Business Executive:**
```
User: "What's your enterprise pricing?"
Agent: "Our Enterprise tier offers custom SLA with dedicated support. 
        Pricing scales with volume: 10K-50K events/month..."
```

## 📁 Project Structure

```
persona_agent/
├── main.py                    # Main Streamlit application
├── persona_detector.py        # Persona detection (HuggingFace)
├── intent_detector.py         # Intent classification (HuggingFace)
├── kb_manager.py              # Knowledge base loader & retrieval
├── ai_agent.py                # Gemini AI response generation
├── escalator.py               # Human escalation logic
├── responder.py               # Tone adaptation based on persona
├── utils.py                   # Logging utilities
├── adsparkx_kb.txt            # Knowledge base articles
├── requirements.txt           # Python dependencies
├── .env                       # API keys (not in git)
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🔧 How It Works

### 1. Persona Detection
Uses HuggingFace's `Mistral` model to classify users into:
- Technical Expert
- Frustrated User
- Business Executive
- General User

Fallback: Keyword-based classification

### 2. Intent Classification
Classifies user queries into:
- `login_issue`
- `payment_issue`
- `api_error`
- `billing_dispute`
- `feature_request`
- `performance_issue`
- `integration_issue`
- `general_query`

### 3. Knowledge Base Retrieval
- Parses structured KB articles
- Calculates similarity scores using `difflib`
- Boosts score if intent matches article tags
- Returns best match if confidence > 0.25

### 4. AI Agent Response
When KB doesn't have an answer:
- Builds context from last 5 conversations
- Sends to Google Gemini (`gemini-2.0-flash-exp`)
- Generates contextual, persona-aware response

### 5. Tone Adaptation
Transforms responses based on persona:
- **Technical**: Precise, technical terminology
- **Frustrated**: Empathetic, apologetic
- **Executive**: Professional, business-focused
- **General**: Friendly, simple language

### 6. Escalation Logic
Routes to human agents based on:
- Urgency keywords (legal, lawsuit)
- Repeated issues by frustrated users
- High-value business matters
- Explicit escalation requests

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)** - Web interface
- **[HuggingFace Inference API](https://huggingface.co/)** - Persona & intent detection
- **[Google Gemini AI](https://ai.google.dev/)** - AI response generation
- **[Python-dotenv](https://pypi.org/project/python-dotenv/)** - Environment variable management
- **difflib** - Text similarity matching
- **re** - Regular expressions for KB parsing

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Venkata Ramana** - [GitHub](https://github.com/ramanakurva164)

## 🙏 Acknowledgments

- HuggingFace for inference API
- Google for Gemini AI
- Streamlit for the amazing framework

## 📞 Support

For questions or issues:
- **Email**: support@adsparkx.com
- **Issues**: [GitHub Issues](https://github.com/ramanakurva164/persona_agent/issues)

---

⭐ **Star this repo** if you find it helpful!
