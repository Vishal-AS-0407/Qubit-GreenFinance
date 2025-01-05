from crewai import Task
from tools import tool
from agents import news_researcher, news_writer

# researcher task
research_task = Task(
    description=(
        "Research and gather information about the following location for a green finance project: {location}. Focus on the following factors:\n" \
             "1. Cultural aspects\n" \
             "2. Demographics and people\n" \
             "3. Climate and weather patterns\n" \
             "4. Natural resources available\n" \
             "5. Local economic conditions\n" \
             "6. Relevant government policies or regulations for sustainability\n" \
             "Provide a comprehensive report on these aspects, citing reliable sources."

    ),
    expected_output="Provide a comprehensive report on these aspects, citing reliable sources."S,
    tools=[tool],
    agent=news_researcher
)

# writing task with language model configuration
