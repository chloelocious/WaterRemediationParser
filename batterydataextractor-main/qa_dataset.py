import argparse
import json
import os

from batterydataextractor.doc import Document

### For creating test data for pretrain script ###

parser = argparse.ArgumentParser()
parser.add_argument('input_dir', help='Path to the input directory')
parser.add_argument('output_file', help='Path to the output file')
args = parser.parse_args()

input_dir = args.input_dir
output_file_path = args.output_file

processed_ids = set()
if os.path.exists(output_file_path):
    with open(output_file_path, 'r') as f:
        for line in f:
            contents = json.loads(line)
            processed_ids.add(contents['id'])

# extract data from each file in the input directory
with open(output_file_path, 'a') as of:
    for filename in os.listdir(input_dir):
        if not filename.endswith('.txt'):
            continue
        file_path = os.path.join(input_dir, filename)
        with open(file_path, 'r') as f:
            text = f.read()
            contents = {'id': filename, 'text': text}
            if contents['id'] in processed_ids:
                continue
            else:
                doc = Document(contents['text'])
                doc.add_models_by_names(["anode"])
                records = doc.records
                for r in records:
                    serialized_result = r.serialize()
                    # add the id field to the serialized result
                    serialized_result['id'] = contents['id']
                    # write the serialized result to the output file
                    of.write(json.dumps(serialized_result) + '\n')
