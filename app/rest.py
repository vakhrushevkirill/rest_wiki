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
        request = request.replace(' ', '_')
        self.result = self._get(request)
        if self.result is not None:
            return self.result.json()

    def clipping(self):
        temp_dict = self.result.json()
    
    def __str__(self):
        return self.result.__dir__


class RequestToWiki():
    def __init__(self):
        self.rest_api_wiki_title = RestApiWiki(method='title')
        self.rest_api_wiki_summary = RestApiWiki(method='summary')

    def get(self, request):
        self.result = self.rest_api_wiki_title.get_json(request)
        self.result.update(self.rest_api_wiki_summary.get_json(request))
        return self.result
    
    def get_list(self, request):
        self.result = self.rest_api_wiki_title.get_json(request)
        self.result.update(self.rest_api_wiki_summary.get_json(request))
        list_json_level = [[]]
        return self.get_rec(self.result, list_json_level)
    


def reqursiv_dict(rec):
    for key in rec:
        print('Stack', key, ': ', rec[key])
        if isinstance(rec[key], dict):
            reqursiv_dict(rec[key])

def get_level_list(rec):
    level_one = []
    level_order = []
    for key in rec:
        if isinstance(rec[key], dict) or isinstance(rec[key], list):
            level_order.append({key: rec[key]})
        else:
            level_one.append({key: rec[key]})
    return level_one, level_order
    
if __name__ == "__main__":
    rq_to_wiki = RequestToWiki()
    get_rq = rq_to_wiki.get('Война и мир')
    # print(get_rq)
    level_one, level_order = get_level_list(get_rq)
    list_level = [level_one]

    for lo in level_order:
        list_level.append(lo)
    print(list_level)
     
    # print(requr_list(get_rq, temp=[[]], index=0))
