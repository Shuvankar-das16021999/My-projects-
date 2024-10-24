import os
from flask import Flask, render_template, request
from google.cloud import aiplatform
import requests
import json

# Replace with your GCP project ID and service account key path
os.environ["GOOGLE_CLOUD_PROJECT"] = "your-project-id"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account.json"

app = Flask(__name__)

def generate_sky_view(location, orientation):
    """Generates a sky view using the Gemini API based on location and orientation."""

    client = aiplatform.gapic.EndpointServiceClient()
    endpoint_id = "your-endpoint-id"  # Replace with your endpoint ID

    prompt = f"Generate a detailed sky view for location {location} with camera orientation {orientation}."

    request = aiplatform.gapic.PredictRequest(
        endpoint=client.endpoint_path(project="your-project-id", location="your-location", endpoint=endpoint_id),
        instances=[{"text": prompt}]
    )

    response = client.predict(request)
    generated_text = response.results[0].text

    return generated_text

@app.route("/", methods=["GET", "POST"])
def index():
    countries = ["USA", "Canada", "UK", "Australia", "India"]  # Add more countries as needed
    states = {
        "USA": ["California", "New York", "Texas", "Florida"],
        "Canada": ["Ontario", "Quebec", "British Columbia", "Alberta"],
        # Add more states for other countries
    }

    if request.method == "POST":
        country = request.form["country"]
        state = request.form["state"]
        location = f"{country}, {state}"
        orientation = request.form["orientation"]
        generated_text = generate_sky_view(location, orientation)
        return render_template("index.html", generated_text=generated_text, countries=countries, states=states, selected_country=country, selected_state=state)
    else:
        return render_template("index.html", countries=countries, states=states)

if __name__ == "__main__":
    app.run()