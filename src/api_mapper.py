import ollama
from src.jarvis_helper import weather_helper, date_time_helper
from src.api.weather_api import jarvis_weather
from src.api.datetime_api import jarvis_datetime

def api_response(prompt):

    if prompt == 'weather':
        data = jarvis_weather()
        weather_prompt = weather_helper(data)
        response = ollama.chat(model='gemma4:31b-cloud', messages=[
            {
                'role': 'user',
                'content': f'{weather_prompt}',
            },
        ])

        return(response['message']['content'])
    elif prompt == 'time':
        data = jarvis_datetime()
        datetime_prompt = date_time_helper(data)
        response = ollama.chat(model='gemma4:31b-cloud', messages=[
            {
                'role': 'user',
                'content': f'{datetime_prompt}',
            },
        ])
        return(response['message']['content'])
    else:
        return(prompt)