import logging
import setting
from pymongo import MongoClient
from bs4 import BeautifulSoup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, CallbackQuery
from aiogram.utils import executor
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.callback_data import CallbackData
import requests


TOKEN = setting.token
admin_chat_id = setting.admin_chat_id
priem_chat_id = setting.priem_chat_id
cluster = MongoClient(setting.mongo)

# Подключаемся к БД
db = cluster["Ded_Moroz_Data"]
# Подключаемся к таблице(коллекции)
workers = db["Bots_Data"]

# Создаём бота
bot = Bot(token=TOKEN)
# Присваиваем хранилище переменной storage, оно нам понадобится позже.
storage = MemoryStorage()
# Создаём диспетчер с аргументами bot и storage
dp = Dispatcher(bot, storage=storage)
# Добавляем встроенную миддлварь для удобного логгирования
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

# Пропишем простую клавиатуру Зарегистрироваться из одной кнопки
reg_button = KeyboardButton("📩 Забронировать дату визита")
reg_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
reg_keyboard.add(reg_button)



# Пропишем простую клавиатуру Отмена из одной кнопки
cancel_button = KeyboardButton("❌ Отменить бронирование")

cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_keyboard.add(cancel_button)

# Пропишем простую клавиатуру Пропустить из одной кнопки
next_button = KeyboardButton("❎ Пропустить")
next_button2 = KeyboardButton("❌ Отменить бронирование")
next_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
next_keyboard.add(next_button)
next_keyboard.add(next_button2)

# Пропишем клавиатуру для Комментариев
next_com_button = KeyboardButton("❎ Пропустить комментарий")
next_com_button2 = KeyboardButton("❌ Отменить бронирование")
next_com_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
next_com_keyboard.add(next_com_button)
next_com_keyboard.add(next_com_button2)

# Пропишем даты календаря
date_button22 = KeyboardButton("22.12.2022")
date_button23 = KeyboardButton("23.12.2022")
date_button24 = KeyboardButton("24.12.2022")
date_button25 = KeyboardButton("25.12.2022")
date_button26 = KeyboardButton("26.12.2022")
date_button27 = KeyboardButton("27.12.2022")
date_button28 = KeyboardButton("28.12.2022")
date_button29 = KeyboardButton("29.12.2022")
date_button30 = KeyboardButton("30.12.2022")
date_button31 = KeyboardButton("31.12.2022")
date_button01 = KeyboardButton("01.01.2023")
date_button02 = KeyboardButton("02.01.2023")
date_button03 = KeyboardButton("03.01.2023")
date_button04 = KeyboardButton("04.01.2023")
date_button05 = KeyboardButton("05.01.2023")
date_button06 = KeyboardButton("06.01.2023")
date_button07 = KeyboardButton("07.01.2023")
date_button08 = KeyboardButton("08.01.2023")
date_button09 = KeyboardButton("09.01.2023")
date_button10 = KeyboardButton("10.01.2023")
date_button11 = KeyboardButton("11.01.2023")
date_button12 = KeyboardButton("12.01.2023")
date_button13 = KeyboardButton("13.01.2023")
date_button14 = KeyboardButton("14.01.2023")

date_button_cancel = KeyboardButton("❌ Отменить бронирование")

date_button = ReplyKeyboardMarkup(resize_keyboard=True)
date_button.add(date_button_cancel)


date_button.add(date_button22, date_button23, date_button24)
date_button.add(date_button25, date_button26, date_button27)
date_button.add(date_button28, date_button29, date_button30)
date_button.add(date_button31)
date_button.add(date_button01, date_button02, date_button03)
date_button.add(date_button04, date_button05, date_button06)
date_button.add(date_button07, date_button08, date_button09)
date_button.add(date_button10, date_button11, date_button12)
date_button.add(date_button13, date_button14)
date_button.add()


# Пропишем время
time_button1 = KeyboardButton("C 10:00 до 12:00")
time_button2 = KeyboardButton("C 12:00 до 14:00")
time_button3 = KeyboardButton("C 14:00 до 16:00")
time_button4 = KeyboardButton("C 16:00 до 18:00")
time_button5 = KeyboardButton("C 18:00 до 20:00")
time_button6 = KeyboardButton("C 20:00 до 22:00")
time_button_cancel = KeyboardButton("❌ Отменить бронирование")

time_button = ReplyKeyboardMarkup(resize_keyboard=True)
time_button.add(date_button_cancel)
time_button.add(time_button1, time_button2, time_button3,)
time_button.add(time_button4, time_button5, time_button6,)
time_button.add()

