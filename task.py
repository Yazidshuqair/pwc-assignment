import streamlit as st
from backend import quiz_generator

# Function to get quiz questions based on user input
def get_quiz_questions():
    st.sidebar.header("Quiz Settings")
    subject = st.sidebar.text_input("Enter Quiz Subject:")
    min_questions = st.sidebar.slider("Minimum Questions", 1, 10, 1)
    max_questions = st.sidebar.slider("Maximum Questions", 1, 40, 10)

    if st.sidebar.button("Generate Quiz"):
        return quiz_generator(subject, min_questions, max_questions)
    else:
        return None

# Function to display quiz and handle user submission
def display_quiz(quiz_questions):
    if quiz_questions:
        st.header("Quiz Time!")
        st.markdown("Select at least one answer for each question.")

        user_answers = {}
        for i, question in enumerate(quiz_questions):
            st.subheader(f"Question {i + 1}: {question['question']}")
            user_answers[i] = st.multiselect("Select Answer(s)", question['options'])

        if st.button("Submit Quiz"):
            show_results(quiz_questions, user_answers)

# Function to show quiz results
def show_results(quiz_questions, user_answers):
    st.header("Quiz Results")
    score = 0

    for i, question in enumerate(quiz_questions):
        st.subheader(f"Question {i + 1}: {question['question']}")
        st.markdown(f"**Correct Answer:** {question['correct_answer']}")
        st.markdown(f"**Your Answer(s):** {', '.join(user_answers.get(i, []))}")

        if set(user_answers.get(i, [])) == set([question['correct_answer']]):
            st.success("Correct!")
            score += 1
        else:
            st.error("Incorrect")

    st.header(f"Your Score: {score}/{len(quiz_questions)}")

# Main Streamlit app
def main():
    st.title("Quiz Generator App")
    quiz_questions = get_quiz_questions()
    display_quiz(quiz_questions)

if __name__ == "__main__":
    main()

#i can not test the app because the api ket didnt work
