import google.generativeai as genai

genai.configure(api_key='AIzaSyBfRpWgkylVc9WmMyy_chmQyehXLEFMbA4')
model = genai.GenerativeModel("gemini-1.5-flash")


def viz_kpi(text):
            
    kpi_prompt = """
            Extract Key Performance Indicators from the following text and present them in a structured format:
            Text: {your_text_here}
            Output Format:
            {
                'KPI': ['KPI 1', 'KPI 2', 'KPI 3'],
                'Value': [value1, value2, value3],
                'Unit': ['Unit1', 'Unit2', 'Unit3']
            }
            """
    
    response = model.generate_content(kpi_prompt + text)
    return response.text

def viz_sroi(text):
            
    sroi_prompt = "Extract Social Return on Investment details from the following text:\n"

    response = model.generate_content(sroi_prompt + text)
    return response.text

def viz_cba(text):

    cba_prompt = "Extract Cost-Benefit Analysis details from the following text:\n"
    response = model.generate_content(cba_prompt + text)
    return response.text

def viz_roi(text):
            
    roi_prompt = """
            Extract Return on Investment (ROI) details from the following text and calculate the ROI:
            Text: {your_text_here}
            Output Format:
            {
                'Initial Investment': value,
                'Projected Revenue': value,
                'Net Profit': value,
                'ROI': 'Calculated ROI in percentage'
            }
            """
    
    response = model.generate_content(roi_prompt + text)
    return response.text
    
