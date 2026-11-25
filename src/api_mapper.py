import ollama
from src.jarvis_helper import weather_helper, date_time_helper, news_helper, email_helper, call_context
from src.api.weather_api import jarvis_weather
from src.api.datetime_api import jarvis_datetime
from src.api.news_api import jarvis_news
from src.api.email.email_api import jarvis_email

def api_response(prompt, context):

    initial_context = call_context(context)

    if prompt == 'weather':
        data = jarvis_weather()
        weather_prompt = weather_helper(data)
        response = ollama.chat(model='gemma4:31b-cloud', messages=[
            {
                'role': 'user',
                'content': f'{weather_prompt, initial_context}',
            },
        ])

        return(response['message']['content'])
    elif prompt == 'time':
        data = jarvis_datetime()
        datetime_prompt = date_time_helper(data)
        response = ollama.chat(model='gemma4:31b-cloud', messages=[
            {
                'role': 'user',
                'content': f'{datetime_prompt, initial_context}',
            },
        ])
        return(response['message']['content'])
    elif prompt == 'news':
        data = jarvis_news()
        news_prompt = news_helper(data)
        response = ollama.chat(model='gemma4:31b-cloud', messages=[
            {
                'role': 'user',
                'content': f'{news_prompt, initial_context}',
            },
        ])
        return(response['message']['content'])
    elif prompt == 'email':
        data = jarvis_email()
        print(data)
        email_prompt = email_helper(data)
        response = ollama.chat(model='gemma4:31b-cloud', messages=[
            {
                'role': 'user',
                'content': f'{email_prompt, initial_context}',
            },
        ])
        return(response['message']['content'])
    else:
        return(prompt)