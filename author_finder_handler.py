from pandas import DataFrame
from threading import Thread, Lock
from os.path import exists

from app.extraction.siteMapScraper import process_site_map_search
from app.extraction.tagScraper import process_tag_scrape
from app.general.util import website_request, seperate_url
from app.data_management.general import directory_path_finder, setup_data, data_request
from app.general.nameScraper import spacey_search
from app.api_calls.hunterio_verifier import hunterio_verifier
from app.data_management.file_manager import FileManager

thread_lock = Lock()


def last_file_check(name_data: list) -> list: 

    inner_file_path = 'data/created_data/hunterio_verified.csv'
    if not exists(inner_file_path):
        return name_data
    pulled_data: DataFrame = data_request(inner_file_path)
    found_emails = pulled_data['base_url'].tolist()

    filtered_names = []
    for data in name_data: 
        if data['base_url'] not in found_emails: 
            filtered_names.append(data)

    return filtered_names

def process_author_name_script(url: str, name_data: list) -> None: 

    base_url, url = seperate_url(url)
        
    name_data_addition = {
        'base_url': base_url, 
        'full_url': url,
        'author_name': None,
        'unknown_accuracy': False
    }

    raw_text, soup = website_request(url)
    tag_name_check: str = process_tag_scrape(soup)
    if tag_name_check != None: 
        name_data_addition['author_name'] = tag_name_check
        with thread_lock:
            name_data.append(name_data_addition)
        return name_data
    
    site_map_check: list = process_site_map_search(base_url)
    if site_map_check != None and site_map_check != []:
        temp_data = []
        for name in site_map_check: 
            inner_data = name_data_addition.copy()
            inner_data['author_name'] = name
            temp_data.append(inner_data)
        with thread_lock:
            name_data.extend(temp_data)
        return name_data
        
    article_check: list = spacey_search(raw_text)
    if article_check != []:
        temp_data = []
        for name in article_check: 
            inner_data = name_data_addition.copy()
            inner_data['author_name'] = name
            inner_data['unknown_accuracy'] = True
            temp_data.append(inner_data)
        with thread_lock:
            name_data.extend(temp_data)
        return name_data
    
def process_hunter_io(name_data: list[dict]):

    base_urls = []
    for data in name_data:
        base_url = data['base_url']
        author_name = data['author_name']

        split_name = author_name.split(' ')
        first_name = split_name[0]
        last_name = split_name[-1]

        if base_url in base_urls:
            continue

        email = hunterio_verifier(base_url, first_name, last_name)
        if email != None: 
            data['unknown_accuracy'] = False
            base_urls.append(base_url)
            filtered_data = [{
                **data,
                **{'email': email}
            }]

            temp_df = DataFrame(filtered_data)

            directory = directory_path_finder()
            inner_file = 'data/created_data/hunterio_verified.csv'
            file_path = directory + inner_file

            if exists(file_path):
                temp_df.to_csv(file_path, mode='a', index=False, header=False)

            else: 
                temp_df.to_csv(file_path, mode='w', index=False)
    
def test():

    name_data = []
    urls = setup_data()
    for url in urls: 
        process_author_name_script(url, name_data)

    return name_data

def main(file_name = None):

    if file_name == None:
        file_name = 'rp_yes_2.csv'

    urls = setup_data(file_name)
    inner_file = "data/created_data/raw_name_scrape.csv"
    file_manager = FileManager(urls, inner_file)

    urls, name_data = file_manager.check_for_scraped_values()
    name_data = last_file_check(name_data)

    if urls != []:
        threads = []
        for url in urls: 
            thread = Thread(target=process_author_name_script, args=(url, name_data,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    file_manager.log_new_data(name_data)
    process_hunter_io(name_data)

if __name__ == "__main__":
    main()




