import streamlit as st
import wave
import pyaudio
import requests
from PIL import Image
import easyocr
import numpy as np
import google.generativeai as genai
import os
import re
import PyPDF2  # Added for PDF processing

# Configure Gemini API
genai.configure(api_key="AIzaSyAjhjE1-c6vcFixyO6lOIHQUE8a15peRd0")
model = genai.GenerativeModel("gemini-1.5-flash")


def record_audio(filename, duration=5, rate=44100, chunk=1024):
    """Records audio from the microphone and saves it as a .wav file."""
    audio = pyaudio.PyAudio()

    # Open the stream
    stream = audio.open(format=pyaudio.paInt16, 
                        channels=1, 
                        rate=rate, 
                        input=True, 
                        frames_per_buffer=chunk)
    
    st.write(f"Recording for {duration} seconds...")
    frames = []

    # Record the audio
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    st.write("Recording complete.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a .wav file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))


def send_to_sarvam_api(filepath):
    """Sends the recorded audio file to the Sarvam AI API for speech-to-text translation."""
    url = "https://api.sarvam.ai/speech-to-text-translate"
    
    headers = {
        'api-subscription-key': 'Enter your Key'
    }
    
    payload = {
        'model': 'saaras:v1',
        'prompt': ''  # Empty prompt if not required
    }

    with open(filepath, 'rb') as audio_file:
        files = [('file', (filepath, audio_file, 'audio/wav'))]
        response = requests.post(url, headers=headers, data=payload, files=files)
    
    if response.status_code == 200:
        response_data = response.json()
        if "transcript" in response_data:
            return response_data["transcript"]
        else:
            return "Transcript key not found in response."
    else:
        return f"Failed to transcribe speech. HTTP Status Code: {response.status_code}"


def generate_response(input_text, chat_history=None):
    try:
        if chat_history:
            input_text = "\n".join(chat_history) + f"\nUser: {input_text}\nBot:"

        input_text = f"""Here's the updated prompt that focuses on analyzing the project for approval, with a critical perspective:

                ---

                **You are an AI-powered assistant designed to evaluate, assess, and critique green finance proposals for approval. Your primary objective is to provide a comprehensive analysis of project proposals in the context of their potential environmental, social, and governance (ESG) impact, financial viability, and sustainability goals.**

                Your task is to analyze the provided project proposal by focusing on the following key aspects:

                1. **Relevance and Impact on Sustainability Goals**:
                    - How well does the project align with the broader sustainability objectives of green finance? 
                    - Evaluate the proposed metrics for measuring ESG impact, and suggest improvements or additional metrics if necessary.

                2. **Evaluation and Scoring Mechanisms**:
                    - Critique the methodology for scoring projects based on their sustainability impact.
                    - Do the predefined ESG metrics adequately capture the key factors that should drive green finance decisions?
                    - Assess the AI model's potential for evaluating project sustainability, identifying gaps in its approach, or suggesting improvements.

                3. **Optimization and Resource Allocation**:
                    - Evaluate the proposed optimization techniques (e.g., linear programming, portfolio theory). Are they suitable for maximizing ESG impact while respecting financial constraints? 
                    - Critique the robustness of the optimization engine in handling various constraints like budget, risk tolerance, and uncertainty.
                    - Can the resource allocation strategy be further enhanced to ensure efficient capital deployment?

                4. **Risk Prediction**:
                    - Assess the platform's ability to predict future risks associated with green investments.
                    - Are there sufficient data sources and risk prediction models? Suggest potential risks not currently covered or other factors that should be considered in forecasting investment risks.

                5. **Data Processing and Integration**:
                    - Analyze the approach for collecting and processing ESG data from various sources. Are these data sources credible, comprehensive, and aligned with industry standards?
                    - Evaluate the integration of climate data (e.g., rainfall, emissions) and economic metrics. Is there any additional data that should be considered to enhance the analysis?

                6. **User Experience and Stakeholder Engagement**:
                    - Review the proposed dashboard features for stakeholders. Are the visualizations intuitive and actionable? 
                    - Critically assess whether the scenario analysis feature is robust enough to support strategic decision-making and if it fully addresses the needs of stakeholders in the financial sector.

                7. **Potential for Improvement**:
                    - Provide actionable insights on how the project proposal can be refined or enhanced to better serve its goals and maximize its impact.
                    - Highlight any potential challenges or risks that the proposal should address to ensure its successful implementation.

                Always maintain a professional, objective, and comprehensive tone while critiquing the proposal. Ensure your analysis provides clear, actionable feedback that can guide the next steps in the project's approval and development process.

                **Now, analyze the following project proposal and provide your detailed insights:**
                THE PROJECT PROPOSAL IS GIVEN BELOW

                {input_text}

                        """

        response = model.generate_content(input_text)
        return response.text if response.text else "No response generated."
    except Exception as e:
        st.error(f"Error: {e}")
        return "Error: Could not generate a response."


def protect_sensitive_info(text):
    def mask_bank_account(match):
        bank_acc_text = match.group(1)
        bank_acc_num = match.group(2)
        visible_part = bank_acc_num[:4]
        masked_part = '*' * (len(bank_acc_num) - 4)
        return f"{bank_acc_text}{visible_part + masked_part}"
    
    bank_acc_pattern = r'(bankacc)(\d+)'
    protected_text = re.sub(bank_acc_pattern, mask_bank_account, text)
    return protected_text


def extract_text_from_pdf(pdf_file):
    """Extracts text from an uploaded PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

        # Apply privacy protection
        protected_text = protect_sensitive_info(text.strip())
        return protected_text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return "Error: Could not extract text from the PDF."


def main():
    st.title("Customer Care and Doubt Clarification")
    st.write("Chat using text, speech, or PDF input!")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    st.sidebar.header("Input Options")
    
    # PDF Upload
    uploaded_pdf = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

    # Speech Input
    st.sidebar.subheader("Speech Input")
    if st.sidebar.button("Start Recording"):
        audio_file = "recorded_audio.wav"
        record_duration = st.sidebar.slider("Recording Duration", 1, 10, 5)
        record_audio(audio_file, duration=record_duration)
        transcribed_text = send_to_sarvam_api(audio_file)
        if os.path.exists(audio_file):
            os.remove(audio_file)
        if transcribed_text:
            st.session_state['speech_input'] = transcribed_text
            st.sidebar.success(f"Transcribed Text: {transcribed_text}")

    prompt = st.text_input("Enter your prompt:", value=st.session_state.get('speech_input', ''))

    protected_prompt = protect_sensitive_info(prompt)

    extracted_text = ""
    if uploaded_pdf is not None:
        extracted_text = extract_text_from_pdf(uploaded_pdf)
        st.write("**Extracted Text from PDF:**")
        st.write(extracted_text)

    if st.button("Send"):
        combined_input = f"PDF context: {extracted_text}\nUser prompt: {protected_prompt}" if extracted_text else protected_prompt
        response = generate_response(combined_input, st.session_state["chat_history"])
        st.session_state["chat_history"].append(f"User: {protected_prompt}")
        st.session_state["chat_history"].append(f"Bot: {response}")
        st.write("**Bot Response:**")
        st.write(response)

    if st.session_state["chat_history"]:
        st.write("**Chat History:**")
        for chat in st.session_state["chat_history"]:
            st.write(chat)


if __name__ == "__main__":
    main()
