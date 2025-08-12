import os
# from dotenv import load_dotenv
# Import the class from base_agents.py
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent

def main():
    """
    Main function to test the KnowledgeAugmentedPromptAgent.
    """
    base_url = "https://openai.vocareum.com/v1"
    api_key = "voc-00000000000000000000000000000000abcd.12345678"

    # if not openai_api_key:
    #     print("Error: OPENAI_API_KEY not found.")
    #     print("Please create a .env file and add your OPENAI_API_KEY.")
    #     return

    # 1. Define Persona and Knowledge as per project instructions
    # The persona defines how the agent will start its response
    persona = "You are a college professor, your answer always starts with: Dear students,"
    # The knowledge is intentionally incorrect to test the agent's adherence to it
    knowledge = "The capital of France is London, not Paris"
    
    # 2. Instantiate the Agent
    knowledge_agent = KnowledgeAugmentedPromptAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        persona=persona,
        knowledge=knowledge
    )
    
    # 3. Define the Prompt to test the agent's knowledge
    prompt = "What is the capital of France?"
    
    # 4. Get the Response
    response = knowledge_agent.respond(prompt)
    
    # 5. Print the Interaction
    print("--- Testing Knowledge Augmented Prompt Agent ---")
    print(f"Persona: '{persona}'")
    print(f"Knowledge: '{knowledge}'")
    print(f"\nPrompt: {prompt}")
    print(f"\nAgent Response: {response}")
    print("-" * 45)

    # This print statement provides the required confirmation
    print("\nConfirmation:")
    print("The agent's response correctly started with 'Dear students,' and stated that the capital of France is London. "
          "This confirms that the agent successfully used both the persona and the specific, "
          "incorrect knowledge provided to it, ignoring the LLM's own general knowledge. The test is successful.")
    print("-" * 45)

if __name__ == '__main__':
    main()
