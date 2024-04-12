from pandas import read_csv, DataFrame
from os import path

from app.general.util import seperate_url
from app.data_management.general import directory_path_finder

class FileManager: 

    def __init__(self, url_list: list, inner_file: str) -> None:

        directory_path = directory_path_finder()
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

        temp_dataframe = DataFrame(name_data)
        temp_dataframe = temp_dataframe.drop_duplicates()

        if path.exists(self.file_path):
            temp_dataframe.to_csv(self.file_path, mode='a', index=False, header=False)
        else: 
            temp_dataframe.to_csv(self.file_path, mode='w', index=False)
