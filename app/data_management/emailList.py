from pandas import DataFrame, Series, concat
from os.path import exists

from app.data_management.general import data_request

def classify_email(data: Series): 

    email_type = 'COLLABORATION'

    support_type = [
        'support', 'service', 'feedback'
        'info', 'membership',
        'help', 'info'
        'feedback', 'help'
        'customer', 'sales'
    ]

    email_name = data.split('@')[0]
    if email_name in support_type:
        email_type = 'MARKETING'

    return email_type

def pull_emails() -> list[dict]:
    dataframes = []

    hunter_io = 'data/created_data/hunterio_verified.csv'
    if exists(hunter_io):
        hunter_io_df: DataFrame = data_request(hunter_io)
        dataframes.append(hunter_io_df)
    mail_gun = 'data/created_data/mailgun_verified.csv'
    if exists(mail_gun):
        mail_gun_df: DataFrame = data_request(mail_gun)
        dataframes.append(mail_gun_df)

    if dataframes == []:
        return []

    email_data = concat(dataframes)

    email_data['role'] = hunter_io_df['email'].apply(classify_email)
    return email_data.to_dict(orient='records')
