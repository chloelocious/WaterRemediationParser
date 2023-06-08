import os
import json
import pandas as pd
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

questions = [
    "What is the anode material?",
    "What is the cathode material?",
    "What is the treated contaminant?",
    "What is the treated pollutant?",
    "What is the electrode configuration?",
    "Is the reactor batch or flow?",
    "What are the removal efficiencies?"
]

def extract_info(model, tokenizer, text, questions):
    answers = []
    text_parts = [text[i:i + 512] for i in range(0, len(text), 512)]
    for question in questions:
        answer_parts = []
        for part in text_parts:
            inputs = tokenizer(question, part, return_tensors='pt', truncation=True, padding=True)
            outputs = model(**inputs)
            start_positions = outputs.start_logits.argmax(dim=-1)
            end_positions = outputs.end_logits.argmax(dim=-1)
            answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start_positions:end_positions+1]))
            answer_parts.append(answer)
        answers.append(' '.join(answer_parts))
    return answers

def append_to_database(model, tokenizer, df, ground_truth_file):
    qa_pipeline = pipeline('question-answering', model=model, tokenizer=tokenizer)
    data = []
    with open(ground_truth_file) as file:
        ground_truth = json.load(file)
    for idx, row in df.iterrows():
        filepath = os.path.join(row['Set'], row['Publisher'], row['Filename'])
        print(f"Processing file: {filepath}")
        with open(filepath, 'r') as file:
            content = file.read()
        answers = extract_info(model, tokenizer, content, questions)
        for i, question in enumerate(questions):
            print(f"Answer for '{question}': {answers[i]}")
            if ground_truth.get(question):
                best_answer = ''
                best_score = 0
                for ground_truth_answer in ground_truth[question]:
                    prediction = qa_pipeline(question=question, context=ground_truth_answer)
                    if prediction['score'] > best_score:
                        best_answer = prediction['answer']
                        best_score = prediction['score']
                answers[i] = best_answer if best_score > 0.9 else answers[i]
        data.append(answers)
    answers_df = pd.DataFrame(data, columns=questions)
    df_extended = pd.concat([df, answers_df], axis=1)
    return df_extended

# load model
model_path = "/home/ssarrouf/Documents/qa_finetune_output_6/checkpoint-16000"
model = AutoModelForQuestionAnswering.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# load dataframe
df_existing = pd.read_excel('/home/ssarrouf/Documents/GitHub/WaterRemediationParser/final_data_sheet.xlsx')

# append answers to dataframe
ground_truth_file = '/home/ssarrouf/Documents/GitHub/WaterRemediationParser/ground_truth_updated.json'
df_extended = append_to_database(model, tokenizer, df_existing, ground_truth_file)
df_extended.to_excel('database_extended.xlsx', index=False)
