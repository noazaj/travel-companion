from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the home page!'
    

if __name__ == '__main__':
    app.run(debug=True)