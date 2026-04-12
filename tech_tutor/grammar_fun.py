import streamlit as st
import openai

from openai import OpenAI
client = OpenAI(api_key="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")



def generate_ds_exercise():
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a data science teacher. Create one short MCQ or fill-in-the-blank question."},
            {"role": "user","content": "Generate one data science exercise."}
        ]
    )
    return completion.choices[0].message.content.strip()

def check_answer(question, user_answer):
    # Using OpenAI to check the user's answer and provide feedback
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
      {"role": "system", "content": "You are a data science expert. your job is to teach people about data science. you will be give a question and an answer, both by the user. you have to evaluate it and share feedback. please be supportive and helpful."},
      {"role": "user", "content": f"Question: {question}\nAnswer: {user_answer}\nEvaluate the correctness of the answer and provide feedback:"}
      ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content.strip()



def app():
    st.header('Data Science and Fun')
    st.write('Sharpen your Data Science skills with these exercises.')

    # State management for exercise generation and user input
    if 'exercise' not in st.session_state:
        st.session_state.exercise = None
    if 'user_response' not in st.session_state:
        st.session_state.user_response = ''

    # Generate exercise button
    if st.button('Start'):
        st.session_state.exercise = generate_ds_exercise()
    
    if st.session_state.exercise:
        st.subheader('Exercise:')
        st.write(st.session_state.exercise)

        # User input for response
        user_response = st.text_input('Your answer:', key="response")

        if st.button('Check Answer'):
            if user_response:
                st.session_state.user_response = user_response
                feedback = check_answer(st.session_state.exercise, user_response)
                st.subheader('Feedback on Your Answer:')
                st.write(feedback)
            else:
                st.error("Please enter an answer before checking.")
