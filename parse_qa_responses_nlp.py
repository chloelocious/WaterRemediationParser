import spacy
import os
import json
from transformers import pipeline

# load spacy model
nlp = spacy.load("en_core_web_sm")

# load the fine-tuned question answering model
qa_pipeline = pipeline("question-answering", 
                        model="/home/ssarrouf/Documents/qa_output/checkpoint-10000", 
                        tokenizer="batterydata/batterybert-cased-squad-v1")

# specify the directory path to the text files
dir_path = "/home/ssarrouf/Documents/test_data_2"

# define the keywords to match
keywords = ["anode", "cathode", "batch", "flow", "electrode", "configuration", "contaminants", "removal", "efficiency", "pollutants", "cell", "column", "vertical", "horizontal", "contaminant", "contamination", "degradation", "efficiency", "pollutant", "pollution"]

# initialize an empty list to store the results
results = []

# loop through each file in the directory
for filename in os.listdir(dir_path):
    if filename.endswith(".txt"):
        # read the file contents
        with open(os.path.join(dir_path, filename), "r") as f:
            text = f.read()
        # process the text with spacy
        doc = nlp(text)
        # extract the relevant sentences from the text
        relevant_sentences = []
        for sent in doc.sents:
            for token in sent:
                if token.lower_ in keywords:
                    relevant_sentences.append(sent.text.strip())
                    break
        # create question-answer pairs based on the relevant sentences
        for sentence_text in relevant_sentences:
            # match the sentence against each keyword and generate the question
            if "anode" in sentence_text or "electrode" in sentence_text:
                question = "What is the anode material?"
                context = sentence_text
            elif "cathode" in sentence_text or "electrode" in sentence_text:
                question = "What is the cathode material?"
                context = sentence_text
            elif "batch" in sentence_text or "flow" in sentence_text or "reactor" in sentence_text:
                question = "Is the reactor batch or flow?"
                context = sentence_text
            elif "electrode" in sentence_text or "configuration" in sentence_text or "cell" in sentence_text or "column" in sentence_text or "vertical" in sentence_text or "horizontal" in sentence_text:
                question = "What is the electrode configuration?"
                context = sentence_text
            elif "contaminants" in sentence_text or "contaminant" in sentence_text or "contamination" in sentence_text:
                question = "What are the treated contaminants?"
                context = sentence_text
            elif "removal" in sentence_text or "efficiency" in sentence_text or "degradation" in sentence_text:
                if "%" in sentence_text:
                    question = "What is the removal efficiency of contaminants?"
                    context = sentence_text
                else:
                    continue
            elif "pollutants" in sentence_text or "pollutant" or "pollution":
                question = "What are the treated pollutants?"
                context = sentence_text
            else:
                continue
            # use the question answering pipeline to generate the answer
            answer = qa_pipeline(question=question, context=context)["answer"]
            results.append({
                "context": context,
                "question": question,
                "answer": answer
            })

# save the results to a json file
with open("spacy_results.json", "w") as f:
    json.dump(results, f, indent=4)
