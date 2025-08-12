import os
# from dotenv import load_dotenv
# Import the class from base_agents.py
# Make sure the RAGKnowledgePromptAgent class provided to you is in this file.
from workflow_agents.base_agents import RAGKnowledgePromptAgent

def main():
    """
    Main function to test the RAGKnowledgePromptAgent.
    """
    base_url = "https://openai.vocareum.com/v1"
    api_key = "voc-18896424415987442761856899cdfba587a8.21820406"

    # if not openai_api_key:
    #     print("Error: OPENAI_API_KEY not found.")
    #     print("Please create a .env file and add your OPENAI_API_KEY.")
    #     return

    # 1. Define a Sample Knowledge Base
    # This simulates a set of documents the RAG agent can retrieve information from.
    knowledge_base = [
        "Document 1: The first programmable computer was the Colossus, created by Tommy Flowers in 1943.",
        "Document 2: An AI agent perceives its environment through sensors and acts upon that environment through actuators.",
        "Document 3: Photosynthesis in plants involves converting light energy into chemical energy, storing it in bonds of sugar."
    ]
    
    # 2. Instantiate the Agent
    # We assume the provided RAG agent class takes the API key and a knowledge_base.
    # If the provided class has a different constructor, adjust this line accordingly.
    rag_agent = RAGKnowledgePromptAgent(
        base_url = base_url, 
        openai_api_key= api_key,
        knowledge_base=knowledge_base
    )
    
    # 3. Define the Prompt
    # This prompt is specifically designed to require information from Document 2.
    prompt = "How does an artificial intelligence agent interact with its surroundings?"
    
    # 4. Get the Response
    # The agent should retrieve the relevant document and use it to answer the prompt.
    response = rag_agent.respond(prompt)
    
    # 5. Print the Interaction
    print("--- Testing RAG Knowledge Prompt Agent ---")
    print(f"Sample Knowledge Base contains {len(knowledge_base)} documents.")
    print(f"\nPrompt: {prompt}")
    print(f"\nAgent Response: {response}")
    print("-" * 40)

    # 6. Explain Knowledge Source
    print("\nKnowledge Source Explanation:")
    print("""
    - Retrieval-Augmented Generation (RAG): This agent works differently from the others. Instead of being given all knowledge upfront in the prompt, it first *retrieves* the most relevant document(s) from its internal knowledge base based on the user's prompt.
    
    - Dynamic Knowledge Sourcing: Once the relevant information is found (in this case, 'Document 2'), the agent *then* uses it to generate a response. This makes the agent more efficient as it only uses a small, relevant subset of its knowledge for any given query.
    
    - The response should be directly based on the information in 'Document 2', demonstrating that the retrieval part of the workflow was successful.
    """)
    print("-" * 40)

if __name__ == '__main__':
    main()
