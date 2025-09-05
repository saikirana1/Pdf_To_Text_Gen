from dotenv import load_dotenv
import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.sql import SQLTools
from sqlmodel import SQLModel, create_engine, Session

# Load environment variables
load_dotenv()

# Get Neon DB URL from .env
db_url = os.getenv("DATABASE_URL")

if not db_url:
    raise ValueError("DATABASE_URL not set in .env!")

# Create SQLModel engine
engine = create_engine(db_url, echo=True)

# (Optional) If you have models, you can create tables:
# SQLModel.metadata.create_all(engine)

# Create a session
session = Session(engine)

# Attach SQL tools (with SQLModel engine)
sql_tools = SQLTools(engine=engine)

# Build the agent
sql_agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),  # or gpt-4o
    tools=[sql_tools],
    show_tool_calls=True,
    markdown=True,
)

print("✅ Connected to Neon Database")
print("💡 Ask me questions like:")
print("- What is the total withdrawal?")
print("- What is the average deposit amount?")
print("- Show me the maximum balance.")
print("- How many invoices are there?")
print("- What is the sum of withdrawals between Jan 2025 and Mar 2025?")
print("Type 'exit' to quit.\n")

# Interactive loop
while True:
    user_question = input("\n❓ Your Question: ")
    if user_question.lower() in ["exit", "quit", "q"]:
        print("👋 Exiting... Goodbye!")
        break

    try:
        answer = sql_agent.run(user_question)
        print("👉 Answer:", answer)
    except Exception as e:
        print("⚠️ Error:", e)
