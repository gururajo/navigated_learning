import pandas as pd
from bs4 import BeautifulSoup
import re
from nltk.stem import WordNetLemmatizer, PorterStemmer


def utils_preprocess_text(text, flg_stemm=False, flg_lemm=True, lst_stopwords=None):

    # Remove HTML
    soup = BeautifulSoup(text, 'lxml')
    text = soup.get_text()

    # Remove punctuations and numbers
    text = re.sub('[^a-zA-Z]', ' ', text)

    # Single character removal
    text = re.sub(r"\s+[a-zA-Z]\s+", ' ', text)

    # Removing multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # Tokenize (convert from string to list)
    lst_text = text.split()

    # remove Stopwords
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in lst_stopwords]

    # Stemming (remove -ing, -ly, ...)
    if flg_stemm == True:
        ps = PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]

    # Lemmatisation (convert the word into root word)
    if flg_lemm == True:
        lem = WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]

    text = " ".join(lst_text)
    return text


def apply_preprocessing(df):
    df['clean_text'] = df['description'].apply(lambda x: x.lower())
    df['clean_text'] = df["clean_text"].apply(lambda x: utils_preprocess_text(
        x, flg_stemm=False, flg_lemm=True, lst_stopwords=stop_words))
    df['tokens'] = df['clean_text'].apply(lambda x: x.split())


if __name__ == "__main__":
    topics = pd.read_excel('DM_topics.xlsx')
