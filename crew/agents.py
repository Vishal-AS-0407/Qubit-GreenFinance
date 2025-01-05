import os
from crewai import Agent
from tools import tool
from dotenv import load_dotenv
from crewai import LLM
load_dotenv()

llm = LLM(
    model="gemini/gemini-1.5-flash",
    temperature=0.7,
    api_key="AIzaSyBNOQJ3D5xVYeKt7xokZlQ-zXZrKwGgspE"
)
# create a senior researcher agent with memory and verbose mode

news_researcher = Agent(
    role="Project Researcher",
    goal="Research and gather detailed information about the project location including culture, people, climate, and natural resources.",
    verbose=True,
    memory=True,
    backstory=("You're a skilled researcher with a strong focus on understanding the environmental, social, and cultural factors of project locations. "
               "You're adept at utilizing web-based tools to gather the most relevant information to inform project development decisions."),
    tools=[tool],
    llm=llm,
    allow_delegation=True
)
# creating a write agent with custom tools responsible in writing news blog

news_writer = Agent(
    role="cHECKER",
    goal="cHECK THE CONTENT GIVEN IS CORRECT ",
    verbose=True,
    memory=True,
    backstory=(
         ""
    ),
    tools=[tool],
    llm=llm,
    allow_delegation=False
)