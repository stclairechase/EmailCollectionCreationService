from app.data_management.general import data_request

def length_check(article_text: str, limit: int) -> str:

    split_article = article_text.split(' ')
    length_ = len(split_article)
    if length_ <= limit:
        return article_text
    
    adj_split = split_article[0:limit]
    new_text = ' '.join(adj_split)
    return new_text

def subject_matter_prompt(details: str) -> str:

    prompt_file_path = 'data/required_data/gpt_prompts/comparision_prompt.txt'

    main_prompt: str = data_request(prompt_file_path)
    prompt = f"{details}\n\n{main_prompt}"

    return prompt

def email_body_prompt(details: str) -> str:

    config_file = "data/required_data/config.json"
    emaiL_example_file = "data/required_data/gpt_prompts/email_example.txt"

    configs = data_request(config_file)
    email_prompt = data_request(emaiL_example_file)

    limits: int = configs['GPT']['ARTICLE_DATA_WORD_COUNT']
    sign_off_name: str = configs['EMAIL_GENERATION_DETAILS']['SIGN_OFF_NAME']

    details = length_check(details, limits)

    extra_details = f"EXTRA DETAILS FROM WEBPAGE: {details}\n\n"
    sign_off_name = f"\n\nSign off the email with my name {sign_off_name}"

    prompt = extra_details + email_prompt + sign_off_name

    return prompt
    


