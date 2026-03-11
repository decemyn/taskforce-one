"""Dynamic LLM Provider for Task Force One.

Provides a generic interface to dynamically load LLM clients
(e.g., from custom enterprise SDKs or LangChain wrappers) based on configuration.
"""

import importlib
from typing import Any

from loguru import logger


class DynamicLLMLoader:
    """Dynamically loads and instantiates LLM classes from external modules."""

    @staticmethod
    def load(provider_module: str, provider_class: str, config: dict[str, Any]) -> Any:
        """Dynamically import and instantiate an LLM provider.

        Args:
            provider_module: The Python module path (e.g., "langchain.chat_models")
            provider_class: The class name to instantiate (e.g., "ChatOpenAI")
            config: A dictionary of kwargs to pass to the class constructor.

        Returns:
            An instantiated LLM object.

        Raises:
            ImportError: If the module cannot be found.
            AttributeError: If the class cannot be found in the module.
            Exception: If instantiation fails.
        """
        try:
            logger.debug(f"Attempting to dynamically load LLM: {provider_module}.{provider_class}")
            module = importlib.import_module(provider_module)
            llm_cls = getattr(module, provider_class)

            # Instantiate the LLM with the provided configuration
            llm_instance = llm_cls(**config)
            logger.info(f"Successfully loaded dynamic LLM instance: {provider_class}")
            return llm_instance

        except ImportError as e:
            logger.error(f"Failed to import module {provider_module}: {e}")
            raise
        except AttributeError as e:
            logger.error(f"Class {provider_class} not found in module {provider_module}: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to instantiate {provider_class} with config {config}: {e}")
            raise
