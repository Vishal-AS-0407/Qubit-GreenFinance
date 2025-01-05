from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import os
import PyPDF2  
from crewai_tools import SerperDevTool  
from crewai import Agent
from dotenv import load_dotenv
import os
from crewai import LLM
load_dotenv()
import PyPDF2
import re

#SETTING UP KEY
os.environ['SERPER_API_KEY'] = "6f2227a931b482b6e1b21298ecc47bb6865beb28"

#LLM
llm = LLM(
    model="gemini/gemini-1.5-flash",
    temperature=0.7,
    api_key="AIzaSyBNOQJ3D5xVYeKt7xokZlQ-zXZrKwGgspE"
)

#TOOLS
# Initialize the tool for internet searching capabilities
serper_tool = SerperDevTool()

#AGENTS
# Define the Raw Material Agent
rawmaterial_inference = Agent(
    role="Raw Material Analysis Agent",
    goal=(
        "Analyze the project proposal to extract raw materials mentioned."
        " If raw materials are not specified, infer the likely raw materials needed."
        " Use web tools like Serper to analyze the sources and methods for obtaining raw materials."
        " Provide scores for each of the 17 sustainability goals across ecological, economical, and social dimensions."
        " Create a detailed report"
        "This is the project proposal content {project_report}"
    ),
    verbose=True,
    memory=True,
    backstory=(
        "This agent helps evaluate the sustainability of raw material usage and collection methods."
    ),
    tools=[serper_tool],
    llm=llm,
)

#TAKS
# Define the Raw Material Task
rawmaterial_task = Task(
    description=(
        "Extract raw materials from the uploaded this project proposal {project_report}."
        " Score the sustainability of the methods used for raw material collection ."
    ),
    expected_output=(
        "A 3x17 matrix of scores where the three is ecological, economical, and social dimensions and for each thing we have 17 sustainable development so the score must be 1 for good 0.5 for partially good 0 for neutral -0.5 for partially bad -1 for bad "
        " (aligned with the 17 Sustainable Development Goals)."
        " A detailed report with insights about the raw materials, collection methods, and this information will be passed into another llm so it should be able to understand the context and information so keep that in minds"
    ),
    tools=[serper_tool],
    agent=rawmaterial_inference,
)

#CREW
crew = Crew(
    agents=[rawmaterial_inference],
    tasks=[rawmaterial_task],
    process=Process.sequential,
)



#HELPER FUNCTIONS
def extract_text_from_pdf(pdf_file):
    """
    Extracts and cleans text from an uploaded PDF file.
    Removes unwanted characters, excessive spaces, and non-text elements.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""

        # Extract text from each page
        for page in pdf_reader.pages:
            raw_text = page.extract_text()
            
            # Clean up the extracted text
            clean_text = re.sub(r'[^\w\s.,;:!?\'\"()\-]', '', raw_text)  # Remove special characters except punctuation
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()  # Remove excessive whitespace
            text += clean_text + "\n"
        
        return text

    except Exception as e:
        print("Error extracting text from PDF:", e)
        return None


#MAIN 
def main(pdf_file_path):
    # Extract text from the project proposal PDF
    extracted_text = extract_text_from_pdf(pdf_file_path)
    if not extracted_text:
        print("Failed to extract text from the PDF.")
        return

    # Provide input to the Crew and kickoff the process
    result = crew.kickoff(inputs={"project_report": extracted_text})
    print(result)


#FINAL CALLER
if __name__ == "__main__":
    pdf_file_path = "C:\\Users\\visha\\OneDrive\\Desktop\\data\\PROPOSAL.pdf"  # Replace with actual PDF file path
    main(pdf_file_path)
        