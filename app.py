import pickle
import gradio as gr
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import requests
import os
import gdown

def download_embeddings():
    file_id = "1XxKjr-Ml_yUyvNpm_dQvYKusJFDBTXwX"
    url = f"https://drive.google.com/uc?id=1XxKjr-Ml_yUyvNpm_dQvYKusJFDBTXwX"
    output = "embeddings.pkl"

    if not os.path.exists(output):
        print("Downloading embeddings.pkl from Google Drive...")
        gdown.download(url, output, quiet=False)
        print("Download complete.")
    else:
        print("embeddings.pkl already exists.")

download_embeddings()



# Load chunks and embeddings from pickle file
with open("embeddings.pkl", "rb") as f:
    data = pickle.load(f)
chunks = data["chunks"]
embeddings = data["embeddings"]

# Load embedding model (same as used in preprocessing)
embed_model = SentenceTransformer("all-mpnet-base-v2")

# Load Eleuther's GPT-Neo 125M response model for text generation
generator = pipeline('text2text-generation', model='google/flan-t5-base', device=-1)

# Set seed for reproducibility
# set_seed(42)

# Function to handle questions and create responses
def answer_question(user_input, history):
    # Embed the user's input
    query_vector = embed_model.encode([user_input])

    # Calculate cosine similarity to each chunk
    similarities = cosine_similarity(query_vector, embeddings)[0]
    
    # Get indices of top 3 most similar chunks
    top_indices = similarities.argsort()[-5:][::-1] # sort descending
    print(similarities[top_indices])

    # If best similarity is too low, return fallback message
    if similarities[top_indices[0]] < 0.3:
        return "I'm not sure how to answer that based on the information I have. Could you try rephrasing your question?"
    # Optional: print top chunk metadata
    for idx in top_indices: 
        score = similarities[idx]
        chunk = chunks[idx]
        print(f"Score: {score:.4f} | Page: {chunk['page']} | Section: {chunk['section']}")


    # Combine top 3 chunks into one prompt
    retrieved_info = ""
    for idx in top_indices:
        chunk = chunks[idx]
        retrieved_info += f"\n[{chunk['page']} > {chunk['section']}]\n{chunk['content']}\n"
    # Build a prompt using context and the user's question
    prompt = f"""You are a friendly and helpful assistant for Russell Tennis Center, Use the information below (retrieved from the official website) to answer the user's question in full sentences.
    Be friendly and professional, like you're chatting with a potential or current member. Please form a clear and complete response. Do not guess or make up information. 
    If the answer cannot be found in the provided text, say 'I’m not sure based on the available information, but you can email us at info@russelltenniscenter.com or try rephrasing'.
    Information:
    {retrieved_info}

    Question: {user_input}
    Answer:"""

    # Generate the response using GPT-Neo
    result = generator(prompt, max_new_tokens=100)
    
    # Get the actual generated string
    response = result[0]["generated_text"]
    # Clean response output
    answer_start = response.find("Answer:")
    if answer_start != -1:
        return response[answer_start + len("Answer:"):].strip()
    else:
        return response.strip()
    
# Wrap answer_question function with the Gradio chat interface
chatbot = gr.ChatInterface(
    fn=answer_question,
    type="messages",
    examples=["What programs do you offer?", "How do I contact Russell Tennis Center?", "What program can a 6-9 year old do?", "What program can a 10-12 year old do?", "What program can a 12-18 year old do?"],
    run_examples_on_click=True,
    cache_examples=True,
    title="🎾 Russell Tennis Center Chatbot",
    description="Ask me anything about programs, clinics, camps, or anything else from the RTC website!<br><br><sub><i>Made by Shaili Vemuri</i></sub>",
    theme="soft",
    submit_btn="Ask",
    stop_btn="Stop", 
)

# Wrap anser_question function with Gradio's ChatInterface
if __name__ == "__main__":
    chatbot.launch(share=True)