---
title: Russell Tennis Center Chatbot
emoji: 🎾
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: "5.34.2"
app_file: app.py
pinned: false
---
# Russell Tennis Center Chatbot 🎾🤖

This is a zero-cost, AI-powered chatbot built for [Russell Tennis Center](https://russelltenniscenter.com). It uses website content and retrieval-based AI to answer visitor questions, hosted via Hugging Face Spaces and embeddable in their site.

## Features
- Retrieval-based question answering
- Dynamic chatbot UI with Gradio
- Runs 100% free on Hugging Face
- Embedded via iframe in club website

## Tech Stack
- Python, Gradio, Hugging Face Spaces
- Sentence-Transformers for embeddings
- Cosine similarity for semantic search

## Local Setup
1. Clone the repo
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
