import fitz
import pandas as pd
import csv

doc =fitz.open('eb_parties.pdf')
pagecount = doc.page_count

e_dataframe = pd.DataFrame()

tables =[]
for i in range(0,pagecount):
    page = doc[i]
    table = page.find_tables()
    e_dataframe = pd.concat([ e_dataframe, table[0].to_pandas()])

e_dataframe.to_csv('file2.csv', index=False)

    
