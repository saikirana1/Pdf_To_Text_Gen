from ai_agents.multi_agent_handoff import multi_agent_handoff
import asyncio
from ai_agents.demo import demo
# from clean_pdf_data.pdf_json_data import pdf_to_json
from clean_pdf_data.pdf_plain_text import extract_plain_text_outside_tables
# from ai_agents.sql_agent import sql_agent


# multi_agents_manager_result = asyncio.run(multi_agents_manager())
# print(multi_agents_manager_result)
# t = multi_agent_handoff()

# # print(t)
# t = demo()
# t = multi_agent_handoff("what is my latest transaction ")
# print(t)


# t=pdf_to_plaintext_json(
#     "invoice-pdf/bank.pdf",
#     "transactions8.json",
   
# )
# print(t)

out = extract_plain_text_outside_tables("invoice-pdf/p_bank.pdf", "plain.json")
if not out:
 print("No plain text outside tables found.")
else:
 print(f"Extracted plain text outside tables -> plain_text_only.json")