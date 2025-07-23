from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    # You can change these options easily from Python
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
