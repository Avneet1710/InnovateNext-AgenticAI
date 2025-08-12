import os
from openai import OpenAI
import numpy as np

# Helper function for cosine similarity, used by the RoutingAgent
def cosine_similarity(v1, v2):
    """Calculates the cosine similarity between two vectors."""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    # Handle potential zero norm case
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return dot_product / (norm_v1 * norm_v2)

# ==============================================================================
# 1. Direct Prompt Agent
# ==============================================================================
class DirectPromptAgent:
    """
    An agent that interacts with an LLM by sending a prompt directly.
    """
    def __init__(self, base_url, openai_api_key):
        """
        Initializes the agent with an OpenAI API key.
        """
        self.base_url = base_url
        self.openai_api_key = openai_api_key
        # Instantiate the OpenAI client
        self.client = OpenAI(base_url = self.base_url, 
                             api_key=self.openai_api_key)

    def respond(self, prompt):
        """
        Sends the user prompt directly to the LLM and returns the text response.
        """
        # Call the OpenAI API using the gpt-3.5-turbo model
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                # Pass the user's prompt directly as a user message.
                # Do not include a system prompt.
                {"role": "user", "content": prompt}
            ]
        )
        # Return only the text content of the LLM's response. [cite: 212]
        return response.choices[0].message.content

# ==============================================================================
# 2. Augmented Prompt Agent
# ==============================================================================
class AugmentedPromptAgent:
    """
    A specialized agent that responds according to a predefined persona.
    """
    def __init__(self, base_url, persona, openai_api_key):
        """
        Initializes the agent with an API key and a persona.
        """
        self.base_url = base_url
        self.openai_api_key = openai_api_key
        # Create an attribute to store the agent's persona.
        self.persona = persona
        self.client = OpenAI(base_url = self.base_url, 
                             api_key=self.openai_api_key)

    def respond(self, prompt):
        """
        Sends a prompt to the LLM with a system message to set the persona.
        """
        # Call the OpenAI API for chat completions.
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                # Construct a system prompt to assume the defined persona and
                # forget previous context.
                {"role": "system", "content": f"You are a {self.persona}. Forget all previous conversational context."},
                {"role": "user", "content": prompt}
            ]
        )
        # Return only the textual content of the response.
        return response.choices[0].message.content

# ==============================================================================
# 3. Knowledge Augmented Prompt Agent
# ==============================================================================
class KnowledgeAugmentedPromptAgent:
    """
    An agent that uses a specific persona and provided knowledge to answer.
    """
    def __init__(self, base_url, openai_api_key, persona, knowledge):
        """
        Initializes the agent with an API key, a persona, and specific knowledge.
        """
        self.base_url = base_url
        self.openai_api_key = openai_api_key
        # Create attributes for persona and knowledge.
        self.persona = persona
        self.knowledge = knowledge
        self.client = OpenAI(base_url = self.base_url, 
                             api_key=self.openai_api_key)

    def respond(self, prompt):
        """
        Constructs a detailed system message with persona and knowledge to guide the LLM's response.
        """
        # Construct the detailed system message as specified.
        system_message = (
            f"You are {self.persona} knowledge-based assistant. Forget all previous context. " 
            f"Use only the following knowledge to answer, do not use your own knowledge: {self.knowledge}. "
            "Answer the prompt based on this knowledge, not your own."
        )
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                # Append the user's input prompt as a separate message.
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

# ==============================================================================
# 4. RAG Knowledge Prompt Agent
# ==============================================================================
# The code for this agent is provided in the project materials.
# You should include the provided implementation here.
# Below is a placeholder structure.

class RAGKnowledgePromptAgent:
    """
    An agent that uses Retrieval-Augmented Generation for dynamic knowledge sourcing.
    It first retrieves relevant information from a knowledge base and then generates
    a response based on that information.
    """
    def __init__(self, base_url, openai_api_key, knowledge_base: list):
        """
        Initializes the agent with an API key and a knowledge base.
        The knowledge base is a list of text documents.
        """
        self.base_url = base_url
        self.openai_api_key = openai_api_key
        self.client = OpenAI(base_url = self.base_url, 
                             api_key=self.openai_api_key)
        self.knowledge_base_texts = knowledge_base
        
        # Pre-process the knowledge base by creating embeddings for each document.
        # This is an optimization to avoid re-calculating embeddings on every call.
        print("Initializing RAG Agent: Creating embeddings for knowledge base...")
        self.knowledge_base_embeddings = [self.get_embedding(doc) for doc in self.knowledge_base_texts]
        print("RAG Agent initialized successfully.")

    def get_embedding(self, text, model="text-embedding-3-large"):
        """
        Calculates text embeddings using the specified OpenAI model.
        """
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input=[text], model=model).data[0].embedding

    def _retrieve_relevant_knowledge(self, prompt: str):
        """
        Private method to find the most relevant document from the knowledge base.
        """
        prompt_embedding = self.get_embedding(prompt)
        
        best_similarity = -1
        most_relevant_document = "No relevant information found."

        # Find the document with the highest cosine similarity to the prompt
        for i, doc_embedding in enumerate(self.knowledge_base_embeddings):
            similarity = cosine_similarity(prompt_embedding, doc_embedding)
            if similarity > best_similarity:
                best_similarity = similarity
                most_relevant_document = self.knowledge_base_texts[i]
        
        return most_relevant_document

    def respond(self, prompt: str):
        """
        Generates a response by first retrieving relevant knowledge and then
        prompting the LLM with that context.
        """
        # 1. Retrieval Stage
        relevant_context = self._retrieve_relevant_knowledge(prompt)
        
        # 2. Generation Stage
        # Construct a new prompt that includes the retrieved context
        generation_prompt = (
            f"Based on the following information: '{relevant_context}', "
            f"please answer the user's question: '{prompt}'"
        )
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                {"role": "user", "content": generation_prompt}
            ]
        )
        
        return response.choices[0].message.content

