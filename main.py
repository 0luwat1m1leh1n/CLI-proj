import os
from openai import OpenAI

API_KEY = "PASTE_YOUR_API_KEY_HERE"
MODEL = "openrouter/free"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

# ---------- FUNCTIONS ---------- #

def show_instructions():
    print("\nSmart Coding Assistant")
    print("1. Modify a Python file")
    print("2. View a file")
    print("3. Quit")


def read_file_data(filename):
    if not os.path.exists(filename):
        print("ERROR: File does not exist.")
        return None

    try:
        with open(filename, "r") as file:
            return file.read()
    except Exception as e:
        print(f"ERROR reading file: {e}")
        return None


def build_coding_prompt(code, instruction):
    return f"""
You are a professional Python coding assistant.

TASK:
{instruction}

RULES:
- Return ONLY the updated Python code
- Do NOT include explanations

CODE:
{code}
"""


def get_ai_response(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ERROR with AI: {e}"


def save_new_file(content, original_filename):
    new_filename = "updated_" + original_filename

    # CLEAN AI OUTPUT (important)
    if "```" in content:
        content = content.replace("```python", "").replace("```", "")

    try:
        with open(new_filename, "w") as file:
            file.write(content)
        print(f"Saved as: {new_filename}")
    except Exception as e:
        print(f"ERROR saving file: {e}")


# ---------- MAIN LOOP ---------- #

def main():
    while True:
        show_instructions()
        choice = input("Choose an option: ")

        if choice == "1":
            filename = input("Enter Python file name: ")

            code = read_file_data(filename)
            if code is None:
                continue

            instruction = input("What do you want to do? ")

            prompt = build_coding_prompt(code, instruction)
            updated_code = get_ai_response(prompt)

            if updated_code.startswith("ERROR"):
                print(updated_code)
                continue

            save_new_file(updated_code, filename)

        elif choice == "2":
            filename = input("Enter file name: ")
            content = read_file_data(filename)
            if content:
                print("\n--- FILE CONTENT ---")
                print(content)

        elif choice == "3" or choice.lower() == "quit":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()