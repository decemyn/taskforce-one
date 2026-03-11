==================================
Generic Enterprise LLM Integration
==================================

Task Force One allows you to dynamically inject Enterprise or Custom SDK LLM models directly into your CrewAI agents without writing custom Python initialization code. Instead of being tightly coupled to a single vendor, Task Force One dynamically loads your preferred LLM clients using Python's ``importlib`` based on a simple configuration.

Configuration Example
---------------------

In your ``agents.yaml`` file, you can specify an ``llm`` block that tells Task Force One exactly which module to import, which class to instantiate, and what configuration parameters to pass into the class constructor.

Here is an example showing how to configure a generic enterprise SDK integration (such as an internal corporate SDK or a standard LangChain provider):

.. code-block:: yaml

    researcher:
      role: "Senior Enterprise Researcher"
      goal: "Investigate highly complex enterprise datasets."
      backstory: "A seasoned veteran in data intelligence."
      verbose: true
      max_iterations: 3
      allow_delegation: false
      llm:
        provider_module: "enterprise_sdk.integrations.langchain"
        provider_class: "EnterpriseChatModel"
        config:
          model: "provider::model-name"
          temperature: 0.1
          max_tokens: 4000

How It Works
------------

1. **Dynamic Loading:** Task Force One reads the ``llm`` block from your configuration.
2. **Importing:** It executes the equivalent of ``from enterprise_sdk.integrations.langchain import EnterpriseChatModel``.
3. **Instantiation:** It instantiates the model as ``EnterpriseChatModel(model="provider::model-name", temperature=0.1, max_tokens=4000)``.
4. **Injection:** The resulting instantiated LLM object is natively passed to the underlying CrewAI ``Agent`` via its ``llm`` parameter.

If the import or instantiation fails, the system will log a warning and fallback to CrewAI's default LLM configuration.

Requirements
------------

Ensure that the SDK you define in ``provider_module`` is installed in your python environment (e.g., inside your virtual environment or Docker container) prior to starting Task Force One.
