from bs4 import BeautifulSoup


class RequestResult:
    SUCCESS = 0
    LOAD_ERROR = 1
    PARSE_ERROR = 2
    TOWN_NOT_FOUND = 3

    def __init__(self, code: int, result: str = None):
        self.code = code
        self.result = result


def fetch_temperature(city: str):
    pass


def _load_page():
    '''
    Либо возвращает страницу в виде строки, либо None, что ознает
    ошибку загрузки (например, в следствие отсутствия интернета);
    в этом методе не обрабатывается ошибка, когда город не найден
    '''
    pass


def _check_city_is_found(page: str):
    'Проверяет, что успешно загруженная страница не содержит ошибки 404'
    pass


def _extract_temperature_from_page(page: str):
    '''
    Извлекает значение температуры из корректной старницы; может вернуть
    ошибку PARSE_ERROR только в том случае, если накосячил программист,
    или при изменении формата html-страницы
    '''
    pass
