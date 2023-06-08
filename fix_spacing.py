import os
import wordninja

top_dir = '/home/ssarrouf/Documents/wiley_txt_files'

# walk through all files in the directory and its subdirectories
for dirpath, dirnames, filenames in os.walk(top_dir):
    for filename in filenames:
        # check if the file is a text file
        if filename.endswith('.txt'):
            file_path = os.path.join(dirpath, filename)
            # open and read the file
            with open(file_path, 'r') as file:
                content = file.read()
                words = wordninja.split(content)
                new_content = ' '.join(words)
            with open(file_path, 'w') as file:
                file.write(new_content)

