# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from openai import OpenAI
import pandas as pd
from datetime import datetime
import numpy as np
import os

def amoofy_demo():

    #Set OpenAI API Key
    client = OpenAI(
    api_key = st.secrets.api.key
    )

    # Upload and display logo
    logo_path = "./pages/files/amoofy.png"
    if os.path.exists(logo_path):
        st.image(logo_path)


    # Streamlit App
    st.subheader(":studio_microphone: Interview Catalyst :studio_microphone: ")
    st.caption("Thank you for engaging with this demo. Please note that your information may be recorded for learning purposes.")
    st.divider()

    # if st.button(":microphone: My First Interview :microphone:"):
    with st.form("my_form"):
        interviewer_name = st.text_input("Your First Name")
        guest_name = st.text_input("Guest First Name")
        relationship = st.text_input("What is your relationship to your guest?")
        st.caption("Feel free to elaborate! The more context, the better!")
        how_know_each_other = st.text_area("How do you know each other?")
        st.caption("Tell us a story of how you met, where you met, or who introduced you.")
        current_happenings = st.text_area("What is currently happening in your guest's life?")
        current_happenings_you = st.text_area("What is currently happening in your life?")
        st.caption("Sharing about what is going on in either of your lives can make for richer conversation. Please provide detail.")
        submitted = st.form_submit_button("Get Questions!")

    log_df = pd.DataFrame(columns=["Interviewer", "Guest", "Relationship", "Context", "Current Happenings", "Current Happenings Me", "Date", "Suggested Questions"])

    if submitted:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time
        combined_context = f"Interviewer is {interviewer_name}, Guest is {guest_name}, Relationship between them is {relationship}, Context on how they know each other is {how_know_each_other}, Current Happenings in guest's life is {current_happenings}, \
            Current Happenings in my life is {current_happenings_you}."

        # Append to the context text
        prompt_text = f"My name is {interviewer_name} and my guest is {guest_name} and our relationship can be best described this way: {relationship}. We met in this context: {how_know_each_other},  and this is what is going on in the guest's life: {current_happenings},\
            and this is what is going on in my life {current_happenings_you}."
        prompt_text += f"I need help thinking of three meaningful and nuanced questions I can ask {guest_name} to get to know them better and draw out their stories. \
                Use {guest_name}\'s name when putting together the questions that are about {guest_name} only.\
                Use context from {current_happenings_you} to create connections between the guest and myself.\
                Make sure to tell me why you're suggesting each question, and (parenthetically) how this question can help open up conversation between us."

        # Display the updated DataFrame and text
        st.divider()

        # Generate follow-up questions
        system_prompt = """You are a nice expert interview assistant that helps people connect through the interview process. You learn from the example of top interviewers
                        around the world that are able to draw out their guests in ways that surprise and delight them.
                        You are STRICTLY FORBIDDEN from creating information about the Interviewer and Guest that is not given to you.
                        You must suggest questions that are asked in the style of the greatest interviewers of our time, like Oprah, Vivek Murthy, Brené Brown, and Tim Ferriss.
                        """

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user",
                    "content": f"{prompt_text}",
                    }]
                )	

        st.write("Suggested Questions:")
        st.write(completion.choices[0].message.content)

        new_row = {
            "Interviewer": interviewer_name,
            "Guest": guest_name,
            "Relationship": relationship,
            "Context": how_know_each_other,
            "Current Happenings": current_happenings,
            "Current Happenings Me": current_happenings_you
            "Date": current_time,
            "Suggested Questions": completion.choices[0].message.content
        }
        # Append data to the DataFrame
        log_df = pd.concat([log_df, pd.DataFrame([new_row])], ignore_index=True)

        log_df.to_csv("./pages/files/interview_log.csv", index=False,mode='a', header=False)

st.set_page_config(page_title="Amoofy Demo", page_icon="🎙️")
st.markdown("# Amoofy Demo")
st.sidebar.header("Amoofy Demo")


amoofy_demo()
