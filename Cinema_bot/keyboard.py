from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

#inline buttons to choose between three options: find film by name, get top-10 by county, get top-10 by genre
by_name = types.InlineKeyboardButton(text="Найти по названию", callback_data="name_movies_series")
top_by_country = types.InlineKeyboardButton(text="Топ по стране", callback_data="countries")
top_by_genre = types.InlineKeyboardButton(text="Топ по жанру", callback_data="genres")
options_kb = InlineKeyboardBuilder()
options_kb.add(by_name).row(top_by_country, top_by_genre)

#inline buttons to choose between three options: get the link, choose another title, choose another option
link_option = types.InlineKeyboardButton(text="Супер! Хочу ссылку!", callback_data="link")
another_choice_option = types.InlineKeyboardButton(text="Введу название ещё раз", callback_data="another")
restart_option = types.InlineKeyboardButton(text="Хочу выбрать другую опцию", callback_data="restart")
additional_options_kb = InlineKeyboardBuilder()
additional_options_kb.row(link_option, another_choice_option).row(restart_option)