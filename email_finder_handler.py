from pandas import DataFrame

from app.extraction.emailScraper import process
from app.data_management.general import setup_data
from app.data_management.file_manager import FileManager

def categorize_emails(email_data: list[dict]):
    if email_data == []:
        return []

    non_personal_email = ['support', 'contact', 'help', 'info', 'membership',
                          'sales', 'customer_service', 'customerservice', 'service']
    email_check = lambda x : 'Non-Personal' if x.split('@')[0] in non_personal_email else 'Personal'

    dataframe = DataFrame(email_data)
    dataframe['email_type'] = dataframe['email'].apply(email_check)
    return dataframe.to_dict(orient='records')

def main(file_name=None): 

    if file_name == None: 
        file_name = '/Users/chasestclaire/Desktop/coding_projects/github/AutomatedEmailCreation/EmailCollectionCreationService/data/input_data/150_test_rows.csv'  
    urls = setup_data(file_name)

    email_data_location = "data/created_data/raw_email_data.csv"
    file_manager = FileManager(urls, email_data_location)
    
    urls, historical_data = file_manager.check_for_scraped_values()
    email_data: list[dict] = []
    for url in urls: 
        new_email_data = process(url, email_data)
        new_email_data = categorize_emails(new_email_data)
        file_manager.log_new_data(new_email_data)
        email_data.extend(new_email_data)
    
if __name__ == "__main__": 
    main()