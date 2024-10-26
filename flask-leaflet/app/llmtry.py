from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Serve the HTML page
@app.route('/')
def index():
    return render_template('map.html')

# Route to handle historical figure query
@app.route('/get-historical-figure', methods=['POST'])
def get_historical_figure():
    data = request.get_json()
    query = data.get('query')

    # Make an API request to ChatGPT (or another NLP model)
    figure_info = get_figure_info_from_gpt(query)

    # Assuming you have a way to fetch location coordinates (e.g., birth place)
    location = get_figure_location(figure_info['name'])

    # Return the information and location
    return jsonify({
        'name': figure_info['name'],
        'gender': figure_info['gender'],
        'birthDate': figure_info['birthDate'],
        'deathDate': figure_info['deathDate'],
        'ethnicity': figure_info['ethnicity'],
        'knownFor': figure_info['knownFor'],
        'location': location  # latitude and longitude
    })

def get_figure_info_from_gpt(query):
    # Call OpenAI API or any GPT-based API here
    # For example, using OpenAI's API:
    response = requests.post('https://api.openai.com/v1/chat/completions', json={
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': query}],
        'temperature': 0.5
    }, headers={
        'Authorization': f'Bearer sk-oaud7nWM0bnj8omujC0qKG0Ac7x9g1Pm4W-o92SYS-T3BlbkFJ5YrnJqBtbHMvh84eEP95KlEq4kReSXXEJOM7lelPIA'
    })

    result = response.json()
    print(result)

def get_figure_location(name):
    # Dummy location based on name (in a real app, use a database or API to get actual coordinates)
    locations = {
        'Albert Einstein': {'lat': 48.1351, 'lng': 11.5820},  # Munich, Germany
        'Cleopatra': {'lat': 31.2001, 'lng': 29.9187}         # Alexandria, Egypt
    }
    return locations.get(name, {'lat': 0, 'lng': 0})  # Default to [0, 0] if unknown

if __name__ == '__main__':
    app.run(debug=True)
