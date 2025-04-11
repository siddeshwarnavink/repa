import os
import json

from celery import shared_task
from dotenv import load_dotenv
from openai import OpenAI
from .models import Process, ProcessFile

load_dotenv()

with open("functions.json", "r") as f:
    tools = json.load(f)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@shared_task
def process_files_task(process_id):
    try:
        process = Process.objects.get(id=process_id)
        process.status = Process.ProcessStatus.RUNNING
        process.save()

        process_files = process.files.all()

        for process_file in process_files:
            try:
                file_path = process_file.file.path
                with open(file_path, 'r') as f:
                    file_content = f.read()
                    resume_input = {
                        "job_title": process.job_title,
                        "required_skills": process.required_skills.split(", "),
                        "min_experience_years": process.min_experience_years,
                        "must_have_keywords": process.must_have_keywords.split(", "),
                        "preferred_education": process.preferred_education.split(", "),
                        "resume_text": file_content
                    }
                    print("Resume input", resume_input)

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
                            }
                        ],
                        tools=tools,
                        tool_choice={"type": "function", "function": {"name": "parse_resume"}}
                    )

                    tool_call = response.choices[0].message.tool_calls[0]
                    function_args = json.loads(tool_call.function.arguments)
                    print("ChatGPT output", function_args)

                    process_file.candidate_name = function_args["name"]
                    process_file.candidate_experience_years = function_args["years_of_experience"]
                    process_file.candidate_skills = function_args["skills"]
                    process_file.candidate_projects = function_args["projects"]
                    process_file.candidate_education = function_args["education"]
                    process_file.score = function_args["rank"]
                    process_file.remarks = function_args["remarks"]
                    process_file.status = ProcessFile.ProcessFileStatus.COMPLETED
                    process_file.save()
            except Exception as e:
                print(str(e))
                process_file.status = ProcessFile.ProcessFileStatus.FAILED
                process_file.remarks = str(e)
                process_file.save()
        process.status = Process.ProcessStatus.COMPLETED
        process.save()
    except Process.DoesNotExist:
        print(f"Process with id {process_id} does not exist.")
    except Exception as e:
        process.status = Process.ProcessStatus.FAILED
        process.save()
