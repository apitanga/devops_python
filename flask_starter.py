from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is a simple Flask app for DevOps use!"

if __name__ == '__main__':
    app.run(debug=True)
