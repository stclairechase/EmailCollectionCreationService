from pandas import DataFrame

def categorize_emails(email_data: list[dict]) -> list:
    if email_data == []:
        return []

    non_personal_email = ['support', 'contact', 'help', 'info', 'membership',
                          'sales', 'customer_service', 'customerservice', 'service', 
                          'communication', 'admin', 'question']
    email_check = lambda x : 'Non-Personal' if x.split('@')[0] in non_personal_email else 'Personal'

    dataframe = DataFrame(email_data)
    dataframe['email_type'] = dataframe['email'].apply(email_check)

    return dataframe.to_dict(orient='records')