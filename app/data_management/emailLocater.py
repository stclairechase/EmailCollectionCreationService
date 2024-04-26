from pandas import DataFrame

from general import data_request

def search_mail_gun_data(base_url: str) -> str: 

    inner_file_path = 'data/created_data/raw_email_data.csv'
    try:
        email_data: DataFrame = data_request(inner_file_path)
    except: 
        return None 
    
    url_mask = email_data['base_url'] == base_url
    filtered_df = email_data[url_mask]
    if filtered_df.empty: 
        return None 
    
    verified_mask = filtered_df['mail_gun_verification'] == True
    filtered_df = filtered_df[verified_mask]
    if filtered_df.empty: 
        return None
    
    personal_email_mask = email_data['email_type'] == 'Personal'
    possible_personal_email = filtered_df[personal_email_mask]
    if possible_personal_email.empty: 
        filtered_email_data = filtered_df.to_dict(orient="records")[0]
    else: 
        filtered_email_data = possible_personal_email.to_dict(orient="records")[0]

    email = filtered_email_data['email']
    return email

def search_hunter_io(base_url: str) -> str: 

    inner_file_path = 'data/created_data/hunterio_verified.csv'
    try:
        email_data: DataFrame = data_request(inner_file_path)
    except: 
        return None 
    
    base_url_mask = email_data['base_url'] == base_url
    filtered_df = email_data[base_url_mask]
    if filtered_df.empty: 
        return None
    
    found_emails = filtered_df['email'].tolist()
    return found_emails[0]


def locate_email_data(base_url: str) -> str | None: 

    email = search_mail_gun_data(base_url)
    if email != None: 
        return email
    email = search_hunter_io(base_url)
    if email != None: 
        return email
    return None


