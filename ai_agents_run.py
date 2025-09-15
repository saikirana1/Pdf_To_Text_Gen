from ai_agents.multi_agent_handoff import multi_agent_handoff
import asyncio
from ai_agents.demo import demo

# from ai_agents.sql_agent import sql_agent


# multi_agents_manager_result = asyncio.run(multi_agents_manager())
# print(multi_agents_manager_result)
# t = multi_agent_handoff()

# # print(t)
# t = demo()
t = multi_agent_handoff("what is my latest transaction ")
print(t)
