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
        combined_context = f"You are a nice interview assistant trying to help {interviewer_name} and {guest_name} reconnect. \
            Their relationship can be described this way: {relationship}.\
            This is how they met: {how_know_each_other}.\
            This is relevant information about what the guest is doing currently in their life: {current_happenings}.\
            This is relevant information about what the interviewer is doing currently in their life: {current_happenings_you}.\
            You MUST help {interviewer_name} create 3 questions that they can use to connect better with {guest_name}. \
            You are STRICTLY FORBIDDEN from generating any questions that are offensive, provocative, or disrespectful.\
            You must give {interviewer_name} 3 questions that use information about {guest_name} to start the conversation. \
            If there is a connection between {current_happenings} and {current_happenings_you} you can refer to that in your question.\
            You MUST think of how to make your questions interesting, in the style of someone that is an expert interviewer like Oprah."
        
        st.divider()

        # Generate follow-up questions
        system_prompt = """You are a nice interview assistant.
            You are STRICTLY FORBIDDEN from generating any questions that are offensive, provocative, or disrespectful.
                        """

        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role":"system", "content": f"{system_prompt}"},
                {"role": "user", "content": f"{combined_context}",}
                ]
                )	
        st.write("Here you go:")
        st.write(completion.choices[0].message.content)

        new_row = {
            "Interviewer": interviewer_name,
            "Guest": guest_name,
            "Relationship": relationship,
            "Context": how_know_each_other,
            "Current Happenings": current_happenings,
            "Current Happenings Me": current_happenings_you,
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
