# from database_sql.database_connection import get_session

# t = get_session()
# print(t)


from open_ai.pdf_to_json_data_extract import pdf_to_json_data_extract, client

from practice_demo.clean_transaction_data import clean_transaction_data
from database_sql.insert_data import insert_data
from database_sql.create_table import create_db_and_tables
from database_sql.query_data import query_data
from open_ai.llm_sql_query import llm_sql_query
from open_ai.synthesizing_data import synthesizing_data
import json
# with open("p-1.pdf", "rb") as f:
#     uploaded_file = client.files.create(file=f, purpose="user_data")

# data = pdf_to_json_data_extract(uploaded_file)
# print(data)

# print(t)


# t = query()
# print(t)

# t = create_db_and_tables()
# print(t)
# input_prompt = "what is maximum withdraw"
# sql_query = llm_sql_query(input_prompt)
# print(sql_query)
# query_result = query_data(sql_query)
# print(query_result)

# final_result = synthesizing_data(input_prompt, sql_query, query_result)
# print(final_result)

# import json

# with open("cleaned_data.json", "r") as file:
#     json_data = json.load(file)
#     print(len(json_data))
# t = insert_data(json_data)


# with open("transactions4.json", "r") as infile:
#     json_data = json.load(infile)

# # Clean the data
# cleaned_data = clean_transaction_data(json_data)

# # Save cleaned data to a new JSON file
# with open("cleaned_data.json", "w") as outfile:
#     json.dump(cleaned_data, outfile, indent=4)

# print("Data cleaned and saved to 'cleaned_data.json'")
