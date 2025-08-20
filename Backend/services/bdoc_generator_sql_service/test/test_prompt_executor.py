"""
Test cases for AsyncSingletonPromptExecutor class.
This module contains unit tests for the AsyncSingletonPromptExecutor class,
which is designed to execute prompts using OpenAI's API with concurrency control.
"""
from unittest.mock import AsyncMock, patch
import pytest

from core.prompt_executor import AsyncSingletonPromptExecutor


@pytest.mark.asyncio
async def test_singleton_instance():
    """
    Test the singleton instance of AsyncSingletonPromptExecutor.
    This test checks if the same instance is returned when multiple instances are created.
    Args:
        None
    Returns:
        None
    """
    inst1 = AsyncSingletonPromptExecutor()
    inst2 = AsyncSingletonPromptExecutor()
    assert inst1 is inst2  # Singleton check


@pytest.mark.asyncio
async def test_init_semaphore():
    """
    Test the initialization of the semaphore in AsyncSingletonPromptExecutor.
    This test checks if the semaphore is initialized with the correct value
    when the init method is called.
    Args:
        None
    Returns:
        None
    """
    executor = AsyncSingletonPromptExecutor()
    await executor.init(max_concurrent_calls=2)
    assert executor._semaphore._value == 2


@pytest.mark.asyncio
@patch("your_module_name.client.chat.completions.create")
async def test_execute_prompt_without_history(mock_create):
    """
    Test executing a prompt without any chat history.
    This test mocks the OpenAI API call and checks if the response is processed correctly.
    It also verifies that the chat history is updated with the assistant's response.

    Args:
        mock_create (AsyncMock): Mocked OpenAI API call.
    Returns:
        None
    """
    mock_response = AsyncMock()
    mock_response.choices = [type("obj", (object,), {
        "message": type("msg", (object,), {"content": "Hello!"})
    })()]
    mock_create.return_value = mock_response

    executor = AsyncSingletonPromptExecutor()
    await executor.init()

    reply, history = await executor.execute_prompt("Hi")
    assert reply == "Hello!"
    assert len(history) == 3
    assert history[-1]['role'] == "assistant"
    assert history[-1]['content'] == "Hello!"


@pytest.mark.asyncio
@patch("your_module_name.client.chat.completions.create")
async def test_execute_prompt_with_history(mock_create):
    """
    Test executing a prompt with existing chat history.
    This test mocks the OpenAI API call and checks if the response is processed correctly.
    It also verifies that the chat history is updated with the assistant's response.
    Args:
        mock_create (AsyncMock): Mocked OpenAI API call.
    Returns:
        None
    """
    mock_response = AsyncMock()
    mock_response.choices = [type("obj", (object,), {
        "message": type("msg", (object,), {"content": "Goodbye!"})
    })()]
    mock_create.return_value = mock_response

    executor = AsyncSingletonPromptExecutor()
    await executor.init()

    history = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]

    reply, updated_history = await executor.execute_prompt("Bye", chat_history=history)
    assert reply == "Goodbye!"
    assert len(updated_history) == 5
