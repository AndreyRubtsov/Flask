import requests
import psycopg2
from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def apple_root():
    # connect to database
    con = psycopg2.connect(
        database= os.getenv('ENV_RDS_DB'),
        user=os.getenv('ENV_RDS_USER'),
        password=os.getenv('ENV_RDS_PASS'),
        host=os.getenv('ENV_RDS_HOST'),
        port="5432"
    )
    cur = con.cursor()

    # creating table if not exit and erasing data
    cur.execute(
        'CREATE TABLE IF NOT EXISTS pink_floyd_table (id serial PRIMARY KEY, kind varchar, collectionName varchar,'
        ' trackName varchar, collectionPrice varchar, trackPrice varchar, primaryGenreName varchar,'
        ' trackCount varchar, trackNumber varchar, releaseDate timestamp);')
    cur.execute('TRUNCATE TABLE pink_floyd_table RESTART IDENTITY;')
    con.commit()

    # get raw data to a list
    raw_list = []

    # search video
    api_url = "https://itunes.apple.com/lookup?id=487143&entity=musicVideo&limit=200"
    r = requests.get(api_url).json()
    del r['results'][0]
    for res in r['results']:
        if res['artistName'] == 'Pink Floyd':
            if 'trackNumber' not in res:
                res['trackNumber'] = 'No Data'
            if 'collectionPrice' not in res:
                res['collectionPrice'] = 'No Data'
            if 'collectionName' not in res:
                res['collectionName'] = 'No Data'
            if 'trackPrice' not in res:
                res['trackPrice'] = 'No Data'
            if 'trackCount' not in res:
                res['trackCount'] = 'No Data'
            if 'releaseDate' not in res:
                res['releaseDate'] = 'No Data'
            raw_list.append(res)

    # search albums but maybe not necessary
    api_url = "https://itunes.apple.com/lookup?id=487143&entity=album&limit=200"
    r = requests.get(api_url).json()
    del r['results'][0]
    for res in r['results']:
        if res['artistName'] == 'Pink Floyd':
            if 'trackNumber' not in res:
                res['trackNumber'] = 'No Data'
            if 'collectionPrice' not in res:
                res['collectionPrice'] = 'No Data'
            if 'trackName' not in res:
                res['trackName'] = 'No Data'
            if 'trackPrice' not in res:
                res['trackPrice'] = 'No Data'
            if 'kind' not in res:
                res['kind'] = 'album'
            raw_list.append(res)

    for offset in range(0, 6000, 200):
        api_url = f'https://itunes.apple.com/search?term=pink+floyd&limit=200&offset={offset}'
        r = requests.get(api_url).json()
        for res in r['results']:
            if res['artistName'] == 'Pink Floyd':
                if 'trackNumber' not in res:
                    res['trackNumber'] = 'No Data'
                if 'collectionPrice' not in res:
                    res['collectionPrice'] = 'No Data'
                if 'trackPrice' not in res:
                    res['trackPrice'] = 'No Data'
                raw_list.append(res)

    # removing duplicates
    clear_list = []
    for a in raw_list:
        if a not in clear_list:
            clear_list.append(a)

    # inserting data to a table
    for res in clear_list:
        cur.execute(
            'INSERT INTO pink_floyd_table (kind, collectionName, trackName, collectionPrice, trackPrice, primaryGenreName, trackCount, trackNumber, releaseDate) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (res['kind'], res['collectionName'], res['trackName'], res['collectionPrice'], res['trackPrice'],
             res['primaryGenreName'], res['trackCount'], res['trackNumber'], res['releaseDate']))
        con.commit()
    con.close()
    return "works!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')