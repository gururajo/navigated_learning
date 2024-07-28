import pandas as pd
from modelsRoutes import db, Course, Topic, app, Enroll, Learner
from model_library import apply_preprocessing, create_topic_embeddings, create_topic_polylines, pushResourcesToDB, push_topics_to_db, create_resource_embeddings, create_resource_polylines, create_keywords_list, create_polyline_highline, rad_plot_axes, rad_plot_poly
from flask import jsonify


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
    push_topics_to_db(topics, topicembedding, topic_polylines, course_id)

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
    # new_polylines = []
    # for single_file in all_polylines:
    #     temp = [ max([single_file[i][j]['y'] for j in range(len(single_file[i]))]) for i in range(len(single_file))]
    #     new_polylines.append(temp)
    # breakpoint()


def login(username, password):
    learner = Learner.query.filter_by(
        username=username, password=password).first()
    if not learner:
        return {"isValid": False}
    print(learner, dir(learner))
    return {"isValid": True, "username": learner.username, "id": learner.id, "cgpa": learner.cgpa, "name": learner.name}


def learner_course_enrolled(id):
    learner = Learner.query.get(id)
    if not learner:
        return jsonify({"error": "Learner not found"}), 404

    enrolled_courses = []
    for enrollment in learner.enrollments:
        course = Course.query.get(enrollment.course_id)
        if course:
            enrolled_courses.append({
                'course_id': course.id,
                'course_name': course.name,
                'course_description': course.description
            })

    return jsonify(enrolled_courses)
