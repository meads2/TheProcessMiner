from flask import Flask

app = Flask(__name__)


@app.route("/")
def root():
    return {"message": "Hello World"}


@app.route("/<process>")
def proc(process):
    return {"message": "Hello World",
            "process": f"{process}"}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)