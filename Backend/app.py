from flask import Flask, render_template, jsonify, send_from_directory
import pandas as pd

app = Flask(__name__)

# Read data from Excel file
excel_file = 'DM_Resource_Plot.xlsx'
df = pd.read_excel(excel_file)
excel_file = 'DM_learner_plot.xlsx'
df_learner = pd.read_excel(excel_file)

# Assuming your Excel file has columns 'x', 'y', and 'video_url'
scatterplot_data = df[['index','name', 'x', 'y', 'video_url']].to_dict(orient='records')
learner_data = df_learner[['index', 'resource_name', 'x', 'y', 'description']].to_dict(orient='records')


@app.route('/data')
def get_data():
    return jsonify(scatterplot_data)

@app.route('/new_positions')
def get_new_data():
    return jsonify(learner_data)


if __name__ == '__main__':
    app.run(debug=True)
