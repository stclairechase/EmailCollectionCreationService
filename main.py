from pandas import DataFrame, isna
from threading import Thread, Lock
from os.path import exists

from app.extraction.siteMapScraper import process_site_map_search
from app.extraction.tagScraper import process_tag_scrape
from app.general.util import data_request, website_request, seperate_url, directory_path_finder
from app.general.nameScraper import spacey_search
from app.api_calls.hunterio_verifier import hunterio_verifier
from app.data_management.authorNames import AuthorFinderDataManagement

thread_lock = Lock()

def setup_data() -> list:

    inner_folder_path = 'data/input_data/'
    file_name = 'rp_yes_2.csv'
    imported_data: DataFrame = data_request(inner_folder_path + file_name)

    json_file_path = 'data/required_data/config.json'
    json_data = data_request(json_file_path)

    url_column: str = json_data['DATA_PROCESSING']['IMPORTS_URL_COLUMN']
    url_list = imported_data[url_column].tolist()

    filtered_list = []
    for url in url_list:
        if not isna(url):
            filtered_list.append(url)

    return filtered_list

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

def main():

    urls = setup_data()[0:15]
    file_manager = AuthorFinderDataManagement(urls)

    urls, name_data = file_manager.check_for_scraped_values()

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




