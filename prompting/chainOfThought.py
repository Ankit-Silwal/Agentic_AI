from dotenv import load_dotenv
from openai import OpenAI
import json
import os

load_dotenv()
client = OpenAI(
  api_key=os.getenv("api_key"),
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
SYSTEM_PROMPT="""
    You are an expert AI Assistant in resolving user queries using chain of thought
    You work on START,PLAN and OUTPUT steps
    you neeed to first plan what needs to be donw .The plan can be multiple steps
    once you think enough plan has been done ,finnaly you can give an output
    RULES:
    -Strictly follow the given json output format 
    -Only run one step at a time
    -The sequence of stesp is start(where user gives an output),plan (that can be multiple times) and finnaly output(whihc is going 
    to be displayed).
    Workflow:
  - If this is the first response, return Start.
  - After Start, return ONE Plan.
  - You may return multiple Plan steps.
  - When planning is complete, return Output.

    Output Json Format:
    {
      "step":"Start"|"Plan"|"Output","content:"string"}
      Example:
      START:Hey ,can you solve 2+4*4
      Plan:{"step":"plan","content":"Seems like user is interested into maths problem}
      plan:{"step":plan":"content":"Looking at the problem,we should use bodmas to solve this"}
      plan:{"step":"Plan":"content":"Yes bodmas is the correct approach for this problme"}
      plan:{"step":"plan":"content":"Firsta we sould multiply be 4 thus the new equation is 2+16}
      plan:{"step":"Plan":content:"now we shouild add the 2 being ans as 18 which is the finall answer" }
      plan:{"step":"Output":content:"Hence,2+4*4=18"}
      18
    }

"""

response=client.chat.completions.create(
  model="gemini-3.1-flash-lite",
  response_format={"type":"json_object"},
  messages=[
    {"role":"system","content":SYSTEM_PROMPT},
    {"role":"user","content":"Hey,write a code to add n numbers in python"},
    {"role":"assistant","content":json.dumps({
  "step": "Start",
  "content": "The user wants a Python code snippet to add 'n' numbers."
})},
    {"role":"assistant","content":json.dumps([{
    "step": "Plan",
    "content": "Define a function that takes a list of numbers as input."
  },
  {
    "step": "Plan",
    "content": "Use the built-in sum() function in Python for efficiency."
  },
  {
    "step": "Plan",
    "content": "Provide an example usage of the function for the user."
  },
  {
    "step": "Output",
    "content": "def add_numbers(numbers):\n    return sum(numbers)\n\n# Example usage:\nn = int(input('How many numbers? '))\nnums = [float(input(f'Enter number {i+1}: ')) for i in range(n)]\nprint(f'The sum is: {add_numbers(nums)}')"
  }])},
    {"role":"assistant","content":json.dumps([
  {
    "step": "Start",
    "content": "The user wants a Python code snippet to add 'n' numbers."
  },
  {
    "step": "Plan",
    "content": "Define a function that takes a list of numbers as input."
  },
  {
    "step": "Plan",
    "content": "Use the built-in sum() function in Python for efficiency."
  },
  {
    "step": "Plan",
    "content": "Provide an example usage of the function for the user."
  },
  {
    "step": "Output",
    "content": "def add_numbers(numbers):\n    return sum(numbers)\n\n# Example usage:\nn = int(input('How many numbers? '))\nnums = [float(input(f'Enter number {i+1}: ')) for i in range(n)]\nprint(f'The sum is: {add_numbers(nums)}')"
  }
])},
    {"role":"assistant","content":json.dumps({
  "step": "Output",
  "content": "def add_numbers(numbers):\n    return sum(numbers)\n\n# Example usage:\nn = int(input('How many numbers to add? '))\nnumbers_list = [float(input(f'Enter number {i+1}: ')) for i in range(n)]\nprint(f'The sum is: {add_numbers(numbers_list)}')"
})}
    ]
)

print(response.choices[0].message.content)