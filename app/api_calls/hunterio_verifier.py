from pyhunter import PyHunter

from general.util import data_request

def hunterio_verifier(domain: str, first_name: str, last_name: str):

    inner_file = 'data/required_data/api_keys.json'
    KEY_DATA = data_request(inner_file)

    hunter = PyHunter(KEY_DATA['HUNTER_IO'])
    email = None
    try:
        hunterio_data = hunter.email_finder(domain=domain, first_name=first_name, last_name=last_name)
        email = hunterio_data[0]
        if email == None: 
            return None
        email_verifier = hunter.email_verifier(email)

        if email_verifier != {}:
            results = email_verifier['result']
            if results != 'deliverable':
                email = None
        else:
            email = None
    except Exception as e:
        return None
    return email