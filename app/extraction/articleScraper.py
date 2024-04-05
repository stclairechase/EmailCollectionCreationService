from newspaper import Article, Config, ArticleException
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


def configuration(config: Config) -> Config:

    USER_AGENTS = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
    CONNECTION_TIMEOUT = 5

    config.browser_user_agent = USER_AGENTS
    config.request_timeout = CONNECTION_TIMEOUT
    config.memoize_articles = False
    return config

def article_pull(url: str) -> tuple(str, str, list, list):

    article_title: str = None 
    article_text: str = None
    article_keywords: list = None
    article_authors: list = None

    client = Config()
    config = configuration(client)

    article_data = Article(url, config=config)

    try: 
        article_data.download()
        article_data.parse()
    except ArticleException:
        pass
    except Exception as e: 
        print(e)

    article_title = article_data.title
    article_text = article_data.text
    article_keywords = article_data.keywords
    article_authors = article_data.authors
    
    return article_title, article_text, article_keywords, article_authors


def make_freq_table(text_string) -> dict:

    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    frequency_table = dict()
    for word in words:
        word = ps.stem(word)

        if word in stop_words:
            continue

        if word in frequency_table:
            frequency_table[word] += 1
        else:
            frequency_table[word] = 1

    return frequency_table


def article_summarizer(article_text: str) -> str:

    tokenized = sent_tokenize(article_text)
    frequency_dict = make_freq_table(article_text)
    temp = {}
    for val in tokenized: 
        word_ct = len(word_tokenize(val))
        for wordValue in frequency_dict:
            if wordValue in val.lower():
                if val[:10] in temp:
                    temp[val[:10]] += frequency_dict[wordValue]
                else:
                    temp[val[:10]] = frequency_dict[wordValue]

        temp[val[:10]] = temp[val[:10]] // word_ct

    sumValues = 0
    for entry in temp:
        sumValues += temp[entry]

    average = int(sumValues / len(temp))

    sentence_count = 0
    summary = ''

    for sentence in tokenized:
        if sentence[:10] in temp and temp[sentence[:10]] > (average*1.5):
            summary += " " + sentence
            sentence_count += 1

    return summary