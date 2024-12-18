from flask import Flask
from flask import render_template
from flask import request


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

@app.route('/services')
def services():
    return render_template('pages/services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        print(name)
        email = request.form['email']
        print(email)
        message = request.form['message']
        print(message)
        with open('contacted.txt', 'a') as file:
            file.write(f"Name: {name}\n")
            file.write(f"Email: {email}\n")
            file.write(f"Message: {message}\n")
            file.write("\n")
        return render_template('pages/home.html')
    return render_template('pages/contact.html')



if __name__ == '__main__':
    app.run(debug=True)