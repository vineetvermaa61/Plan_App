# app.py
import os
import io
import tempfile
from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL, IMAGE_SIZES, SECRET_KEY
from PIL import Image
import tweepy

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Home page – shows Twitter login and the upload form.
@app.route('/')
def index():
    twitter_logged_in = 'access_token' in session and 'access_token_secret' in session
    return render_template('index.html', twitter_logged_in=twitter_logged_in)

# Route to start the Twitter (X) OAuth flow.
@app.route('/login')
def login():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)
    try:
        redirect_url = auth.get_authorization_url()
        # Store the request token in session
        session['request_token'] = auth.request_token
        return redirect(redirect_url)
    except tweepy.TweepError:
        flash("Error! Failed to get request token.")
        return redirect(url_for('index'))

# OAuth callback route – Twitter redirects here after login.
@app.route('/callback')
def twitter_callback():
    request_token = session.get('request_token')
    if request_token is None:
        flash("Missing request token.")
        return redirect(url_for('index'))
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    try:
        auth.get_access_token(verifier)
        # Store access tokens in session
        session['access_token'] = auth.access_token
        session['access_token_secret'] = auth.access_token_secret
        flash("Successfully authenticated with Twitter!")
    except tweepy.TweepError:
        flash("Error! Failed to get access token.")
    return redirect(url_for('index'))

# Route to handle image upload, processing, and posting to Twitter.
@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        flash("No file part in the request.")
        return redirect(url_for('index'))
    file = request.files['image']
    if file.filename == '':
        flash("No file selected.")
        return redirect(url_for('index'))
    
    # Validate file extension.
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        flash("Unsupported file type.")
        return redirect(url_for('index'))
    
    # Open the image using Pillow.
    try:
        img = Image.open(file.stream)
    except Exception as e:
        flash("Error processing image: " + str(e))
        return redirect(url_for('index'))
    
    # Resize the image to each configured dimension.
    resized_images = {}
    for size_label, dimensions in IMAGE_SIZES.items():
        try:
            # Use LANCZOS filter instead of ANTIALIAS for high-quality downsampling.
            resized_img = img.resize(dimensions, Image.LANCZOS)
            # Save the resized image to a BytesIO object.
            img_io = io.BytesIO()
            resized_img.save(img_io, format='PNG')
            img_io.seek(0)
            resized_images[size_label] = img_io
        except Exception as e:
            flash(f"Error resizing image for {size_label}: " + str(e))
            return redirect(url_for('index'))

    
    # Ensure the user is authenticated with Twitter.
    if 'access_token' not in session or 'access_token_secret' not in session:
        flash("Please log in with Twitter to publish images.")
        return redirect(url_for('index'))
    
    # Set up the Twitter API client.
    access_token = session['access_token']
    access_token_secret = session['access_token_secret']
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    media_ids = []
    try:
        # For each resized image, save temporarily and upload to Twitter.
        for label, img_io in resized_images.items():
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp:
                temp.write(img_io.read())
                temp.flush()
                media = api.media_upload(temp.name)
                media_ids.append(media.media_id_string)
            # Reset BytesIO pointer (if needed)
            img_io.seek(0)
        
        # Compose a tweet that attaches all four images.
        tweet_text = "Automated image upload with multiple sizes: " + ", ".join(IMAGE_SIZES.keys())
        api.update_status(status=tweet_text, media_ids=media_ids)
        flash("Images have been successfully posted to your Twitter account!")
    except Exception as e:
        flash("Error posting images to Twitter: " + str(e))
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
