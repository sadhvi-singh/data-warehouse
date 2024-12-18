# -*- coding: utf-8 -*-
"""process_bestbookever_csv_2_clean_jsonl.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EYAhhbiSeR0O7OsA7OgEocJpbpfUpXbu
"""

import pandas as pd

df = pd.read_csv('books_1.Best_Books_Ever.csv')
df.columns

import json

def combine_features(row):
  try:
    return row['description']+" "+row["genres"]
  except:
    print ("Error:", row)

def process_bestbookever_csv(input_file, output_file):

  books = pd.read_csv('books_1.Best_Books_Ever.csv')

  for f in ['title','description','genres']:
    books[f] = books[f].fillna('')

  books["text"] = books.apply(combine_features,axis=1)
  # Select only 'id', 'original_title', and 'text' columns
  books = books[['bookId', 'title', 'text']]
  #replaced only one column because rest all are fine
  books.rename(columns={'bookId': 'doc_id'}, inplace=True)

  # Create 'fields' column as JSON-like structure of each record
  books['fields'] = books.apply(lambda row: row.to_dict(), axis=1)

  # Create 'put' column based on 'doc_id'
  books['put'] = books['doc_id'].apply(lambda x: f"id:hybrid-search:doc::{x}")

  df_result = books[['put', 'fields']]
  print(df_result.head())
  df_result.to_json(output_file, orient='records', lines=True)


process_bestbookever_csv("books_1.Best_Books_Ever.csv", "clean_bestbooksever.jsonl")

import os
print("Saving file in:", os.getcwd())