import pandas as pd
import re

df_existing = pd.read_excel('output_3.xlsx')
# split strings at "title" or "type"
def split_at_keywords(s):
    return re.split('title|type', s, flags=re.IGNORECASE)[0]

# change the 'DOI' values for rows where the 'Publisher' is 'Elsevier'
df_existing.loc[df_existing['Publisher'] == 'Elsevier', 'DOI'] = df_existing.loc[df_existing['Publisher'] == 'Elsevier', 'DOI'].apply(split_at_keywords)
# save to Excel file
df_existing.to_excel('output_3.xlsx', index=False)
