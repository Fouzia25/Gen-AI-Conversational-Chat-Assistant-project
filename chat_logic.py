"""
chat_logic.py - the "brain" of the chat assistant.

This file has NO web-page code. It only:
  1. Loads settings (API key, model name) from the .env file
  2. Trims the conversation history (short-term memory)
  3. Builds the prompt with LangChain
  4. Sends the prompt to OpenAI and returns the answer
  5. Turns technical errors into friendly messages

Keeping it separate from app.py makes it easy to test.
"""

import os
from dataclasses import dataclass

import openai
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# The "personality" and rules of the assistant. The model sees this first, every time.
SYSTEM_PROMPT = (
    "You are a friendly, helpful assistant. "
    "Give clear, accurate answers in simple language. "
    "Use the earlier messages in this conversation to understand follow-up questions. "
    "If you don't know something, say so honestly."
)

DEFAULT_MODEL = "gpt-6-luna"
DEFAULT_MAX_HISTORY = 10
PLACEHOLDER_KEY = "your-api-key-here"


class MissingAPIKeyError(Exception):
    """Raised when OPENAI_API_KEY is missing from the .env file."""


# ---------------------------------------------------------------------------
# 1. Settings
# ---------------------------------------------------------------------------
@dataclass
class Settings:
    api_key: str
    model: str
    max_history: int


def load_settings() -> Settings:
    """Read settings from the .env file (the key is never printed)."""
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if api_key == PLACEHOLDER_KEY:
        api_key = ""

    model = os.getenv("OPENAI_MODEL", "").strip() or DEFAULT_MODEL

    try:
        max_history = int(os.getenv("MAX_HISTORY_MESSAGES", DEFAULT_MAX_HISTORY))
    except ValueError:
        max_history = DEFAULT_MAX_HISTORY

    return Settings(api_key=api_key, model=model, max_history=max(max_history, 0))


# ---------------------------------------------------------------------------
# 2. Short-term memory: keep only the most recent messages
# ---------------------------------------------------------------------------
def trim_history(messages: list[dict], max_messages: int) -> list[dict]:
    """
    Keep only the last `max_messages` messages.

    Each message is a dict like {"role": "user", "content": "Hi"}.
    If the trimmed list would start with an assistant reply, that reply is
    dropped too, so the memory always starts with a user question.
    """
    if max_messages <= 0:
        return []

    recent = messages[-max_messages:]

    while recent and recent[0]["role"] != "user":
        recent = recent[1:]

    return recent


def to_langchain_messages(messages: list[dict]) -> list:
    """Convert our simple dicts into LangChain message objects."""
    converted = []
    for message in messages:
        if message["role"] == "user":
            converted.append(HumanMessage(content=message["content"]))
        elif message["role"] == "assistant":
            converted.append(AIMessage(content=message["content"]))
    return converted


# ---------------------------------------------------------------------------
# 3. Prompt + model
# ---------------------------------------------------------------------------
def build_prompt() -> ChatPromptTemplate:
    """
    The prompt has three parts, in this order:
      - SystemMessage: the assistant's instructions (fixed)
      - MessagesPlaceholder("history"): the recent conversation (memory)
      - ("human", "{question}"): the new question from the user
    """
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )


def build_model(settings: Settings) -> ChatOpenAI:
    """Create the connection to the OpenAI chat model."""
    if not settings.api_key:
        raise MissingAPIKeyError()

    return ChatOpenAI(
        model=settings.model,
        api_key=settings.api_key,
        timeout=60,
        max_retries=2,
    )


def get_answer(question: str, history: list[dict], settings: Settings) -> str:
    """
    Send the question plus recent history to the model and return its answer.

    `history` should contain only the messages BEFORE this question.
    """
    model = build_model(settings)
    prompt = build_prompt()

    # The "|" joins steps into a chain: fill in the prompt, then send it to the model.
    chain = prompt | model

    recent = trim_history(history, settings.max_history)
    response = chain.invoke(
        {
            "history": to_langchain_messages(recent),
            "question": question,
        }
    )
    return response.text


# ---------------------------------------------------------------------------
# 4. Friendly error messages (never include the key or raw error text)
# ---------------------------------------------------------------------------
def friendly_error_message(error: Exception) -> str:
    """Turn a technical error into a short, safe message for the user."""
    if isinstance(error, MissingAPIKeyError):
        return (
            "🔑 **No API key found.** Copy `.env.example` to `.env`, put your key after "
            "`OPENAI_API_KEY=`, save the file, and restart the app."
        )

    if isinstance(error, openai.AuthenticationError):
        return (
            "🔑 **Your API key was rejected.** Check that the key in `.env` is complete "
            "and hasn't been deleted at platform.openai.com/api-keys, then restart the app."
        )

    if isinstance(error, openai.RateLimitError):
        error_code = getattr(error, "code", None)
        body = getattr(error, "body", None)
        if isinstance(body, dict):
            error_code = error_code or body.get("code")
        if error_code == "insufficient_quota":
            return (
                "💳 **Your OpenAI API account has no credits.** API usage is billed "
                "separately from ChatGPT subscriptions. Add credits at "
                "platform.openai.com → Settings → Billing."
            )
        return "⏳ **Too many requests right now.** Please wait a moment and try again."

    if isinstance(error, openai.PermissionDeniedError):
        return (
            "🚫 **Your account doesn't have access to this model.** Try a different "
            "`OPENAI_MODEL` in `.env` (for example `gpt-6-luna`) and restart the app."
        )

    if isinstance(error, openai.NotFoundError):
        return (
            "🔍 **Model not found.** Check the `OPENAI_MODEL` name in `.env` "
            "and restart the app."
        )

    # APITimeoutError is a kind of APIConnectionError, so this covers both.
    if isinstance(error, openai.APIConnectionError):
        return (
            "🌐 **Couldn't reach OpenAI.** Check your internet connection and try again."
        )

    if isinstance(error, openai.APIStatusError):
        return (
            f"⚠️ **OpenAI returned an error (code {error.status_code}).** "
            "Please try again in a moment."
        )

    return "⚠️ **Something went wrong.** Please try again."
