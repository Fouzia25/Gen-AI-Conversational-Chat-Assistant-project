# Gen AI Conversational Chat Assistant

## 1. Project Overview

The **Gen AI Conversational Chat Assistant** is a browser-based AI application built using Python, LangChain, the OpenAI API, and Streamlit.

The application allows users to ask questions, receive AI-generated responses, and continue conversations using short-term conversation memory.

This project demonstrates how different LangChain components work together to build a basic Generative AI application.

## 2. Project Objectives

- Build a conversational AI assistant using Python.
- Understand the basic components of LangChain.
- Connect an OpenAI language model using the OpenAI API.
- Use prompt templates to structure instructions and user messages.
- Implement short-term conversational memory.
- Create an interactive chat interface using Streamlit.
- Learn how to configure API keys securely.
- Run and test a Gen AI application locally.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| LangChain | Manages prompts, messages, and model interactions |
| OpenAI API | Generates AI responses |
| ChatOpenAI | Connects LangChain to an OpenAI chat model |
| Streamlit | Creates the browser-based user interface |
| python-dotenv | Loads environment variables from a `.env` file |
| Pytest | Tests application logic |

## 4. Application Features

- Interactive chat interface.
- AI-generated answers to user questions.
- Short-term conversational memory.
- Context-aware follow-up questions.
- New Chat option to clear the conversation.
- Loading indicator while the assistant generates a response.
- Error handling for missing API keys and API failures.
- Secure API key configuration using environment variables.

**Note:** Conversation memory is temporary and limited to recent messages. It is not permanent storage.

## 5. How the Application Works

1. The user enters a question in the Streamlit chat interface.
2. The application retrieves recent conversation history.
3. LangChain combines the system instructions, conversation history, and new user message.
4. ChatOpenAI sends the messages to the configured OpenAI model.
5. The model generates a response.
6. Streamlit displays the response in the chat interface.
7. The conversation history is updated for subsequent questions.

## 6. Project Structure

```text
GenAI-Chat-Assistant/
│
├── app.py                 # Main application
├── requirements.txt       # Required Python packages
├── .env                   # Private API key configuration
├── .env.example           # Example environment configuration
├── .gitignore             # Files excluded from Git
├── README.md              # Project documentation
│
└── tests/
    └── test_history.py    # Conversation history tests
```

The exact structure may vary slightly depending on the implementation.

## 7. Prerequisites

Before running the application, ensure you have:

- Python installed.
- Visual Studio Code installed.
- Claude Code installed and configured, if using it to develop the project.
- An OpenAI API key.
- An internet connection.
- API access and available billing or credits for your selected OpenAI model.

**Important:** ChatGPT subscriptions and OpenAI API usage are separate. A ChatGPT subscription does not automatically provide API credits.

## 8. Installation and Setup

### Step 1: Open the Project

Open the project folder in Visual Studio Code.

Open the integrated terminal using:

**Terminal → New Terminal**

### Step 2: Create a Virtual Environment

Run:

```powershell
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

The terminal should display `(.venv)` when the environment is activated.

### Step 4: Install Dependencies

Run:

```powershell
python -m pip install --upgrade pip
```

Then install the required packages:

```powershell
python -m pip install -r requirements.txt
```

### Step 5: Configure the OpenAI API Key

Create a file named `.env` in the project root directory.

Add your own API key locally:

```dotenv
OPENAI_API_KEY=your_actual_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

Replace the placeholder with your valid API key.

Use a model that is currently supported and available to your API account.

**Security:** Never upload the real `.env` file to GitHub or share your API key in screenshots, source code, or public repositories.

## 9. Run the Application

After completing the setup, run:

```powershell
python -m streamlit run app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser to use the chat assistant.

Keep the terminal running while you use the application.

To stop the application, press `Ctrl + C` in the terminal.

## 10. Test the Application

### Test 1: Normal Question

Enter:

```text
What is Generative AI?
```

Expected result: The assistant generates an appropriate response.

### Test 2: Conversational Memory

First enter:

```text
My name is Sara, and I am learning Python.
```

Then enter:

```text
What is my name, and what am I learning?
```

Expected result: The assistant identifies Sara and Python using the recent conversation history.

### Test 3: New Chat

Click the New Chat button.

Expected result: The previous conversation is cleared from the current session.

### Test 4: Error Handling

Test the application with a missing or invalid API key in a safe local configuration.

Expected result: The application displays a helpful error without exposing credentials.

### Test 5: Automated Tests

Run:

```powershell
python -m pytest -v
```

Expected result: The automated tests execute and report whether they pass or fail.

## 11. Understanding the LangChain Components

### ChatOpenAI

Connects the application to an OpenAI chat model.

### ChatPromptTemplate

Structures the instructions and messages that will be sent to the model.

### SystemMessage

Defines the assistant's role, behavior, and response instructions.

### HumanMessage

Represents a message submitted by the user.

### Conversation History

Stores a limited number of recent messages and supplies them to the model so it can respond to follow-up questions.

### invoke()

Sends the prepared messages to the model and returns the response.

## 12. Security Best Practices

- Store the API key in `.env`.
- Load secrets using environment variables.
- Add `.env` to `.gitignore`.
- Never commit API keys to GitHub.
- Keep API keys out of browser-side code.
- Do not print or log secret values.
- Rotate the key if it is accidentally exposed.
- Monitor API usage and configure spending limits where available.

## 13. Current Limitations

- Requires an internet connection to call the OpenAI API.
- API usage may incur charges.
- Responses depend on the selected model.
- Conversation memory is temporary and limited to recent messages.
- The application does not provide permanent conversation storage.
- The local URL is normally accessible only from the same computer unless additional network or deployment configuration is provided.

## 14. Future Enhancements

Possible improvements include:

- Persistent conversation history.
- Multiple conversation sessions.
- User authentication.
- Streaming responses.
- PDF document question answering using Retrieval-Augmented Generation (RAG).
- Chat export functionality.
- Deployment to a cloud hosting platform.
- Usage tracking and analytics.

## 15. Learning Outcomes

By completing this project, I will understand how to:

- Build a basic Generative AI application.
- Integrate an OpenAI model using LangChain.
- Structure prompts and chat messages.
- Implement short-term conversational memory.
- Create a chat interface with Streamlit.
- Configure environment variables securely.
- Test and troubleshoot a Python application.

## Conclusion

This project provides a practical introduction to building a Generative AI conversational assistant using Python, LangChain, OpenAI, and Streamlit.

It demonstrates the fundamental workflow of accepting user input, preparing messages, calling a language model, maintaining recent conversation context, and displaying AI-generated responses in a web interface.

