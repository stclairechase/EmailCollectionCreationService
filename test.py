from app.data_management.general import setup_data
from app.extraction.emailScraper import process
from app.general.util import website_request

inner_file = "/Users/chasestclaire/Desktop/coding_projects/github/AutomatedEmailCreation/EmailCollectionCreationService/data/input_data/rp_yes_2.csv"
url_list = setup_data(file_name=inner_file)
email_list = []
for url in url_list:
    process(url, email_list)

print(1)