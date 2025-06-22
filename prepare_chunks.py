import os
import pickle
import json

# Folder where .txt files are stored
data_folder = "data"
filename = "rtc_cleaned.txt"

# Full path to the file
filepath = os.path.join(data_folder, filename)

# This list will hold all chunks from all files
all_chunks = []

# Read the file
with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

current_page = None
current_section = None
content_lines = []

    # Loop over the rest of the lines
for line in lines[1:]:
    line = line.strip()
    # Normalize unicode characters to ASCII equivalents
    line = line.replace('\u00a0', ' ')  # non-breaking space → space
    line = line.replace('\u2013', '-')  # en dash → dash
    line = line.replace('\u2019', "'")  # curly apostrophe → straight apostrophe
    line = line.replace('\u201c', '"')  # left quote → straight quote
    line = line.replace('\u201d', '"')  # right quote → straight quote
    # Skip blank lines
    if not line:
        continue
    # Check if line starts with ### Page ---> new category
    if line.startswith("### Page:"):
        current_page = line.replace("### Page:", "").strip()
        continue
    
    # Check if line starts with ## Section: ---> new section under the category
    if line.startswith("## Section:"):
        # Save previous section if exists
        if current_section and content_lines:
            chunk = {
                "page": current_page,
                "section": current_section,
                "content": " ".join(content_lines)
            }
            all_chunks.append(chunk)
            content_lines = []
        current_section = line.replace("## Section:", "").strip()
        continue

    # Otherwise, save line as content
    content_lines.append(line)

# After loop ends, save the last chunk
if current_section and content_lines:
    chunk = {
        "page": current_page,
        "section": current_section,
        "content": " ".join(content_lines)
    }
    all_chunks.append(chunk)

# Save all chunks to a Pickle file for later use
with open("chunks.pkl", "wb") as f:
    pickle.dump(all_chunks, f)

# Save JSON version for readability
with open("chunks.json", "w", encoding="utf-8") as f_json:
    json.dump(all_chunks, f_json, indent=2)

print(f"Saved {len(all_chunks)} to chunks.pkl")