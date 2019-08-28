from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return 'hey man!'


if __name__ == "__main__":
    app.run(port=7777)
