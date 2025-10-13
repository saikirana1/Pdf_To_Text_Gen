# # from clean_pdf_data.extract_pages import extract_pages
# # from ai_agents.data_decison_agent import data_decison_agent
# # import asyncio

# # t=extract_pages("invoice-pdf/p-1.pdf")
# # final_result = asyncio.run(data_decison_agent(t))
# # print(final_result)
# # from open_ai.invoice_pdf_to_json import invoice_pdf_json


# # t = invoice_pdf_json("invoice-pdf/invoice4.pdf")
# # print(t)

# # from database_sql.create_table import create_db_and_tables
# # t=create_db_and_tables()
# # print(t)


# import json

# import datetime
# data = {
#     "result": [
#         {
#             "invoice_no": "19221",
#             "invoice_date": datetime.date(2025, 9, 17),
#             "items": [
#                 {
#                     "item_name": "L-Mini Tub Sitaphal - 125 ML (6 Nos) - P-Code:211",
#                     "hsn_code": "21050000",
#                     "quantity": 1.0,
#                     "unit_price": 360.0,
#                     "unit_taxable_amount": 305.08,
#                     "tax": "18%",
#                     "unit_tax_amount": 54.92,
#                     "amount": 360.0,
#                     "mrp_price": 360.0,
#                 }
#             ],
#             "bank_details": [
#                 {
#                     "account_number": "259866000988",
#                     "ifsc_code": "INDB0001723",
#                     "holder_name": "Harvish Enterprises",
#                     "bank_name": "IndusInd Bank",
#                     "branch": "Jubliee Hills",
#                 }
#             ],
#             "sellers": [
#                 {
#                     "address": "Opposite N.M.D.C Office, Shop No. 4, Ground Floor, 10-3-316, Gulmohar Garden, Masab Tank, Hyderabad, 500028",
#                     "contact": "harvish.icecream@gmail.com",
#                     "gst_number": "36AAPFH2469F1Z4",
#                     "fssai_no": "10021042000455",
#                     "pin_code": "500028",
#                 }
#             ],
#             "payments": [
#                 {
#                     "sub_total": 360.0,
#                     "s_gst": None,
#                     "c_gst": None,
#                     "discount": None,
#                     "total": 360.0,
#                 }
#             ],
#             "customers": [
#                 {
#                     "name": "Retail-Masab Tank",
#                     "address": "gulmohar Garden Masab Tank, Opp NMDC, Hyderabad, Hyderabad, Telangana - 500028",
#                     "gst_number": "NA",
#                 }
#             ],
#         }
#     ]
    
# }


# print(json.dumps(data, indent=4, default=str))


# agents_example.py


# import asyncio
# from agents import Agent, Runner, SQLiteSession

# from open_ai.client import openai_client



# client = openai_client()






# async def main():
#     agent = Agent(
#         name="Assistant",
#         instructions="Reply very concisely.",
#     )
#     session = SQLiteSession("conversation_123", "conversation_history.db")

#     print("=== Sessions Example ===")
#     print("The agent will remember previous messages automatically.\n")

#     # First turn
#     print("First turn:")
#     print("User: What city is the Golden Gate Bridge in?")
#     result = await Runner.run(
#         agent, "What city is the Golden Gate Bridge in?", session=session
#     )
#     print(f"Assistant: {result.final_output}")
#     print()

#     # Second turn - the agent will remember the previous conversation
#     print("Second turn:")
#     print("User: What state is it in?")
#     result = await Runner.run(agent, "What state is it in?", session=session)
#     print(f"Assistant: {result.final_output}")
#     print()

#     # Third turn - continuing the conversation
#     print("Third turn:")
#     print("User: What's the population of that state?")
#     result = await Runner.run(
#         agent, "What's the population of that state?", session=session
#     )
#     print(f"Assistant: {result.final_output}")
#     print()

#     print("=== Conversation Complete ===")
#     print("Notice how the agent remembered the context from previous turns!")
#     print("Sessions automatically handles conversation history.")


# if __name__ == "__main__":
#     asyncio.run(main())



# from pinecone_v_db.create_dense_db import dense_create_or_get_db
# t=dense_create_or_get_db()
# print(t)


from supabase_packages.upload_file import do
from supabase_packages.get_file_url import get_file_url
t =get_file_url("demo.pdf")
print(t)






