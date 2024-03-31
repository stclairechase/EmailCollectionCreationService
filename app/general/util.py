from requests import session, Response
from bs4 import BeautifulSoup

def website_request(url: str, parser = None) -> tuple[str, BeautifulSoup]: 

    if parser == None: 
        parser = 'html.parser'

    session_ = session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    raw: Response = session_.get(url, headers)
    status: int = raw.status_code
    VALID_STATUS_CODE = 200
    if status != VALID_STATUS_CODE: 
        return None, None

    raw_data: str = raw.text
    soup = BeautifulSoup(raw_data, parser)
    
    session_.close()
    return raw_data, soup

