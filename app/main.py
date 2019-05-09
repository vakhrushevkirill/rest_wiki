from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        print(request.form['text_request'])
    return render_template('base.html')



if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)