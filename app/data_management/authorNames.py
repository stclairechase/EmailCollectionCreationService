from pandas import read_csv, DataFrame
from os import path

from general.util import directory_path_finder, seperate_url

class AuthorFinderDataManagement: 

    def __init__(self, url_list=None) -> None:

        directory_path = directory_path_finder()
        inner_file = "data/created_data/raw_name_scrape.csv"
        self.file_path = directory_path + inner_file
        
        self.imported_url_list = url_list

    def check_for_scraped_values(self) -> tuple[list]:

        current_data = []
        filtered_url_list = []

        if not path.exists(self.file_path):
            return self.imported_url_list, current_data
        
        base_urls = []
        for url in self.imported_url_list: 
            base_url, full_url = seperate_url(url)
            base_urls.append(base_url)
        
        raw_dataframe = read_csv(self.file_path)
        url_check_mask = raw_dataframe['base_url'].isin(base_urls)

        filtered_df = raw_dataframe[url_check_mask]
        current_data = filtered_df.to_dict(orient='records')

        current_url_data = filtered_df['base_url'].tolist()
        for url in self.imported_url_list: 
            base_url, full_url = seperate_url(url)
            if base_url not in current_url_data:
                filtered_url_list.append(full_url)

        return filtered_url_list, current_data

    def log_new_data(self, name_data: list):

        if path.exists(self.file_path):
            MODE = 'w'
        else: 
            MODE = 'a'

        temp_dataframe = DataFrame(name_data)
        temp_dataframe.to_csv(self.file_path, mode=MODE, index=False)