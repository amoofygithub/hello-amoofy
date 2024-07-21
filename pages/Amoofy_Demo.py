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
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import tiktoken

def amoofy_demo():

    #Set OpenAI API Key
    client = OpenAI(
    api_key = st.secrets.api.key
    )

    #filtering words
    def filter_short_words(text):
        return " ".join([str(word).lower() for word in text.split() if len(word) >= 5])

    # Custom color function for the word cloud
    def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        colors = ["#b19cd9", "#dcd0ff", "#ffb6c1", "#bebebe"]
        return random.choice(colors)


    # Upload and display logo
    logo_path = "./pages/files/amoofy.png"
    if os.path.exists(logo_path):
        st.image(logo_path)

     # Token count function
    def count_tokens(text):
        encoding = tiktoken.encoding_for_model("gpt-4")
        tokens = encoding.encode(text)
        return len(tokens)


    # Streamlit App
    st.subheader(":studio_microphone: Interview Catalyst :studio_microphone: ")
    st.caption("Thank you for engaging with this demo. Please note that your information may be recorded for learning purposes.")
    st.caption("In this demo, you’ll provide information for a one-time conversation with each person you wish to connect to.")
    st.divider()

    if 'extra_context' not in st.session_state:
        st.session_state['extra_context'] = ""

    tab1, tab2 = st.tabs(["My First Interview :studio_microphone:", "Keeping the Conversation Going :speech_balloon:"])

    with tab1:
        # if st.button(":microphone: My First Interview :microphone:"):
        with st.form("my_form"):
            interviewer_name = st.text_input("Your First Name")
            guest_name = st.text_input("Your Guest's First Name")
            st.caption("Who would you like to get to know better?")
            st.write("\n\n")
            relationship = st.text_input("What is your relationship with this person?")
            st.caption("Tell us a story of how you met, where you met, or who introduced you,\
                        or if this person is within your family, elaborate who this person is to you. \
                        Feel free to elaborate! The more context, the better!")
            st.write("\n\n")
            how_know_each_other = st.text_area("How do you know each other?")
            st.caption("Tell us a story of how you met, where you met, or who introduced you.")
            st.write("\n\n")
            importance = st.text_area("Why is it important for you to capture their story?")
            st.caption("Can you tell us what is your reason to ask this person something, \
                    what do you wish to know about them or any specific moments or advice you wish to ask for.")
            st.write("\n\n")
            current_happenings = st.text_area("Can you give a brief background about the person you want to interview?")
            st.caption("Can you provide any context on what is happening in their life: where do they live, work, etc?")
            st.write("\n\n")
            current_happenings_you = st.text_area("Can you give a brief background about yourself?")
            st.caption("Provide some context on what is happening in your life: where you live, work, etc.")
            submitted = st.form_submit_button("Get Questions!")

        # log_df = pd.DataFrame(columns=["Interviewer", "Guest", "Relationship", "Context", "Current Happenings", "Current Happenings Me", "Date", "Suggested Questions"])

        if submitted:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time
            combined_context = f"You are a nice interview assistant trying to help {interviewer_name} and {guest_name} reconnect. \
            Their relationship can be described this way: {relationship}.\
            This is why it is important for {interviewer_name} to connection with {guest_name}: {importance}.\
            This is how they met: {how_know_each_other}.\
            This is relevant information about what the guest is doing currently in their life: {current_happenings}.\
            This is relevant information about what the interviewer is doing currently in their life: {current_happenings_you}.\
            You MUST help {interviewer_name} create 3 questions that they can use to connect better with {guest_name}. \
            You are STRICTLY FORBIDDEN from generating any questions that are offensive, provocative, or disrespectful.\
            You must give {interviewer_name} 3 questions that use information about {guest_name} to start the conversation. \
            If there is a connection between {current_happenings} and {current_happenings_you} you can refer to that in your question.\
            You MUST think of how to make your questions interesting, in the style of someone that is an expert interviewer like Oprah."

            st.session_state['extra_context'] = combined_context 
            # Display the updated DataFrame and text
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

            # new_row = {
            #     "Interviewer": interviewer_name,
            #     "Guest": guest_name,
            #     "Relationship": relationship,
            #     "Context": how_know_each_other,
            #     "Current Happenings": current_happenings,
            #     "Current Happenings Me": current_happenings_you,
            #     "Date": current_time,
            #     "Suggested Questions": completion.choices[0].message.content
            # }
            # Append data to the DataFrame
            # log_df = pd.concat([log_df, pd.DataFrame([new_row])], ignore_index=True)

            # log_df.to_csv("./pages/files/interview_log.csv", index=False,mode='a', header=False)

            st.divider()

    with tab2:
        st.subheader("Keep the Conversation Going...",divider='rainbow')

        # if st.session_state['extra_context']:
        #     st.write(f"The extra context entered in Tab 1 is: {st.session_state['extra_context']}")
        # else:
        #     st.write("No extra_context has been entered in Tab 1 yet.")


        with st.form("my_form_2"):     
            q_and_a = st.text_area("Select whichever questions you wish from the choices provided. \
                                Paste into the following window, and add your guest's answers.\
                                Make sure to define who is speaking for each question or answer.")
            uploaded_file = st.file_uploader("Or upload a text file with the Q&A (max 60KB)", type=["txt"])
            submitted = st.form_submit_button("Keep the Conversation Going")

        if uploaded_file:
            if uploaded_file.size > 60 * 1024:
                st.error("The uploaded file exceeds the 60KB size limit. Please upload a smaller file.")
            else:
                tmp_q_and_a = uploaded_file.read().decode("utf-8")
                if count_tokens(tmp_q_and_a) > 10000:
                    st.error("The uploaded file exceeds the 10,000 token limit. Please upload a smaller file.")
                else:
                    st.success("File uploaded successfully.")
                    q_and_a = tmp_q_and_a
        
        if submitted and q_and_a:

            st.subheader(":speaking_head_in_silhouette: Your Conversational Summary and Next Steps :speaking_head_in_silhouette:", divider= 'rainbow')
            
            
            new_context = f"{interviewer_name} and {guest_name} have had their first conversation using the questions you suggested previously.\
                You already know this about them:\
                Their relationship can be described this way: {relationship}.\
                This is why it is important for {interviewer_name} to make a connection with {guest_name}: {importance}.\
                This is how they met: {how_know_each_other}.\
                This is relevant information about what the guest is doing currently in their life: {current_happenings}.\
                This is relevant information about what the interviewer is doing currently in their life: {current_happenings_you}.\
                \n \
                The full conversation they had after they used your suggested questions is found here: {q_and_a}.\
                You MUST help {interviewer_name} create 3 additional questions that they can use to keep the conversation going \
                with {guest_name}. You MUST think of how to make your questions interesting, in the style of someone that is an expert interviewer like Oprah.\
                You are STRICTLY FORBIDDEN from generating any questions that are offensive, provocative, or disrespectful.\
                "

            # Display the updated DataFrame and text
            st.divider()


            # Generate follow-up questions
            system_prompt_2 = """You are a nice interview assistant.
                You are STRICTLY FORBIDDEN from generating any questions that are offensive, provocative, or disrespectful.
                Give me an analysis of the conversation thus far in the following format:
                First, give a brief summary of what they have covered so far with the questions and answers.
                Second, give 3 follow up questions that can help these two people continue the conversation in the future.
                            """

            completion_2 = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role":"system", "content": f"{system_prompt_2}"},
                    {"role": "user", "content": f"{new_context}",}
                    ]
                    )	
            st.write("Summary and Follow Up Questions:")
            st.write(completion_2.choices[0].message.content)

st.set_page_config(page_title="Amoofy Demo", page_icon="🎙️")
st.markdown("# Amoofy Demo")
st.sidebar.header("Amoofy Demo")


amoofy_demo()
