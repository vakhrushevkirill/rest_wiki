from flask import Flask, render_template, request, url_for, redirect, session
from rest import RequestToWiki

app = Flask(__name__)
app.secret_key = 'sdasd'

rq_to_wiki = RequestToWiki()
global index_to_wiki
index_to_wiki = 0
result_wiki = []

@app.route('/', methods=['POST', 'GET'])
def main(requset_string=None):
    if request.method == 'POST':
        requset_string = request.form['text_request']
        session['requset_string'] = request.form['text_request']
        return redirect(url_for('answer'))

    return render_template('index.html', requset_string=requset_string)

def view(view_l):
    html_templ="""
    {% extends "answer.html" %}
    {% block view %}
    """
    if isinstance(view_l, dict):
        for item in view_l:
            if isinstance(view_l[item],dict):
                html_templ += """<h3>{}</h3>""".format(item)
                for 

    html_templ += """{% endblock %}"""


# @app.route('/answer/<int:index_to_wiki>', methods=['POST', 'GET'])
@app.route('/answer', methods=['POST', 'GET'])
def answer():

    if request.method == 'GET' and rq_to_wiki.index == 0:
        rq_to_wiki.get_level_list(session['requset_string'])
        rq_to_wiki.index += 1
        return render_template('answer.html', 
            index=rq_to_wiki.index, 
            result_wiki=rq_to_wiki.list_level[rq_to_wiki.index])
    elif request.method == 'GET' and rq_to_wiki.index > 0 and rq_to_wiki.index < (len(rq_to_wiki) -1) and request.args.get('action') == 'Продолжить':
        print(rq_to_wiki.list_level)
        rq_to_wiki.index += 1
        return render_template('answer.html', 
            index=rq_to_wiki.index, 
            result_wiki=rq_to_wiki.list_level[rq_to_wiki.index])
    elif request.method == 'GET' and rq_to_wiki.index >= 2 and rq_to_wiki.index <= len(rq_to_wiki) and request.args.get('action') == 'Вернуться':
        print(rq_to_wiki.list_level)
        rq_to_wiki.index -= 1
        return render_template('answer.html', 
            index=rq_to_wiki.index, 
            result_wiki=rq_to_wiki.list_level[rq_to_wiki.index])
    else:
        return render_template('answer.html', 
            index=rq_to_wiki.index, 
            result_wiki=rq_to_wiki.list_level[rq_to_wiki.index])

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
