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
from modelsRoutes import db, Resource, Course, Topic, app, Enroll, Learner
import math
from keybert import KeyBERT

nltk.download('stopwords')
nltk.download('wordnet')
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


def create_topic_embeddings(topics):

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


def create_topic_polylines(topics, topicembedding):
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

            polyline.append(cos_sim)  # format 1
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
            templ.append(temp)
        new_polylines.append(templ)
    return new_polylines


#
#
#
# learners functions
#
#
#

def create_embeddings_centroid_list(l):
    new_keybert_embeddings_list = []
    for i in l:
        # find the centroid of the embeddings for a doc
        index_averages = [sum(x) / len(x) for x in zip(*i)]
        new_keybert_embeddings_list.append(index_averages)
    return new_keybert_embeddings_list


def rad_plot_axes(num, x_max, y_max):  # function to plot the competency axes
    empt_arr = []  # a temporary container
    xstop = []  # list to store x coordinate of the axes endpoints
    ystop = []  # list to store y coordinate of the axes endpoints
    tlen = []  # list to store the length of axes
    ttempl = []  # a temporary container
    theta = ((np.pi)/(num-1))/2
    b = 0
    while (b*theta) <= (np.arctan(y_max/x_max)):
        empt_arr.append(x_max * math.tan(b*theta))
        ystop.append(empt_arr[b])
        ttemp = math.sqrt(
            ((x_max * x_max) + (x_max * math.tan(b*theta) * x_max * math.tan(b*theta))))
        tlen.append(ttemp)
        if (b*theta != np.arctan(y_max/x_max)):
            ttempl.append(ttemp)
        b = b+1

    while b < num:
        ystop.append(y_max)
        b = b+1
    tlen.extend(list(reversed(ttempl)))
    xstop = list(reversed(ystop))
    # print(tlen)
    # print(ystop)

    for d in range(num):
        x_values = [0, xstop[d]]
        y_values = [0, ystop[d]]
        # plt.plot(x_values, y_values, label=f'topic {d+1}', alpha=1, linewidth=0.2)
    return tlen, theta


def rad_plot_poly(num, hd_point, tlen, theta):
    k = 0  # just a looping var
    coordinates = []
    for pnt in hd_point:
        new_pnt = []
        x_values = []
        y_values = []
        for p in range(num):
            new_pnt.append(pnt[p])
            rlen = pnt[p]*tlen[p]
            x_values.append(rlen * math.cos(p*theta))
            y_values.append(rlen * math.sin(p*theta))
        # plt.plot(x_values, y_values, label=f'polyline', alpha=0.6, linewidth=0.5)
        average_x = sum(x_values)/num
        average_y = sum(y_values)/num

        coordinates.append([float(average_x), float(average_y)])
        k = k+1

    print("Red    - Resources ")

    return coordinates


def pushTopicsToDB(topics, topicembedding, topic_polylines, course_id):

    print(len(topics), len(topic_polylines), len(topicembedding))
    feature_length = len(topic_polylines["polyline"][0])
    (tlen, theta) = rad_plot_axes(feature_length, 1, 1)
    centroid_list = rad_plot_poly(
        feature_length, topic_polylines["polyline"], tlen, theta)
    allTopics = []
    with app.app_context():
        for i in range(len(topics)):
            topic = Topic(
                name=topics["name"][i],
                description=topics["description"][i],
                keywords=topics["tokens"][i],
                polyline=topic_polylines["polyline"][i],
                x_coordinate=centroid_list[i][0],
                y_coordinate=centroid_list[i][1],
                course_id=course_id,
                embedding=topicembedding[i].tolist()
            )
            allTopics.append(topic)
        db.session.add_all(allTopics)
        db.session.commit()
    print("added topics to DB")


def pushResourcesToDB(resources, resourceembedding, resource_polylines, course_id):
    print(len(resources), len(resource_polylines), len(resourceembedding))

    feature_length = len(resource_polylines[0])
    (tlen, theta) = rad_plot_axes(feature_length, 1, 1)
    centroid_list = rad_plot_poly(
        feature_length, resource_polylines, tlen, theta)
    allresources = []
    with app.app_context():
        for i in range(len(resources)):
            new_resource = Resource(
                name=resources["name"][i],
                description=resources["description"][i],
                keywords=resources['keywords'][i],
                polyline=resource_polylines[i],
                x_coordinate=centroid_list[i][0],
                y_coordinate=centroid_list[i][1],
                course_id=course_id,
                type=1,
                embedding=resourceembedding[i]
            )
            # print(new_resource.to_dict())
            allresources.append(new_resource)
            # db.session.add(new_resource)
            # db.session.commit()
        db.session.add_all(allresources)
        db.session.commit()
    print("added resources to the DB")
    # breakpoint()


