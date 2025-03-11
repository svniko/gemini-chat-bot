# Gemini API чат-бот
## Встановлення
1. Відкрийте Visual Studio Code

2. Створіть/відкрийте відповідну папку
   
4. Завантажте zip та розархівуйте, або склонуйте вміст репозиторію.<br>
Для завантаження zip - зелена кнопка `<>Code` > `Download ZIP`

5. Відкрийте термінал (меню Terminal)

6. Створіть віртуальне оточення
```
python -m venv venv
```

5. Активуйте віртуальне оточення

Якщо користуєтесь `Windows`
```
venv\Scripts\activate
```
Якщо `mac`/`linux`
```
source venv/bin/activate
```
6. Встановіть необхідні модулі<br>
```
pip install -r requirements.txt
```
або ж
``` 
pip install google-genai python-dotenv rich
```
7. Створіть файл `.env` в папці з файлом `bot.py` і додайте туди API ключ
 ```
 GEMINI_API_KEY=YOUR_API_KEY
 ```



    
