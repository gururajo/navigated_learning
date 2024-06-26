from flask import request, jsonify
# from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy
from datetime import datetime
from init import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://otageri:784512963@localhost/navigated_learning'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = flask_sqlalchemy.SQLAlchemy(app)

# Models


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2048))
    description = db.Column(db.JSON)
    keywords = db.Column(db.JSON)
    polyline = db.Column(db.JSON)
    x_coordinate = db.Column(db.Float)
    y_coordinate = db.Column(db.Float)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    type = db.Column(db.Integer)
    embedding = db.Column(db.JSON)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'keywords': self.keywords,
            'polyline': self.polyline,
            'x_coordinate': self.x_coordinate,
            'y_coordinate': self.y_coordinate,
            'course_id': self.course_id,
            'type': self.type,
            'embedding': self.embedding
        }


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250))
    description = db.Column(db.JSON)
    keywords = db.Column(db.JSON)
    polyline = db.Column(db.JSON)
    x_coordinate = db.Column(db.Float)
    y_coordinate = db.Column(db.Float)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    embedding = db.Column(db.JSON)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'keywords': self.keywords,
            'polyline': self.polyline,
            'x_coordinate': self.x_coordinate,
            'y_coordinate': self.y_coordinate,
            'course_id': self.course_id,
            'embedding': self.embedding
        }


class Learner(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    registered_date = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(250))
    cgpa = db.Column(db.String(2))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'registered_date': self.registered_date.isoformat() if self.registered_date else None,
            'name': self.name,
            'cgpa': self.cgpa,
            'username': self.username,
            'password': self.password
        }


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250))
    description = db.Column(db.JSON)
    resources = db.relationship('Resource', backref='course', lazy=True)
    topics = db.relationship('Topic', backref='course', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'resources': [resource.to_dict() for resource in self.resources],
            'topics': [topic.to_dict() for topic in self.topics]
        }


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    type_id = db.Column(db.Integer)
    enroll_id = db.Column(db.Integer, db.ForeignKey('enroll.id'))
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'time': self.time.isoformat() if self.time else None,
            'type_id': self.type_id,
            'enroll_id': self.enroll_id,
            'resource_id': self.resource_id
        }


class Enroll(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    learner_id = db.Column(db.Integer, db.ForeignKey('learner.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    x_coordinate = db.Column(db.Float)
    y_coordinate = db.Column(db.Float)
    polyline = db.Column(db.JSON)
    contributions = db.relationship(
        'Contribution', backref='enroll', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'learner_id': self.learner_id,
            'course_id': self.course_id,
            'x_coordinate': self.x_coordinate,
            'y_coordinate': self.y_coordinate,
            'polyline': self.polyline,
            'contributions': [contribution.to_dict() for contribution in self.contributions]
        }


class Contribution(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    enroll_id = db.Column(db.Integer, db.ForeignKey('enroll.id'))
    submitted_on = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(1024))
    description = db.Column(db.JSON)
    prev_polyline = db.Column(db.JSON)
    polyline = db.Column(db.JSON)
    x_coordinate = db.Column(db.Float)
    y_coordinate = db.Column(db.Float)
    embedding = db.Column(db.JSON)

    def to_dict(self):
        return {
            'id': self.id,
            'enroll_id': self.enroll_id,
            'submitted_on': self.submitted_on.isoformat() if self.submitted_on else None,
            'file_path': self.file_path,
            'description': self.description,
            'prev_polyline': self.prev_polyline,
            'polyline': self.polyline,
            'x_coordinate': self.x_coordinate,
            'y_coordinate': self.y_coordinate,
            'embedding': self.embedding
        }


# Initialize database
with app.app_context():
    db.create_all()

# Routes

# Learners


@app.route('/learners', methods=['GET'])
def get_learners():
    learners = Learner.query.all()
    return jsonify([learner.to_dict() for learner in learners])


@app.route('/learners', methods=['POST'])
def create_learner():
    data = request.get_json()
    new_learner = Learner(
        name=data['name'],
        cgpa=data['cgpa'],
        username=data['username'],
        password=data['password']
    )
    db.session.add(new_learner)
    db.session.commit()
    return jsonify(new_learner.to_dict()), 201

# Courses


@app.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses])


@app.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    new_course = Course(
        name=data['name'],
        description=data['description']
    )
    db.session.add(new_course)
    db.session.commit()
    return jsonify(new_course.to_dict()), 201

# Resources


@app.route('/resources', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    return jsonify([resource.to_dict() for resource in resources])


@app.route('/resources', methods=['POST'])
def create_resource():
    data = request.get_json()
    new_resource = Resource(
        name=data['name'],
        description=data['description'],
        keywords=data['keywords'],
        polyline=data['polyline'],
        x_coordinate=data['x_coordinate'],
        y_coordinate=data['y_coordinate'],
        course_id=data['course_id'],
        type=data['type'],
        embedding=data['embedding']
    )
    db.session.add(new_resource)
    db.session.commit()
    return jsonify(new_resource.to_dict()), 201

# Topics


@app.route('/topics', methods=['GET'])
def get_topics():
    topics = Topic.query.all()
    return jsonify([topic.to_dict() for topic in topics])


@app.route('/topics', methods=['POST'])
def create_topic():
    data = request.get_json()
    new_topic = Topic(
        name=data['name'],
        description=data['description'],
        keywords=data['keywords'],
        polyline=data['polyline'],
        x_coordinate=data['x_coordinate'],
        y_coordinate=data['y_coordinate'],
        course_id=data['course_id'],
        embedding=data['embedding']
    )
    db.session.add(new_topic)
    db.session.commit()
    return jsonify(new_topic.to_dict()), 201

# Enrolls


@app.route('/enrolls', methods=['GET'])
def get_enrolls():
    enrolls = Enroll.query.all()
    return jsonify([enroll.to_dict() for enroll in enrolls])


@app.route('/enrolls', methods=['POST'])
def create_enroll():
    data = request.get_json()
    new_enroll = Enroll(
        learner_id=data['learner_id'],
        course_id=data['course_id'],
        x_coordinate=data['x_coordinate'],
        y_coordinate=data['y_coordinate'],
        polyline=data['polyline']
    )
    db.session.add(new_enroll)
    db.session.commit()
    return jsonify(new_enroll.to_dict()), 201

# Activities


@app.route('/activities', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([activity.to_dict() for activity in activities])


@app.route('/activities', methods=['POST'])
def create_activity():
    data = request.get_json()
    new_activity = Activity(
        time=datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S'),
        type_id=data['type_id'],
        enroll_id=data['enroll_id'],
        resource_id=data['resource_id']
    )
    db.session.add(new_activity)
    db.session.commit()
    return jsonify(new_activity.to_dict()), 201

# Contributions


@app.route('/contributions', methods=['GET'])
def get_contributions():
    contributions = Contribution.query.all()
    return jsonify([contribution.to_dict() for contribution in contributions])


@app.route('/contributions', methods=['POST'])
def create_contribution():
    data = request.get_json()
    new_contribution = Contribution(
        enroll_id=data['enroll_id'],
        submitted_on=datetime.strptime(
            data['submitted_on'], '%Y-%m-%d %H:%M:%S'),
        file_path=data['file_path'],
        description=data['description'],
        prev_polyline=data['prev_polyline'],
        polyline=data['polyline'],
        x_coordinate=data['x_coordinate'],
        y_coordinate=data['y_coordinate'],
        embedding=data['embedding']
    )
    db.session.add(new_contribution)
    db.session.commit()
    return jsonify(new_contribution.to_dict()), 201


if __name__ == '__main__':
    app.run(debug=True)
