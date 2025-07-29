from langchain import LLMChain, PromptTemplate
from sqlalchemy import text

class RAGPipeline:
    def __init__(self, llm, retriever, engine):
        self.llm = llm
        self.retriever = retriever
        self.engine = engine
        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
                        Schema:
                        {context}

                        Generate a SQL query for the following question:
                        {question}
                        Only output the SQL.
                    """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def run(self, question: str):
        docs = self.retriever.get_relevant_documents(question)
        context = "\n".join([d.page_content for d in docs])
        sql = self.chain.run({"context": context, "question": question}).strip()

        # run query on database
        with self.engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.fetchall()
        return sql, rows