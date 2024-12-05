from groq import Groq
from config import GROQ_API



prompt = '''
understand this query and generate me a script to generate a {number_of_sides} pager slide. the output should be a valid list of dictionaries with correct formatting.

each dictionary has following keys - 

heading - heading of the slide

image_query  - generate a query suitable for google search or image generation models to create/retreive a image related to slide content

content - text for the slide

'''


client = Groq(
    api_key=GROQ_API,
)


chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama3-8b-8192",
    stream=False,
)

print(chat_completion.choices[0].message.content)