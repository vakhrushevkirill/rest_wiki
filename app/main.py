from flask import Flask, render_template, request, url_for, redirect, session, send_file
from rest import RequestToWiki, RestApiWiki
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

from office_save import Excel, Word

app = Flask(__name__)
app.secret_key = 'sdasd'

rq_to_wiki = RequestToWiki()


class Index:
    def __init__(self):
        self.i = 0
        self.i_max = 0

index = Index()

result_wiki = []


def DForm(kwargs):
    """Фабрика по созданию wtf на основе входных данных"""
    class StaticForm(FlaskForm):
        pass
    setattr(StaticForm, 'kwargs', kwargs)

    def is_dict(args, StaticForm):
        for key in args:
            if isinstance(key, dict):
                is_dict(key, StaticForm)
            elif isinstance(key, list):
                is_list(key, StaticForm)
            else:
                setattr(StaticForm, key, TextAreaField(
                key, 
                validators=[DataRequired()], 
                default=args[key]))

    def is_list(args, StaticForm):
        for item in args:
            if isinstance(item, dict):
                is_dict(item, StaticForm)
            elif isinstance(item, list):
                is_list(item, StaticForm)

    if isinstance(kwargs, list):
        is_list(kwargs, StaticForm)
    elif isinstance(kwargs, dict):
        is_dict(kwargs, StaticForm)
    return StaticForm()


@app.route('/', methods=['POST', 'GET'])
def main(requset_string=None):
    if request.method == 'POST':
        requset_string = request.form['text_request']
        session['requset_string'] = request.form['text_request']
        rq_to_wiki.get_level_list(request.form['text_request'])
        # Статус код 200 означает что запрос к rest api wiki был успешно обработан
        # во всех остальных случаях, предлагаем пользователю перейти на справку
        if rq_to_wiki.status_code != 200:
            label_code_error = rq_to_wiki.status_code
            return render_template(
                'index.html', 
                requset_string=requset_string, 
                label_code_error=label_code_error
                )
        else:
            return redirect(url_for('answer'))
    else:
        return render_template('index.html')

    return render_template('index.html', requset_string=requset_string)


@app.route('/answer', methods=['POST', 'GET'])
def answer():
    if (request.method == 'GET') and index.i == 0 and request.form.get('button') != 'Вернуться':
        level = rq_to_wiki.list_level[index.i]
        form = DForm(level)
        index.i_max = len(rq_to_wiki.list_level)
        return render_template(
            'answer.html',
            json_data=level,
            form=form,
            index=index.i,
            index_max=index.i_max
            )
    elif request.method == 'POST' and index.i >= 0 and index.i <= index.i_max-1:
        for key in request.form:
            if isinstance(rq_to_wiki.list_level[index.i], list):
                for item in rq_to_wiki.list_level[index.i]:
                    if isinstance(item, dict):
                        for key_item in item:
                            if key == key_item:
                                item[key_item] = request.form[key]
            elif isinstance(rq_to_wiki.list_level[index.i], dict):
                for item in rq_to_wiki.list_level[index.i]:
                    if isinstance(rq_to_wiki.list_level[index.i][item], list):
                        for value in rq_to_wiki.list_level[index.i][item]:
                            if isinstance(value, dict):
                                for key_value in value:
                                    if key == key_value:
                                        value[key_value] = request.form[key] 
                    elif isinstance(rq_to_wiki.list_level[index.i][item], dict):
                        for value in rq_to_wiki.list_level[index.i][item]:
                            if key == value:
                                rq_to_wiki.list_level[index.i][item][value] = request.form[key]
        if request.form.get('button') == 'Продолжить':
            index.i += 1
        elif request.form.get('button') == 'Вернуться':
            index.i -= 1
        level = rq_to_wiki.list_level[index.i]
        if isinstance(level, dict):
            for item in level:
                if isinstance(level[item], list):
                    level = level[item]
                else:
                    level = [level[item]]
        form = DForm(level)
        if request.form.get('button') == 'Сохранить Excel':
            print('sadasdas')
            ex = Excel(rq_to_wiki.list_level, session['requset_string'])
            return send_file(ex.filename, as_attachment=ex.title)
        if request.form.get('button') == 'Сохранить Word':
            wb = Word(rq_to_wiki.list_level, session['requset_string'])
            return send_file(wb.filename, as_attachment=wb.title)
        return render_template(
            'answer.html', 
            json_data=level, 
            form=form, 
            index=index.i, 
            index_max=index.i_max
            )
    else:
        return redirect(url_for('answer'))

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    # form = DForm(name='sdadas')