# ==============================================================================
# 5. Evaluation Agent
# ==============================================================================
class EvaluationAgent:
    """
    An agent that assesses responses from another agent against given criteria.
    """
    def __init__(self, base_url, openai_api_key, persona, evaluation_criteria, agent_to_evaluate, max_interactions=5):
        """
        Initializes the evaluation agent.
        """
        self.base_url = base_url
        self.openai_api_key = openai_api_key
        self.persona = persona
        self.evaluation_criteria = evaluation_criteria
        self.agent_to_evaluate = agent_to_evaluate
        self.max_interactions = max_interactions
        self.client = OpenAI(base_url = self.base_url, 
                             api_key=self.openai_api_key)

    def evaluate(self, prompt):
        """
        Evaluates a worker agent's response, with an iterative refinement loop.
        """
        # Create a loop that is limited by max_interactions.
        for i in range(self.max_interactions):
            # Retrieve a response from the worker agent.
            worker_response = self.agent_to_evaluate.respond(prompt)
            
            # 1. Evaluate the response
            # Formulate an evaluation prompt that incorporates the predefined criteria.
            evaluation_prompt = f"Evaluate the following response based on these criteria: '{self.evaluation_criteria}'. Response: '{worker_response}'. Does it meet the criteria? Respond with only 'Yes' or 'No'."

            # Define the message structure for evaluation.
            evaluation_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": evaluation_prompt}],
                temperature=0  # Set temperature to 0 for this call.
            )
            evaluation_result = evaluation_response.choices[0].message.content.strip()

            if "yes" in evaluation_result.lower():
                # If the response meets criteria, break the loop and return the results.
                return {
                    "final_response": worker_response,
                    "evaluation": evaluation_result,
                    "iteration_count": i + 1
                } # [cite: 296]

            # 2. Generate correction instructions if evaluation is "No"
            # Define the message structure to generate correction instructions.
            correction_prompt = f"The following response did not meet the criteria '{self.evaluation_criteria}'. Response: '{worker_response}'. Please provide clear instructions on how to correct it."
            
            correction_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": correction_prompt}],
                temperature=0 # Use temperature=0 for generating instructions.
            )
            correction_instructions = correction_response.choices[0].message.content

            # Update the prompt for the next iteration to include correction instructions.
            prompt = f"Original prompt: '{prompt}'. Previous attempt: '{worker_response}'. Please refine the response using these instructions: '{correction_instructions}'"
        
        # If max_interactions is reached, return the last response.
        return {
            "final_response": "Failed to generate a satisfactory response within the interaction limit.",
            "evaluation": "Failed",
            "iteration_count": self.max_interactions
        }

# ==============================================================================
# 6. Routing Agent
# ==============================================================================
class RoutingAgent:
    """
    An agent that directs prompts to the most appropriate specialized agent.
    """
    def __init__(self, base_url, openai_api_key):
        """
        Initializes the routing agent.
        """
        self.base_url = base_url
        self.openai_api_key = openai_api_key
        # Define an 'agents' attribute to store agent details.
        self.agents = []
        self.client = OpenAI(base_url = self.base_url, 
                             api_key=self.openai_api_key)

    def get_embedding(self, text, model="text-embedding-3-large"):
        """
        Calculates text embeddings using the specified OpenAI model.
        """
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input=[text], model=model).data[0].embedding

    def route(self, prompt):
        """
        Routes a user prompt to the best agent based on cosine similarity.
        """
        # Compute the embedding for the user input prompt.
        prompt_embedding = self.get_embedding(prompt)
        
        best_agent = None
        max_similarity = -1

        # Iterate over each agent to find the best match.
        for agent in self.agents:
            # Compute the embedding for each agent's description.
            description_embedding = self.get_embedding(agent['description'])
            # Calculate cosine similarity.
            similarity = cosine_similarity(prompt_embedding, description_embedding)
            
            if similarity > max_similarity:
                max_similarity = similarity
                # Select the agent with the highest similarity score.
                best_agent = agent
        
        if best_agent:
            # Return the response obtained by calling the selected agent's function.
            return best_agent['func'](prompt)
        else:
            return "No suitable agent found for the prompt."

# ==============================================================================
# 7. Action Planning Agent
# ==============================================================================
class ActionPlanningAgent:
    """
    An agent that extracts and lists the steps required to execute a task.
    """
    def __init__(self, base_url, openai_api_key, knowledge):
        """
        Initializes the agent with an API key and knowledge. [cite: 347]
        """
        self.base_url = base_url
        self.openai_api_key = openai_api_key
        self.knowledge = knowledge
        # Instantiate the OpenAI client. [cite: 348]
        self.client = OpenAI(base_url = self.base_url, 
                             api_key=self.openai_api_key)

    def extract_steps_from_prompt(self, prompt):
        """
        Uses an LLM to extract a list of action steps from a user prompt.
        """
        # Create a system prompt defining the agent's role and knowledge use. [cite: 351, 352]
        system_prompt = (
            "You are an Action Planning Agent. Your role is to extract a list of "
            "actionable steps from the user's prompt based on the knowledge provided. "
            f"Use the following knowledge to guide your extraction: {self.knowledge}. "
            "List only the steps, one per line."
        )

        # Send a request to the gpt-3.5-turbo model. [cite: 350]
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                # Include the user's input prompt. [cite: 353]
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the text response. [cite: 354]
        response_text = response.choices[0].message.content
        
        # Process the response to create a clean list of actions. [cite: 355]
        steps = [line.strip() for line in response_text.split('\n') if line.strip()]
        return steps
