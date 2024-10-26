import sqlite3
from flask import jsonify

def dataRetrieval(name):
    conn = sqlite3.connect("historical_figures.db")
    cursor = conn.cursor()

    # Query to fetch all figures from the figures table
    cursor.execute("SELECT id FROM figures WHERE name = ?", (name,))
    figure = cursor.fetchone()

    if figure:
        figure_id = figure[0]

        cursor.execute('SELECT attribute_name, attribute_value FROM attributes WHERE figure_id = ? ', (figure_id,))
        attributes = cursor.fetchall()

        figure_data = {attr_name: attr_value for attr_name, attr_value in attributes}
        figure_data['name'] = name

    return figure_data


def get_historical_figure(name):
    x = dataRetrieval(name)
    
    if x:
        return jsonify(x)

y = get_historical_figure("Albert Einstein")

print(y)
