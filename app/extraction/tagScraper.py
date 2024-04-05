from ..general.util import website_request

from bs4 import BeautifulSoup
from bs4.element import Tag

def tag_to_dict(element_tag: Tag) -> dict:

    meta_data = {}

    element_tag_str = str(element_tag)
    clean_str = lambda x : x.replace('<','').replace('>','').replace('"','').replace('/','')

    tag_split = element_tag_str.split('" ')
    for tag in tag_split:
        try:
            meta_tag_key = clean_str(tag.split('=')[0])
            meta_tag_value = clean_str(tag.split('=')[1])

            meta_data[meta_tag_key] = meta_tag_value
        except IndexError:
            continue
    return meta_data

def meta_tag_processor(article_soup: BeautifulSoup) -> str:

    author_name = None

    meta_tag_data: list[Tag] = article_soup.find_all('meta')
    meta_tag_detail_options = ['author', 'writer', 'publisher']

    KEY_VALUE = 'name'
    filtered_meta_tag = {}

    for search_key in meta_tag_detail_options:
        for meta_tag in meta_tag_data:

            meta_tag_data = {}

            if search_key in meta_tag:
                meta_tag_data: dict = tag_to_dict(meta_tag)
                meta_tag_keys = meta_tag_data.keys()

                if KEY_VALUE in meta_tag_keys and meta_tag_keys[KEY_VALUE] == search_key: 
                    filtered_meta_tag = meta_tag_data
                    break 
    
    if filtered_meta_tag == {}:
        return author_name 
    
    value_key = ['content', 'meta content']

    for value in value_key: 
        if value in filtered_meta_tag.keys():
            author_name: str = filtered_meta_tag[value]
            break
    return author_name
            
def article_tag_processor(article_soup: BeautifulSoup) -> str: 
    
    author_name = None

    SEARCH_KEY = 'author'
    article_tag_data: list[Tag] = article_soup.find_all('article')

    for tag in article_tag_data:

        if SEARCH_KEY in tag: 
            tag_data = tag_to_dict(tag)
            author_name = tag_data['author']
            break 
    return author_name

def div_tag_processor(article_soup: BeautifulSoup) -> str:

    author_name = None

    SEARCH_KEY = 'author'
    div_tag_data: list[Tag] = article_soup.find_all('div')
    
    for tag in div_tag_data: 
        if SEARCH_KEY in tag: 
            author_name = tag.get_text(strip=True)
            break
    return author_name


def process_tag_scrape(article_soup: BeautifulSoup) -> str:

    author_name = None 

    processors = [
        meta_tag_processor, 
        article_tag_processor, 
        div_tag_processor
    ]
    
    for processor in processors:
        author_name = processor(article_soup)
        if author_name != None: 
            break
    return author_name