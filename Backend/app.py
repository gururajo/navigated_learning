from init import app, DBcreated
import pandas as pd
from flask import jsonify, request
from repository import create_Course, update_position
import modelsRoutes
# Read data from Excel file
excel_file = 'DM_Resource_Plot.xlsx'
df = pd.read_excel(excel_file)
excel_file = 'DM_learner_plot.xlsx'
df_learner = pd.read_excel(excel_file)

# Assuming your Excel file has columns 'x', 'y', and 'video_url'
scatterplot_data = df[['index', 'name', 'x',
                       'y', 'video_url']].to_dict(orient='records')
learner_data = df_learner[['index', 'resource_name',
                           'x', 'y', 'description']].to_dict(orient='records')

if DBcreated:
    print("creating the course")
    create_Course("Discreate Mathematics",
                  "this is the description of DM", None, None)


@app.route('/data')
def get_data():
    # print(cursor, dir(cursor))
    return jsonify(scatterplot_data)


@app.route('/new_positions')
def get_new_data():
    return jsonify(learner_data)


@app.route("/login", methods=['POST'])
def login_user():
    data = request.get_json()
    username = data["username"]
    password = data["password"]


@app.route("/submitsummary", methods=['POST'])
def get_new_postion():
    data = request.get_json()
    summary = data["summary"]
    enrollId = data["enroll_id"]
    courseId = data["course_id"]
    pos = update_position(summary, enrollId, courseId)
    return jsonify(pos), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, ssl_context='adhoc')
