import requests


class RestApiWiki:
    """Класс реализует взаимодействие с rest api русской версии сайта wikipedia\n
        Справка по методам доступа к api на странице Wikipedia\n
        https://en.wikipedia.org/api/rest_v1/#/Page%20content/get_page_metadata__title_ \n
        :param method: метод запроса"""
    string_request_summary = 'https://ru.wikipedia.org/api/rest_v1/page/summary/{}'
    string_request_title = 'https://en.wikipedia.org/api/rest_v1/page/title/{}'
    def __init__(self, method='summary'):
        self.method = method
    
    def _get(self, request):
        if self.method == 'summary':
            result = requests.get(self.string_request_summary.format(request))
            self.status_code = result.status_code
            return result
        elif self.method == 'title':
            result = requests.get(self.string_request_title.format(request))
            self.status_code = result.status_code
            return result
        else:
            return None
    
    def get_json(self, request):
        self.result = self._get(request)
        if self.result is not None:
            return self.result.json()

    def clipping(self):
        temp_dict = self.result.json()
    
    def __str__(self):
        return self.result.__dir__

def reqursiv_dict(rec):
    if isinstance(rec, dict):
        for item in rec:
            print(item, ': ', rec[item])
            reqursiv_dict(rec[item])
    elif isinstance(rec, list):
        for item in rec:
            print(item)
            reqursiv_dict(item)

    
if __name__ == "__main__":
    rest_api_wiki_title = RestApiWiki(method='title')
    rest_api_wiki_summary = RestApiWiki()
    result = rest_api_wiki_title.get_json('Звезда')
    result.update(rest_api_wiki_summary.get_json('Звезда'))
    # print(result)
    reqursiv_dict(result)
