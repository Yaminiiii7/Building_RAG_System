"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            #strip removes white space
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """Split short posts by paragraph and sentence, keeping each item coherent."""
    chunks: list[Chunk] = []

    for doc in documents:
        text = doc.text.strip()
        if not text:
            continue

        # Short campus-life posts are often complete in one or two paragraphs,
        # so keep the whole document together unless it is clearly too long.
        if len(text) <= config.CHUNK_SIZE:
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=0,
                    produced_by="chunker.py::split_documents",
                )
            )
            continue

        # First split on paragraph breaks, which preserves the natural unit of
        # advice and discussion in these documents.
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]
        current = ""
        index = 0

        for paragraph in paragraphs:
            candidate = paragraph if not current else f"{current}\n\n{paragraph}"

            if len(candidate) <= config.CHUNK_SIZE:
                current = candidate
                continue

            if current:
                chunks.append(
                    Chunk(
                        text=current.strip(),
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1
                current = paragraph
                continue

            # A single paragraph can still be too long. Break it on sentences so
            # we do not lose a useful fact mid-way through a long answer.
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", paragraph) if s.strip()]
            sentence_buffer = ""
            for sentence in sentences:
                next_text = sentence if not sentence_buffer else f"{sentence_buffer} {sentence}"
                if len(next_text) <= config.CHUNK_SIZE:
                    sentence_buffer = next_text
                    continue

                if sentence_buffer:
                    chunks.append(
                        Chunk(
                            text=sentence_buffer.strip(),
                            source=doc.source,
                            index=index,
                            produced_by="chunker.py::split_documents",
                        )
                    )
                    index += 1
                    sentence_buffer = sentence
                else:
                    sentence_buffer = sentence

            if sentence_buffer:
                current = sentence_buffer

        if current.strip():
            chunks.append(
                Chunk(
                    text=current.strip(),
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
