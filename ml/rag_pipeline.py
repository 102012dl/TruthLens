"""
TruthLens RAG pipeline — LangChain + FAISS + OpenAI GPT-4o-mini.

Used for retrieval-augmented Q&A over news/knowledge base.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVER_K = 5


@dataclass
class RAGAnalyzer:
    """RAG analyzer for TruthLens news analysis based on LangChain + FAISS.

    This class:
      - indexes raw text documents with RecursiveCharacterTextSplitter;
      - builds a FAISS vector store using OpenAIEmbeddings;
      - runs a RetrievalQA chain using GPT-4o-mini for structured news analysis.
    """

    vector_store: FAISS | None = None

    def index_documents(self, texts: Iterable[str], metadata: dict[str, Any] | None = None) -> None:
        """Split and index input texts into a FAISS vector store.

        Args:
            texts: Iterable of raw text documents (e.g., news articles).
            metadata: Optional metadata attached to every chunk.
        """

        all_metadata = metadata or {}
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

        docs: list[Document] = []
        for text in texts:
            if not text or not str(text).strip():
                continue
            for chunk in splitter.split_text(str(text)):
                docs.append(Document(page_content=chunk, metadata=all_metadata))

        if not docs:
            raise ValueError("No non-empty documents provided for indexing.")

        embeddings = OpenAIEmbeddings()  # Uses OPENAI_API_KEY from env
        self.vector_store = FAISS.from_documents(docs, embedding=embeddings)

    def _ensure_vector_store(self) -> FAISS:
        if self.vector_store is None:
            raise RuntimeError("Vector store is not initialized. Call index_documents() first.")
        return self.vector_store

    def analyze(self, question: str) -> str:
        """Run retrieval-augmented analysis with a custom news prompt.

        Args:
            question: User query / topic, e.g. a news headline or claim.

        Returns:
            LLM-generated report string.
        """

        if not question or not question.strip():
            raise ValueError("Question must be a non-empty string.")

        vector_store = self._ensure_vector_store()

        model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
        )

        retriever = vector_store.as_retriever(search_kwargs={"k": RETRIEVER_K})

        prompt_template = (
            "You are TruthLens, an expert AI news analyst. "
            "Use only the following context to answer the question. "
            "If information is missing, say so explicitly.\n\n"
            "Produce a *structured* analysis with:\n"
            "1) Key factual points and timeline.\n"
            "2) Overall sentiment and tone (e.g., optimistic, fearful, neutral).\n"
            "3) Credibility indicators: sources mentioned, hedging language, sensationalism.\n"
            "4) Potential misinformation or bias (if any), with justification based on the text.\n"
            "5) Actionable recommendations for the reader (e.g., cross-check, be cautious).\n\n"
            "Use markdown headings and bullet points. Be concise but information-dense.\n\n"
            "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        )
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"],
        )

        chain = RetrievalQA.from_chain_type(
            llm=model,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt},
        )

        result = chain.invoke({"query": question})

        if isinstance(result, dict):
            return str(result.get("result") or result.get("answer") or "")
        return str(result)


def build_vector_store(texts: list[str], embeddings: Any | None = None) -> Any:
    """Legacy helper: build FAISS index from texts and embeddings.

    Prefer using RAGAnalyzer.index_documents(); this is kept for compatibility.
    """

    analyzer = RAGAnalyzer()
    analyzer.index_documents(texts)
    return analyzer.vector_store


def query_rag(question: str, vector_store: Any, llm: Any | None = None) -> str:
    """Legacy helper: run RAG with an existing vector_store and optional LLM."""

    analyzer = RAGAnalyzer(vector_store=vector_store)
    return analyzer.analyze(question)

