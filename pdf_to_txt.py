import os

rootDir = '/home/ssarrouf/Documents/train_data_3'

for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        # open the files in directory
        with open(os.path.join(dirName, fname), 'r') as file:
            file_content = file.read()
            # replace multiple spaces with a single space
            file_content = re.sub(' +', ' ', file_content)
            # remove spaces between a lowercase and an uppercase letter
            file_content = re.sub(r'([a-z]) ([A-Z])', r'\1\2', file_content)
            # remove spaces between lowercase letters and between uppercase letters
            file_content = re.sub(r'([a-z]) ([a-z])|([A-Z]) ([A-Z])', r'\1\2\3\4', file_content)

        # write the cleaned content back to the file
        with open(os.path.join(dirName, fname), 'w') as file:
            file.write(file_content)

