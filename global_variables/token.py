import os
import sys
from envparse import env
from vkbottle import API

if os.path.exists('.env'):
    env.read_envfile('.env')

# Выводим все переменные окружения для отладки
print("=== Переменные окружения ===", flush=True)
print(f"TOKEN задан: {'да' if os.environ.get('TOKEN') else 'НЕТ'}", flush=True)
print(f"POSTGRES_HOST: {os.environ.get('POSTGRES_HOST', 'НЕ ЗАДАН')}", flush=True)
print(f"POSTGRES_PORT: {os.environ.get('POSTGRES_PORT', 'НЕ ЗАДАН')}", flush=True)
print(f"POSTGRES_USER задан: {'да' if os.environ.get('POSTGRES_USER') else 'НЕТ'}", flush=True)
print(f"POSTGRES_DB: {os.environ.get('POSTGRES_DB', 'НЕ ЗАДАН')}", flush=True)
print(f"GROUP_ID: {os.environ.get('GROUP_ID', 'НЕ ЗАДАН')}", flush=True)
print("===========================", flush=True)

try:
    TOKEN = env.str('TOKEN')
    POSTGRES_HOST = env.str('POSTGRES_HOST', default='localhost')
    POSTGRES_PORT = env.str('POSTGRES_PORT', default='5432')
    POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD', default='')
    POSTGRES_USER = env.str('POSTGRES_USER')
    POSTGRES_DB = env.str('POSTGRES_DB')
    GROUP_ID = env.int('GROUP_ID')
except Exception as e:
    print(f"КРИТИЧЕСКАЯ ОШИБКА: переменная окружения не задана: {e}", flush=True)
    print("Проверь переменные окружения в панели bothost!", flush=True)
    sys.exit(1)

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db_auth_data = {
    'database': POSTGRES_DB,
    'user': POSTGRES_USER,
    'password': POSTGRES_PASSWORD,
    'host': POSTGRES_HOST,
    'port': POSTGRES_PORT
}

print(f"DATABASE URL: postgresql+asyncpg://{POSTGRES_USER}:***@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}", flush=True)

api = API(token=TOKEN)
