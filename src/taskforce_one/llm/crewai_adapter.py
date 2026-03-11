"""CrewAI LLM Adapter for Task Force One.

Wraps any LangChain-compatible chat model into CrewAI's BaseLLM interface
so it can be natively used by CrewAI agents.
"""

from typing import Any

from crewai.llms.base_llm import BaseLLM
from loguru import logger


class LangChainLLMAdapter(BaseLLM):
    """Wraps a LangChain BaseChatModel into CrewAI's BaseLLM interface."""

    def __init__(self, langchain_llm: Any):
        self._langchain_llm = langchain_llm

    def call(
        self,
        messages: str | list,
        tools: list | None = None,
        callbacks: list | None = None,
        available_functions: dict | None = None,
        from_task: Any = None,
        from_agent: Any = None,
        response_model: Any = None,
    ) -> str:
        """Delegate to the underlying LangChain model."""
        if isinstance(messages, str):
            from langchain_core.messages import HumanMessage
            lc_messages = [HumanMessage(content=messages)]
        else:
            from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
            lc_messages = []
            for m in messages:
                role = m.get("role", "user") if isinstance(m, dict) else getattr(m, "role", "user")
                content = m.get("content", "") if isinstance(m, dict) else getattr(m, "content", "")
                if role == "system":
                    lc_messages.append(SystemMessage(content=content))
                elif role == "assistant":
                    lc_messages.append(AIMessage(content=content))
                else:
                    lc_messages.append(HumanMessage(content=content))

        logger.debug(f"LangChainLLMAdapter calling underlying LLM with {len(lc_messages)} messages")
        response = self._langchain_llm.invoke(lc_messages)
        return response.content if hasattr(response, "content") else str(response)

    async def acall(
        self,
        messages: str | list,
        tools: list | None = None,
        callbacks: list | None = None,
        available_functions: dict | None = None,
        from_task: Any = None,
        from_agent: Any = None,
        response_model: Any = None,
    ) -> str:
        """Async delegate to the underlying LangChain model."""
        if isinstance(messages, str):
            from langchain_core.messages import HumanMessage
            lc_messages = [HumanMessage(content=messages)]
        else:
            from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
            lc_messages = []
            for m in messages:
                role = m.get("role", "user") if isinstance(m, dict) else getattr(m, "role", "user")
                content = m.get("content", "") if isinstance(m, dict) else getattr(m, "content", "")
                if role == "system":
                    lc_messages.append(SystemMessage(content=content))
                elif role == "assistant":
                    lc_messages.append(AIMessage(content=content))
                else:
                    lc_messages.append(HumanMessage(content=content))

        response = await self._langchain_llm.ainvoke(lc_messages)
        return response.content if hasattr(response, "content") else str(response)

    def provider(self) -> str:
        return type(self._langchain_llm).__name__

    def is_litellm(self) -> bool:
        return False

    def supports_stop_words(self) -> bool:
        return False

    def supports_multimodal(self) -> bool:
        return False

    def get_context_window_size(self) -> int:
        return 8192

    def get_token_usage_summary(self):
        from crewai.types.usage_metrics import UsageMetrics
        return UsageMetrics()

    def get_file_uploader(self) -> Any:
        return None

    def format_text_content(self, content: Any) -> str:
        return str(content)
