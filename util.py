from flask import Flask, render_template,session,request, redirect, url_for
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os 
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = 'user-library-read'

def create_spotify_oauth():
    redirect_uri = url_for("redirect_page", _external=True)
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=redirect_uri,
        scope=SCOPE
    )



def get_token():
    # Retrieve the token info using the user's ID
    token_info = session.get("token_info")
    if not token_info:
        raise Exception(f"No token info found.")

    # Check if the token is expired
    now = time.time()
    is_expired = token_info["expires_at"] - now < 60
    if is_expired:
        print(f"Debug: Token expired for user. Refreshing token...")
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
        session["token_info"] = token_info 

    return token_info
