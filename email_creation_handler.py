from pandas import isna

from app.extraction.articleScraper import article_pull, article_summarizer
from app.data_management.general import setup_data, data_request
from app.data_management.file_manager import FileManager
from app.processing.promptCreator import subject_matter_prompt, email_body_prompt
from app.general.util import seperate_url
from app.api_calls.chatgpt_call import process_chat_gpt, generate_request
from app.data_management.emailList import pull_emails
from app.data_management.emailLocater import locate_email_data


def check_last_data(base_url: str, url: str, email_data: dict):
    existing_data = False

    for data in email_data: 
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

def process_script(url: str, extra_detail: list, email_data: list, summarize_article = False, role = None): 

    base_url, url = seperate_url(url)
    
    exisiting_data = check_last_data(base_url, url, email_data)
    if exisiting_data == True: 
        return 
    

    additional_data = {
        "url": url, 
        "base_url": base_url,
        "article_title": None,
        "article_text": None, 
        "article_keywords": None,
        "article_authors": None,
        "subject_line": None,   
        "email_body": None,
        "email": None
    }

    article_title, article_text, article_keywords, article_authors = article_pull(url, summarize_article)

    if additional_data['article_title'] == None:
        additional_data['article_title'] = article_title
    if additional_data['article_text'] == None:
        additional_data['article_text'] = article_text
    if additional_data['article_keywords'] == None:
        additional_data['article_keywords'] = article_keywords
    if additional_data['article_authors'] == None: 
        additional_data['article_authors'] = article_authors

    hierarchy = [
        article_text, article_title, article_keywords, url]
    hierarchy = hierarchy + extra_detail
    
    query_data = prompt_detail_decider(hierarchy)

    if additional_data['email'] == None:
        email = locate_email_data(base_url)
        additional_data['email'] = email
    
    if additional_data['email'] == None: 
        email_data.append(additional_data)
        return email_data

    if additional_data['subject_line'] == None:
        subject_prompt = subject_matter_prompt(query_data)
        generated_subject = process_chat_gpt(subject_prompt)
        additional_data['subject_line'] = generated_subject

    if additional_data['email_body'] == None:
        body_prompt = email_body_prompt(query_data)
        generated_body = process_chat_gpt(body_prompt)
        additional_data['email_body'] = generated_body
    email_data.append(additional_data)
    return email_data

def main(file_name=None): 

    json_file_path = 'data/required_data/config.json'
    json_data = data_request(json_file_path)
    url_column: str = json_data['DATA_PROCESSING']['IMPORTS_URL_COLUMN']
    additions: list = json_data['EMAIL_GENERATION_DETAILS']["ADDITIONAL_IMPORTED_COLUMNS"]

    if file_name == None: 
        file_name = "rp_yes_2.csv"
    imported_data: list[dict] = setup_data(file_name, asdict=True)

    urls = [x[url_column] for x in imported_data]
    inner_file = "data/created_data/generated_emails.csv"
    file_manager = FileManager(urls, inner_file)

    base_urls, email_data = file_manager.check_for_scraped_values()

    for data in imported_data:
        url = data[url_column] 

        additional_data = []
        for addition in additions: 
            if addition in data.keys():
                new_value = data[addition]
                additional_data.append(new_value)

        process_script(url, additional_data, email_data, role='MARKETING')
        file_manager.log_new_data(email_data)

if __name__ == "__main__":
    main()
