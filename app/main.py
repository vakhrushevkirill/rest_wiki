from flask import Flask, render_template, request, url_for, redirect, session, escape
from rest import RestApiWiki

app = Flask(__name__)
app.secret_key = 'sdasd'

rest_api_wiki = RestApiWiki()

@app.route('/', methods=['POST', 'GET'])
def main(requset_string=None):
    if request.method == 'POST':
        
        requset_string = request.form['text_request']
        session['requset_string'] = request.form['text_request']
        return redirect(url_for('answer'))
    
    return render_template('base.html', requset_string=requset_string)

@app.route('/answer', methods=['POST', 'GET'])
def answer():
    
    return rest_api_wiki.get(session.get('requset_string'))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)