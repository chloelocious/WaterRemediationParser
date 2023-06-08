import os
import pandas as pd
from transformers import AutoModelForQuestionAnswering, AutoTokenizer

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

def extract_info(model, tokenizer, text, questions):
    answers = []
    text_parts = [text[i:i + 512] for i in range(0, len(text), 512)] # Break the text into chunks
    for question in questions:
        answer_parts = []
        for part in text_parts:
            inputs = tokenizer(question, part, return_tensors='pt', truncation=True, padding=True)
            outputs = model(**inputs)
            start_positions = outputs.start_logits.argmax(dim=-1)
            end_positions = outputs.end_logits.argmax(dim=-1)
            answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start_positions:end_positions+1]))
            answer_parts.append(answer)
        answers.append(' '.join(answer_parts)) # Join all parts of the answer
    return answers


def append_to_database(model, tokenizer, df):
    data = []
    for idx, row in df.iterrows():
        try:
            filepath = os.path.join(row['Set'], row['Publisher'], row['Filename'])
            print(f"Processing file: {filepath}")
            with open(filepath, 'r') as file:
                content = file.read()
            answers = extract_info(model, tokenizer, content, questions)
            for i, question in enumerate(questions):
                print(f"Answer for '{question}': {answers[i]}")
            data.append(answers)
        except Exception as e:
            print(f"Error processing file {filepath}: {str(e)}")
            data.append([None for _ in questions])  # Append None values if there was an error
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
df_extended = append_to_database(model, tokenizer, df_existing)

# write to an Excel file
df_extended.to_excel('database_extended.xlsx', index=False)
