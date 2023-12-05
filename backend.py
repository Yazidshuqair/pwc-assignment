# the necessary libraries and modules
from langchain.llms import OpenAI
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate

# load environment variable
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

llm = OpenAI(openai_api_key=openai_api_key)
prompt_template = PromptTemplate.from_template("""Generate an esay multiple choice questions  about {subject} along with the right answers
     make sure that the right answer is labeled with 'right Answer:' 
    and followed by the answer itself""")

# Function to generate quiz questions for a given topic
def quiz_generator(subject, min_questions=1, max_questions=40):
    questions = []
    total_questions = min_questions + max_questions

    while len(questions) < total_questions:
        formatted_prompt = prompt_template.format(subject=subject)
        response = llm.invoke(formatted_prompt)
        processed_responses = process_response(response)

        for processed in processed_responses:
            if isinstance(processed, dict) and len(processed.get('options', [])) == 4:
                questions.append(processed)
                if len(questions) == total_questions:
                    break

    return questions
def process_response(response):
    quiz_data = []

    for block in response.strip().split("Q:"):
        lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
        
        if len(lines) < 2:
            continue

        question = lines[0]

        correct_answer = next((line.split("Correct Answer:")[1].strip() for line in lines[1:] if "Correct Answer:" in line), None)

        options = [line.strip() for line in lines[1:] if line.strip() and line[0].isalpha() and line[1] in [".", ")"]]

        if question and options and correct_answer:
            quiz_data.append({"question": question, "options": options, "correct_answer": correct_answer})

    return quiz_data

"""
Quiz Generation Script

This script interacts with the OpenAI API to dynamically generate multiple-choice quiz questions based on a specified subject.

Libraries and Modules:
- langchain.llms: OpenAI module for language model interaction
- os: Operating system module
- dotenv: Module for loading environment variables from a file
- langchain.prompts: Module for creating prompt templates

Environment Setup:
- Load environment variables from a file named '.env'.
- Retrieve the OpenAI API key from the environment variables.

Usage:
1. Instantiate the OpenAI class with the API key.
2. Create a prompt template with a placeholder for the subject.

Functions:
1. quiz_generator(subject, min_questions=1, max_questions=40):
   - Generates multiple-choice quiz questions for the specified subject.
   - Parameters:
     - subject: The topic for which questions are generated.
     - min_questions: Minimum number of questions to generate (default: 1).
     - max_questions: Maximum number of questions to generate (default: 40).
   - Returns a list of dictionaries representing quiz questions.

2. process_response(response):
   - Processes the OpenAI API response to extract quiz questions, options, and correct answers.
   - Parameters:
     - response: The API response containing generated content.
   - Returns a list of dictionaries representing processed quiz data.

Note:
- The script assumes that the OpenAI API response follows a specific format with questions, options, and correct answers.
- Additional error handling and security measures, especially regarding sensitive information, should be considered for production use.
"""
