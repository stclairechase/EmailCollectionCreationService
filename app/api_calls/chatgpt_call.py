from openai._exceptions import RateLimitError
import openai
from time import sleep

from ..general.util import data_request

def gpt_call(model: str, api_key: str, parameters: list[dict]):

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

def generate_request(query: str, article_limit: int, role_data: str) -> str:

    request_parameters = []

    length_of_query = len(query)
    if length_of_query > article_limit: 
        query = query[0:article_limit]

    query_parameters = {
        "role": "user",
        "content": query
    }
    request_parameters.append(query_parameters)
    if role_data != None: 
        role_parameters = {
            "role": "system",
            "content": role_data
        }
        request_parameters.append(role_parameters)

    return request_parameters

def process_chat_gpt(query: str, role_name: str):

    config_inner_file_path = 'data/required_data/config.json'
    api_inner_file_path = 'data/required_data/api_keys.json'

    config_data = data_request(config_inner_file_path)
    api_data = data_request(api_inner_file_path)

    MODEL = config_data['GPT']['MODEL']
    API_KEY = api_data['CHAT_GPT']
    ARTICLE_SIZE_LIMIT = config_data['GPT']['LIMITS']['ARTICLE_DATA_WORD_COUNT']

    ROLE_OPTIONS = list(config_data['ROLES'].keys())
    if role_name not in ROLE_OPTIONS and role_name != None:
        raise ValueError('Please select one of these role names: %s' % ROLE_OPTIONS)
    
    ROLE_DATA = None
    if role_name != None: 
        ROLE_DATA = config_data['GPT']['ROLES'][role_name]

    parameters = generate_request(query, ARTICLE_SIZE_LIMIT, ROLE_DATA)
    response = gpt_call(MODEL, API_KEY, parameters)

    return response
