from langchain.vectorstores import FAISS
from sqlalchemy import inspect
from llm_utils import load_embeddings

# extract tabel's metadata
def build_retriever(engine, embeddings, index_path: str = "faiss_index"):
    inspector = inspect(engine)
    docs = []
    for table_name in inspector.get_table_names():
        cols = inspector.get_columns(table_name)
        schema = f"Table: {table_name}\nColumns:\n"
        for col in cols:
            schema += f" - {col['name']} ({col['type']})\n"
        docs.append({"page_content": schema, "metadata": {"table": table_name}})

    vector_store = FAISS.from_documents(docs, embeddings)
    # vector_store.save_local(index_path)
    # vector_store = FAISS.load_local(index_path, embeddings)
    return vector_store.as_retriever(search_kwargs={"k": 3})