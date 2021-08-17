import requests
import psycopg2


def apple_getdata():
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
    cur.execute('CREATE TABLE pink_floyd_table (id serial PRIMARY KEY, kind varchar, collectionName varchar,'
                ' trackName varchar, collectionPrice varchar, trackPrice varchar, primaryGenreName varchar,'
                ' trackCount varchar, trackNumber varchar, releaseDate varchar);')
    con.commit()

    for res in r['results']:
        pink_floyd_data = {
            "kind": res['kind'],
            "collectionName": res['collectionName'],
            "trackName": res['trackName'],
            "collectionPrice": res['collectionPrice'],
            "trackPrice": res['trackPrice'],
            "primaryGenreName": res['primaryGenreName'],
            "trackCount": res['trackCount'],
            "trackNumber": res['trackNumber'],
            "releaseDate": res['releaseDate'],
        }
        cur.execute("INSERT INTO pink_floyd_table (kind, collectionName, trackName, collectionPrice, trackPrice, primaryGenreName, trackCount, trackNumber, releaseDate) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (res['kind'], res['collectionName'], res['trackName'], res['collectionPrice'], res['trackPrice'],
             res['primaryGenreName'], res['trackCount'], res['trackNumber'], res['releaseDate']))
        con.commit()

    con.close()

apple_getdata()
