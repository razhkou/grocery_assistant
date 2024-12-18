from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Инструкция')],
                                     [KeyboardButton(text='Мои данные')],
                                     [KeyboardButton(text='Начать')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

my_data = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Имя', callback_data='name')],
    [InlineKeyboardButton(text='Город', callback_data='city')],
    [InlineKeyboardButton(text='Предпочтительные продукты',
                          callback_data='preferred_products')],
    [InlineKeyboardButton(text='Предпочтительные магазины',
                          callback_data='preferred_stores')]])


start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Регистрация/Изменить данные', callback_data='registration')],
    [InlineKeyboardButton(text='Отправить запрос', callback_data='request')]])
