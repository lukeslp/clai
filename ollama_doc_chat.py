# ollama_doc_chat.py

#!/usr/bin/env python3
"""
Document Chat CLI (Ollama Version)

Ingests all .txt and .md files in a directory, creates a SQLite DB storing contents and embeddings,
and allows interactive chat with the ingested documents.

Requirements:
  - numpy
  - requests

Usage:
  python doc_chat_ollama.py ingest --dir PATH [--db PATH] [--model MODEL_NAME] [--endpoint URL]
  python doc_chat_ollama.py chat   [--db PATH] [--model MODEL_NAME] [--topk N] [--endpoint URL]
"""
import os
import sys
import argparse
import sqlite3
import numpy as np
from numpy.linalg import norm
import requests
import json

# Default parameters
DEFAULT_DB_PATH = ".llamaline.db"
DEFAULT_EMBEDDING_MODEL = "nomic-embed-text"  # Ollama embedding model
DEFAULT_CHAT_MODEL = "llama3"  # Ollama chat model
DEFAULT_ENDPOINT = os.environ.get('OLLAMA_ENDPOINT', 'http://localhost:11434')

def init_db(db_path: str) -> sqlite3.Connection:
    """
    Initialize SQLite database with tables for documents and embeddings.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Documents table: filename + content
    c.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            content TEXT
        )
    """)
    # Embeddings table: doc_id + embedding blob
    c.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            doc_id INTEGER PRIMARY KEY,
            embedding BLOB,
            FOREIGN KEY(doc_id) REFERENCES documents(id)
        )
    """)
    conn.commit()
    return conn


def get_embedding(text: str, model: str, endpoint: str) -> np.ndarray:
    """Get embedding from Ollama API"""
    url = f"{endpoint}/api/embeddings"
    payload = {
        "model": model,
        "prompt": text
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        embedding = np.array(data.get('embedding'), dtype=np.float32)
        return embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        raise


def ingest_files(directory: str, db_path: str, model_name: str, endpoint: str) -> None:
    """
    Ingest all text files in `directory`, compute embeddings, and store in SQLite DB.
    """
    conn = init_db(db_path)
    c = conn.cursor()

    for fname in os.listdir(directory):
        path = os.path.join(directory, fname)
        if os.path.isfile(path) and fname.lower().endswith((".txt", ".md")):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if not content:
                continue
            # Insert or ignore document
            c.execute(
                "INSERT OR IGNORE INTO documents (filename, content) VALUES (?, ?)",
                (fname, content)
            )
            conn.commit()
            # Retrieve document ID
            c.execute("SELECT id, content FROM documents WHERE filename = ?", (fname,))
            row = c.fetchone()
            doc_id, doc_content = row
            # Compute embedding
            try:
                emb = get_embedding(doc_content, model_name, endpoint)
                emb_blob = emb.tobytes()
                # Upsert embedding
                c.execute(
                    "INSERT OR REPLACE INTO embeddings (doc_id, embedding) VALUES (?, ?)",
                    (doc_id, emb_blob)
                )
                conn.commit()
                print(f"[+] Ingested '{fname}' (doc_id={doc_id})")
            except Exception as e:
                print(f"[!] Error generating embedding for '{fname}': {e}")
    conn.close()


def search_embeddings(query: str,
                      db_path: str,
                      model_name: str,
                      top_k: int,
                      endpoint: str) -> list:
    """
    Search the SQLite DB for the top_k documents most similar to the query.
    """
    # Compute query embedding with Ollama
    query_emb = get_embedding(query, model_name, endpoint)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT doc_id, embedding FROM embeddings")

    scores = []
    for doc_id, emb_blob in c.fetchall():
        emb = np.frombuffer(emb_blob, dtype=np.float32)
        sim = float(np.dot(query_emb, emb) / (norm(query_emb) * norm(emb)))
        scores.append((doc_id, sim))
    conn.close()

    # Sort by similarity descending
    scores.sort(key=lambda x: x[1], reverse=True)
    top = scores[:top_k]

    # Retrieve document info
    results = []
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for doc_id, score in top:
        c.execute("SELECT filename, content FROM documents WHERE id = ?", (doc_id,))
        fname, content = c.fetchone()
        results.append((fname, content, score))
    conn.close()
    return results


def chat_with_ollama(model: str, messages: list, endpoint: str) -> str:
    """Send a chat request to Ollama API"""
    url = f"{endpoint}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get('message', {}).get('content', '')
    except Exception as e:
        print(f"Error calling Ollama chat API: {e}")
        raise


def chat_loop(db_path: str, embedding_model: str, chat_model: str, top_k: int, endpoint: str) -> None:
    """
    Interactive chat loop: user asks questions, system retrieves context and calls Ollama Chat API.
    """
    print("\nDocument Chat (Ollama). Type 'exit' or 'quit' to end.\n")
    while True:
        query = input("You: ")
        if query.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        
        # Retrieve top-k matching documents
        docs = search_embeddings(query, db_path, embedding_model, top_k, endpoint)
        
        # Build context
        context = ""
        for fname, content, score in docs:
            context += f"== {fname} (score={score:.4f}) ==\n{content}\n\n"
        
        # Create messages
        system_message = "You are an assistant that answers questions based on provided document excerpts. Use the context to provide a thorough answer."
        user_message = f"Context:\n\n{context}\n\nQuestion: {query}"
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        # Call Ollama Chat API
        try:
            answer = chat_with_ollama(chat_model, messages, endpoint)
            print(f"Assistant: {answer}\n")
        except Exception as e:
            print(f"[Error] Ollama API call failed: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Document Chat CLI (Ollama): ingest files, build embeddings, and chat via LLM."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # Ingest command
    p_ingest = sub.add_parser("ingest", help="Ingest files and build embeddings DB")
    p_ingest.add_argument(
        "--dir", required=True, help="Directory containing .txt/.md files to ingest"
    )
    p_ingest.add_argument(
        "--db", default=DEFAULT_DB_PATH, help=f"SQLite DB path (default: {DEFAULT_DB_PATH})"
    )
    p_ingest.add_argument(
        "--model", default=DEFAULT_EMBEDDING_MODEL,
        help=f"Ollama embedding model (default: {DEFAULT_EMBEDDING_MODEL})"
    )
    p_ingest.add_argument(
        "--endpoint", default=DEFAULT_ENDPOINT, 
        help=f"Ollama API endpoint (default: {DEFAULT_ENDPOINT})"
    )

    # Chat command
    p_chat = sub.add_parser("chat", help="Enter interactive chat mode")
    p_chat.add_argument(
        "--db", default=DEFAULT_DB_PATH, help=f"SQLite DB path (default: {DEFAULT_DB_PATH})"
    )
    p_chat.add_argument(
        "--embedding-model", default=DEFAULT_EMBEDDING_MODEL,
        help=f"Ollama embedding model (default: {DEFAULT_EMBEDDING_MODEL})"
    )
    p_chat.add_argument(
        "--chat-model", default=DEFAULT_CHAT_MODEL,
        help=f"Ollama chat model (default: {DEFAULT_CHAT_MODEL})"
    )
    p_chat.add_argument(
        "--topk", type=int, default=3,
        help="Number of top documents to use as context (default: 3)"
    )
    p_chat.add_argument(
        "--endpoint", default=DEFAULT_ENDPOINT, 
        help=f"Ollama API endpoint (default: {DEFAULT_ENDPOINT})"
    )

    args = parser.parse_args()
    if args.command == "ingest":
        ingest_files(args.dir, args.db, args.model, args.endpoint)
    elif args.command == "chat":
        chat_loop(args.db, args.embedding_model, args.chat_model, args.topk, args.endpoint)


if __name__ == "__main__":
    main()

