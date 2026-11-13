from flask import Flask, render_template, request
from src.jarvis_helper import prompt_helper, weather_helper
from src.api.weather_api import jarvis_weather
import ollama

app = Flask(__name__)

@app.route('/')
def jarvis_template():
    return render_template("index.html")

@app.route('/prompt', methods=['POST'])
def model():
    prompt = request.data.decode('utf-8')
    jarvis_prompt = prompt_helper(prompt)
    process = ollama.chat(model='gemma4:31b-cloud' \
    '', messages=[
        {
            'role': 'user',
            'content': f'{jarvis_prompt}',
        },
    ])

    if process['message']['content'] == 'weather':
        data = jarvis_weather()
        weather_prompt = weather_helper(data)
        response = ollama.chat(model='gemma4:31b-cloud', messages=[
            {
                'role': 'user',
                'content': f'{weather_prompt}',
            },
        ])

        return(response['message']['content'])
    else:
        return(process['message']['content'])

if __name__ == 'main':
    app.run(debug=True)
