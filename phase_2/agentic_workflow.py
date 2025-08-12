import os
# from dotenv import load_dotenv

# TODO 1: Import all the agent classes from base_agents
from base_agents import (
    ActionPlanningAgent,
    KnowledgeAugmentedPromptAgent,
    EvaluationAgent,
    RoutingAgent
)

# --- Main Orchestration Script ---
def main():
    """
    Main function to orchestrate the agentic workflow.
    """
    # TODO 2: Load your OpenAI API key from environment variables
    # load_dotenv()
    # openai_api_key = os.getenv("OPENAI_API_KEY")
    # if not openai_api_key:
    #     print("Error: OPENAI_API_KEY not found.")
    #     return

    base_url = "https://openai.vocareum.com/v1"
    api_key = "voc-18896424415987442761856899cdfba587a8.21820406"

    # TODO 3: Load the content of the Product-Spec-Email-Router.txt document
    try:
        with open('Product-Spec-Email-Router.txt', 'r') as f:
            product_spec = f.read()
    except FileNotFoundError:
        print("Error: Product-Spec-Email-Router.txt not found.")
        print("Please create this file and add your product specifications.")
        return

    # --- Starter Prompts and Knowledge (as provided in starter code) ---
    workflow_prompt = "Generate a comprehensive project plan for the Email Router product, including user stories, features, and engineering tasks."
    knowledge_action_planning = "The project plan should be broken down into three main phases: 1. Define user stories. 2. Define product features. 3. Define engineering tasks for implementation."
    
    # Personas
    persona_product_manager = "You are a Product Manager responsible for defining user stories."
    persona_program_manager = "You are a Program Manager responsible for defining product features based on user stories."
    persona_dev_engineer = "You are a Development Engineer responsible for creating detailed engineering tasks from product features."

    # Evaluation Personas
    persona_product_manager_eval = "You are an evaluation agent that checks the answers of other worker agents"
    persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents"
    persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents"
    
    # Knowledge (partially provided, completed in TODO 5)
    knowledge_product_manager = "Base your user stories on the following product specification: "
    knowledge_program_manager = "You are defining features for an Email Router. Base your features on the user stories provided."
    knowledge_dev_engineer = "You are defining engineering tasks for an Email Router. Base your tasks on the features provided."
    
    # --- Agent Instantiation ---

    # TODO 4: Instantiate the Action Planning Agent
    action_planning_agent = ActionPlanningAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        knowledge=knowledge_action_planning
    )

    # --- Product Manager Team ---
    # TODO 5: Complete the Product Manager's knowledge by appending the product_spec
    knowledge_product_manager += product_spec

    # TODO 6: Instantiate the Product Manager's Knowledge Agent
    product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        persona=persona_product_manager,
        knowledge=knowledge_product_manager
    )

    # TODO 7: Instantiate the Product Manager's Evaluation Agent
    pm_evaluation_criteria = "The answer should be stories that follow the following structure: As a [type of user], I want [an action or feature] so that [benefit/value]."
    product_manager_evaluation_agent = EvaluationAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        persona=persona_product_manager_eval,
        evaluation_criteria=pm_evaluation_criteria,
        agent_to_evaluate=product_manager_knowledge_agent
    )

    # --- Program Manager Team ---
    # First, instantiate the KnowledgeAugmentedPromptAgent for the Program Manager
    program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        persona=persona_program_manager,
        knowledge=knowledge_program_manager
    )

    # TODO 8: Instantiate the Program Manager's Evaluation Agent
    prog_m_evaluation_criteria = (
        "The answer should be product features that follow the following structure: "
        "Feature Name: A clear, concise title that identifies the capability\n"
        "Description: A brief explanation of what the feature does and its purpose\n"
        "Key Functionality: The specific capabilities or actions the feature provides\n"
        "User Benefit: How this feature creates value for the user"
    )
    program_manager_evaluation_agent = EvaluationAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        persona=persona_program_manager_eval,
        evaluation_criteria=prog_m_evaluation_criteria,
        agent_to_evaluate=program_manager_knowledge_agent
    )

    # --- Development Engineer Team ---
    # First, instantiate the KnowledgeAugmentedPromptAgent for the Development Engineer
    dev_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        persona=persona_dev_engineer,
        knowledge=knowledge_dev_engineer
    )

    # TODO 9: Instantiate the Development Engineer's Evaluation Agent
    dev_eng_evaluation_criteria = (
        "The answer should be tasks following this exact structure: "
        "Task ID: A unique identifier for tracking purposes\n"
        "Task Title: Brief description of the specific development work\n"
        "Related User Story: Reference to the parent user story\n"
        "Description: Detailed explanation of the technical work required\n"
        "Acceptance Criteria: Specific requirements that must be met for completion\n"
        "Estimated Effort: Time or complexity estimation\n"
        "Dependencies: Any tasks that must be completed first"
    )
    dev_engineer_evaluation_agent = EvaluationAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        persona=persona_dev_engineer_eval,
        evaluation_criteria=dev_eng_evaluation_criteria,
        agent_to_evaluate=dev_engineer_knowledge_agent
    )

    # --- Support Functions (TODO 11) ---
    def product_manager_support_function(query):
        # This function chains the knowledge agent and evaluation agent for the PM
        return product_manager_evaluation_agent.evaluate(query)['final_response']

    def program_manager_support_function(query):
        # This function chains the knowledge agent and evaluation agent for the ProgM
        return program_manager_evaluation_agent.evaluate(query)['final_response']

    def development_engineer_support_function(query):
        # This function chains the knowledge agent and evaluation agent for the DevEng
        return dev_engineer_evaluation_agent.evaluate(query)['final_response']

    # --- Routing Agent (TODO 10) ---
    routing_agent = RoutingAgent(base_url = base_url, 
                                 openai_api_key= api_key)
    routing_agent.agents = [
        {
            "name": "Product Manager",
            "description": "Responsible for defining product personas and user stories only. Does not define features or tasks.",
            "func": product_manager_support_function
        },
        {
            "name": "Program Manager",
            "description": "Responsible for defining product features based on existing user stories.",
            "func": program_manager_support_function
        },
        {
            "name": "Development Engineer",
            "description": "Responsible for defining detailed engineering tasks based on existing product features.",
            "func": development_engineer_support_function
        }
    ]

    # --- Workflow Execution (TODO 12) ---
    print("--- Starting Agentic Workflow for Project Plan Generation ---")
    
    # Get the list of workflow steps from the Action Planning Agent
    workflow_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
    
    # Initialize an empty list for completed steps
    completed_steps = []
    
    # Iterate through the workflow steps
    for i, step in enumerate(workflow_steps):
        print(f"\n--- Processing Step: {step} ---")
        
        # Use the routing agent to invoke the appropriate support function
        result = routing_agent.route(step)
        
        # Append the result to the completed_steps list
        completed_steps.append(result)
        
        # Print the result of the current step
        print("\n--- Result of Step ---")
        print(result)
        print("-" * 25)

    # After processing all steps, print the final output
    print("\n\n--- Final Output of the Workflow ---")
    final_output = completed_steps[-1] if completed_steps else "No output generated."
    print(final_output)
    print("--- Workflow Complete ---")


if __name__ == '__main__':
    main()
