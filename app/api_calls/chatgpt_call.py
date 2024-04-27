from openai._exceptions import RateLimitError
import openai
from time import sleep

from app.data_management.general import data_request

def gpt_call(model: str, parameters: list[dict], api_key = None):

    if api_key == None: 
        api_file_path = 'data/required_data/api_keys.json'
        api_data = data_request(api_file_path)
        try:
            api_key = api_data['CHAT_GPT']
        except: 
            raise ValueError('Please add an gpt api-key to the config.json file')

    openai.api_key = api_key

    attempts = 3 
    response = None
    THREE_MINUTES = 3*60

    while attempts < 3: 
        attempts -= 1 

        try: 
            response = openai.chat.completions.create(model=model, messages=parameters)
        except RateLimitError:
            sleep(THREE_MINUTES)
        except Exception as e: 
            pass

    if response == None: 
        return response
    
    response = response.choices[0].message.content
    return response

def generate_request(query: str, role: str) -> str:

    request_parameters = []

    query_parameters = {
        "role": "user",
        "content": query
    }
    request_parameters.append(query_parameters)
    if role != None: 

        config_file = 'data/required_data/config.json'
        config_data = data_request(config_file)

        roles: dict = config_data['GPT']['ROLES']
        if role not in roles.keys():
            return request_parameters
        
        role_parameters = {
            "role": "system",
            "content": roles[role]
        }
        request_parameters.append(role_parameters)

    return request_parameters

def process_chat_gpt(query: str, role_name = None) -> str:

    config_inner_file_path = 'data/required_data/config.json'
    api_inner_file_path = 'data/required_data/api_keys.json'

    config_data = data_request(config_inner_file_path)
    api_data = data_request(api_inner_file_path)

    MODEL = config_data['GPT']['MODEL']
    API_KEY = api_data['CHAT_GPT']

    ROLE_OPTIONS = list(config_data['GPT']['ROLES'].keys())
    if role_name not in ROLE_OPTIONS and role_name != None:
        raise ValueError('Please select one of these role names: %s' % ROLE_OPTIONS)
    
    ROLE_DATA = None
    if role_name != None: 
        ROLE_DATA = config_data['GPT']['ROLES'][role_name]

    parameters = generate_request(query, ROLE_DATA)
    response = gpt_call(MODEL, API_KEY, parameters)

    return response
