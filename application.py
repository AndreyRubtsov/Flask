from flask import Flask,render_template
var1 = "Undrey"
var2 = "Test"
application = Flask(__name__)



@application.route("/")
def root():
    return render_template("index.html")


if __name__== "__main__":
    application.debug= True
    application.run()
