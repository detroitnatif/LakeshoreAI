import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import re

class LakeshoreAI:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.assistant_id = os.getenv("ASSISTANT_ID")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI()

    def run(self):
        st.set_page_config(page_title='LakeshoreTireAI')

        if 'previous_messages_text' not in st.session_state:
            st.session_state['previous_messages_text'] = []

        if 'displayed_questions' not in st.session_state:
            st.session_state['displayed_questions'] = []

        if 'displayed_answers' not in st.session_state:
            st.session_state['displayed_answers'] = []

        
        left_col, mid_col, right_col = st.columns([4.5,5,.5])  

        with mid_col:
            st.image("blue.svg", width=50)  

        duke_blue = "#00539B"
        st.markdown(f"""
    <h1 style='text-align: center; color: Black; font-size: 30px;'>Welcome to LakeshoreTireAI!</h1>
    <style>
        .caption-style {{
            color: grey;
            text-align: center;
        }}
        .stApp {{
            background-color: white;
        }}
        .stTextInput>div>div>input {{
            color: black !important;
            background-color: white !important;
            border-color: grey !important;
            caret-color: blue; /* Adds a blue blinking cursor */
        }}

        .stTextInput>div {{
            border-color:  {duke_blue} !important;
            border-width: 1.5px !important;
        }}
        /* Updated selector to target all buttons within Streamlit apps */
        .stButton>button {{
            display: inline-block;
            background-color: white;
            border: 2px solid #BEC2D1;;
            padding: 5px;
            margin: 2px;
            cursor: pointer;
            color: #9599B3;
            border-radius: 5px;
            width: 300px; /* Ensures equal width */
            height: 120px; /* Ensures equal height */
            text-align: center; /* Center text */
            line-height: 40px; /* Adjust line height for vertical alignment */
        }}

        
        .stButton>button:hover {{
            background-color: #f0f0f0; /* Changes background to light grey */
            color: {duke_blue}; /* Keeps the text color the same */
            border: 2px solid grey; /* Keeps the border color the same */
        }}
          .stButton {{
            margin-left: 20px !important;
        }}
        
    </style>
    <p class='caption-style' style='font-size: 24px; color: black;'>Work smarter with <span style='color: {duke_blue};'>Lakeshore Assisstant</span>.</p>
    """, unsafe_allow_html=True)



        examples = ["I hear a wobble on the back left of 2011 Jeep Wrangler", "How do I change the spark plugs on 2006 Saab 93?", "Recommend a variety of causes for a low battery car light", "Find me the best price on synthetic oil"]
        if 'current_input' not in st.session_state:
            st.session_state['current_input'] = ""

        
        cols = st.columns(2)
        
        for i, example in enumerate(examples):

            with cols[i % 2]:
                if st.button(example, key=f"example{i+1}"):
                    st.session_state['current_input'] = example  
                    st.rerun()


        # Setup the input field outside the button loop to avoid duplicate key error
        prompt = st.text_input("What are you fixing?", value=st.session_state['current_input'], placeholder="Search...", key="new")


        
        for question in st.session_state['displayed_questions']:
            st.markdown(f'<div style="color: black;"><b>You: </b> {question}</div>', unsafe_allow_html=True)

        for answer in st.session_state['displayed_answers']:
            st.markdown(f'<div style="color: {duke_blue};"><b>LakeshoretireAI: </b>{answer}</div>', unsafe_allow_html=True)

        
        if prompt:


            st.session_state['displayed_questions'].append(prompt)
            question_box = st.container()
            question_box.markdown(f'<div style="color: black;"><b>You:</b> {prompt}</div>', unsafe_allow_html=True)

            st.session_state['previous_messages_text'].append('User question was: ' + prompt)
            api_message = ''.join(st.session_state['previous_messages_text'])

            # Stream the answer
            report = []
            res_box = st.empty()
            output = ''
            stream = self.client.beta.threads.create_and_run(
                assistant_id=self.assistant_id,
                thread={"messages": [{'role': 'user', 'content': api_message}]},
                stream=True
            )
            for event in stream:
                if event.data.object == 'thread.message.delta':
                    for content in event.data.delta.content:
                        if content.type == 'text' and content.text.value is not None:
                            report.append(content.text.value)
                            result = ''.join(report).strip()
                            cleaned_result = re.sub(r"【\d+†source】", "", result)
                            # Prepend "LakeshoretireAI:" in bold and blue to the streamed content
                            res_box.markdown(f'<div style="color: {duke_blue};"><b>Lakeshore Assisstant: </b> {cleaned_result}</div>', unsafe_allow_html=True)
                            output = result



            res_box.empty()
            cleaned_output = re.sub(r"【\d+†source】", "", output).strip()
            st.session_state['displayed_answers'].append(cleaned_output)  # Append new answer to session state to display later

            st.session_state['previous_messages_text'].append('The output response was: ' + cleaned_output)
            st.session_state['previous_messages_text'].append('This marks the next question, use the previous text to help determine the answer')

            # Directly append the new answer below previous ones without clearing them
            res_box.markdown(f'<div style="color: {duke_blue};"><b>Lakeshore Assisstant: </b> {cleaned_result}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    app = LakeshoreAI()
    app.run()