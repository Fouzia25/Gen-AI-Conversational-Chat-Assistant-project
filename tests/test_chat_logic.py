"""
Automated tests for chat_logic.py.

These tests do NOT need an API key or internet, and they cost nothing.
Run them with:   python -m pytest
"""

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from chat_logic import (
    MissingAPIKeyError,
    Settings,
    get_answer,
    to_langchain_messages,
    trim_history,
)


def make_conversation(turns: int) -> list[dict]:
    """Build a fake chat: user 1, assistant 1, user 2, assistant 2, ..."""
    messages = []
    for i in range(1, turns + 1):
        messages.append({"role": "user", "content": f"question {i}"})
        messages.append({"role": "assistant", "content": f"answer {i}"})
    return messages


# --- trim_history: the short-term memory limit ---------------------------

def test_short_history_is_kept_unchanged():
    history = make_conversation(2)  # 4 messages
    assert trim_history(history, 10) == history


def test_long_history_keeps_only_the_most_recent_messages():
    history = make_conversation(10)  # 20 messages
    trimmed = trim_history(history, 4)

    assert len(trimmed) == 4
    assert trimmed[0]["content"] == "question 9"
    assert trimmed[-1]["content"] == "answer 10"


def test_trimmed_history_always_starts_with_a_user_message():
    history = make_conversation(5)  # 10 messages
    trimmed = trim_history(history, 3)  # last 3 would start with an assistant reply

    assert trimmed[0]["role"] == "user"
    assert len(trimmed) == 2


def test_zero_limit_means_no_memory():
    assert trim_history(make_conversation(3), 0) == []


def test_empty_history_stays_empty():
    assert trim_history([], 10) == []


def test_trimming_does_not_change_the_original_list():
    history = make_conversation(5)
    original_length = len(history)
    trim_history(history, 2)
    assert len(history) == original_length


# --- Converting to LangChain messages -------------------------------------

def test_roles_become_the_right_langchain_message_types():
    converted = to_langchain_messages(make_conversation(1))

    assert isinstance(converted[0], HumanMessage)
    assert isinstance(converted[1], AIMessage)
    assert converted[0].content == "question 1"


# --- Missing API key -------------------------------------------------------

def test_missing_api_key_raises_a_clear_error_without_calling_openai():
    settings = Settings(api_key="", model="gpt-6-luna", max_history=10)
    with pytest.raises(MissingAPIKeyError):
        get_answer("Hello", [], settings)
