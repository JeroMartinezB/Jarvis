from flask import Flask, render_template, request
import ollama

app = Flask(__name__)

@app.route('/')
def jarvis_template():
    return render_template("index.html")

@app.route('/prompt', methods=['POST'])
def model():
    prompt = request.data.decode('utf-8')
    response = ollama.chat(model='gemma4:31b-cloud', messages=[
        {
            'role': 'user',
            'content': f'{prompt}',
        },
    ])
    return(response['message']['content'])

if __name__ == 'main':
    app.run(debug=True)
