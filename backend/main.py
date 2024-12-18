from flask import Flask
from flask import render_template

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/test')
def test():
    return render_template('pages/test.html')



if __name__ == '__main__':
    app.run(debug=True)