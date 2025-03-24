from atlassian import Confluence
import logging

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Функция получения информации о странице (дата создания изменения)
def get_confluence_page_details(url, username, password, page_title, space_key):
    """
    Получает детали страницы Confluence.

    :param url: URL Confluence (например, 'https://your-domain.atlassian.net/wiki')
    :param username: Ваш email для входа в Atlassian
    :param api_token: API токен (сгенерируйте в настройках Atlassian)
    :param page_title: Название страницы
    :param space_key: Ключ пространства (например, 'SD')
    :return: Словарь с данными страницы или None в случае ошибки
    """
    try:
        # Инициализация клиента Confluence
        confluence = Confluence(url=CONFLUENCE_URL, username=username, password=password, verify_ssl=False)

        # Поиск страницы по названию
        page = confluence.get_page_by_title(space=space_key, title=page_title)
        if not page:
            logging.error(f"Страница '{page_title}' не найдена в пространстве '{space_key}'")
            return None

        # Получение расширенных данных
        page_id = page['id']
        page_info = confluence.get_page_by_id(
            page_id,
            expand='history,version,metadata.labels'
        )

        # Извлечение данных
        created_date = page_info['history']['createdDate']
        created_by = page_info['history']['createdBy']['displayName']
        modified_date = page_info['version']['when']
        modified_by = page_info['version']['by']['displayName']
        labels = [label['name'] for label in page_info['metadata']['labels']['results']]

        return {
            'page_title': page_title,
            'created_date': created_date,
            'created_by': created_by,
            'modified_date': modified_date,
            'modified_by': modified_by,
            'labels': labels
        }

    except Exception as e:
        logging.error(f"Ошибка: {str(e)}")
        return None


# Пример использования
if __name__ == "__main__":
    # Замените параметры на свои
    CONFLUENCE_URL = ""
    USERNAME = ""
    PASSWORD = ""
    PAGE_TITLE = ""
    SPACE_KEY = ""
    verify_ssl = False

    page_details = get_confluence_page_details(
        CONFLUENCE_URL,
        USERNAME,
        PASSWORD,
        PAGE_TITLE,
        SPACE_KEY
    )

    if page_details:
        print(f"Детали страницы: {page_details['page_title']}")
        print(f"Создана: {page_details['created_date']} пользователем {page_details['created_by']}")
        print(f"Последнее изменение: {page_details['modified_date']} пользователем {page_details['modified_by']}")
        print(f"Метки: {', '.join(page_details['labels']) if page_details['labels'] else 'Нет меток'}")
