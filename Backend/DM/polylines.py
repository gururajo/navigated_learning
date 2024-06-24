import pandas as pd
from bs4 import BeautifulSoup
import re
import nltk
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
import numpy as np
from transformers import BertModel, BertTokenizer, BertForMaskedLM
import torch


nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


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


def create_topic_embeddings():

    count = 0
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    topicembedding = []

    for i in range(len(topics)):
        embedding2 = model.encode(
            topics.loc[i, "description"], convert_to_tensor=True)
        topicembedding.append(embedding2.cpu())
    return topicembedding


def get_cos_sim(a, b):
    """Takes 2 vectors a, b and returns the cosine similarity according
    to the definition of the dot product"""

    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)


def create_topic_polylines():
    topic_names = topics["name"].tolist()  # Topic keyphrases
    length = len(topics)
    topic_modules = []  # Topic module number
    for i in range(12):
        topic_modules.append(1)
    for i in range(8):
        topic_modules.append(2)
    nowl = len(topic_modules)
    for i in range(length-nowl):
        topic_modules.append(3)
    # Topic embedding - mean of topic embeddings of individual words of a keyphrase
    topic_embeddings = topicembedding
    top_poly = []
    top_module = []
    topic = []

    # Going through each topic and computing the cosine similarity between it's embedding and all other topic's embeddings
    for i in range(len(topic_names)):
        polyline = []
        for j in range(len(topic_names)):
            cos_sim = 0
            if topic_names[i] == topic_names[j]:
                cos_sim = 1
            else:
                topic1_vector = topic_embeddings[i]
                topic2_vector = topic_embeddings[j]

                # scaling cosine similarity value from [-1,1] to [0,1]
                cos_sim = (get_cos_sim(
                    (topic1_vector), (topic2_vector)) + 1) / 2

            polyline.append({"x": j, "y": cos_sim})  # format 1
            # polyline.append((j, cos_sim)) #format 2

        topic.append(topic_names[i])
        top_module.append(topic_modules[i])
        top_poly.append(polyline)

    polyline_dict = {"topic": topic,
                     "module": top_module, "polyline": top_poly}
    # converting the topic polyline to a dataframe
    topic_polylines = pd.DataFrame(polyline_dict)
    return topic_polylines


#
#
# Resources functions start
#
#

def create_resource_embeddings(keywords):
    model_name = 'bert-base-uncased'
    tokenizer = BertTokenizer.from_pretrained(model_name)
    new_model = BertModel.from_pretrained(model_name)

    keybert_embeddings_list = []
    for i in keywords:

        # Tokenize the keywords and convert them into token IDs
        tokenized_inputs = tokenizer(
            i, padding=True, truncation=True, return_tensors="pt")

        # Obtain the embeddings from the BERT model
        with torch.no_grad():
            outputs = new_model(**tokenized_inputs)

        # Extract the embeddings corresponding to the [CLS] token
        embeddings = outputs.last_hidden_state[:, 0, :].numpy()
        embeddings = embeddings.tolist()
        keybert_embeddings_list.append(embeddings)
    return keybert_embeddings_list


def create_resource_polylines(topicembedding, keybert_embeddings_list):
    all_polylines = []
    topic_embeddings = topicembedding
    for embeddings in keybert_embeddings_list:
        single_file_polyline = []
        for i in range(len(embeddings)):
            docVector = embeddings[i]
            polyline = []
            for j in range(len(topic_embeddings)):
                wordVector = topic_embeddings[j]
                # find the cosine similarity between resource embeddings and the topic embeddings
                cos_sim = (get_cos_sim(wordVector, docVector) + 1) / 2
                polyline.append({'x': j, 'y': cos_sim})
            single_file_polyline.append(polyline)
        all_polylines.append(single_file_polyline)
    new_polylines = []
    for single_file_polyline in all_polylines:
        templ = []
        for i in range(len(topicembedding)):
            temp = 0
            # between the multiple polylines for each doc find the highline and set that as the final polyline
            for j in range(len(single_file_polyline)):
                if single_file_polyline[j][i]['y'] > temp:
                    temp = single_file_polyline[j][i]['y']
            templ.append({'x': i, 'y': temp})
        new_polylines.append(templ)
    return new_polylines


if __name__ == "__main__":
    topics = pd.read_excel(
        r'C:\MINE\temp\navigated_learning\Backend\DM\DM_topics.xlsx')
    topicembedding = create_topic_embeddings()
    topic_polylines = create_topic_polylines()
    print("Done")

    resource_keylist = pd.read_excel(
        r'C:\MINE\temp\navigated_learning\Backend\DM\DM_Resource_Keywords.xlsx')
    resource_keylist['keywords'] = resource_keylist['description'].apply(
        lambda x: x.split(','))
    resource_embeddings = create_resource_embeddings(
        resource_keylist['keywords'])
    resource_polylines = create_resource_polylines(
        topicembedding, resource_embeddings)
    print(resource_polylines[0])
    # breakpoint()