# Пропишем инлайн клавиатуру для чата админов
# Задаём параметры Callback данных
reg_callback = CallbackData("reg", "status", "chat_id", "nick", "date_z", "name_c")


# Оборачиваем клаву в функцию, чтобы было удобнее использовать.
def inline(chat_id, nick, date_z, name_c):
    confirm = InlineKeyboardButton(
        text="✅ Одобрить",
        callback_data=reg_callback.new(
            status="1", chat_id=chat_id, nick=nick, date_z=date_z, name_c=name_c
        ),
    )
    cancel = InlineKeyboardButton(
        text="❌ Отклонить",
        callback_data=reg_callback.new(
            status="0", chat_id=chat_id, nick="-", date_z="-", name_c="-"
        ),
    )
    conf_inline = InlineKeyboardMarkup()
    conf_inline.insert(confirm).insert(cancel)
    return conf_inline

## Отмена заявки
def inline2(chat_id, nick, date_z, name_c):
    cancel = InlineKeyboardButton(
        text="❌ Отменить бронирование",
        callback_data=reg_callback.new(
            status="00", chat_id=chat_id, nick="-", date_z="-", name_c="-"
        ),
    )
    conf_inline = InlineKeyboardMarkup()
    conf_inline.insert(cancel)
    return conf_inline

## Отмена заявки
def inline3(chat_id, nick, date_z, name_c):
    cancel = InlineKeyboardButton(
        text="❌ Отменить бронирование",

    )
    conf_inline = InlineKeyboardMarkup()
    conf_inline.insert(cancel)
    return conf_inline

# Создаём класс, передаём в него StatesGroup, он нам понадобится, чтобы провести юзера через анкету
# и сохранить каждый ответ. Если кто-то хочет почитать поподробнее, загуглите "aiogram машина состояний"
class Anketa(StatesGroup):
    # внутри объявляем Стейты(состояния), далее мы будем вести пользователя по цепочке этих стейтов
    date_z = State()
    timer_r = State()
    model_r = State()
    name_c = State()
    date_r = State()
    nomer_ts = State()
    comments = State()
    text = State()

@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):

        await bot.send_message(
            message.chat.id,
            f"<b>Приветствую Вас, {message.from_user.username}!</b>\n\n"
            f"Чтобы забронировать визит Деда Мороза, нажмите кнопку \n👇\n<b>✉ Забронировать дату визита</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=reg_keyboard,
        )

@dp.message_handler(Text(equals="/instagram"), state="*")
async def problem(message: types.Message, state: FSMContext):
    await bot.send_message(
        message.chat.id,
        f"<b>👉 Это наш Instagram:</b>\nhttps://instagram.com/idedmoroz",
        parse_mode=ParseMode.HTML,
    )

@dp.message_handler(Text(equals="/whatsapp"), state="*")
async def problem(message: types.Message, state: FSMContext):
    await bot.send_message(
        message.chat.id,
        f"<b>👉 Это чат с нами: https://bit.ly/3vd8ubW</b>\nЕсть впорос? Напишите нам!",
        parse_mode=ParseMode.HTML,
    )

@dp.message_handler(Text(equals="/site"), state="*")
async def problem(message: types.Message, state: FSMContext):
    await bot.send_message(
        message.chat.id,
        f"<b>👉 Это наш сайт: https://github.com/Casqeaux</b>\nЗаходите к нам!",
        parse_mode=ParseMode.HTML,
    )

@dp.message_handler(Text(equals="/date"), state="*")
async def problem(message: types.Message, state: FSMContext):
    await bot.send_message(
        message.chat.id,
        f"<b>👉 Это таблица дат: https://bit.ly/3Wg2AD3</b>\nСвободные даты и время для бронирования",
        parse_mode=ParseMode.HTML,
    )

