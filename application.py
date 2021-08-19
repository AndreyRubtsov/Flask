import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def apple_root():
    con = psycopg2.connect(
        database="flask",
        user="undrey",
        password="1234asDF",
        host="3.15.200.187",
        port="5432"
    )
    cur = con.cursor()
    cur.execute('select * from pink_floyd_table;')
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

    if request.method == 'POST':
        if request.form.get('submit_b'):
            undrey_year=request.form.get('text_field')
            return render_template("index.html", year=undrey_year)
    return render_template("index.html", datas=track_array)


if __name__ == "__main__":
    app.debug = True
    app.run()
