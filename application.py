import requests
import psycopg2
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def apple_root():
    api_url = "https://itunes.apple.com/lookup?id=487143&entity=song&limit=200"
    r = requests.get(api_url).json()

    del r['results'][0]

    con = psycopg2.connect(
        database="flask",
        user="undrey",
        password="1234asDF",
        host="3.15.200.187",
        port="5432"
    )
    cur = con.cursor()
    cur.execute('CREATE TABLE pink_floyd_table (id serial PRIMARY KEY, num integer, collectionName varchar,'
                ' trackName varchar, collectionPrice varchar, trackPrice varchar, primaryGenreName varchar,'
                ' trackCount varchar, trackNumber varchar, releaseDate varchar);')
    con.commit()


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
        cur.execute("INSERT INTO pink_floyd_table (num, collectionName, trackName, collectionPrice, trackPrice, primaryGenreName, trackCount, trackNumber, releaseDate) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (i, res['collectionName'], res['trackName'],res['collectionPrice'],res['trackPrice'],res['primaryGenreName'],res['trackCount'],res['trackNumber'],res['releaseDate']))
        con.commit()
        track_array.append(pink_floyd_data)
    con.close()
    return render_template("index.html", datas=track_array)


if __name__ == "__main__":
    app.debug = True
    app.run()
