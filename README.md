# Gen AI Conversational Chat Assistant

A browser-based chat assistant built with **Python**, **LangChain**, the **OpenAI API**, and **Streamlit**.
It remembers the recent conversation, so you can ask follow-up questions.

## Features

- Chat in your browser with an OpenAI model
- Short-term memory: the last few messages (default 10) are sent with each question
- **New chat** button to clear the conversation
- Loading indicator while the AI is thinking
- Friendly error messages for a missing/invalid API key, no credits, network problems, and other API errors (secrets are never shown)
- Automated tests that run without an API key

## Project files

| File | Purpose |
|---|---|
| `app.py` | The Streamlit web page (chat screen) |
| `chat_logic.py` | The "brain": settings, memory trimming, LangChain prompt, model call, error messages |
| `tests/test_chat_logic.py` | Automated tests (no API key needed) |
| `requirements.txt` | Python packages to install |
| `.env.example` | Settings template (safe to share) |
| `.env` | **Your real API key - private, never commit** |
| `.gitignore` | Keeps `.env` and `.venv` out of Git |
| `pytest.ini` | Test settings |

## Setup (Windows PowerShell)

You need **Python 3.10+** installed. Run these commands in the project folder (for example in VS Code's terminal).

**1. Create and activate a virtual environment**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` at the start of the prompt.
If you get *"running scripts is disabled"*, run this once and try again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**2. Install the packages**

```powershell
python -m pip install -r requirements.txt
```

**3. Add your OpenAI API key**

```powershell
Copy-Item .env.example .env
```

Open `.env` in your editor and replace `your-api-key-here` with your key from
<https://platform.openai.com/api-keys>. Save the file.

> **Note:** The OpenAI API is billed separately from ChatGPT Plus/Pro subscriptions.
> Add credits at platform.openai.com → Settings → Billing.

Optional settings in `.env`:

| Setting | Default | Meaning |
|---|---|---|
| `OPENAI_MODEL` | `gpt-6-luna` | Model to use (`gpt-6-luna`, `gpt-6.1-sol`, `gpt-6-astra`) |
| `MAX_HISTORY_MESSAGES` | `10` | How many recent messages the assistant remembers |

## Run the app

```powershell
streamlit run app.py
```

Your browser opens at <http://localhost:8501>. If it doesn't, open that address yourself.
Keep the terminal open while chatting. Press **Ctrl+C** in the terminal to stop the app.

## Run the tests

```powershell
python -m pytest -v
```

All tests should pass. They don't use the API, so they cost nothing.

## How it works (LangChain)

Each time you send a message, the app builds a prompt with three parts and sends it to OpenAI:

1. **`SystemMessage`**: fixed instructions for the assistant
2. **`MessagesPlaceholder("history")`**: the recent conversation, as `HumanMessage` and `AIMessage` objects
3. **`("human", "{question}")`**: your new question

`ChatPromptTemplate` combines these parts, and `ChatOpenAI` sends them to the model.
They are joined into a chain with `prompt | model`. The conversation is stored in
`st.session_state` and trimmed by `trim_history()` so only recent messages are sent.

## Security

- The API key is read from `.env` with `python-dotenv` and is never printed or shown in the app.
- `.env` and `.venv/` are listed in `.gitignore`, so they are not committed to Git.
- Only `.env.example` (with placeholders) should ever be shared.
