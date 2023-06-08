import json
from transformers import BertTokenizerFast, BertForQuestionAnswering

# load model
model = BertForQuestionAnswering.from_pretrained('/home/ssarrouf/Documents/qa_finetune_output_3/checkpoint-5400/')
tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')

# load validation dataset
validation_dataset = '/home/ssarrouf/Documents/GitHub/WaterRemediationParser/performance_evaluation/updated_data_6_reformatted.json'  # Preprocessed validation dataset

# generate prediction for a single example
def predict(context, question):
    inputs = tokenizer.encode_plus(question, context, return_tensors='pt', max_length=384, truncation=True)
    input_ids = inputs['input_ids']
    token_type_ids = inputs['token_type_ids']
    attention_mask = inputs['attention_mask']

    outputs = model(input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask)
    start_logits, end_logits = outputs.start_logits, outputs.end_logits

    all_tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    answer = ' '.join(all_tokens[torch.argmax(start_logits): torch.argmax(end_logits) + 1])
    return tokenizer.convert_tokens_to_string(answer)

# generate predictions
predictions = {}
for example in validation_dataset:
    context = example['context']
    question = example['question']
    question_id = example['id']
    answer = predict(context, question)
    predictions[question_id] = answer

# save predictions to a JSON file
with open('qa_output_3_predictions.json', 'w') as outfile:
    json.dump(predictions, outfile)
import torch
from batterybert.finetune import QAModel, FinetuneTokenizerFast
from transformers import BertForQuestionAnswering

# load fine-tuned model and custom tokenizer
model_name_or_path = "/path/to/your/fine-tuned/model"
model = QAModel(model_name_or_path).get_model()
tokenizer = FinetuneTokenizerFast(model_name_or_path).get_tokenizer()

def predict(context, question):
    inputs = tokenizer.encode_plus(question, context, return_tensors="pt", max_length=512, truncation=True)
    input_ids = inputs["input_ids"].tolist()[0]

    outputs = model(**inputs)
    answer_start_scores = outputs.start_logits
    answer_end_scores = outputs.end_logits

    answer_start = torch.argmax(answer_start_scores)  # Get the most likely beginning of the answer
    answer_end = torch.argmax(answer_end_scores) + 1  # Get the most likely end of the answer (inclusive)

    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

    return answer
