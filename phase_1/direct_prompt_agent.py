import os
# from dotenv import load_dotenv
# Import the class from base_agents.py
from workflow_agents.base_agents import DirectPromptAgent

def main():
    """
    Main function to test the DirectPromptAgent.
    """
    base_url = "https://openai.vocareum.com/v1"
    api_key = "voc-18896424415987442761856899cdfba587a8.21820406"

    # if not openai_api_key:
    #     print("Error: OPENAI_API_KEY not found.")
    #     print("Please create a .env file and add your OPENAI_API_KEY.")
    #     return

    # 1. Instantiate the Agent
    # Create an instance of the DirectPromptAgent class using the loaded API key
    direct_agent = DirectPromptAgent(
        base_url = base_url, 
        openai_api_key= api_key)
    
    # 2. Define the Prompt
    prompt = "What is the Capital of France?"
    
    # 3. Get the Response
    # Send the prompt to the agent and store the response
    response = direct_agent.respond(prompt)
    
    # 4. Print the Interaction
    print("--- Testing Direct Prompt Agent ---")
    print(f"Prompt: {prompt}")
    print(f"Agent Response: {response}")
    print("-" * 35)

    # This print statement explains the knowledge source as required
    print("Knowledge Source Explanation:")
    print("The agent responded using its general knowledge from the LLM model's training data. "
          "It does not use any external documents, real-time information, or a specific persona. "
          "The response is a direct result of how the 'gpt-3.5-turbo' model answers the question based on its pre-existing information.")
    print("-" * 35)

if __name__ == '__main__':
    main()
