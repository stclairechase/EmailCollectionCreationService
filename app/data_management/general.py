from pandas import DataFrame, read_csv, isna
from pathlib import Path
from json import load
from os.path import exists


def directory_path_finder() -> str: 

    github_name = 'EmailCollectionCreationService'
    script_path = str(Path(__file__))
    split_path = script_path.split(github_name)

    directory_path = split_path[0] + github_name + '/'

    return directory_path

def data_request(inner_file_name) -> dict or DataFrame:

    directory_path = directory_path_finder()
    data_file_path = directory_path + inner_file_name

    if not exists(data_file_path): 
        raise ValueError(f"File: {inner_file_name} does not exist, please add file to correct directory")
    
    if 'json' in data_file_path:
        with open(data_file_path, 'r') as json_:
            return load(json_)
    if 'csv' in data_file_path: 
        return read_csv(data_file_path)

def setup_data(file_name: str, asdict=False) -> list:

    file_delimitter = '/'
    if file_delimitter in file_name:
        formatted_file_name = file_name.split(file_delimitter)[-1]
        file_name = formatted_file_name

    inner_folder_path = 'data/input_data/'
    imported_data: DataFrame = data_request(inner_folder_path + file_name)

    if asdict == True: 
        return imported_data.to_dict(orient='records')

    json_file_path = 'data/required_data/config.json'
    json_data = data_request(json_file_path)

    url_column: str = json_data['DATA_PROCESSING']['IMPORTS_URL_COLUMN']

    url_list = imported_data[url_column].tolist()

    filtered_list = []
    for url in url_list:
        if not isna(url):
            filtered_list.append(url)

    return filtered_list
