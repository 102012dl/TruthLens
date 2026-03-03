"""
Unit tests for TruthLens RAG pipeline — RAGAnalyzer with mocked embeddings and LLM.

Runs without OPENAI_API_KEY: mocks OpenAIEmbeddings and RetrievalQA chain.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from ml.rag_pipeline import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    RETRIEVER_K,
    RAGAnalyzer,
    build_vector_store,
    query_rag,
)


# Deterministic fake embeddings (no API call). OpenAI-like dimension.
FAKE_EMBEDDING_DIM = 1536


class FakeEmbeddings:
    """In-memory embeddings for tests: same dimension for all texts, no API."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[0.1] * FAKE_EMBEDDING_DIM for _ in texts]

    def embed_query(self, text: str) -> list[float]:
        return [0.1] * FAKE_EMBEDDING_DIM


# --- index_documents (mocked embeddings) ---


@patch("ml.rag_pipeline.OpenAIEmbeddings", new=FakeEmbeddings)
def test_index_documents_creates_vector_store() -> None:
    """index_documents splits text and builds FAISS store without API key."""
    analyzer = RAGAnalyzer()
    texts = [
        "First article about climate change. " + "More text. " * 50,
        "Second article about elections.",
    ]
    analyzer.index_documents(texts)
    assert analyzer.vector_store is not None
    # Retriever should return something
    retriever = analyzer.vector_store.as_retriever(search_kwargs={"k": 2})
    # LangChain: invoke() or get_relevant_documents()
    docs = getattr(retriever, "invoke", retriever.get_relevant_documents)("climate")
    assert len(docs) <= 2
    assert all(hasattr(d, "page_content") for d in docs)


@patch("ml.rag_pipeline.OpenAIEmbeddings", new=FakeEmbeddings)
def test_index_documents_with_metadata() -> None:
    """index_documents accepts optional metadata on chunks."""
    analyzer = RAGAnalyzer()
    analyzer.index_documents(["Short text."], metadata={"source": "test"})
    assert analyzer.vector_store is not None
    retriever = analyzer.vector_store.as_retriever(search_kwargs={"k": 1})
    docs = getattr(retriever, "invoke", retriever.get_relevant_documents)("text")
    if docs:
        assert docs[0].metadata.get("source") == "test"


def test_index_documents_empty_raises() -> None:
    """index_documents with no non-empty texts raises ValueError."""
    analyzer = RAGAnalyzer()
    with pytest.raises(ValueError, match="No non-empty documents"):
        analyzer.index_documents([])
    with pytest.raises(ValueError, match="No non-empty documents"):
        analyzer.index_documents(["", "   ", "\n"])


# --- analyze (mocked chain / LLM) ---


def _mock_retrieval_qa_invoke(*args: object, **kwargs: object) -> dict[str, str]:
    return {"result": "Mocked analysis: key facts, sentiment neutral, credibility 7/10."}


@patch("ml.rag_pipeline.OpenAIEmbeddings", new=FakeEmbeddings)
@patch("ml.rag_pipeline.RetrievalQA.from_chain_type")
def test_analyze_returns_mocked_result(mock_from_chain_type: MagicMock) -> None:
    """analyze() returns chain output without calling real LLM."""
    mock_chain = MagicMock()
    mock_chain.invoke = MagicMock(side_effect=_mock_retrieval_qa_invoke)
    mock_from_chain_type.return_value = mock_chain

    analyzer = RAGAnalyzer()
    analyzer.index_documents(["Article content here. " * 30])
    out = analyzer.analyze("What is the credibility?")
    assert "Mocked analysis" in out
    assert "credibility" in out.lower()
    mock_chain.invoke.assert_called_once()
    pos = mock_chain.invoke.call_args[0]
    if pos:
        assert isinstance(pos[0], dict) and pos[0].get("query") == "What is the credibility?"


@patch("ml.rag_pipeline.OpenAIEmbeddings", new=FakeEmbeddings)
@patch("ml.rag_pipeline.RetrievalQA.from_chain_type")
def test_analyze_returns_answer_key_if_no_result(mock_from_chain_type: MagicMock) -> None:
    """If chain returns 'answer' instead of 'result', we still return it."""
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {"answer": "Fallback answer text."}
    mock_from_chain_type.return_value = mock_chain

    analyzer = RAGAnalyzer()
    analyzer.index_documents(["Some text."])
    out = analyzer.analyze("Question?")
    assert out == "Fallback answer text."


def test_analyze_without_index_raises() -> None:
    """analyze() without prior index_documents raises RuntimeError."""
    analyzer = RAGAnalyzer()
    with pytest.raises(RuntimeError, match="Vector store is not initialized"):
        analyzer.analyze("Any question")


def test_analyze_empty_question_raises() -> None:
    """analyze() with empty question raises ValueError."""
    with patch("ml.rag_pipeline.OpenAIEmbeddings", new=FakeEmbeddings):
        analyzer = RAGAnalyzer()
        analyzer.index_documents(["Text."])
    with pytest.raises(ValueError, match="Question must be a non-empty"):
        analyzer.analyze("")
    with pytest.raises(ValueError, match="Question must be a non-empty"):
        analyzer.analyze("   ")


# --- Constants ---


def test_constants() -> None:
    """RAG constants match spec."""
    assert CHUNK_SIZE == 1000
    assert CHUNK_OVERLAP == 200
    assert RETRIEVER_K == 5


# --- Legacy helpers ---


@patch("ml.rag_pipeline.OpenAIEmbeddings", new=FakeEmbeddings)
def test_build_vector_store() -> None:
    """build_vector_store returns a FAISS store."""
    store = build_vector_store(["Doc one.", "Doc two."])
    assert store is not None


@patch("ml.rag_pipeline.OpenAIEmbeddings", new=FakeEmbeddings)
@patch("ml.rag_pipeline.RetrievalQA.from_chain_type")
def test_query_rag_legacy(mock_from_chain_type: MagicMock) -> None:
    """query_rag(question, vector_store) runs analyze without API."""
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {"result": "Legacy RAG answer."}
    mock_from_chain_type.return_value = mock_chain

    store = build_vector_store(["Content."])
    out = query_rag("Query?", store)
    assert out == "Legacy RAG answer."
