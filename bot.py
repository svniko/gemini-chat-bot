import os
from google import genai
from google.genai import types

# модуль для форматованого виведення в консоль
from rich.console import Console
from rich.markdown import Markdown

# Модуль для змінних оточення
from dotenv import load_dotenv

# Модуль для опрацювання дати і часу
from datetime import datetime

# Збережіть ключ API в файлі .env
load_dotenv('.env')

# Об'єкт для форматованого виведення в консоль
console = Console()
keywords = []

def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),

        # Так неправильно, але працює
        # api_key="XXXXXXXXXXXXXXXXXXXXXXXXXX"
    )

    # Код можнга використовувати з різними моделями 
    model = "gemini-2.0-pro-exp-02-05"
    # model = "gemini-2.0-flash-exp"
   
    # Список для збереження питань та відповідей
    contents = []

    generate_content_config = types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        top_k=64,
        max_output_tokens=8192,
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_ONLY_HIGH",  # Block few
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_ONLY_HIGH",  # Block few
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_ONLY_HIGH",  # Block few
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_ONLY_HIGH",  # Block few
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_CIVIC_INTEGRITY",
                threshold="BLOCK_LOW_AND_ABOVE",  # Block most
            ),
        ],
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""You are a teacher explaining some difficult concepts to non-specialists. Explain clearly, but with real-life examples. When providing mathematical formulas, give explanations for them. Ask questions to understand the user's level better"""),
        ],
    )

    print("Bot: Привіт. Чим можу допомогти?")    
   
    while True:
        user_input = input("\nYou: ")
        print()

        if user_input.lower() == "stop":
            print("Bot: На все добре!")

            # Визначаємо ключові слова чату
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text="Give 2 or more keywords about whole conversation. Just keywords without additional text. Use main language of conversation")],
                )
            )
            response = client.models.generate_content(
                model=model, 
                contents=contents)
            keywords = response.text
            # print (keywords)

            break

        # Додаємо запит користувача в список контенту
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_input)],
            )
        )

        # Отримуємо відповідь моделі
        # В якості параметів передаємо ім'я моделі 
        # та список запитів користувача та відповідей моделі (список contents)
        response = client.models.generate_content(
            model=model, 
            contents=contents)
        
        # Додаємо відповідь моделі до списку контенту
        contents.append(types.Content(
                role="model",
                parts=[
                    types.Part.from_text(text=response.text),
                ],
            ),
        )

        #Виводимо відповідь 
        md = Markdown(response.text)
        console.print("Bot:", md)

    #Зберігаємо історію спілкування в чаті

    # Отримуємо поточну дату і час у форматі YYYY-MM-DD_HH-MM-SS
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_name = f"history_{timestamp}.txt"

    with open(file_name, 'w', encoding="utf-8") as out:
        out.write(f"Ключові слова:\n{keywords}\n\n")
        for content in contents:
            out.write(f"{content.role}: ")
            out.write(f"{content.parts[0].text}\n")

if __name__ == "__main__":
    generate()