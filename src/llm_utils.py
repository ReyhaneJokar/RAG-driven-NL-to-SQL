from langchain.llms import LlamaCpp
from langchain.embeddings import HuggingFaceEmbeddings

def load_llm(model_path: str = "models/llama-7b/ggml-model.bin"):
    return LlamaCpp(
        model_path=model_path,
        n_ctx=2048, # number of tokens
        temperature=0.0,
    )
    
# convert text to vector
def load_embeddings(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    return HuggingFaceEmbeddings(model_name=model_name)