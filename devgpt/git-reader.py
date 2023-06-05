import os
import pathlib
from chroma_instance import Chroma, OpenAIEmbeddings
from openai import OpenAI
from typing import Generator

# You might need to install or create the `qa_chain` and `text_splitter` modules
from qa_chain import load_qa_chain, RetrievalQA
from text_splitter import CharacterTextSplitter


def get_repo_docs(repo_path: str) -> Generator:
    repo = pathlib.Path(repo_path)

    for md_file in repo.glob("**/*.md"):
        with open(md_file, "r") as file:
            rel_path = md_file.relative_to(repo)
            yield {"page_content": file.read(), "metadata": {"source": str(rel_path)}}


def get_source_chunks(repo_path: str):
    source_chunks = []
    splitter = CharacterTextSplitter(separator="\n", chunk_size=1024, chunk_overlap=0)

    for source in get_repo_docs(repo_path):
        for chunk in splitter.split_text(source["page_content"]):
            source_chunks.append(
                {"page_content": chunk, "metadata": source["metadata"]}
            )

    return source_chunks


def main():
    REPO_PATH = "<absolute path to the repo>/EIPs"
    CHROMA_DB_PATH = f"./chroma/{os.path.basename(REPO_PATH)}"

    vector_db = None

    if not os.path.exists(CHROMA_DB_PATH):
        print(f"Creating Chroma DB at {CHROMA_DB_PATH}")
        source_chunks = get_source_chunks(REPO_PATH)
        vector_db = Chroma.from_documents(
            source_chunks, OpenAIEmbeddings(), persist_directory=CHROMA_DB_PATH
        )
        vector_db.persist()
    else:
        print(f"Loading Chroma DB from {CHROMA_DB_PATH}...")
        vector_db = Chroma(
            persist_directory=CHROMA_DB_PATH, embedding_function=OpenAIEmbeddings()
        )

    qa_chain = load_qa_chain(OpenAI(temperature=1), chain_type="stuff")
    qa = RetrievalQA(
        combine_documents_chain=qa_chain, retriever=vector_db.as_retriever()
    )

    while True:
        print("\n\n\033[31m" + "Ask a question" + "\033[0m")
        user_input = input()
        print("\033[31m" + qa.run(user_input) + "\033[0m")


if __name__ == "__main__":
    main()
