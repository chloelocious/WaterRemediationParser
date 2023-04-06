import re
import os
from transformers import pipeline
import json

# Load the fine-tuned model
qa_pipeline = pipeline("question-answering", model="/home/ssarrouf/Documents/qa_output/checkpoint-10000", tokenizer="batterydata/batterybert-cased-squad-v1")
# Define regular expressions to match relevant information
anode_regex = r"(?i)\b(anode|electrode)\b.*[.?!]"
cathode_regex = r"(?i)\b(cathode|electrode)\b.*[.?!]"
reactor_regex = r"(?i)\b(reactor)\b.*[.?!]"
batch_flow_regex = r"(?i)\b(batch|flow)\b.*[.?!]"
electrode_regex = r"(?i)\b(electrode configuration|configuration|electrode|cell|cells|column|vertical|horizontal)\b.*[.?!]"
contaminant_regex = r"(?i)\b(contaminant|contaminants|surfactant|surfactants|contamination)\b.*[.?!]"
efficiency_regex = r"(?i)\b(removal efficiency|efficienc(?:y|ies))\b.*[.?!]"
pollutant_regex = r"(?i)\b(pollutant|pollutants|pollution)\b.*[.?!]"
results = []
# Define a function to extract the relevant information from a text file
def extract_information(directory_path):
    context = "Default context value" 
    
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r") as f:
                text = f.read()

            # Extract relevant information
             # check if context is empty
        if not context:
            context="Default context value"
        else:    
            context = text.strip()
        
        question = ""
        answer = ""

        # Extract relevant information and generate question
        matches = re.findall(anode_regex, text)
        if len(matches) > 0:
            match = matches[0]
            start = text.rfind(".", 0, text.find(match)) + 1
            end = text.find(".", text.find(match))
            if isinstance(end, tuple):
                end = -1
            else:
                end += 1
            context = text[start:end].strip()
            #print(context)
            question = "What is the anode material?"
            answer = qa_pipeline(question=question, context=context)["answer"]
            #print(answer)
            results.append({"context": context, "question": question, "answer": answer})

        # Extract relevant information and generate question
        matches = re.findall(cathode_regex, text)
        if len(matches) > 0:
            match = matches[0]
            start = text.rfind(".", 0, text.find(match)) + 1
            end = text.find(".", text.find(match))
            if isinstance(end, tuple):
                end = -1
            else:
                end += 1
            context = text[start:end].strip()
            #print(context)
            question = "What is the cathode material?"
            answer = qa_pipeline(question=question, context=context)["answer"]
            #print(answer)
            results.append({"context": context, "question": question, "answer": answer})


        reactor_matches = re.findall(reactor_regex, text)
        batch_flow_matches = re.findall(batch_flow_regex, text)
        if len(reactor_matches) > 0 and len(batch_flow_matches) > 0:
            reactor_match = reactor_matches[0]
            batch_flow_match = batch_flow_matches[0]
            start = max(text.rfind(".", 0, text.find(reactor_match)), text.rfind(".", 0, text.find(batch_flow_match))) + 1
            end = text.find(".", text.find(match))
            if isinstance(end, tuple):
                end = -1
            else:
                end += 1
            context = text[start:end].strip()
            if not context:
                context = "Default context"
            #print(context)
            reactor_question = "Is the reactor batch or flow?"
            reactor_answer = qa_pipeline(question=reactor_question, context=context)["answer"]
            batch_flow_question = "What is the batch or flow rate?"
            batch_flow_answer = qa_pipeline(question=batch_flow_question, context=context)["answer"]
            results.append({"context": context, "question": reactor_question, "answer": reactor_answer})
            results.append({"context": context, "question": batch_flow_question, "answer": batch_flow_answer})
        elif len(reactor_matches) > 0:
            match = reactor_matches[0]
            start = text.rfind(".", 0, text.find(match[0])) + 1
            end = text.find(".", text.find(match))
            if isinstance(end, tuple):
                end = -1
            else:
                end += 1
            context = text[start:end].strip()
            #print(context)
            question = "Is the reactor batch or flow?"
            answer = qa_pipeline(question=question, context=context)["answer"]
            #print(answer)
            results.append({"context": context, "question": question, "answer": answer})
        elif len(batch_flow_matches) > 0:
            match = batch_flow_matches[0]
            start = text.rfind(".", 0, text.find(match[0])) + 1
            end = text.find(".", text.find(match))
            if isinstance(end, tuple):
                end = -1
            else:
                end += 1
            context = text[start:end].strip()
            #print(context)
            question = "Is the reactor batch or flow?"
            answer = qa_pipeline(question=question, context=context)["answer"]
            #print(answer)
            results.append({"context": context, "question": question, "answer": answer})

        matches = re.findall(electrode_regex, text)
        if len(matches) > 0:
            match = matches[0]
            start = text.rfind(".", 0, text.find(match[0])) + 1
            end = text.find(".", text.find(match))
            if isinstance(end, tuple):
                end = -1
            else:
                end += 1
            context = text[start:end].strip()
            #print(context)
            question = "What is the electrode configuration?"
            answer = qa_pipeline(question=question, context=context)["answer"]
            #print(answer)
            results.append({"context": context, "question": question, "answer": answer})

        matches = re.findall(contaminant_regex, text)
        if len(matches) > 0:
            match = matches[0]
            start = text.rfind(".", 0, text.find(match[0])) + 1
            end = text.find(".", text.find(match))
            if isinstance(end, tuple):
                end = -1
            else:
                end += 1
            context = text[start:end].strip()
            #print(context)
            question = "What are the treated contaminants?"
            answer = qa_pipeline(question=question, context=context)["answer"]
            #print(answer)
            results.append({"context": context, "question": question, "answer": answer})


        matches = re.findall(efficiency_regex, text)
        if len(matches) > 0:
            match = matches[0]
            start = text.rfind(".", 0, text.find(match[0])) + 1
            end = text.find(".", text.find(match))
            if isinstance(end, tuple):
                end = -1
            else:
                end = end + 1
            context = text[start:end].strip()
            #print(context)
            question = "What is the removal efficiency of contaminants?"
            answer = qa_pipeline(question=question, context=context)["answer"]
            #print(answer)
            results.append({"context": context, "question": question, "answer": answer})
        
        matches = re.findall(pollutant_regex, text)
        if len(matches) > 0:
            match = matches[0]
            #print(match)
            start = text.rfind(".", 0, text.find(match[0])) + 1
            end_index = text.find(match[0])
            if end_index != -1:
                end = text.find(".", end_index) if text.find(".", end_index) != -1 else text.find("?", end_index)
            else:
                end = -1
            context = text[start:end].strip()
            #print(context)
            question = "What are the treated pollutants?"
            answer = qa_pipeline(question=question, context=context)["answer"]
            #print(answer)
            results.append({"context": context, "question": question, "answer": answer})

# assume the list of dictionaries is stored in the variable `output_list`
qa_format_output_file = 'qa_format_output3.json'

extract_information('/home/ssarrouf/Documents/test_data_2')
with open(qa_format_output_file, 'w') as f:
    json.dump(results, f)

