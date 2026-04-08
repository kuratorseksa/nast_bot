import asyncio
import sys
import os
from bot_configurator import start_bot

# Защита от двойного запуска
lock_file = '/tmp/nast_bot.lock'
if os.path.exists(lock_file):
    print("Бот уже запущен! Выход.")
    sys.exit(1)

with open(lock_file, 'w') as f:
    f.write(str(os.getpid()))

try:
    if __name__ == "__main__":
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_bot(loop)
finally:
    # Удаляем lock-файл при завершении
    if os.path.exists(lock_file):
        os.remove(lock_file)