# find the keywords for all the documents and store it in a list
def create_keywords_list(content_list):
    kw_model = KeyBERT(model='all-mpnet-base-v2')
    num_keywords = 10
    all_keywords_list = []
    all_weight_list = []
    for i in range(len(content_list)):
        keywords = kw_model.extract_keywords(content_list[i], keyphrase_ngram_range=(
            1, 2), stop_words='english', highlight=False, top_n=num_keywords)
        keywords_list = list(dict(keywords).keys())
        cs_list = list(dict(keywords).values())
        weight = sum(cs_list)/len(cs_list)
        all_keywords_list.append(keywords_list)
        all_weight_list.append(weight)
    return all_keywords_list, all_weight_list


# Load pre-trained BERT model and tokenizer
def create_embeddings_list(l):
    model_name = 'bert-base-uncased'
    tokenizer = BertTokenizer.from_pretrained(model_name)
    new_model = BertModel.from_pretrained(model_name)

    keybert_embeddings_list = []
    for i in l:

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


def create_polyline(l, course_id):
    all_polylines = []
    embeddings = db.session.query(
        Topic.embedding).filter_by(course_id=course_id).all()
    topic_embeddings = embeddings
    for keybert_embeddings in l:
        docVector = keybert_embeddings
        polyline = []
        for j in range(len(topic_embeddings)):
            wordVector = topic_embeddings[j]
            # find cosine similarity between the learner embeddings and the topic embeddings
            cos_sim = (get_cos_sim(wordVector, docVector) + 1) / 2
            polyline.append(cos_sim)
        all_polylines.append(polyline)
    return all_polylines


def create_polyline_highline(old, new):
    feature_len = len(old)
    polyline = []
    for i in range(feature_len):
        polyline.append(max(max(old[i]), new[i]))
    return polyline


def update_position(summary, enrollId, courseId):
    print(summary, enrollId, courseId)
    # (all_keywords_list, all_weight_list) = create_keywords_list([summary])
    # keybert_embeddings_list = create_embeddings_list(all_keywords_list)
    # new_keybert_embeddings_list = create_embeddings_centroid_list(
    #     keybert_embeddings_list)
    # all_polylines = create_polyline(new_keybert_embeddings_list, courseId)
    # polylines = db.session.query(Enroll.polyline).filter_by(id=enrollId).all()
    # print(polylines)

    (all_keywords_list, all_weight_list) = create_keywords_list([summary])
    learner_embeddings = create_resource_embeddings(all_keywords_list)
    topicembedding = db.session.query(
        Topic.embedding).filter_by(course_id=courseId).all()
    if not topicembedding:
        raise IndexError()

    learner_polylines = create_resource_polylines(
        topicembedding, learner_embeddings)
    print(learner_polylines)
    # print(centroid_list)
    enroll: Enroll = Enroll.query.get(enrollId)
    if not enroll:
        raise IndexError
    polylines = enroll.polyline
    print(polylines)
    new_polylines = create_polyline_highline(
        learner_polylines[0], polylines)
    print(new_polylines)

    feature_length = len(learner_polylines[0])
    (tlen, theta) = rad_plot_axes(feature_length, 1, 1)
    centroid_list = rad_plot_poly(
        feature_length, [new_polylines], tlen, theta)
    print(centroid_list)
    enroll.x_coordinate = centroid_list[0][0]
    enroll.y_coordinate = centroid_list[0][1]
    enroll.polyline = new_polylines
    db.session.commit()
    return centroid_list[0]


def create_Course(name, description, topics: pd.DataFrame, resource_keylist: pd.DataFrame):
    new_course = Course(
        name=name,
        description=description
    )
    with app.app_context():
        db.session.add(new_course)
        db.session.commit()
        new_learner = Learner(
            name="Gururaj",
            cgpa=4.0,
            username="guru",
            password="guru"
        )
        db.session.add(new_learner)
        db.session.commit()
        new_enroll = Enroll(
            learner_id=1,
            course_id=1,
            x_coordinate=0.0,
            y_coordinate=0.0,
            polyline=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )
        db.session.add(new_enroll)
        db.session.commit()
        course_id = new_course.id
        print(new_course.to_dict())
    print("this si the new course id", course_id)
    topics = pd.read_excel(
        r'C:\MINE\temp\navigated_learning\Backend\DM\DM_topics.xlsx')
    apply_preprocessing(topics)
    topicembedding = create_topic_embeddings(topics)
    topic_polylines = create_topic_polylines(topics, topicembedding)
    print("Done")
    pushTopicsToDB(topics, topicembedding, topic_polylines, course_id)

    resource_keylist = pd.read_excel(
        r'C:\MINE\temp\navigated_learning\Backend\DM\DM_Resource_Keywords.xlsx')
    resource_keylist['keywords'] = resource_keylist['description'].apply(
        lambda x: x.split(','))
    resource_embeddings = create_resource_embeddings(
        resource_keylist['keywords'])
    resource_polylines = create_resource_polylines(
        topicembedding, resource_embeddings)
    print(resource_polylines[0])
    pushResourcesToDB(resource_keylist, resource_embeddings,
                      resource_polylines, course_id)

    # breakpoint()
