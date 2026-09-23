from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import json
from bs4 import BeautifulSoup


# Load env variables
load_dotenv()

# 1. Define the Python tool that actually fetches the URL


def fetch_webpage(url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)

        # Parse HTML and strip away scripts and styles
        soup = BeautifulSoup(response.text, "html.parser")
        for script_or_style in soup(["script", "style", "header", "footer", "nav"]):
            script_or_style.decompose()

        # Get text content and remove excess whitespace
        text = soup.get_text(separator=" ")
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase for line in lines for phrase in line.split("  "))
        clean_text = "\n".join(chunk for chunk in chunks if chunk)

        # Truncate to a safe length (e.g., ~8,000 characters) to prevent overloading
        return clean_text[:8000]

    except Exception as e:
        return f"Error fetching URL: {str(e)}"


# 2. Describe the tool to OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_webpage",
            "description": "Fetches the text content of a specific web URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "https://www.cl.cam.ac.uk/teaching/2425/Databases/",
                    }
                },
                "required": ["url"],
            },
        },
    }
]

# Create a client that communicates with ollama
# client = OpenAI()
# Create a client that communicates with ollama
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
)


# 3. Ask the model a question containing a URL
messages = [
    {
        "role": "user",
        "content": """From the given link: 
            https://www.cl.cam.ac.uk/teaching/2425/Databases/
            
            Extract the following information in json format:
            - Extract "Lectures" from this page. 
            - Put the extracted lectuers in a well structure format. 
            - I am mostly conerned with the topics in the lecture collectively. 
            - Classify each topen on difficulty level - "Easy", "Medium" and "Hard" """
    }
]
# Send a question to AI model
response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=messages,
    tools=tools,
)





# 4. Check if the model decided it needs to use the tool
tool_calls = response.choices[0].message.tool_calls
if tool_calls:
    for tool_call in tool_calls:
        if tool_call.function.name == "fetch_webpage":
            print("Loading Arguments")
            # Extract the arguments the model provided
            args = json.loads(tool_call.function.arguments)
            url_to_fetch = args.get("url")

            # Execute your Python function
            print("Fetching web content")
            web_content = fetch_webpage(url_to_fetch)

            # Append the model's request and your function's result to the history
            messages.append(response.choices[0].message)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": web_content,
                }
            )
            # with open("sample111.html", "w") as fw:
            #     fw.write(messages[-1])

            # Send it back to the model for the final answer
            final_response = client.chat.completions.create(
                model=os.getenv("MODEL"), messages=messages
            )

            print(final_response.choices[0].message.content)

print("-----------Tool Calls---------------", tool_calls)


# 3. Extract the usage statistics
usage = response.usage

print("--- Token Consumption ---")
print(f"Input (Prompt) Tokens:      {usage.prompt_tokens}")
print(f"Output (Completion) Tokens: {usage.completion_tokens}")
print(f"Total Tokens:               {usage.total_tokens}")
print("-------------------------\n")

# Display the response
print(response.choices[0].message.content)