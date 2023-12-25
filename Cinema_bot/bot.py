from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import text
from film_info_processor import film_info
from top_genre import genre_info
from top_country import country_info
from link import link
import keyboard as kb

headers = {"X-API-KEY": ""}

bot = Bot(token="")
dp = Dispatcher(storage=MemoryStorage())


class RequiredInfo:
    required_name = ""
    top = []

"""class for queries indication"""
class Options(StatesGroup):
    get_by_name = State()
    top_country = State()
    top_genre = State()


"""start command"""
@dp.message(Command("start"))
async def start_greeting(message: types.Message):
    greeting = text.greeting_builder(message.chat.username, message.chat.first_name)
    await message.answer(greeting)

    await message.answer(
        "\U00002753Выбери, что ты хочешь найти:", 
        reply_markup=kb.options_kb.as_markup()        
    )


"""
callback function
check (by c.data) if user wants to find movie by its name and if true, set a get_by_name state
"""
@dp.callback_query(lambda c: c.data ==  "name_movies_series" or c.data ==  "another")
async def send_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введи название фильма или сериала")
    await state.set_state(Options.get_by_name)

"""
input: message (name of the movie)
output: movie info 
"""
@dp.message(Options.get_by_name)
async def find_by_name(message: types.Message, state: FSMContext):
    name, movie_info, url = film_info.get_by_title(message)
    if not url:
        await bot.send_message(message.chat.id, movie_info)
        RequiredInfo.required_name = ""
        await bot.send_message(message.chat.id, text.restart)
    else:
        await bot.send_photo(message.chat.id, photo=url, caption=movie_info)
        RequiredInfo.required_name = name

        await message.answer(
        "\U00002753Что дальше",
        reply_markup=kb.additional_options_kb.as_markup()     
        )
    await state.clear()


"""
callback function
check (by c.data) if user wants to find movie by its name and if true, set a top_country state
"""
@dp.callback_query(lambda c: c.data ==  "countries")
async def send_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введи страну")
    await state.set_state(Options.top_country)

"""
input: message (name of the country)
output: list of Top-10 movies by country            конопочки: номер, callback_data=название -> RequiredInfo.top список из названий, callback_query (lambda c: c.data in RequiredInfo.top)
"""
@dp.message(Options.top_country)
async def country_top_10(message: types.Message, state: FSMContext):
    flag, info, RequiredInfo.top = country_info.get_by_country(message.text)
    if flag == 0:
        await message.answer(info)
        await message.answer(text.restart)
    else:
        top_keyboard = InlineKeyboardBuilder()
        for i in range(0, len(RequiredInfo.top), 2):
            first_button = types.InlineKeyboardButton(text=f"{i+1}", callback_data=RequiredInfo.top[i]) 
            second_button = types.InlineKeyboardButton(text=f"{i+2}", callback_data=RequiredInfo.top[i+1]) 
            top_keyboard.row(first_button, second_button)
        if len(RequiredInfo.top)%2:
            top_keyboard.add(types.InlineKeyboardButton(text=f"{len(RequiredInfo.top)}", callback_data=RequiredInfo.top[-1]))
        await message.answer(
            info,
            reply_markup=top_keyboard.as_markup()     
        )
    await state.clear()

@dp.callback_query(lambda c: c.data in RequiredInfo.top)
async def get_from_top_by_name(callback: types.CallbackQuery, state: FSMContext):
    title = str(callback.data)
    RequiredInfo.required_name = title
    name, movie_info, url = film_info.get_by_title(title)
    if url == None:
        await callback.message(movie_info)
        RequiredInfo.required_name = ""
        await callback.message.answer(text.restart)
    await callback.message.answer_photo(photo=url, caption=movie_info)
    await state.clear()

    await callback.message.answer(
        "\U00002753Что дальше?",
        reply_markup=kb.additional_options_kb.as_markup()     
    )

"""
callback function
check (by c.data) if user wants to find movie by its name and if true, set a top_genre state
"""
@dp.callback_query(lambda c: c.data ==  "genres")
async def send_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text.genres)
    await callback.message.answer("Введи жанр")
    await state.set_state(Options.top_genre)

"""
input: message (name of the genre)
output: list of Top-10 movies by genre
"""
@dp.message(Options.top_genre)
async def genre_top_10(message: types.Message, state: FSMContext):
    flag, info, RequiredInfo.top = genre_info.get_by_genre(message.text)
    if flag == 0:
        await message.answer(info)
        await message.answer(text.restart)
    else:
        top_keyboard = InlineKeyboardBuilder()
        for i in range(0, len(RequiredInfo.top), 2):
            first_button = types.InlineKeyboardButton(text=f"{i+1}", callback_data=RequiredInfo.top[i]) 
            second_button = types.InlineKeyboardButton(text=f"{i+2}", callback_data=RequiredInfo.top[i+1]) 
            top_keyboard.row(first_button, second_button)
        if len(RequiredInfo.top)%2:
            top_keyboard.add(types.InlineKeyboardButton(text=f"{len(RequiredInfo.top)}", callback_data=RequiredInfo.top[-1]))
        await message.answer(
            info,
            reply_markup=top_keyboard.as_markup()     
        )
    await state.clear()


"""processing of link request"""
@dp.callback_query(lambda c: c.data ==  "link")
async def send_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("\U0001F64CВот ссылочка")
    links = link.get_link(RequiredInfo.required_name)
    links_final = InlineKeyboardBuilder()
    if len(links)==2:
        ivi = types.InlineKeyboardButton(text="ivi", url = links["ivi"])  
        lordfilm = types.InlineKeyboardButton(text="Lordfilm", url = links["Lordfilm"]) 
        links_final.row(ivi, lordfilm)
    else:
        if links.get("ivi"):
            ivi = types.InlineKeyboardButton(text="ivi", url = links["ivi"])  
            links_final.add(ivi)
        else:
            lordfilm = types.InlineKeyboardButton(text="Lordfilm", url = links["Lordfilm"]) 
            links_final.add(lordfilm)
    await callback.message.answer(
        "\U00002753Выбери, где посмотреть:", 
        reply_markup=links_final.as_markup()        
    )
    RequiredInfo.required_name = ""
    await callback.message.answer(text.restart)

"""restart command"""
@dp.message(Command("restart"))
async def restart_function(message: types.Message):
    await message.answer(
        "\U00002753Выбери, что ты хочешь найти:", 
        reply_markup=kb.options_kb.as_markup()        
    )

"""processing restart request"""
@dp.callback_query(lambda c: c.data ==  "restart")
async def send_name(callback: types.CallbackQuery, state: FSMContext):
    RequiredInfo.required_name = ""
    await callback.message.answer(
        "\U00002753Выбери, что ты хочешь найти:", 
        reply_markup=kb.options_kb.as_markup()        
    )


@dp.message(lambda message: message.text[0] == '/')
async def try_wrong_command(message):
    await bot.send_message(message.chat.id, text.cannot_handle)
