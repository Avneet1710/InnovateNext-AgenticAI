import os
# from dotenv import load_dotenv
# Import the class from base_agents.py
from workflow_agents.base_agents import AugmentedPromptAgent

def main():
    """
    Main function to test the AugmentedPromptAgent.
    """
    base_url = "https://openai.vocareum.com/v1"
    api_key = "voc-00000000000000000000000000000000abcd.12345678" # put your API key here

    # if not openai_api_key:
    #     print("Error: OPENAI_API_KEY not found.")
    #     print("Please create a .env file and add your OPENAI_API_KEY.")
    #     return

    # 1. Define the Persona
    # This persona will guide the agent's tone and style.
    pirate_persona = "a witty, swashbuckling pirate captain who has seen it all"
    
    # 2. Instantiate the Agent
    # Create an instance of the AugmentedPromptAgent with the API key and persona
    augmented_agent = AugmentedPromptAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        persona=pirate_persona
    )
    
    # 3. Define the Prompt
    prompt = "What's the best way to find treasure in the modern world?"
    
    # 4. Get the Response
    # Send the prompt to the agent and store the result.
    augmented_agent_response = augmented_agent.respond(prompt)
    
    # 5. Print the Interaction
    print("--- Testing Augmented Prompt Agent ---")
    print(f"Persona: '{pirate_persona}'")
    print(f"Prompt: {prompt}")
    print("\nAgent Response:")
    # Clearly print the agent's response.
    print(augmented_agent_response)
    print("-" * 35)

    # This print statement provides the required discussion on persona impact
    print("\nExplanatory Comments:")
    print("""
    - Knowledge Source: The agent's response is generated from the vast knowledge of the underlying LLM (gpt-3.5-turbo). It doesn't use external documents but instead synthesizes information from its training data to fit the context of the prompt.
    
    - Persona's Effect on Output: The persona profoundly shapes the agent's output. Instead of a straightforward, factual answer about modern 'treasure hunting' (like investing or finding collectibles), the agent adopts pirate-themed language, metaphors, and a worldview consistent with a 'swashbuckling pirate captain'. This demonstrates how the system prompt successfully guides the LLM to generate a stylized, contextually relevant response.
    """)
    print("-" * 35)

if __name__ == '__main__':
    main()
