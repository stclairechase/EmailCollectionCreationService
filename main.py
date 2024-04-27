from author_finder_handler import main as author_finder
from email_creation_handler import main as email_creation
from email_finder_handler import main as email_scraper

def main():

    file_name = "testing_feb_20.csv"

    #author_finder(file_name)
    #email_scraper(file_name)
    email_creation(file_name)

if __name__ == "__main__": 
    main()