from flask import Flask, render_template, request, url_for, redirect, session, escape
from rest import RequestToWiki

app = Flask(__name__)
app.secret_key = 'sdasd'

rq_to_wiki = RequestToWiki()

@app.route('/', methods=['POST', 'GET'])
def main(requset_string=None):
    if request.method == 'POST':
        requset_string = request.form['text_request']
        session['requset_string'] = request.form['text_request']
        return redirect(url_for('answer'))
    
    return render_template('index.html', requset_string=requset_string)

@app.route('/answer', methods=['POST', 'GET'])
def answer():
    wiki = 'wiki'
    result_wiki = rq_to_wiki.get(session['requset_string'])
    print(result_wiki)
    return render_template('answer.html', result_wiki=result_wiki)



if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)