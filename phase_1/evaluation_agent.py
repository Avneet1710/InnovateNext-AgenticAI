import os
# from dotenv import load_dotenv
# Import the required classes from base_agents.py
from workflow_agents.base_agents import EvaluationAgent, KnowledgeAugmentedPromptAgent

def main():
    """
    Main function to test the EvaluationAgent.
    """
    base_url = "https://openai.vocareum.com/v1"
    api_key = "voc-00000000000000000000000000000000abcd.12345678"

    # if not openai_api_key:
    #     print("Error: OPENAI_API_KEY not found.")
    #     print("Please create a .env file and add your OPENAI_API_KEY.")
    #     return

    # 1. Instantiate the Worker Agent
    # This agent is intentionally given incorrect knowledge to test the evaluation loop.
    worker_agent = KnowledgeAugmentedPromptAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        persona="You are a college professor, your answer always starts with: Dear students,",
        knowledge="The capitol of France is London, not Paris" 
    )

    # 2. Define Evaluation Criteria
    # The evaluation agent will check the worker's response against this criterion.
    evaluation_criteria = "The response must correctly identify Paris as the capital of France."

    # 3. Instantiate the Evaluation Agent
    # This agent will manage the evaluation and refinement process.
    evaluation_agent = EvaluationAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        persona="You are a strict fact-checker.",
        evaluation_criteria=evaluation_criteria,
        agent_to_evaluate=worker_agent,
        max_interactions=10 #
    )

    # 4. Define the Prompt
    prompt = "What is the capital of France?" #

    # 5. Get the Evaluated Response
    # This will trigger the iterative evaluation loop.
    final_result = evaluation_agent.evaluate(prompt)

    # 6. Print the Interaction and Results
    print("--- Testing Evaluation Agent ---")
    print(f"Worker Agent's Hardcoded Knowledge: '{worker_agent.knowledge}'")
    print(f"Evaluation Agent's Criteria: '{evaluation_criteria}'")
    print(f"\nInitial Prompt: {prompt}")
    
    print("\n--- Final Evaluation Result ---")
    # Print the resulting evaluation dictionary
    print(f"Final Response: {final_result.get('final_response')}")
    print(f"Final Evaluation: {final_result.get('evaluation')}")
    print(f"Iterations: {final_result.get('iteration_count')}")
    print("-" * 35)

if __name__ == '__main__':
    main()
