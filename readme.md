# AI-Powered Agentic Workflow for Project Management

This project involves engineering a sophisticated, reusable agentic workflow designed to assist technical project managers (TPMs). The system addresses the challenge of inconsistently transforming brilliant ideas into well-defined user stories, product features, and detailed engineering tasks, a common bottleneck at the client company, InnovateNext Solutions.

The project is developed in two main phases:

1.  **Phase 1: The Agentic Toolkit** - The construction of a robust library of diverse, reusable AI agents.
2.  **Phase 2: The Project Management Workflow** - The deployment of selected agents to build a general-purpose agentic workflow, demonstrated using an "Email Router" product specification as a pilot.

## Project Phases

### Phase 1: The Agentic Toolkit

In this phase, a Python package named `workflow_agents` is created, containing seven meticulously crafted and individually tested agent classes in a single `base_agents.py` file.

The library includes the following agents:

  * `DirectPromptAgent`
  * `AugmentedPromptAgent`
  * `KnowledgeAugmentedPromptAgent`
  * `RAGKnowledgePromptAgent`
  * `EvaluationAgent`
  * `RoutingAgent` 
  * `ActionPlanningAgent`

### Phase 2: The Project Management Workflow Implementation

This phase involves using agents from the Phase 1 library to create a multi-step workflow for technical project management. This workflow is designed to be general-purpose but is piloted with the "Email Router" product specification.

The workflow orchestrates the `ActionPlanningAgent`, `KnowledgeAugmentedPromptAgent`, `EvaluationAgent`, and `RoutingAgent` to break down a high-level goal into sub-tasks, route them to specialized agents, and generate a comprehensively planned project complete with user stories, features, and engineering tasks.

## Agent Library Overview

The core of this project is the library of reusable agents, each with a unique capability:

  * **Direct Prompt Agent**: Offers the most straightforward method for LLM interaction, relaying a user's prompt directly to the model without additional context or tools.
  * **Augmented Prompt Agent**: A specialized agent designed to respond according to a predefined persona.
  * **Knowledge Augmented Prompt Agent**: Designed to incorporate specific, provided knowledge alongside a defined persona when responding to prompts.
  * **RAG Knowledge Prompt Agent**: Uses retrieval-augmented generation for dynamic knowledge sourcing. The code for this agent is provided.
  * **Evaluation Agent**: Assesses responses from another "worker" agent against a given set of criteria, potentially refining the response through iterative feedback.
  * **Routing Agent**: Directs user prompts to the most appropriate specialized agent from a collection based on semantic similarity.
  * **Action Planning Agent**: Uses its provided knowledge to dynamically extract and list the steps required to execute a task described in a user's prompt.

## Directory Structure

The project files are organized as follows:

```
phase_1/
└── workflow_agents/
    ├── __init__.py 
    ├── base_agents.py 
├── direct_prompt_agent.py    # Test script for DirectPromptAgent
├── augmented_prompt_agent.py # Test script for AugmentedPromptAgent
├── knowledge_augmented_prompt_agent.py # Test script for KnowledgeAugmentedPromptAgent
├── rag_knowledge_prompt_agent.py       # Test script for RAGKnowledgePromptAgent
├── evaluation_agent.py       # Test script for EvaluationAgent
├── routing_agent.py          # Test script for RoutingAgent
└── action_planning_agent.py  # Test script for ActionPlanningAgent

phase_2/
└── agentic_workflow.py           # Main script for the project management workflow
```

## Setup & Installation

1.  **Clone the Repository**

    ```sh
    git clone https://github.com/Avneet1710/InnovateNext-AgenticAI.git
    cd InnovateNext-AgenticAI
    ```

2.  **Install Dependencies**
    The project requires the following Python libraries. Install them using `pip`:

    ```sh
    pip install pandas==2.2.3 openai==1.78.1 python-dotenv==1.1.0
    ```

3.  **Configure Environment**

      * Create a file named `.env` in the `tests/` folder (or another appropriate location as per your setup).
      * Add your OpenAI API key to the `.env` file:
        ```
        OPENAI_API_KEY=your_openai_api_key
        ```

## How to Run

### Phase 1: Agent Testing

Each agent in the library has a standalone test script to verify its behavior. To run a test, navigate to the `phase_1` directory and execute the desired script.

**Example:**

```sh
python phase_1/direct_prompt_agent_test.py
```

Run all seven test scripts to ensure each agent functions correctly.

### Phase 2: Running the Agentic Workflow

The main agentic workflow is orchestrated by the `agentic_workflow.py` script. This script uses the agent library to process the `Product-Spec-Email-Router.txt` and generate a full project plan.

**To run the workflow:**

```sh
python phase_2/agentic_workflow.py
```

The script will print the steps as they are processed by the workflow and produce a final, structured output representing the planned project.
