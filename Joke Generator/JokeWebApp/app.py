from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# HTML template with enhanced UI features
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Joke Generator</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            text-align: center;
            background: url('https://source.unsplash.com/1920x1080/?nature,light') no-repeat center center fixed;
            background-size: cover;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: #333;
            text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
            transition: background-color 0.3s ease;
        }
        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.5);
            z-index: -1;
            transition: background-color 0.3s ease;
        }
        .container {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            width: 90%;
            transition: all 0.3s ease;
        }
        h1 {
            color: #32cd32; /* Lime Green */
        }
        p {
            font-size: 1.5em;
            margin: 20px 0;
            transition: opacity 0.3s ease;
        }
        .button-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            margin-top: 20px;
        }
        button {
            background-color: #32cd32; /* Lime Green */
            color: #fff;
            border: none;
            padding: 10px 20px;
            font-size: 1em;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        button:focus {
            outline: 2px solid #fff;
        }
        button:hover {
            background-color: #228b22; /* Forest Green */
            transform: scale(1.05);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
        }
        #jokeButton {
            font-weight: bold; /* Added this line to make the text bold */
        }
        footer {
            margin-top: 20px;
            font-size: 0.9em;
            color: #666;
        }
        footer a {
            color: #32cd32; /* Lime Green */
            text-decoration: none;
        }
        footer a:hover {
            text-decoration: underline;
        }
        .error {
            color: red;
            font-size: 1.2em;
            margin-top: 20px;
        }
        .history, .favorites {
            margin-top: 20px;
            font-size: 1em;
            color: #666;
            display: none;
            list-style-type: disc; /* Added bullet points */
            padding-left: 20px; /* Added padding to align bullets */
        }
        .history p, .favorites p {
            margin: 5px 0;
        }
        .dark-mode {
            background-color: #121212; /* Dark background */
            color: #fff;
        }
        .dark-mode .overlay {
            background-color: rgba(0, 0, 0, 0.7); /* Darker overlay */
        }
        .dark-mode .container {
            background-color: rgba(34, 34, 34, 0.9); /* Darker container */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        }
        .dark-mode button {
            background-color: #444; /* Darker button */
            color: #fff;
        }
        .dark-mode button:hover {
            background-color: #666; /* Darker hover button */
        }
        .dark-mode footer a {
            color: #32cd32; /* Keep link color same */
        }
        .spinner {
            display: none;
            border: 4px solid rgba(0, 0, 0, 0.1);
            border-left-color: #32cd32;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    <script>
        let jokeHistory = [];
        let favoriteJokes = [];
        let darkMode = false;

        async function fetchJoke() {
            const jokeElement = document.getElementById('joke');
            const errorElement = document.getElementById('error');
            const buttonElement = document.getElementById('jokeButton');
            const historyElement = document.getElementById('history');
            const spinnerElement = document.getElementById('spinner');

            jokeElement.style.opacity = '0';
            errorElement.style.display = 'none';
            buttonElement.disabled = true;
            spinnerElement.style.display = 'block';

            try {
                const response = await fetch('/joke');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                jokeElement.textContent = `${data.setup} ${data.punchline}`;
                jokeElement.style.opacity = '1';
                jokeHistory.push(jokeElement.textContent);
                updateHistory(historyElement);
            } catch (error) {
                errorElement.textContent = "Oops! Couldn't fetch a joke right now. Try again later.";
                errorElement.style.display = 'block';
            } finally {
                buttonElement.disabled = false;
                spinnerElement.style.display = 'none';
            }
        }

        function updateHistory(historyElement) {
            historyElement.innerHTML = '<h3>Joke History</h3>';
            jokeHistory.forEach(joke => {
                const jokeItem = document.createElement('p');
                jokeItem.textContent = joke;
                historyElement.appendChild(jokeItem);
            });
        }

        function toggleHistory() {
            const historyElement = document.getElementById('history');
            if (historyElement.style.display === 'none' || historyElement.style.display === '') {
                historyElement.style.display = 'block';
            } else {
                historyElement.style.display = 'none';
            }
        }

        function addFavorite() {
            const jokeElement = document.getElementById('joke');
            const favoritesElement = document.getElementById('favorites');
            const jokeText = jokeElement.textContent;

            if (!favoriteJokes.includes(jokeText)) {
                favoriteJokes.push(jokeText);
                updateFavorites(favoritesElement);
            } else {
                alert("This joke is already in your favorites!");
            }
        }

        function updateFavorites(favoritesElement) {
            favoritesElement.innerHTML = '<h3>Favorite Jokes</h3>';
            favoriteJokes.forEach(joke => {
                const jokeItem = document.createElement('p');
                jokeItem.textContent = joke;
                favoritesElement.appendChild(jokeItem);
            });
        }

        function toggleFavorites() {
            const favoritesElement = document.getElementById('favorites');
            if (favoritesElement.style.display === 'none' || favoritesElement.style.display === '') {
                favoritesElement.style.display = 'block';
            } else {
                favoritesElement.style.display = 'none';
            }
        }

        function toggleDarkMode() {
            const bodyElement = document.body;
            darkMode = !darkMode;
            if (darkMode) {
                bodyElement.classList.add('dark-mode');
            } else {
                bodyElement.classList.remove('dark-mode');
            }
        }
    </script>
</head>
<body>
    <div class="overlay"></div>
    <div class="container" role="main">
        <h1>Joke Generator</h1>
        <p id="joke" aria-live="polite">{{ joke }}</p>
        <p id="error" class="error"></p>
        <div class="spinner" id="spinner"></div>
        <div class="button-container">
            <button onclick="toggleHistory()" aria-label="Toggle joke history" title="Toggle joke history">Joke History</button>
            <button id="jokeButton" onclick="fetchJoke()" aria-label="Get a new joke" title="Get a new joke">Get a New Joke</button>
            <button onclick="addFavorite()" aria-label="Add to favorites" title="Add to favorites">Add to Favorites</button>
            <button onclick="toggleFavorites()" aria-label="Toggle favorite jokes" title="Toggle favorite jokes">Favorite Jokes</button>
            <button onclick="toggleDarkMode()" aria-label="Toggle dark mode" title="Toggle dark mode">Dark Mode</button>
        </div>
        <div id="history" class="history"></div>
        <div id="favorites" class="favorites"></div>
        <footer>Powered by the <a href="https://official-joke-api.appspot.com/" target="_blank">Official Joke API</a></footer>
    </div>
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
        return joke
    except requests.exceptions.RequestException:
        return None

@app.route("/", methods=["GET"])
def index():
    joke = fetch_joke()
    joke_text = f"{joke['setup']} {joke['punchline']}" if joke else "Oops! Couldn't fetch a joke right now. Try again later."
    return render_template_string(HTML_TEMPLATE, joke=joke_text)

@app.route("/joke", methods=["GET"])
def get_joke():
    joke = fetch_joke()
    if joke:
        return joke
    else:
        return {"error": "Could not fetch joke"}, 500

if __name__ == "__main__":
    app.run(debug=True)
