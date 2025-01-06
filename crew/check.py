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
        "Identify the current market share of this industry and it's future prospects . Get the location of the company. Get possible legal problems this industry might face"
        "give the projected growth of the industry. the output i want is either negative growth, no growth, low growth, hight growth or very high growth"
        "give if the location is prone to natural disaster the output should be not prone, very rarely, rarely, frequently, very frequently"
        "give if the business is prone to legal trouble answer should be not likely, very slight chances, slight chance, high chances, very high chances"
        "make this into json format with growth as key and corresponding output as value and respectively with other outputs as well"
        "Analyze the project proposal to extract raw materials mentioned."
        "If raw materials are not specified, infer the likely raw materials needed for the business."
        "analyze the project proposal to extract the raw material suppliers."
        "if raw material supplier not mentioned in proposal,find the raw material supplier which is best (just get the name of the company). do this for all the raw materials. make sure that you always give a company name"
        " Use web tools like Serper to analyze the sources and methods for obtaining raw materials by each company and check how eco-friendly they are. If no information about the company is avialable then use general extraction process and check how eco-friendly it is"
        "Provide scores for each of the following sustainability goals affordable and clean energy,decent work and economic growth, industry, innovation, and infrastructure, responsible consumption and production, climate action, no poverty, zero hunger, good health and well-being, quality education, gender equality, clean water and sanitation, reduced inequalities, sustainable cities and communities,  peace, justice, and strong institutions, partnerships for the goals across ecological, economical, and social dimensions using the way raw material is extracted"
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
        "give the projected growth of the industry. the output i want is either negative growth, no growth, low growth, high growth or very high growth"
        "give if the location is prone to natural disaster the output should be not prone, very rarely, rarely, frequently, very frequently"
        "give if the business is prone to legal trouble answer should be not likely, very slight chances, slight chance, high chances, very high chances"
        "make this into json format with growth as key and corresponding output as value and respectively with other outputs as well"
        "A 3x15 matrix of scores where the three is ecological, economical, and social dimensions and for each thing we have 15 sustainable development so the score must be 1 for good 0.5 for partially good 0 for neutral -0.5 for partially bad -1 for bad "
        " (aligned with the Sustainable development goals; 'no poverty', 'zero hunger', 'good health and well-being', 'quality education', 'gender equality', 'clean water and sanitation', 'reduced inequalities', 'sustainable cities and communities', 'peace, justice, and strong institutions', 'partnerships for the goals''affordable and clean energy', 'decent work and economic growth', 'industry, innovation, and infrastructure', 'responsible consumption and production', 'climate action'). This score should be based on how eco-friendly the company that extract the materials is and the way the material is extracted give the reason for the score as notes based on the company that is extracting raw materials. the reason should saw how the company extracting the raw material affects this score"
        "give it to me in json format with keys as SDG goal name given and value as another dictionary with keys as Ecological, Economic, social, notes with corresponding output as value. finally make 1 single json format with first key as risk and give the dictinory with growth value second keh as resources with value as another dictionary with raw material name as key and company providing it as value and create another key as matrix and value as this dictionary you created for the 3X15 matrix"
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
    pdf_file_path = "..\\PROPOSAL.pdf"  # Replace with actual PDF file path
    main(pdf_file_path)
        