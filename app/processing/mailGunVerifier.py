from json import loads
from pandas import DataFrame

from app.data_management.general import data_request
from app.general.util import website_request

def verify_email(email: str):
    
    config_file_path = "data/required_data/api_keys.json"
    api_keys = data_request(config_file_path)
    mail_gun_api_key = api_keys['MAIL_GUN']

    url = f"https://api.eu.mailgun.net/v3/address/validate"
    auth = ('api', mail_gun_api_key)
    data = {
        "address": email
        }

    raw_data, soup = website_request(url, auth=auth, params=data)
    if raw_data == None: 
        return False
    mail_gun_data = loads(raw_data)
    valid_email = mail_gun_data['is_valid']

    if valid_email == True: 
        return True
    return False

def process_verification(email_data: list) -> list: 
    
    if email_data == []: 
        return email_data

    temp_dataframe = DataFrame(email_data)
    temp_dataframe['mail_gun_verification'] = temp_dataframe['email'].apply(verify_email)

    return temp_dataframe.to_dict(orient='records')



