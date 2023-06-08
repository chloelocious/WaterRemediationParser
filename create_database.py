import os
import pandas as pd
import json
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

# the list of questions
questions = [
    "What is the anode material?",
    "What is the cathode material?",
    "What is the treated contaminant?",
    "What is the treated pollutant?",
    "What is the electrode configuration?",
    "Is the reactor batch or flow?",
    "What are the removal efficiencies?"
]

# load model
model_path = "/home/ssarrouf/Documents/qa_finetune_output_11/checkpoint-16000"
model = AutoModelForQuestionAnswering.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
qa_pipeline = pipeline('question-answering', model=model, tokenizer=tokenizer)

def extract_info(model, tokenizer, text):
    data = []
    text_parts = [text[i:i + 512] for i in range(0, len(text), 512)] # Break the text into chunks
    for question in questions:
        best_score = 0
        best_answer = ""
        for part in text_parts:
            inputs = tokenizer(question, part, return_tensors='pt', truncation=True, padding=True)
            outputs = model(**inputs)
            start_positions = outputs.start_logits.argmax(dim=-1)
            end_positions = outputs.end_logits.argmax(dim=-1)
            answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start_positions:end_positions+1]))
            prediction = qa_pipeline(question=question, context=part)
            if prediction['score'] > best_score:
                best_score = prediction['score']
                best_answer = answer
        data.append(best_answer)
    return data

def append_to_database(model, tokenizer, df):
    data = []
    for idx, row in df.iterrows():
        filepath = os.path.join(row['Set'], row['Publisher'], row['Filename'])
        print(f"Processing file: {filepath}")
        with open(filepath, 'r') as file:
            content = file.read()
        answers = extract_info(model, tokenizer, content)
        for i, question in enumerate(questions):
            print(f"Answer for '{question}': {answers[i]}")
        data.append(answers)
    answers_df = pd.DataFrame(data, columns=questions)
    df_extended = pd.concat([df, answers_df], axis=1)
    return df_extended

# load the existing dataframe
df_existing = pd.read_excel('/home/ssarrouf/Documents/GitHub/WaterRemediationParser/final_data_sheet.xlsx')

# append answers to dataframe
df_extended = append_to_database(model, tokenizer, df_existing)

df_extended.to_excel('database_extended.xlsx', index=False)
