import os

from dotenv import load_dotenv
from telethon import TelegramClient, events
import logging
import json
import requests

load_dotenv()

# Логирование
logging.basicConfig(level=logging.INFO)

# Данные для подключения
api_id = int(os.environ.get("TG_BOT_API_ID"))
api_hash = os.environ.get("TG_BOT_API_HASH")
bot_token = os.environ.get("TG_BOT_TOKEN")

# Инициализация клиента с уникальным именем сессии
client = TelegramClient('session_name', api_id, api_hash)  

# Храним ID пользователей, которые подписались на уведомления
subscribed_users = set()

# Храним известных участников группы
known_members = set()

# Путь к файлу, в который будем записывать информацию
json_file_path = 'new_members.json'

# URL API для отправки данных
api_url = os.environ.get("TG_BOT_SERVER_API_CREATE_URL")


# Функция для отправки данных на API
def send_to_api(data):
    try:
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            logging.info(f"Данные успешно отправлены на API.")
        else:
            logging.error(f"Ошибка при отправке данных на API: {response.status_code}")
    except Exception as e:
        logging.error(f"Ошибка при отправке данных на API: {e}")


# Функция для записи информации в JSON файл
def update_json(data):
    try:
        # Проверяем, существует ли файл, если нет, создаём его
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                members = json.load(f)
        except FileNotFoundError:
            members = []

        # Добавляем нового участника
        members.append(data)

        # Записываем обновленные данные обратно в файл
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(members, f, ensure_ascii=False, indent=4)

        # Отправляем данные на API
        send_to_api(data)

        logging.info(f"Информация о пользователе добавлена в {json_file_path} и отправлена на API.")

    except Exception as e:
        logging.error(f"Ошибка при обновлении файла: {e}")


# Функция для отправки информации о новом участнике
async def notify_new_member(new_member_id, chat_id, action_type):
    user = await client.get_entity(new_member_id)
    print()
    user_info = (
        f"🔹 Новый участник!\n\n"
        f"👤 Имя: {user.first_name}\n"
        f"👤 Фамилия: {user.last_name if user.last_name else 'Нет'}\n"
        f"🆔 ID: {user.id}\n"
        f"💾 Тэг: @{user.username if user.username else 'Нет'}"
    )
    
    if action_type == "added":
        logging.info(f"Новый участник: {user_info}")
    elif action_type == "left":
        user_info = f"🔹 Пользователь покинул группу:\n\n{user_info}"
        logging.info(f"Пользователь покинул группу: {user_info}")
    
    # Обновляем JSON файл с информацией о пользователе
    user_data = {
        'first_name': user.first_name,
        'last_name': user.last_name if user.last_name else 'Нет',
        'user_tag': f'@{user.username}' if user.username else 'Нет',
        'user_id': user.id,
        'group_id': chat_id
    }
    update_json(user_data)

    # Отправка информации всем подписанным пользователям
    for user_id in subscribed_users:
        try:
            await client.send_message(user_id, user_info)
            logging.info(f"Отправлено пользователю {user_id}")
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")


# Обработчик для отслеживания вступления и выхода участников из группы
@client.on(events.ChatAction)
async def chat_action(event):
    if event.user_added:  # Проверяем, что это новый участник
        new_member_id = event.user_id
        chat_id = event.chat_id
        
        if new_member_id not in known_members:
            # Если участник новый, отправляем сообщение подписанным пользователям
            await notify_new_member(new_member_id, chat_id, "added")

            # Добавляем нового участника в список известных
            known_members.add(new_member_id)
    
    elif event.user_left:  # Проверяем, что участник покинул группу
        user_left_id = event.user_id
        chat_id = event.chat_id
        await notify_new_member(user_left_id, chat_id, "left")
        
        # Удаляем пользователя из списка известных, если он покинул группу
        if user_left_id in known_members:
            known_members.remove(user_left_id)


# Команда для подписки на уведомления
@client.on(events.NewMessage(pattern='/start'))
async def start(message):
    user_id = message.sender_id
    if user_id not in subscribed_users:
        subscribed_users.add(user_id)
        await message.reply("Вы успешно подписались на уведомления о новых участниках!")
        logging.info(f"Пользователь {user_id} подписался на уведомления.")
    else:
        await message.reply("Вы уже подписаны на уведомления!")


async def get_group_id(group_name):
    # Получаем информацию о группе по имени
    entity = await client.get_entity(group_name)
    # Получаем ID группы
    print(f"ID группы {group_name}: {entity.id}")


# Запуск клиента
async def main():
    await client.start(bot_token=bot_token) 
    print("Бот запущен...")
    await client.run_until_disconnected()


client.loop.run_until_complete(main())
