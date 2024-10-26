import json
import sqlite3

# Load data from JSON file
with open('app/einstein.json', 'r') as file:
    data = json.load(file)

# Connect to the database
conn = sqlite3.connect('historical_figures.db')
cursor = conn.cursor()

# Loop through each figure in the JSON data
for figure in data:
    # Insert the figure into the figures table
    cursor.execute('''
        INSERT INTO figures (name)
        VALUES (?)
    ''', (figure['name'],))

    # Retrieve the figure_id of the newly inserted figure
    figure_id = cursor.lastrowid

    # Insert each attribute into the attributes table
    for key, value in figure.items():
        # Skip inserting the figure name itself, since it's already in the figures table
        if key != 'name':
            cursor.execute('''
                INSERT INTO attributes (figure_id, attribute_name, attribute_value)
                VALUES (?, ?, ?)
            ''', (figure_id, key, value))

# Commit changes and close the connection
conn.commit()
conn.close()
