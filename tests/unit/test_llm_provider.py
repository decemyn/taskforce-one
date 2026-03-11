"""Unit tests for the dynamic LLM provider."""

import sys
import types

import pytest

from taskforce_one.llm import DynamicLLMLoader


# ── Dummy LLM class used as the test target ───────────────────────────────────

class DummyLLM:
    """A dummy LLM class for testing dynamic loading."""

    def __init__(self, model_name: str, temperature: float = 0.0):
        self.model_name = model_name
        self.temperature = temperature


# ── Fixture: register DummyLLM as a fake importable module ───────────────────

@pytest.fixture(autouse=False)
def dummy_module():
    """Inject a fake 'dummy_llm_module' into sys.modules for the duration of the test.

    This avoids relying on the test file itself being importable via importlib,
    which breaks when the test runner's working directory is not in sys.path.
    """
    module_name = "dummy_llm_module"
    fake_module = types.ModuleType(module_name)
    fake_module.DummyLLM = DummyLLM
    sys.modules[module_name] = fake_module
    yield module_name
    sys.modules.pop(module_name, None)


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_dynamic_loader_success(dummy_module):
    """Test that the dynamic loader can successfully load and instantiate a class."""
    config = {"model_name": "test-model", "temperature": 0.5}

    llm = DynamicLLMLoader.load(
        provider_module=dummy_module,
        provider_class="DummyLLM",
        config=config,
    )

    assert llm.__class__.__name__ == "DummyLLM"
    assert llm.model_name == "test-model"
    assert llm.temperature == 0.5


def test_dynamic_loader_import_error():
    """Test that loading fails with ImportError for a missing module."""
    with pytest.raises(ImportError):
        DynamicLLMLoader.load(
            provider_module="non_existent_module_xyz",
            provider_class="SomeClass",
            config={},
        )


def test_dynamic_loader_attribute_error(dummy_module):
    """Test that loading fails with AttributeError for a missing class."""
    with pytest.raises(AttributeError):
        DynamicLLMLoader.load(
            provider_module=dummy_module,
            provider_class="NonExistentClass",
            config={},
        )


def test_dynamic_loader_instantiation_error(dummy_module):
    """Test that loading fails when invalid config kwargs are provided."""
    with pytest.raises(TypeError):
        DynamicLLMLoader.load(
            provider_module=dummy_module,
            provider_class="DummyLLM",
            config={"invalid_kwarg": "value"},
        )
