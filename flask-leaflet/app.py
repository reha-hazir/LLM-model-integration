from flask import Flask, request, jsonify, render_template
import requests
import google.generativeai as genai

app = Flask(__name__)

# Serve the HTML page
@app.route('/')
def index():
    return render_template('map.html')

# Route to handle historical figure query
@app.route('/get-historical-figure', methods=['POST'])
def get_historical_figure():
    print("Received request for historical figure")  # Debugging statement
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        print("No query provided")  # Debugging statement
        return jsonify({'error': 'No query provided'}), 400
    
    figure_info = get_figure_info_from_gemini(query)
    
    if not figure_info:
        print("No figure info returned")  # Debugging statement
        return jsonify({'error': 'Could not retrieve figure info'}), 500
    
    location = get_figure_location(figure_info['name'])
    
    return jsonify({
        'name': figure_info['name'],
        'gender': figure_info['gender'],
        'birthDate': figure_info['birthDate'],
        'deathDate': figure_info['deathDate'],
        'ethnicity': figure_info['ethnicity'],
        'knownFor': figure_info['knownFor'],
        'location': location
    })

def get_figure_info_from_gemini(query):
    print(f"Querying Gemini with: {query}")
    model_name = "gemini-1.5-flash"
    response = requests.post(f"https://api.gemini.com/v1beta/models/{model_name}:generateText", json={
        'inputs': [{'text': query}],  # Update to fit the text generation format
        'temperature': 0.5
    }, headers={
        'Authorization': f'Bearer AIzaSyCT6_lgHBuU-jKIuz30DoIJI75ZKpOQ_uA'
    })

    print("Response received from Gemini API")  # Debugging statement
    result = response.json()
    print(result)  # Print the entire response for debugging

    # Handle the response accordingly
    if 'choices' in result and len(result['choices']) > 0:
        content = result['choices'][0]['message']['content'].strip()  # Get the response text

        # You may need to parse the content for structured data.
        # Here's an example of mock data; you can implement parsing logic here.
        if "Albert Einstein" in content:
            return {
                'name': "Albert Einstein",
                'gender': "Male",
                'birthDate': "March 14, 1879",
                'deathDate': "April 18, 1955",
                'ethnicity': "German",
                'knownFor': "Theory of Relativity"
            }

    return None  # Or handle the error appropriately

def get_figure_location(name):
    # Dummy location based on name (in a real app, use a database or API to get actual coordinates)
    locations = {
        'Albert Einstein': {'lat': 48.1351, 'lng': 11.5820},  # Munich, Germany
        'Cleopatra': {'lat': 31.2001, 'lng': 29.9187}         # Alexandria, Egypt
    }
    return locations.get(name, {'lat': 0, 'lng': 0})  # Default to [0, 0] if unknown

if __name__ == '__main__':
    app.run(debug=True)
