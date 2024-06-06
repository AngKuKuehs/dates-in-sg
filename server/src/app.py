# TODO: Validate add/update against schema
"""
Loads the app.
"""

from flask import Flask

app = Flask(__name__)
from routes import app

@app.route("/", methods=["GET"])
def default_route():
    """
    Returns a string
    """
    return "Landing page for to-do-list project"

if __name__ == "__main__":
    app.run(debug=False)
