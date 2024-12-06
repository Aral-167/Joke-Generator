from flask import Flask, render_template_string
import requests

app = Flask(__name__)

# HTML template with embedded CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Joke Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        h1 {
            color: #333;
        }
        p {
            font-size: 1.5em;
            color: #555;
            margin: 20px 0;
        }
        button {
            background-color: #007BFF;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 1em;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #0056b3;
        }
        footer {
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }
    </style>
</head>
<body>
    <h1>Joke Generator</h1>
    <p>{{ joke }}</p>
    <form action="/" method="post">
        <button type="submit">Get a New Joke</button>
    </form>
    <footer>Powered by the <a href="https://official-joke-api.appspot.com/" target="_blank">Official Joke API</a></footer>
</body>
</html>
"""

def fetch_joke():
    """Fetch a random joke from the Official Joke API."""
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(url)
        response.raise_for_status()
        joke = response.json()
        return f"{joke['setup']} {joke['punchline']}"
    except requests.exceptions.RequestException:
        return "Oops! Couldn't fetch a joke right now. Try again later."

@app.route("/", methods=["GET", "POST"])
def index():
    joke = fetch_joke()
    return render_template_string(HTML_TEMPLATE, joke=joke)

if __name__ == "__main__":
    app.run(debug=True)
