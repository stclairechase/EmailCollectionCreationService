from pandas import isna

from app.extraction.articleScraper import article_pull, article_summarizer
from app.data_management.general import setup_data, data_request
from app.data_management.file_manager import FileManager
from app.processing.promptCreator import subject_matter_prompt, email_body_prompt
from app.general.util import seperate_url
from app.api_calls.chatgpt_call import gpt_call


def check_last_data(base_url: str, url: str, article_data: list):
    existing_data = False

    for data in article_data: 
        if base_url == data['base_url']:
            if url != data['url']:
                data['body'] = None
                data['subject'] = None
            else: 
                existing_data = True
            break
    return existing_data
        
def prompt_detail_decider(details: list):

    valid_detail: str = None
    for detail in details: 
        if detail in ([], "", None) or isna(detail):
            continue
        valid_detail = detail
        break
    return valid_detail

def process_script(url: str, extra_detail: list, article_data: list, summarize_article = False): 

    base_url, url = seperate_url(url)
    
    exisiting_data = check_last_data(base_url, url, article_data)
    if exisiting_data == True: 
        return

    article_title, article_text, article_keywords, article_authors = article_pull(url)
    if summarize_article == True: 
        article_text = article_summarizer(article_text)

    hierarchy = [
        article_text,
        article_title,
        article_keywords, 
        url
    ]
    hierarchy.extend(list(extra_detail))
    additional_detail = prompt_detail_decider(hierarchy)

    email_subject = subject_matter_prompt(additional_detail)
    email_body = email_body_prompt(additional_detail)


    return

def main(file_name=None): 

    article_data = []

    json_file_path = 'data/required_data/config.json'
    json_data = data_request(json_file_path)
    url_column: str = json_data['DATA_PROCESSING']['IMPORTS_URL_COLUMN']
    additions: list = json_data['EMAIL_GENERATION_DETAILS']["ADDITIONAL_IMPORTED_COLUMNS"]

    if file_name == None: 
        file_name = "rp_yes_2.csv"
    imported_data: list[dict] = setup_data(file_name, asdict=True)

    base_urls = [data['base_url'] for data in imported_data]
    inner_file = "data/created_data/raw_article_scrape.csv"
    file_manager = FileManager(base_urls, inner_file)

    base_urls, article_data = file_manager.check_for_scraped_values()

    for data in imported_data:
        url = data[url_column] 

    
        additional_data = []
        for addition in additions: 
            if addition in data.keys():
                new_value = data[addition]
                additional_data.append(new_value)

        process_script(url, additional_data)

if __name__ == "__main__":
    main()
