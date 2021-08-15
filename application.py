import requests
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route("/")
def apple_root():
    api_url = "https://itunes.apple.com/lookup?id=487143&entity=song&limit=200"
    r = requests.get(api_url).json()

    del r['results'][0]
    track_array = []
    i = 0
    for res in r['results']:
        i += 1
        pink_floyd_data = {
            "num": i,
            "collectionName": res['collectionName'],
            "trackName": res['trackName'],
            "collectionPrice": res['collectionPrice'],
            "trackPrice": res['trackPrice'],
            "primaryGenreName": res['primaryGenreName'],
            "trackCount": res['trackCount'],
            "trackNumber": res['trackNumber'],
            "releaseDate": res['releaseDate'],
        }
        track_array.append(pink_floyd_data)

    return render_template("index.html", datas=track_array)


if __name__ == "__main__":
    app.debug = True
    app.run()
