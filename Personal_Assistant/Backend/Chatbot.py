from groq import Groq
from json import dump, load, JSONDecodeError  # import JSONDecodeError
import datetime
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

messages = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} 
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. .
"""
SystemChatBot = [{"role": "system", "content": System}]

# Function to safely load JSON
def load_messages():
    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = f.read().strip()
            if messages:
                return load(f)
            else:
                return []
    except (FileNotFoundError, JSONDecodeError):
        return []

# Function for timestamp
def RealtimeDatetime():
    now = datetime.datetime.now()
    return now.strftime(
        "Use this real-time info if needed,\n"
        "Day: %A\nDate: %d\nMonth: %B\nYear: %Y\n"
        "Time: %H hours:%M minutes: %S seconds.\n"
    )

def AnswerModifier(Ans):
    return "\n".join(line for line in Ans.split('\n') if line.strip())

def ChatBot(Query):
    try:
        messages = load_messages()
        messages.append({"role": "user", "content": Query})
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeDatetime()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""
        for i in completion:
            if i.choices[0].delta.content:
                Answer += i.choices[0].delta.content
        Answer = Answer.replace("</s>", "")

        messages.append({"role": "assistant", "content": Answer})
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer)
    except Exception as e:
        print(f"Error: {e}")
        # Reset the log and return an error message (no recursion)
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return "An error occurred. Chat history was reset. Please try again."

if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        if user_input.strip().lower() in ("exit", "quit", "bye"):
            print("Assistant: Goodbye!")
            break
        response = ChatBot(user_input)
        print(f"Assistant: {response}")





