import fitz  # PyMuPDF
import re
import os
import numpy as np
import json
import sqlite3
from transformers import AutoTokenizer, AutoModel
import faiss
from yake import KeywordExtractor  # keyword extraction

# Domain-specific stopwords (add more as needed)
DOMAIN_STOPWORDS = {
    "shall", "article", "directive", "member", "competent", "market", 
    "financial", "investment", "firm", "trading", "regulation", "state", 
    "authority", "provision", "paragraph", "point", "accordance", "person",
    "supervisory", "requirement", "service", "information", "regulatory",
    "activity", "management", "contract", "report", "client", "annex"
}

# Helper function to sanitize filenames
def sanitize_filename(title):
    # Replace invalid characters with underscores
    return re.sub(r'[\\/*?:"<>|]', "_", title).strip()

# Step 1: Extract text and metadata from PDF
def extract_text_and_metadata(pdf_path):
    doc = fitz.open(pdf_path)
    metadata = doc.metadata
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return metadata, text

# Step 2: Rule-based chunking
def rule_based_chunking(text, max_chunk_size=1000):
    # Split by headings (e.g., "1. Introduction", "Article 5")
    chunks = re.split(r"\n\s*\d+\.\s+|\n\s*Article\s+\d+\.\s+", text)
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    
    # Further split large chunks into smaller ones
    final_chunks = []
    for chunk in chunks:
        if len(chunk) <= max_chunk_size:
            final_chunks.append(chunk)
        else:
            # Split by sentences or paragraphs
            sub_chunks = re.split(r"(?<=[.!?])\s+", chunk)
            current_chunk = ""
            for sub_chunk in sub_chunks:
                if len(current_chunk) + len(sub_chunk) <= max_chunk_size:
                    current_chunk += " " + sub_chunk
                else:
                    final_chunks.append(current_chunk.strip())
                    current_chunk = sub_chunk
            if current_chunk:
                final_chunks.append(current_chunk.strip())
    return final_chunks

# Step 3: Generate embeddings using a pre-trained model
def generate_embeddings(chunks):
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    
    embeddings = []
    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        # Use mean pooling to get sentence embeddings
        embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        embeddings.append(embedding)
    return np.vstack(embeddings)

# Step 4: Index embeddings using FAISS
def index_embeddings(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity search
    index.add(embeddings)
    return index

# Step 5: Keyword extraction using YAKE
def extract_keywords(chunks, top_k=20):
    kw_extractor = KeywordExtractor(lan="en", top=top_k * 2)  # Extract more candidates initially
    keywords = []
    for chunk in chunks:
        # Extract candidate keywords using YAKE
        candidate_phrases = kw_extractor.extract_keywords(chunk)
        
        # Filter out domain-specific stopwords
        candidate_phrases = [
            phrase for phrase, _ in candidate_phrases
            if not any(word in phrase.lower() for word in DOMAIN_STOPWORDS)
        ]
        
        # Select top_k unique keywords
        selected_keywords = []
        for phrase in candidate_phrases:
            # Skip if the phrase is a sub-phrase of any already selected keyword
            if any(
                phrase.lower() != existing.lower() and phrase.lower() in existing.lower()
                for existing in selected_keywords
            ):
                continue
            # Skip if any selected keyword is a sub-phrase of the current phrase
            if any(
                existing.lower() != phrase.lower() and existing.lower() in phrase.lower()
                for existing in selected_keywords
            ):
                continue
            # Add the phrase to the selected keywords
            selected_keywords.append(phrase)
            # Stop if we have enough keywords
            if len(selected_keywords) >= top_k:
                break
        
        keywords.append(selected_keywords)
    return keywords

# Step 6: Store indexed data in SQLite
def store_in_database(metadata, chunks, embeddings, keywords, output_dir="indexed_documents"):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Use the document title as the base filename
    title = metadata.get("title", "untitled")
    sanitized_title = sanitize_filename(title)
    db_path = os.path.join(output_dir, f"{sanitized_title}.db")
    json_path = os.path.join(output_dir, f"{sanitized_title}.json")
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            creation_date TEXT,
            file_path TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            chunk_text TEXT,
            keywords TEXT,
            embedding BLOB,
            FOREIGN KEY (document_id) REFERENCES documents (id)
        )
    """)
    
    # Insert document metadata
    cursor.execute("""
        INSERT INTO documents (title, author, creation_date, file_path)
        VALUES (?, ?, ?, ?)
    """, (metadata.get("title"), metadata.get("author"), metadata.get("creationDate"), pdf_path))
    document_id = cursor.lastrowid
    
    # Insert chunks
    for i, (chunk, keyword_list, embedding) in enumerate(zip(chunks, keywords, embeddings)):
        cursor.execute("""
            INSERT INTO chunks (document_id, chunk_text, keywords, embedding)
            VALUES (?, ?, ?, ?)
        """, (document_id, chunk, json.dumps(keyword_list), embedding.tobytes()))
    
    conn.commit()
    conn.close()
    
    # Save chunks and metadata to JSON
    output = {
        "metadata": metadata,
        "chunks": chunks,
        "embeddings": embeddings.tolist(),
        "keywords": keywords,
    }
    with open(json_path, "w") as f:
        json.dump(output, f, indent=4)
    
    print(f"Indexed document saved to '{json_path}' and '{db_path}'.")

# Main function
def main(pdf_path):
    # Step 1: Extract text and metadata
    metadata, text = extract_text_and_metadata(pdf_path)
    print("Metadata:", metadata)
    
    # Step 2: Chunk the text
    chunks = rule_based_chunking(text)
    print(f"Number of chunks: {len(chunks)}")
    
    # Step 3: Generate embeddings
    embeddings = generate_embeddings(chunks)
    
    # Step 4: Index embeddings
    index = index_embeddings(embeddings)
    print("Embeddings indexed successfully!")
    
    # Step 5: Extract keywords
    keywords = extract_keywords(chunks, top_k=20)  # Increase to 20 keywords per chunk
    for i, chunk_keywords in enumerate(keywords):
        print(f"Chunk {i+1} Keywords:", chunk_keywords)
    
    # Step 6: Store in SQLite database and JSON
    store_in_database(metadata, chunks, embeddings, keywords)

# Run the script
if __name__ == "__main__":
    pdf_path = "CELEX_32014L0065_EN_TXT.pdf"
    main(pdf_path)