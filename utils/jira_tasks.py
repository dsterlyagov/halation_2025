import logging
import json
from datetime import datetime, timedelta
from atlassian import Confluence, Jira

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def get_confluence_pages(confluence, space_key):
    """
    Получает все страницы из указанного пространства в Confluence.
    """
    try:
        pages = confluence.get_all_pages_from_space(space_key, start=0, limit=100)
        return pages
    except Exception as e:
        logging.error(f"Ошибка при получении страниц Confluence: {e}")
        return []


def get_jira_issues(jira, project_key, start_date, end_date):
    """
    Получает информацию о задачах в Jira за определенный период.
    """
    try:
        jql = f'project = {project_key} AND created >= "{start_date}" AND created <= "{end_date}"'
        issues = jira.jql(jql).get('issues', [])
        issues_data = []

        for issue in issues:
            print(issue)
            print('====1==============')
            # print(issue['fields']['reporter'])
            # print('====2==============')
            # print(issue['fields'])
            # print('====3==============')
            issue_data = {
                'key': issue['key'],
                'summary': issue['fields'].get('summary', 'Нет данных'),
                'issue_type': issue['fields']['issuetype']['name'],
                'assignee': issue['fields'],
                'created_date': issue['fields'].get('created', 'Нет данных'),
                'updated_date': issue['fields'].get('updated', 'Нет данных'),
                'subtasks': [subtask['key'] for subtask in issue['fields'].get('subtasks', [])],
            }
            issues_data.append(issue_data)
        # print(issues_data)

        return issues_data
    except Exception as e:
        logging.error(f"Ошибка при получении задач Jira: {e}")
        return []

def save_data_to_file(data, filename):
    """
    Сохраняет данные в JSON-файл.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Данные успешно сохранены в {filename}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении данных в файл: {e}")

# Данные для подключения
CONFLUENCE_URL = ""
JIRA_URL=''
USERNAME = ""
PASSWORD = ""
SPACE_KEY = ""
PROJECT_KEY = ""

# Определение периода сбора данных
DAYS_BACK = 30  # Количество дней в прошлом, за которые собираем данные
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=DAYS_BACK)).strftime('%Y-%m-%d')

# Инициализация клиентов
#confluence = Confluence(url=CONFLUENCE_URL, username=USERNAME, password=PASSWORD, verify_ssl=False)
jira = Jira(url=JIRA_URL, username=USERNAME, password=PASSWORD, verify_ssl=False)

# Получение данных
#confluence_pages = get_confluence_pages(confluence, SPACE_KEY)
jira_issues = get_jira_issues(jira, PROJECT_KEY, start_date, end_date)

# Сохранение в отдельные файлы
#save_data_to_file(confluence_pages, "confluence_data.json")
save_data_to_file(jira_issues, "jira_data.json")