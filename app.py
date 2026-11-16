from flask import Flask, render_template, request
from src.jarvis_helper import prompt_helper
from src.api_mapper import api_response
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

    response = api_response(process['message']['content'], prompt)
    return response

if __name__ == 'main':
    app.run(debug=True)
