from spacy import load
import re

def regex_name_filter(text: str) -> str:
    possible_names = []
    pattern = "^[A-Z][a-z]+\s[A-Za-z]+$"

  
    possible_names = re.findall(pattern, text)
    
    if possible_names == []:
        return None
    return possible_names

def spacey_search(html_text: str) -> list:

    MAX_LIMIT = 1000000

    found_names = []
    if html_text == None: 
        return found_names

    language_model = load('en_core_web_sm')
    initial_name_search = regex_name_filter(html_text)
    if initial_name_search == None: 
        text_data = html_text
    else: 
        text_data = ', '.join([" ".join(x) for x in initial_name_search])

    length_of_text = len(text_data)
    if MAX_LIMIT < length_of_text: 
        text_data = text_data [0:MAX_LIMIT]
        
    parsed_string = language_model(text_data)

    for data in parsed_string.ents: 
        label = data.label_

        if label == 'PERSON':
            temp_text = data.text
            validated_name = regex_name_filter(temp_text)
            if validated_name != None:
                found_names.append(validated_name[0])

    return found_names
