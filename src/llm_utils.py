from langchain.llms import openai
from langchain.embeddings import HuggingFaceEmbeddings

def load_llm(model_name: str = "gemma-3-12b", api_base: str = "http://127.0.0.1:11434/v1"):
    """
        Uses LM Studio's OpenAI-compatible API to load Gemma-3-12B.
        api_base should point to LM Studio's server.
    """
    return openai(
        model_name=model_name,
        openai_api_base=api_base,
        n_ctx=2048, # maximum number of tokens
        temperature=0.0,
    )
    
# convert text to vector
def load_embeddings(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    return HuggingFaceEmbeddings(model_name=model_name)