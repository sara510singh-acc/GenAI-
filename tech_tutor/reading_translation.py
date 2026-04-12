import streamlit as st
import openai
from openai import OpenAI
client = OpenAI(api_key="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")

def generate_sql_question():
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                { "role": "system", "content": "You are a database teacher. Generate one simple English question that requires writing an SQL query."},
                { "role": "user", "content": "Generate a SQL practice question."}
            ]
        )
        return completion.choices[0].message.content.strip()

def verify_translation(user_question, user_sql):
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
      {"role": "system", "content": "You are a SQL expert and teacher.You will be given: An English question and A SQL query written by the user.Your job: Check if the SQL query correctly answers the question, point out mistakes ,Suggest improvements,and appreciate the user Also provide the correct SQL query for reference."},
      {"role": "user", "content": f"Query Description: {user_question},User SQL query {user_sql}Evaluate the sql query."}
      ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content.strip()



def app():
    st.header('SQL Practice and Feedback')
    st.write('Convert the given English question into an SQL query.')

    # State management
    if 'generated_question' not in st.session_state:
        st.session_state.generated_question = None
    if 'sql_input' not in st.session_state:
        st.session_state.sql_input = ''

    # Generate question
    if st.button('Start'):
        st.session_state.generated_question = generate_sql_question()

    if st.session_state.generated_question:
        st.subheader('Question:')
        st.write(st.session_state.generated_question)

        # User SQL input
        user_sql = st.text_area('Write your SQL query:', key="sql")

        if st.button('Verify SQL'):
            if user_sql:
                st.session_state.sql_input = user_sql
                feedback = verify_sql(st.session_state.generated_question, user_sql)
                st.subheader('Feedback:')
                st.write(feedback)
            else:
                st.error("Please enter your SQL query before verifying.")