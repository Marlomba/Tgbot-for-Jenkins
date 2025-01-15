import telebot
import datetime
import requests
import base64
import json

bot = telebot.TeleBot("8049413383:AAFDAzfhxicB_sTeSVXVSGAKkmT34v-ScxU")
JENKINS_URL = "http://87.251.78.132:8081/api/python?tree=jobs[name,builds[number,result,timestamp,duration,fullDisplayName]]"
JENKINS_USERNAME = "admin"
JENKINS_PASSWORD = "ggWk8b-U_SmD"


def get_jenkins_data():
    """Получает данные из Jenkins API."""
    try:
        auth_string = f"{JENKINS_USERNAME}:{JENKINS_PASSWORD}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        headers = {"Authorization": f"Basic {encoded_auth}"}
        response = requests.get(JENKINS_URL, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Ошибка при запросе к Jenkins: {e}"}


def format_build_info(build):
    """Форматирует информацию о сборке."""
    timestamp = datetime.datetime.fromtimestamp(build['timestamp'] / 1000).strftime(
        '%Y-%m-%d %H:%M:%S') if 'timestamp' in build else 'Неизвестно'
    duration = str(datetime.timedelta(milliseconds=build['duration'])) if 'duration' in build else 'Неизвестно'
    result = build.get('result', 'Неизвестно')
    full_display_name = build.get('fullDisplayName', 'Неизвестно')
    number = build.get('number', 'Неизвестно')

    return (f"   - Сборка №: {number}\n"
            f"     Статус: {result}\n"
            f"     Название: {full_display_name}\n"
            f"     Время начала: {timestamp}\n"
            f"     Продолжительность: {duration}")


def format_jenkins_data(data):
    """Форматирует данные из Jenkins для вывода в Telegram."""
    if "error" in data:
        return data["error"]

    output_text = ""
    for job in data.get('jobs', []):
        output_text += f"<b>Проект:</b> {job['name']}\n"
        if 'builds' in job and job['builds']:
            for build in job['builds']:
                output_text += format_build_info(build) + "\n"
        else:
            output_text += "   Сборок нет.\n"
        output_text += "------------------------\n"
    if not output_text:
        output_text = "Нет данных для отображения."
    return output_text


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет! Я бот, который может показать данные из Jenkins. Используй команду /jenkins, чтобы увидеть информацию.")


@bot.message_handler(commands=['jenkins'])
def send_jenkins_info(message):
    jenkins_data = get_jenkins_data()
    formatted_data = format_jenkins_data(jenkins_data)
    bot.send_message(message.chat.id, formatted_data, parse_mode="HTML")


if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)