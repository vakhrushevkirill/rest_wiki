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
    
    def __str__(self):
        return self.result.__dir__


class RequestToWiki():
    def __init__(self):
        self.rest_api_wiki_title = RestApiWiki(method='title')
        self.rest_api_wiki_summary = RestApiWiki(method='summary')
        self.index = 0
        self.list_level = []

    def get(self, request):
        self.result = self.rest_api_wiki_title.get_json(request)
        self.result.update(self.rest_api_wiki_summary.get_json(request))
        return self.result
    
    def get_level_list(self, request):
        self.get(request)
        level_one = []
        level_order = []
        for key in self.result:
            if isinstance(self.result[key], dict) or isinstance(self.result[key], list):
                level_order.append({key: self.result[key]})
            else:
                level_one.append({key: self.result[key]})
        
        self.list_level = [level_one]
        for lo in level_order:
            self.list_level.append(lo)
        return self.list_level

    def __len__(self):
        return len(self.list_level)

def recur_view(collect, keys_list):
    if isinstance(collect, dict):
        for key in collect:
            keys_list.append(key)
            recur_view(collect[key], keys_list)
    elif isinstance(collect, list):
        for item in collect:
            if isinstance(item, dict):
                recur_view(item, keys_list)


    """ for key in collect:
        print(key, ': ')
        input()
        if isinstance(collect[key], dict):
            recur_view(collect[key])
        if isinstance(collect[key], list):
            recur_view(collect[key]) """

    
if __name__ == "__main__":
    rq_to_wiki = RestApiWiki(method='title')
    test = rq_to_wiki.get_json('Звезда')
    keys_list = []
    recur_view(test, keys_list)
    print(keys_list)
    print(test)