from pandas import read_csv
from difflib import get_close_matches

def first_name_examples() -> list: 

    file_path = '/Users/chasestclaire/Desktop/coding_projects/github/AutomatedEmailCreation/EmailCollectionCreationService/data/required_data/us_birth_data_2011-2014.csv'

    baby_names_df = read_csv(file_path)
    first_names = sorted(list(set(baby_names_df["Child's First Name"].tolist())))
    return first_names

def filter_by_name_properties(names: list) -> list: 

    NOT_A_FULL_NAME = 1
    FULL_NAME_LIMIT = 3
    NO_DATA = ''
    filtered_list = []

    for name in names: 

        split_name = name.split(' ')
        length_of_name = len(split_name)

        if type(name) != str: 
            continue
        if name == NO_DATA: 
            continue
        if length_of_name == NOT_A_FULL_NAME:
            continue
        if length_of_name > FULL_NAME_LIMIT: 
            continue
        filtered_list.append(name)
    return filtered_list

def find_matches(names: list, possible_names: list) -> list: 

    filtered_list = []
    for name in names:
        match = get_close_matches(name.split(' ')[0], possible_names, n=1, cutoff=.8)
        if match != []:
            filtered_list.append(name)
    return filtered_list

def filter_out_names(name_list: list) -> list:

    filtered_names = filter_by_name_properties(name_list)
    name_options = first_name_examples()

    valid_names = find_matches(filtered_names, name_options)

    return valid_names
