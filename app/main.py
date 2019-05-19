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
            # Сознательно ограничиваем создание формы, дабы не усложнять вывод
            # if isinstance(args[key], dict):
            #     is_dict(args[key], StaticForm)
            # elif isinstance(args[key], list):
            #     is_list(args[key], StaticForm)
            # else:
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


def init():
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


def accept_changes(rq_lv_index, form):
    """Перезапись данных из формы"""
    def is_dict(kwargs, form, key_form):
        for key in kwargs:
            if isinstance(kwargs[key], list):
                is_list(kwargs[key], form, key_form)
            elif isinstance(kwargs[key], dict):
                is_dict(kwargs[key], form, key_form)
            else:
                if key == key_form:
                    kwargs[key] = form[key_form] 

    def is_list(args, form, key_form):
        for item in args:
            if isinstance(item, dict):
                is_dict(item, form, key_form)
            elif isinstance(item, list):
                is_list(item, form, key_form)

    for key in form:
        if isinstance(rq_lv_index, list):
            is_list(rq_lv_index, form, key)
        elif isinstance(rq_lv_index, dict):
            is_dict(rq_lv_index, form, key)


def check_level(level):
    # Необходимое зло. Тут мы привязанны к DBForm и сознательно оборачиваем каждый уровень в словарь.
    # Как исправить знаю, но я уже и так потратил достаточно Вашего времени.
    if isinstance(level, dict):
        for item in level:
            if isinstance(level[item], list):
                level = level[item]
                print(level)
            else:
                level = [level[item]]
    return level

@app.route('/answer', methods=['POST', 'GET'])
def answer():
    if (request.method == 'GET' and 
        index.i == 0 and 
        request.form.get('button') != 'Вернуться'):
        return init()
    elif request.method == 'POST' and index.i >= 0 and index.i <= index.i_max-1:
        accept_changes(rq_to_wiki.list_level[index.i], request.form)              
        if request.form.get('button') == 'Продолжить':
            index.i += 1
        elif request.form.get('button') == 'Вернуться':
            index.i -= 1
        level = rq_to_wiki.list_level[index.i]
        level = check_level(level)
        form = DForm(level)
        if request.form.get('button') == 'Сохранить Excel':
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
