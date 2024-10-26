import subprocess
from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

def get_figure_from_db(name):
    # Connect to the database
    conn = sqlite3.connect('historical_figures.db')
    cursor = conn.cursor()

    # Query the figures table for the figure's ID
    cursor.execute('SELECT id FROM figures WHERE name = ?', (name,))
    figure = cursor.fetchone()

    if figure:
        figure_id = figure[0]

        # Query the attributes table for this figure's attributes
        cursor.execute('SELECT attribute_name, attribute_value FROM attributes WHERE figure_id = ?', (figure_id,))
        attributes = cursor.fetchall()

        # Convert the attributes into a dictionary
        figure_data = {attr_name: attr_value for attr_name, attr_value in attributes}
        figure_data['name'] = name  # Include the name in the response
        return figure_data
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-historical-figure', methods=['POST'])
def get_historical_figure():
    data = request.get_json()
    query = data.get('query')  # e.g., "Albert Einstein"
    print(f'the data returned from prompt: {query}')
    
    # Step 1: Check if the figure is in the database
    figure_data = get_figure_from_db(query)
    
    if figure_data:
        print(f'the figure that retrieved from database: {figure_data}')

        response_data = {
            'name': figure_data.get('name', 'Undefined'),
            'born': figure_data.get('Born', 'Undefined'),
            'signature': figure_data.get('Signature', 'Undefined'),
            'attributes': {key: figure_data[key] for key in figure_data if key not in ['name', 'Born', 'signature']}
        }
        
        return jsonify(response_data)
    else:
        return jsonify({'error': 'Figure can not retrieve from the database'}), 404

    
    os.chdir('historical_figures')
    
    # Step 2: If not found, run the spider to fetch data
    process = subprocess.Popen(['scrapy', 'crawl', 'spider', '-a', f'figure_name={query}'])
    process.wait()  # Wait for the spider to complete

    # Step 3: Re-check the database after the spider completes
    figure_data = get_figure_from_db(query)
    
    if figure_data:
        return jsonify(figure_data)
    else:
        return jsonify({'error': 'Figure not found'}), 404
