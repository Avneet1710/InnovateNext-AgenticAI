import os
# from dotenv import load_dotenv
# Import the required classes from base_agents.py
from workflow_agents.base_agents import RoutingAgent, KnowledgeAugmentedPromptAgent

def main():
    """
    Main function to test the RoutingAgent.
    """
    base_url = "https://openai.vocareum.com/v1"
    api_key = "voc-18896424415987442761856899cdfba587a8.21820406"

    # if not openai_api_key:
    #     print("Error: OPENAI_API_KEY not found.")
    #     print("Please create a .env file and add your OPENAI_API_KEY.")
    #     return

    # 1. Instantiate Specialized Agents
    # Each agent has a specific knowledge domain.
    texas_agent = KnowledgeAugmentedPromptAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        persona="You are a Texas history expert.",
        knowledge="Rome, Texas, is a small unincorporated community in Smith County."
    )
    
    europe_agent = KnowledgeAugmentedPromptAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        persona="You are a European history expert.",
        knowledge="Rome, Italy, is the capital city of Italy, famous for its ancient history and the Roman Empire."
    )

    math_agent = KnowledgeAugmentedPromptAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        persona="You are a math tutor who is great at word problems.",
        knowledge="To solve this, multiply the number of stories by the days per story."
    )

    # 2. Instantiate the Routing Agent
    routing_agent = RoutingAgent(base_url = base_url,
                                 openai_api_key= api_key)

    # 3. Define Agent Functions/Lambdas and Descriptions
    # The 'description' is crucial as it's used for semantic routing.
    routing_agent.agents = [{
            "name": "Texas History Agent",
            "description": "Specializes in questions about Texas history and geography.",
            "func": lambda prompt: texas_agent.respond(prompt)
        },
        {
            "name": "European History Agent",
            "description": "Specializes in questions about European history and geography.",
            "func": lambda prompt: europe_agent.respond(prompt)
        },
        {
            "name": "Math Problem Agent",
            "description": "Specializes in solving mathematical word problems.",
            "func": lambda prompt: math_agent.respond(prompt)
        }
    ]

    # 4. Test Routing with Prompts
    # These prompts are designed to trigger different routes.
    prompts_to_test = [
        "Tell me about the history of Rome, Texas",
        "Tell me about the history of Rome, Italy",
        "One story takes 2 days, and there are 20 stories"
    ]

    print("--- Testing Routing Agent ---")

    for prompt in prompts_to_test:
        print(f"\nRouting Prompt: '{prompt}'")
        # The route() method determines the best agent and gets its response.
        response = routing_agent.route(prompt)
        print(f"Agent Response: {response}")
        print("-" * 30)


if __name__ == '__main__':
    main()
