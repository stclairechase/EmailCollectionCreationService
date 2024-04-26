from app.extraction.emailScraper import process_scrapers
from app.data_management.general import setup_data
from app.data_management.file_manager import FileManager
from app.general.emailCategorizer import categorize_emails
from app.processing.mailGunVerifier import process_verification

def main(file_name=None): 

    if file_name == None: 
        file_name = '/Users/chasestclaire/Desktop/coding_projects/github/AutomatedEmailCreation/EmailCollectionCreationService/data/input_data/testing_feb_20.csv'  
    urls = setup_data(file_name)

    email_data_location = "data/created_data/raw_email_data.csv"
    file_manager = FileManager(urls, email_data_location)
    
    urls, historical_data = file_manager.check_for_scraped_values()
    email_data: list[dict] = []
    for url in urls: 
        email_data: list = process_scrapers(url, email_data)
        email_data: list = categorize_emails(email_data)
        email_data: list = process_verification(email_data)
        file_manager.log_new_data(email_data)
    
if __name__ == "__main__": 
    main()