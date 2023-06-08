from transformers import BertTokenizerFast, BertForTokenClassification
from transformers import Trainer, TrainingArguments
import torch
import os

class MyDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def parse_brat_file(directory, basename):
    txt_file = os.path.join(directory, f'{basename}.txt')
    ann_file = os.path.join(directory, f'{basename}.ann')

    with open(txt_file, 'r') as f:
        text = f.read()

    with open(ann_file, 'r') as f:
        annotations = f.readlines()

    entities = []
    for annotation in annotations:
        parts = annotation.strip().split('\t')
        if parts[0].startswith('T'):
            entity_id, entity_info, entity_text = parts
            entity_type, start_char, end_char = entity_info.split(' ')
            start_char, end_char = int(start_char), int(end_char)
            assert text[start_char:end_char] == entity_text
            entities.append({
                'id': entity_id,
                'type': entity_type,
                'start_char': start_char,
                'end_char': end_char,
                'text': entity_text,
            })

    return text, entities

# Update the directory to match your data
directory = '/path/to/your/files'

# Initialize a tokenizer
tokenizer = BertTokenizerFast.from_pretrained('your-model')

# Initialize a model
model = BertForTokenClassification.from_pretrained('your-model', num_labels=3)

# Loop through the .ann files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.ann'):
        basename = os.path.splitext(filename)[0]

        # Parse the brat file
        text, entities = parse_brat_file(directory, basename)

        # Let's say you've parsed multiple documents and have the following lists:
        texts = [text]  # list of document texts
        entities_lists = [entities]  # list of corresponding lists of entities

        # Convert the data into a list of dictionaries, each representing one example
        data = []
        for text, entities in zip(texts, entities_lists):
            labels = ['O'] * len(text)
            for entity in entities:
                start_char = entity['start_char']
                end_char = entity['end_char']
                label = 'B-' + entity['type']
                labels[start_char] = label
                for i in range(start_char+1, end_char):
                    labels[i] = 'I-' + entity['type']

            data.append({'text': text, 'labels': labels})

        # Tokenize the texts
        encoding = tokenizer([example['text'] for example in data], truncation=True, padding=True)

        # Convert the labels to the format expected by BertForTokenClassification and map them to token level
        labels = []
        for i, (example, annotation) in enumerate(zip(data, encoding.encodings)):
            doc_labels = ['O'] * len(annotation.tokens)
            for entity in example['labels']:
                entity_start, entity_end, entity_label = entity['start_char'], entity['end_char'], entity['type']
                for token_start, token_end, token_id in annotation.offsets:
                    if entity_start <= token_start and token_end <= entity_end:
                        doc_labels[token_id] = entity_label
                    elif entity_start <= token_start < entity_end or entity_start < token_end <= entity_end:
                        doc_labels[token_id] = 'I-' + entity_label

            labels.append(doc_labels)

        # Convert labels to their corresponding IDs in the model's classification head
        label_map = {'O': 0, 'B-TYPE': 1, 'I-TYPE': 2}
        label_ids = [[label_map[label] for label in doc_labels] for doc_labels in labels]

        # Add the label_ids to the encoding
        encoding['labels'] = label_ids

        # Convert the encoding to a PyTorch dataset
        dataset = MyDataset(encoding, label_ids)

        # Define training arguments
        training_args = TrainingArguments(
            output_dir=f'./results/{basename}',
            num_train_epochs=3,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=64,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir=f'./logs/{basename}',
        )

        # Initialize a Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset,
        )

        # Train the model
        trainer.train()
