from docx import Document 
import os
import pandas as pd

os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
# if os.path.exists("word_counts_no_one_counts.txt"):
df = pd.read_csv("word_frequency_no_one_counts.txt")

# df = df.reset_index()
batches = []
# counts = df["counts"].values.tolist()
words = df["words"].values.tolist()

batch_size = 5000

for i in range(len(words)):
  if i % batch_size == 0:
    batches.append(words[i:i+batch_size])

# for i in range(len(batches)):
#   with open(f'words{i}.txt', 'w', encoding="utf-8" ) as f:
#     for word in batches[i]:
#         f.write("%s\n" % word)

# df = pd.DataFrame(data={"words": words})
# df.to_csv("words.txt")

for i in range(len(batches)):
  current_batch = ""
  for txt in batches[i]:
    current_batch = current_batch + str(txt) + "\n"
  document = Document()
  document.add_paragraph(current_batch)
  document.save(f'words{i}.docx')
    
