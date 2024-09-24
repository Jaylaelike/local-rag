import os
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
from get_vector_db import get_vector_db

LLM_MODEL = os.getenv('LLM_MODEL', 'llama3.1')

# Function to get the prompt templates for generating alternative questions and answering based on context
def get_prompt():
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate five
        different versions of the given user question to retrieve relevant documents from
        a vector database. By generating multiple perspectives on the user question, your
        goal is to help the user overcome some of the limitations of the distance-based
        similarity search. Provide these alternative questions separated by newlines.
        Original question: {question}""",
    )

    template = """Answer the question based ONLY on the following context:
    {context}
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    return QUERY_PROMPT, prompt

# Main function to handle the query process
def query(input):
    if input:
        # Initialize the language model with the specified model name
        llm = ChatOllama(model=LLM_MODEL)
        # Get the vector database instance
        db = get_vector_db()
        # Get the prompt templates
        QUERY_PROMPT, prompt = get_prompt()

        # Set up the retriever to generate multiple queries using the language model and the query prompt
        retriever = MultiQueryRetriever.from_llm(
            db.as_retriever(), 
            llm,
            prompt=QUERY_PROMPT
        )

        # Define the processing chain to retrieve context, generate the answer, and parse the output
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        response = chain.invoke(input)
        
        return response

    return None


# import os
# import logging
# from langchain_community.chat_models import ChatOllama
# from langchain.prompts import ChatPromptTemplate, PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from langchain.retrievers.multi_query import MultiQueryRetriever
# from get_vector_db import get_vector_db

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Fetch the LLM model name from environment variables
# LLM_MODEL = os.getenv('LLM_MODEL', 'llama3.1')

# # Function to get the prompt templates for generating alternative questions and answering based on context
# def get_prompt():
#     QUERY_PROMPT = PromptTemplate(
#         input_variables=["question"],
#         template="""# INSTRUCTION:
# You are an AI language model assistant. Your task is to generate five different versions of the given user question to retrieve relevant documents from a vector database.

# # RULES:
# 1. Generate questions that cover different perspectives of the original question.
# 2. Ensure the questions are relevant and coherent.

# # INPUT EXAMPLE:
# Original question: What are the benefits of using renewable energy sources?

# # OUTPUT EXAMPLE:
# 1. What are the advantages of renewable energy sources?
# 2. How do renewable energy sources contribute to environmental sustainability?
# 3. What are the economic benefits of using renewable energy?
# 4. How do renewable energy sources impact climate change?
# 5. What are the long-term benefits of transitioning to renewable energy?

# # OUTPUT EXPLAIN:
# The output provides five different questions that explore various aspects of the original question, ensuring a comprehensive search for relevant documents.

# # INPUT:
# {question}

# # OUTPUT:
# """,
#     )

#     template = """# INSTRUCTION:
# Answer the question based ONLY on the following context.

# # RULES:
# 1. Provide a concise and accurate answer.
# 2. Do not include information not present in the context.

# # INPUT EXAMPLE:
# Context: Renewable energy sources include solar, wind, hydro, and geothermal. They are sustainable and have minimal environmental impact.
# Question: What are the benefits of using renewable energy sources?

# # OUTPUT EXAMPLE:
# The benefits of using renewable energy sources include sustainability and minimal environmental impact.

# # OUTPUT EXPLAIN:
# The output directly answers the question using the provided context, focusing on sustainability and environmental impact.

# # INPUT:
# Context: {context}
# Question: {question}

# # OUTPUT:
# """

#     prompt = ChatPromptTemplate.from_template(template)

#     return QUERY_PROMPT, prompt

# # Main function to handle the query process
# def query(input):
#     if not input:
#         logger.warning("No input provided.")
#         return None

#     try:
#         # Initialize the language model with the specified model name
#         llm = ChatOllama(model=LLM_MODEL)
#         logger.info(f"Initialized language model with model: {LLM_MODEL}")

#         # Get the vector database instance
#         db = get_vector_db()
#         logger.info("Retrieved vector database instance.")

#         # Get the prompt templates
#         QUERY_PROMPT, prompt = get_prompt()
#         logger.info("Retrieved prompt templates.")

#         # Set up the retriever to generate multiple queries using the language model and the query prompt
#         retriever = MultiQueryRetriever.from_llm(
#             db.as_retriever(), 
#             llm,
#             prompt=QUERY_PROMPT
#         )
#         logger.info("Set up retriever for generating multiple queries.")

#         # Define the processing chain to retrieve context, generate the answer, and parse the output
#         chain = (
#             {"context": retriever, "question": RunnablePassthrough()}
#             | prompt
#             | llm
#             | StrOutputParser()
#         )
#         logger.info("Defined processing chain.")

#         response = chain.invoke(input)
#         logger.info("Generated response.")
        
#         return response

#     except Exception as e:
#         logger.error(f"An error occurred: {e}")
#         return None

# # Example usage
# if __name__ == "__main__":
#     user_input = "What are the benefits of using renewable energy sources?"
#     response = query(user_input)
#     if response:
#         print(response)
#     else:
#         print("No response generated.")
