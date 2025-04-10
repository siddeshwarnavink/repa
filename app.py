import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

with open("functions.json", "r") as f:
    tools = json.load(f)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

resume_input = {
    "job_title": "Senior Machine Learning Engineer",
    "required_skills": ["Python", "Machine Learning", "TensorFlow", "Data Analysis"],
    "min_experience_years": 3,
    "must_have_keywords": ["production", "deployed", "real-time"],
    "preferred_education": ["B.Tech", "M.Tech", "MS in Computer Science"],
    "strictness": 1.0,
    "resume_text": """
        John Doe is a software engineer with over 5 years of experience in Python and machine learning.
        Built a production-grade fraud detection system using TensorFlow.
        Holds a B.Tech in Computer Science from IIT Delhi.
    """
}

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": "Please parse the resume using the structured input below.",
        },
        {
            "role": "user",
            "content": json.dumps(resume_input)
        },
        {
            "role": "user",
            "content": (
                "Please extract structured resume data from the following input and return a JSON with:\n"
                "- name\n"
                "- years_of_experience\n"
                "- skills (array)\n"
                "- projects (array of {name, description, tech_stack, quality_score})\n"
                "- education (array)\n"
                "- decision: Accepted or Rejected based on HR inputs\n\n"
                "Evaluate based on:\n"
                "- required_skills match\n"
                "- min_experience_years\n"
                "- must_have_keywords in resume_text\n"
                "- preferred_education\n"
                "- strictness of evaluation on a scale of 0 to 1"
            )
        }
    ],
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "parse_resume"}}
)

tool_call = response.choices[0].message.tool_calls[0]
function_args = json.loads(tool_call.function.arguments)

print(json.dumps(function_args, indent=2))
