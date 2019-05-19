Основными целями тестового задания считаю следущее:
1) Выбрать существующий REST API для наибольшей практической ценности.
2) Научиться обрабатывать разнородные json структуры.
3) Реализовать редактирование json в не зависимости от его содержания и структуры.
4) Как следствие из пункта 3, следует иметь возможность создавать набор текстовых полей исходя их структуры самого json.
5) Изменения текстовых полей должны хранится в области рабочей памяти разрабатываемого веб-клиента.
6) Движение по набору текстовых полей должны осуществляться по модели двухсвязного списка.
7) Отредактированный json необходимо сохранять либо в как word, либо как excel документы, при чем созданые документы должны уничтожаться, после того как перестанут быть нужны.
8) Раскрыть понятия итераторов и генераторов на примере языка программирования Python.

Список используемых фреймворков для выполнения настоящего тестового задания находится в файле requirements.txt.
Выполнение тестового задания осуществлялось с помощью инетрпритатора Python 3.6.7
Все используемые пакеты были установлены при помощи виртуального окружения в папке venv

Команда для запуска виртуального окружения.
source venv/bin/activate

Запуск веб клиента выполняется из папки app командой
python3 main.py

Обоснование решения.
Используемые фреймворки:
- Flask - микрофреймворк для создания вебсайтов на языке программирования Python. Данный фреймворк был выбран в качестве минималистичного решения предложенной задачи.
- Flask-WTF - расширение WTForm для интеграции с jinja, предоставляющий набор инструментов для создания и обработки веб-форм.
- Requests - наиболее популярное и простое решение для работы с http.
- Openpyxl - пожалуй мой самый любимый фреймворк, неоднократно выручавший меня в вооруженных силах. Позволяет организовать удобную и понятную работу с excel-документами.
- Python-docx - решение для создания word-документов.

Проектные решения как ответы на поставленные цели.
1) В качестве используемого REST API был выбран всем известный сервис Wikipedia, предлагающий обширную документация по API.
https://en.wikipedia.org/api/rest_v1/.

Выбор API Wikipedia обусловлен так же тем, что настоящий проект можно расширить для генерации конспектов по одному лишь запросу к сервису. Практическая ценность для определенной аудитории очевидна.

2) В качестве обработки json струкур в исходном коде вы уведите множество реализаций рекурсивного перехода по структурам, в зависимости от того что представляет из себя поле: словарь или список.

3) Реализация отображения и редактирования json была реализована не по уровням вложенности, а по внутренним словарям, где каждый словарь сам по себе является конечной логической единицей. Количество создаваемых блоков может разнится в зависимости от запросов. При смене блока, новая информация записывается в json непосредственно из генерированных форм. Локализация названия полей не была реализована, так как это все пока еще тестовое задание.

4) Создание самих текстовых полей тесно переплетается со структурой получаемого json. Для каждого конечного блока реализуется свой набор текстовых полей, основываясь на ключах, как на метках, и на значениях, как на отображаемой и редактируемой информацией.

5) Для наглядности и простоты исполнения было решено хранить полученный json непосредственно в оперативной памяти, вместо сохранения его на физической памяти в качестве файла с последующей его обработкой, используя итераторы.

6) Для реализации перемещения по json структуре был создан класс-синглтон, эмулирующий курсор по списку блоков.

7) Сохранение json в форматы office осуществляется при помощи соответствующих фреймворков и созданных на их основе классов, предлагающих оговоренный ранее блочный вывод. Описанные классы реализуют уничтожение созданных файлов при помощи "сборщика мусора", переопределив метод __del__

8) Итераторы и генераторы раскрываются в модуле iterAndGen.py.

По наиболее значимым моментам пояснения приведены в исходном коде проекта.

Благодарю за интересное задание и Ваше терпение. В независимости от результатов искренне надеюсь на объективное ревью.