@dp.message_handler(Text(equals="❌ Отменить бронирование"), state="*")
async def menu_button(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(
        message.chat.id,

        f"<b>🎯 Регистрация заявки на визит Деда Мороза отменена, {message.from_user.username}!</b>\n\n"
        f"Чтобы забронировать визит Деда Мороза на дом, нажмите кнопку \n👇\n<b>✉ Забронировать дату визита</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=reg_keyboard,

    )

@dp.message_handler(Text(equals="❎ Пропустить"))
async def menu_button(message: types.Message, state: FSMContext):
    await bot.send_message(
        message.chat.id, "Пропускаем"
    )

# Теперь пропишем цепочку хэндлеров для анкеты
@dp.message_handler(Text(equals="📩 Забронировать дату визита"), state="*")
async def date_z(message: types.Message, state: FSMContext):
    await bot.send_message(
        message.chat.id,
        f"<b>Дата(дд.мм.гг):</b>\n\n"
        f"🔔 Выберите дату из списка или введите свою дату \n\n ❌ Важно! Если нужная дата (кнопка с датой отсутствует), значит день уже расписан!",
        parse_mode=ParseMode.HTML,
        reply_markup=date_button
    )

    # Переходим на следующий стейт
    await Anketa.date_z.set()
@dp.message_handler(state=Anketa.date_z, content_types=types.ContentTypes.TEXT)
async def timer_r(message: types.Message, state: FSMContext):
    # Записываем ответ в storage
    await state.update_data(date_z=message.text)
    await bot.send_message(
        message.chat.id,
        f"<b>Выберите временной интервал визита Деда Мороза:</b>\n\n"
        f"🔔 У нас временной интервал. Временной интервал прибытия 2 часа",
         parse_mode=ParseMode.HTML,
         reply_markup=time_button
    )
    await Anketa.timer_r.set()

#дата ремонта
@dp.message_handler(state=Anketa.timer_r, content_types=types.ContentTypes.TEXT)
async def model_r(message: types.Message, state: FSMContext):
    # Записываем ответ в storage
    await state.update_data(timer_r=message.text)
    await bot.send_message(
        message.chat.id, "<b>Ваше имя:\n 🔔 Как к Вам можно обращаться?</b>", reply_markup=cancel_keyboard, parse_mode=ParseMode.HTML,
    )
    await Anketa.model_r.set()

#время ремонта
@dp.message_handler(state=Anketa.model_r, content_types=types.ContentTypes.TEXT)
async def name_c(message: types.Message, state: FSMContext):
    # Записываем ответ в storage
    await state.update_data(model_r=message.text)
    await bot.send_message(
        message.chat.id, "<b>Введите Ваш номер телефона:\n 🔔 Можете указать номер WhatsApp, Viber, Telegram\n\nНапример:\n +7 777 777 777 если можно по WhatsApp</b>", reply_markup=cancel_keyboard, parse_mode=ParseMode.HTML,
    )

    await Anketa.nomer_ts.set()

    @dp.message_handler(state=Anketa.nomer_ts, content_types=types.ContentTypes.TEXT)
    async def comments(message: types.Message, state: FSMContext):
        # Записываем ответ в storage
        await state.update_data(nomer_ts=message.text)
        await bot.send_message(
            message.chat.id, "<b>Ваш эмират: \n 🔔 Укажите пожалуйста Эмират где будет проходить мероприятие.</b>",
            reply_markup=cancel_keyboard,
            parse_mode=ParseMode.HTML
        )

        await Anketa.comments.set()

#сообщение
@dp.message_handler(state=Anketa.comments, content_types=types.ContentTypes.TEXT)
async def text(message: types.Message, state: FSMContext):
    # Записываем ответ в storage
    await state.update_data(name_c=message.text)
    await bot.send_message(
        message.chat.id, "<b>Комментарий:\n 🔔 Можете указать Ваши пожелания, дополнительную информацию</b>",
        reply_markup=next_com_keyboard,
        parse_mode=ParseMode.HTML
    )

    await Anketa.text.set()


@dp.message_handler(state=Anketa.text, content_types=types.ContentTypes.TEXT)
async def confirmation(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await bot.send_message(
        message.chat.id, "✅ Заявка на визит успешно заполнена и отправлена!\n\n Мы с Вами свяжемся!",
        reply_markup=reg_keyboard,

    )

    # Insert БД
    workers.insert_one(
        {
            "Дата": data.get("date_z"),
            "Время": data.get("timer_r"),
            "Имя": data.get("model_r"),
            "Номер телефона": data.get("nomer_ts"),
            "Эмират": data.get("name_c"),
            "Комментарий": data.get("text"),
        }
    )
    # Отправляем сообщение в чат админов с анкетой и добавляем 2 инлайн кнопки с callback данными
    await bot.send_message(
        admin_chat_id,
        f"<b>Поступила заявка от</b> @{message.from_user.username}\n\n"
        f'<b>Дата:</b> {data.get("date_z")}\n'
        f'<b>Время:</b> {data.get("timer_r")}\n\n'
        f'<b>Имя клиента:</b> {data.get("model_r")}\n'
        f'<b>Номер телефона:</b> {data.get("nomer_ts")}\n'
        f'<b>Эмират клиента:</b> {data.get("name_c")}\n\n'
        f'<b>Комментарий:</b> {data.get("text")}',
        parse_mode=ParseMode.HTML,
        reply_markup=inline(
            f"{message.chat.id}",
            f"{message.from_user.username}",
            f'{"text"}',
            f'{"model_r"}',
        ),
    )
    await bot.send_message(
        priem_chat_id,
        f"<b>Поступила заявка от</b> @{message.from_user.username}\n\n"
        f'<b>Дата:</b> {data.get("date_z")}\n'
        f'<b>Время:</b> {data.get("timer_r")}\n\n'
        f'<b>Имя клиента:</b> {data.get("model_r")}\n'
        f'<b>Номер телефона:</b> {data.get("nomer_ts")}\n'
        f'<b>Эмират клиента:</b> {data.get("name_c")}\n\n'
        f'<b>Комментарий:</b> {data.get("text")}',
        parse_mode=ParseMode.HTML,
        reply_markup=inline2(
            f"{message.chat.id}",
            f"{message.from_user.username}",
            f'{"text"}',
            f'{"model_r"}',
        ),
    )

    # Заканчиваем "опрос"
    await state.finish()


# Теперь пропишем хэндлеры для inline

@dp.callback_query_handler(reg_callback.filter(status="0"))
# callback данные мы сразу же преобразуем в словарь для удобства работы
async def decline(call: CallbackQuery, callback_data: dict):
    await call.answer()
    print(call.message.message_id, "❌ ОТМЕНЕНО")
    await call.message.forward(priem_chat_id, call.message.message_id)
    # Редачим сообщение в чате админов
    await bot.edit_message_text(

        "❌ Заявка отклонена.", admin_chat_id, call.message.message_id
    )
    await bot.send_message(
        priem_chat_id,

        "❌ Заявка отклонена. Визата не будет!"
    )
    # Отправляем вердикт.
    await bot.send_message(int(callback_data.get("chat_id")), "❌ Заявка ОТКЛОНЕНА. Визита не будет!")

@dp.callback_query_handler(reg_callback.filter(status="00"))
# callback данные мы сразу же преобразуем в словарь для удобства работы
async def decline(call: CallbackQuery, callback_data: dict):
    await call.answer()
    print(call.message.message_id, "❌ ОТКЛОНЕНО")
    await call.message.forward(admin_chat_id, call.message.message_id)
    await call.message.forward(priem_chat_id, call.message.message_id)
    # Редачим сообщение в чате админов
    await bot.edit_message_text(

        "❌ Заявка ОТМЕНЕНА. Кто-то отменил заявку! Визита не будет!", priem_chat_id, call.message.message_id
    )
    await bot.send_message(
        admin_chat_id,

        "☝ Вот эта\n"
        "❌ Заявка ОТМЕНЕНА. Кто-то отменил заявку! Визита не будет!\n\n"
        "‼ Если отмена заявки произошла случайно или по ошибке, данную заявку можно выделить и переслать обратно в группу!",


    )
    await bot.send_message(
        priem_chat_id,

        "☝ Вот эта\n"
        "❌ Заявка ОТМЕНЕНА. Кто-то отменил заявку! Визита не будет!\n\n"
        "‼ Если отмена заявки произошла случайно или по ошибке, сообщите мне @casqeaux",

    )


@dp.callback_query_handler(reg_callback.filter(status="1"))
async def accept(call: CallbackQuery, callback_data: dict, ):
    await call.answer()
    print(call.message.message_id, "✅ ОДОБРЕНО")
    await call.message.forward(priem_chat_id, call.message.message_id)
    await bot.edit_message_text(
        "✅ Заявка одобрена и направлена для исполнения.", admin_chat_id, call.message.message_id

    )
    await bot.send_message(
        priem_chat_id,

        "✅ Заявка просмотрена и одобрена."
    )

    # Отправляем вердикт.
    await bot.send_message(
        int(callback_data.get("chat_id")), "🔥 Заявка просмотрена и одобрена. \n Направлена в группу для исполнения", reply_markup=reg_keyboard,
    )

    @dp.message_handler(Text(equals="заявки"), state="*")
    async def problem(message: types.Message, state: FSMContext):
        await bot.send_message(
            message.chat.id,
            f"<b>👉 Список отправленных заявок:</b> https://bit.ly/3yj7Rjq",
            parse_mode=ParseMode.HTML,

        )

if __name__ == "__main__":
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)