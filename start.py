import asyncio
import sys

try:
    from bot_configurator import start_bot
except Exception as e:
    print(f"ОШИБКА ПРИ ИМПОРТЕ: {e}", flush=True)
    sys.exit(1)

if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_bot(loop)
    except Exception as e:
        print(f"ОШИБКА ПРИ ЗАПУСКЕ: {e}", flush=True)
        sys.exit(1)
