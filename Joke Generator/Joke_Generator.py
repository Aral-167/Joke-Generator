import tkinter as tk
import requests

def fetch_joke():
    """Fetch a random joke from the Official Joke API."""
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(url)
        response.raise_for_status()
        joke = response.json()
        joke_text = f"{joke['setup']}\n\n{joke['punchline']}"
    except requests.exceptions.RequestException as e:
        joke_text = "Oops! Couldn't fetch a joke right now. Try again later."
    joke_label.config(text=joke_text)

# Create the main window
app = tk.Tk()
app.title("Joke Generator")

# Create a label to display the joke
joke_label = tk.Label(app, text="Click the button to get a joke!", wraplength=400, justify="center", font=("Arial", 14))
joke_label.pack(pady=20)

# Create a button to fetch a new joke
joke_button = tk.Button(app, text="Get a Joke", command=fetch_joke, font=("Arial", 12), bg="#add8e6")
joke_button.pack(pady=10)

# Run the application
app.mainloop()
