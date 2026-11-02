from semantic_kernel import Kernel

from agents.document_agent import DocumentAgent
from agents.emi_agent import EMIAgent
from agents.affordability_agent import AffordabilityAgent
from agents.credit_history_agent import CreditHistoryAgent
from agents.underwriting_manager import UnderwritingManager


def test_semantic_kernel_registration():

    kernel = Kernel()

    agents = {
        "DocumentAgent": DocumentAgent(),
        "EMIAgent": EMIAgent(),
        "AffordabilityAgent": AffordabilityAgent(),
        "CreditHistoryAgent": CreditHistoryAgent(),
        "UnderwritingManager": UnderwritingManager()
    }

    for plugin_name, agent in agents.items():
        kernel.add_plugin(
            plugin=agent,
            plugin_name=plugin_name
        )

    print("\nSemantic Kernel Plugin Registration:")

    for plugin_name in agents:
        plugin = kernel.plugins[plugin_name]

        print(f"\n{plugin_name}:")
        for function_name in plugin.functions:
            print(f"- {function_name}")

    assert len(kernel.plugins) == 5

    print("\nSemantic Kernel registration test passed!")


if __name__ == "__main__":
    test_semantic_kernel_registration()