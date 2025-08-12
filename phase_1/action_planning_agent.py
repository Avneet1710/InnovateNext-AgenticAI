import os
# Import the required class from base_agents.py
from workflow_agents.base_agents import ActionPlanningAgent

def main():
    """
    Main function to test the ActionPlanningAgent.
    """

    base_url = "https://openai.vocareum.com/v1"
    api_key = "voc-18896424415987442761856899cdfba587a8.21820406"

    # openai_api_key = os.getenv("OPENAI_API_KEY")
    # if not openai_api_key:
    #     print("Error: OPENAI_API_KEY not found.")
    #     print("Please create a .env file and add your OPENAI_API_KEY.")
    #     return

    # 1. Define Knowledge for the Agent
    # This knowledge helps guide the agent in breaking down tasks.
    knowledge = "The agent should break down a user's request into a clear, numbered list of steps. These steps should be logical and sequential."
    
    # 2. Instantiate the Agent
    # Create an instance of the ActionPlanningAgent with the API key and knowledge.
    action_planner = ActionPlanningAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        knowledge=knowledge
    )
    
    # 3. Define the Prompt
    # This is the high-level task to be broken down.
    prompt = "One morning I wanted to have scrambled eggs" #

    # 4. Get the Action Steps
    # The agent will extract a list of steps from the prompt.
    action_steps = action_planner.extract_steps_from_prompt(prompt)
    
    # 5. Print the Interaction and Results
    print("--- Testing Action Planning Agent ---")
    print(f"Prompt: '{prompt}'")
    
    print("\nExtracted Action Steps:")
    if action_steps:
        # Print the extracted steps in a clean, numbered list.
        for i, step in enumerate(action_steps, 1):
            print(f"{step}")
    else:
        print("No action steps were extracted.")
    print("-" * 35)

if __name__ == '__main__':
    main()
