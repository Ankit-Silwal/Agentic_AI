from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client=OpenAI(
  api_key=os.getenv("api_key"),
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-3.1-flash-lite",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://images.pexels.com/photos/16323580/pexels-photo-16323580.jpeg"
                    }
                }
            ]
        }
    ]
)
print(response.choices[0].message.content)