# config.py
import os

# Twitter API keys (set these as environment variables or replace with your keys)
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
# This is the callback URL you registered in your Twitter developer app
CALLBACK_URL = os.environ.get("CALLBACK_URL", "http://localhost:5000/callback")

# Predefined (but configurable) image sizes.
IMAGE_SIZES = {
    "300x250": (300, 250),
    "728x90": (728, 90),
    "160x600": (160, 600),
    "300x600": (300, 600)
}

# Secret key for Flask sessions (replace with a secure key or set as an environment variable)
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")
