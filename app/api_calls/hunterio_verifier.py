from pyhunter import PyHunter


def hunterio_verifier(domain: str, first_name: str, last_name: str):

    hunter = PyHunter('42ecc3395b3773c5203c59bd135174fa6078d6c7')
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