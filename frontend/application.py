import psycopg2
import os
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def apple_root():
    con = psycopg2.connect(
        database=os.getenv('ENV_RDS_DB'),
        user=os.getenv('ENV_RDS_USER'),
        password=os.getenv('ENV_RDS_PASS'),
        host=os.getenv('ENV_RDS_HOST'),
        port="5432"
    )
    cur = con.cursor()
    cur.execute('select * from pink_floyd_table;')
    # select * from pink_floyd_table where DATE_PART('year', releasedate::date) = 1967;
    result = cur.fetchall()
    # con.close()
    track_array = []

    for res in result:
        pink_floyd_data = {
            "num": res[0],
            "kind": res[1],
            "collectionName": res[2],
            "trackName": res[3],
            "collectionPrice": res[4],
            "trackPrice": res[5],
            "primaryGenreName": res[6],
            "trackCount": res[7],
            "trackNumber": res[8],
            "releaseDate": res[9],
        }
        track_array.append(pink_floyd_data)

    if request.method == 'POST':
        if request.form.get('submit_b'):
            undrey_year = int(request.form.get('text_field'))

            # some test
            cur = con.cursor()
            cur.execute(
                f'select * from pink_floyd_table where DATE_PART(\'year\', releasedate::date) = {undrey_year} order by trackPrice desc;')
            result = cur.fetchall()
            con.close()
            track_array = []

            for res in result:
                pink_floyd_data = {
                    "num": res[0],
                    "kind": res[1],
                    "collectionName": res[2],
                    "trackName": res[3],
                    "collectionPrice": res[4],
                    "trackPrice": res[5],
                    "primaryGenreName": res[6],
                    "trackCount": res[7],
                    "trackNumber": res[8],
                    "releaseDate": res[9],
                }
                track_array.append(pink_floyd_data)

            return render_template("index.html", datas=track_array)
        if request.form.get('submit_c'):
            for i in range(0, 1000):
                #1000000 is too much
                n = 100000
                factorial = 1
                for i in range(2, n + 1):
                    factorial *= i
                print(factorial)
            return render_template("index.html", datas=track_array)
    return render_template("index.html", datas=track_array)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
