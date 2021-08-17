import requests
import psycopg2

# connect to database
con = psycopg2.connect(
    database="flask",
    user="undrey",
    password="1234asDF",
    host="127.0.0.1",
    port="5432"
)

cur = con.cursor()

# creating table if not exit and erasing data
cur.execute(
    'CREATE TABLE IF NOT EXISTS pink_floyd_table (id serial PRIMARY KEY, kind varchar, collectionName varchar,'
    ' trackName varchar, collectionPrice varchar, trackPrice varchar, primaryGenreName varchar,'
    ' trackCount varchar, trackNumber varchar, releaseDate varchar);')
cur.execute('TRUNCATE TABLE pink_floyd_table RESTART IDENTITY;')
con.commit()

undrey_list = []
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
            undrey_list.append(res)

test = []
print(undrey_list)
for a in undrey_list:
    if a not in test:
        test.append(a)

print(len(test))

for res in test:
    cur.execute(
        'INSERT INTO pink_floyd_table (kind, collectionName, trackName, collectionPrice, trackPrice, primaryGenreName, trackCount, trackNumber, releaseDate) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        (res['kind'], res['collectionName'], res['trackName'], res['collectionPrice'], res['trackPrice'],
         res['primaryGenreName'], res['trackCount'], res['trackNumber'], res['releaseDate']))
    con.commit()

con.close()
