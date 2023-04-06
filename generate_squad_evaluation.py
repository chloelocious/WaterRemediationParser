import json
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

# Load the SQuAD ground truth file
with open('/home/ssarrouf/Documents/GitHub/WaterRemediationParser/performance_evaluation/train-v1.1.json', 'r') as f:
    squad_data = json.load(f)

# Initialize an empty list for the predictions
predictions = []

# Load your tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("/home/ssarrouf/Documents/qa_output/checkpoint-10000")
model = AutoModelForQuestionAnswering.from_pretrained("/home/ssarrouf/Documents/qa_output/checkpoint-10000")

# Check the model's configuration
print(model.config)

# Loop over each article in the SQuAD ground truth file
for article in squad_data['data']:
    # Initialize an empty list for the paragraphs in the article
    paragraphs = []

    # Loop over each paragraph in the article
    for paragraph in article['paragraphs']:
        # Initialize an empty list for the QA pairs in the paragraph
        qas = []

        # Loop over each QA pair in the paragraph
        for qa in paragraph['qas']:
            # Tokenize the question and context
            question = qa['question']
            context = paragraph['context']
            inputs = tokenizer.encode_plus(question, context, return_tensors="pt", truncation=True, max_length=512)

            print(inputs)

            # Generate the model's prediction
            outputs = model(**inputs)
            print(outputs)  # Print the outputs to debug
            start_scores, end_scores = outputs['start_logits'], outputs['end_logits']

            # Convert start_scores and end_scores to tensors if they are not already
            if not isinstance(start_scores, torch.Tensor):
                start_scores = torch.tensor(start_scores)
            if not isinstance(end_scores, torch.Tensor):
                end_scores = torch.tensor(end_scores)

            print(type(start_scores))
            print(type(end_scores))
            answer_start = torch.argmax(start_scores)
            answer_end = torch.argmax(end_scores) + 1


            # Get the tokens corresponding to the best start and end positions
            answer_tokens = inputs["input_ids"][0][answer_start:answer_end]
            answer = tokenizer.decode(answer_tokens)

            # Create the answer dictionary
            answer_dict = {
                'text': answer,
                'answer_start': answer_start.item()
            }

            # Create the QA dictionary
            qa_dict = {
                'question': qa['question'],
                'id': qa['id'],
                'answers': [answer_dict]
            }

            # Add the QA dictionary to the list of QA pairs
            qas.append(qa_dict)

        # Create the paragraph dictionary
        paragraph_dict = {
            'context': paragraph['context'],
            'qas': qas
        }

        # Add the paragraph dictionary to the list of paragraphs
        paragraphs.append(paragraph_dict)

    # Create the article dictionary
    article_dict = {
        'title': article['title'],
        'paragraphs': paragraphs
    }

    # Add the article dictionary to the list of articles
    predictions.append(article_dict)

# Save the predictions to a JSON file
with open('squad_train_v1.1_predictions.json', 'w') as f:
    json.dump({'data': predictions}, f)
