# Document Retrieval System

A Python-based RAG (Retrieval Augmented Generation) application that stores text chunks with their vector embeddings in PostgreSQL and retrieves relevant content using semantic search.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Example](#example)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- Embed text with a transformer model
- Store content and embeddings in a PostgreSQL database
- Find the most relevant chunks for any input query using cosine similarity
- Simple command-line interface

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/document-retrieval-system.git
   cd document-retrieval-system
   ```

2. **Create directory for the db:**
   ```sh
   mkdir db/pgData
   ```

3. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up [Ollama](https://ollama.com/):**
   - Install and run Ollama with your desired model (such as llama3).
   - Make sure Ollama is running and listening on a port.

5. **Set environment variables:**  
   Create a `.env` file with the following content:
   ```
    OLLAMA_PORT=11434
    OLLAMA_MODEL=llama3
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_DB=db_name
   ```

> **Note:**
> Be sure to set the `OLLAMA_PORT` value in your `.env` file to match the port your Ollama server is using.

6. **Set up and launch PostgreSQL using Docker:**
   - Build the image:
     ```sh
     docker build -t rag-db:latest db/.
     ```
   - Run the container:
     ```sh
     docker run -d \
       --name pgvector-db \
       --env-file .env \
       -p 5432:5432 \
       -v ./db/pgData:/var/lib/postgresql/data \
       rag-db:latest
     ```

---

## Usage

**Commands:**

- `add` — Add new documents to the system (e.g. specify a text file).
- `query` — Ask a question and get an answer based on your uploaded documents and context.
- `exit` — Exit the CLI.

Start the program:
```sh
python main.py
```

cli interface:

```text
Usage: Enter a command (add or query or exit)-> add
enter ur documents: document.pdf 

Usage: Enter a command (add or query or exit)-> query
enter a question: ask it a question and based on the context provided through the db it will answer accordingly
```

> **Note:**
> Be sure the files u add are in the data directory.

## Configuration

- Models: This project uses [sentence-transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`) for embedding.
- DB: Adjust the `.env` file for your database configuration.

---

## Contact

- Author: [Youssef ayedder](mailto:youssefayedder@email.com)
- Linkedin: [LinkedIn profile](https://www.linkedin.com/in/youssefayedder)