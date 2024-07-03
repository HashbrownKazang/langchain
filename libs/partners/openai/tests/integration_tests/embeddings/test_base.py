"""Test OpenAI embeddings."""

import openai
import pytest

from langchain_openai import OpenAIEmbeddings


@pytest.fixture
def embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model="text-embedding-3-small")


def test_embedding_documents(embeddings: OpenAIEmbeddings) -> None:
    """Test openai embeddings."""
    output = embeddings.embed_documents(["foo bar", "baz buz"])
    assert len(output) == 2
    assert len(output[0]) > 0


def test_embedding_query(embeddings: OpenAIEmbeddings) -> None:
    """Test openai embeddings."""
    output = embeddings.embed_query("foo bar")
    assert len(output) > 0


def test_embeddings_dimensions() -> None:
    """Test openai embeddings with dimensions param."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=128)
    output = embeddings.embed_documents(["foo bar", "baz buz"])
    assert len(output) == 2
    assert len(output[0]) == 128


def test_embeddings_equivalent_to_raw(embeddings: OpenAIEmbeddings) -> None:
    documents = ["disallowed special token '<|endoftext|>'"]

    lc_output = embeddings.embed_documents(documents)[0]
    direct_output = (
        openai.OpenAI()
        .embeddings.create(input=documents, **embeddings._invocation_params)
        .data[0]
        .embedding
    )
    assert lc_output == direct_output


async def test_embeddings_equivalent_to_raw_async(embeddings: OpenAIEmbeddings) -> None:
    documents = ["disallowed special token '<|endoftext|>'"]

    lc_output = (await embeddings.aembed_documents(documents))[0]
    client = openai.AsyncOpenAI()
    direct_output = (
        (
            await client.embeddings.create(
                input=documents, **embeddings._invocation_params
            )
        )
        .data[0]
        .embedding
    )
    assert lc_output == direct_output


def test_embed_documents_long(embeddings: OpenAIEmbeddings) -> None:
    """Test openai embeddings."""
    long_text = " ".join(["foo bar"] * embeddings.embedding_ctx_length)
    token_splits, _ = embeddings._tokenize_and_split([long_text])
    assert len(token_splits) > 1
    output = embeddings.embed_documents([long_text])
    assert len(output) == 1
    assert len(output[0]) > 0


async def test_embed_documents_long_async(embeddings: OpenAIEmbeddings) -> None:
    """Test openai embeddings."""
    long_text = " ".join(["foo bar"] * embeddings.embedding_ctx_length)
    token_splits, _ = embeddings._tokenize_and_split([long_text])
    assert len(token_splits) > 1
    output = await embeddings.aembed_documents([long_text])
    assert len(output) == 1
    assert len(output[0]) > 0
