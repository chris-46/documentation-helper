from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain # retriever

load_dotenv()

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain #augments prompt
from langchain_pinecone import PineconeVectorStore


from langchain_openai import ChatOpenAI, OpenAIEmbeddings

INDEX_NAME = "langchain-documentation-index"


def run_llm(query: str):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    docsearch = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    chat = ChatOpenAI(verbose=True, temperature=0)

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)

    qa = create_retrieval_chain(
        retriever=docsearch.as_retriever(), combine_docs_chain=stuff_documents_chain
    )
    result = qa.invoke(input={"input": query})
    new_result = {
        "query": result["input"],
        "result": result["answer"],
        "source_documents": result["context"],
    }
    return new_result


if __name__ == "__main__":
    res = run_llm(query="What is a LangChain Chain?")
    print(res["result"])