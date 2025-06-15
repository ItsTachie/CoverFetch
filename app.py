
from flask import Flask, render_template,session,request, redirect, url_for
from util import *

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path='/')
app.secret_key = os.urandom(24).hex() 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    session.clear()
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/redirect")
def redirect_page():
    sp_oauth = create_spotify_oauth()
    session.clear()  # Clear the session to avoid conflicts
    code = request.args.get("code")
    if not code:
        return "Authorization failed: No code provided.", 400

    # Get the access token
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        token_info = sp_oauth.get_access_token(code)

    # Store the token info with a unique key
    session['token_info'] = token_info
    return redirect(url_for("getImages", _external=True))

@app.route("/getImages")
def getImages():
    try:
        token_info = get_token()
        print(f"Debug: Token info retrieved")
    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for("login", _external=True))
    access_token = token_info if isinstance(token_info, str) else token_info['access_token']
    sp = spotipy.Spotify(auth=access_token)

    #list of dictionaries of album info
    albums = []
    limit = 50
    offset = 0

    while True:
        saved_albums = sp.current_user_saved_albums(limit=limit, offset=offset)
        if not saved_albums["items"]:
            break
        for item in saved_albums["items"]:
            album_info = item["album"]
            name = album_info["name"]
            artist = album_info["artists"][0]["name"]
            url = album_info["images"][0]["url"]
            album = {"name": name , "artist": artist, "image":url }
            albums.append(album)
        offset += limit

    # List files in the user's folder
    return render_template('download.html', albums=albums)

if __name__ == "__main__":
    app.run()

