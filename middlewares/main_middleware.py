import os
from vkbottle import BaseMiddleware
from vkbottle.bot import Message
from global_variables.variables import predsed_team_ids

# Список всех админских команд
ADMIN_COMMANDS = {
    'Админ-панель', 'Страйки', 'Выдать страйк', 'Убрать страйк',
    'Матрица компетенций', 'Активность', 'Ответственность',
    'Соблюдение правил', 'Взаимодействия', 'Доп комментарий',
    'Отметить отсутствующих', 'Кикнуть дауна', 'Загрузить календарь',
    'Домашка', 'Поставить дедлайн', 'Выгрузить домашку', 'Топы',
    'По возрастанию', 'По убыванию'
}


class NoBotMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        if self.event.from_id < 0:
            self.stop("Groups are not allowed to use bot")


class AdminMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        # Проверяем только если сообщение — админская команда
        if self.event.text.lower().strip() not in ADMIN_COMMANDS:
            return None

        if self.event.from_id in predsed_team_ids:
            return None

        await self.event.answer("Нельзя тебе сюда!")
        self.stop(f'vk_id: {self.event.from_id} пытался попасть в Админ-панель')
