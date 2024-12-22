from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram import Router, F

from aiogram.fsm.context import FSMContext

from .keyboards import main, my_data, start
from .answer_state import Register, Request

from .database.requests import set_new_user, get_user

from .api_main import process

router = Router()


@router.message(CommandStart())
async def command_hello(message: Message):
    await message.answer('Добро пожаловать в наш проект!', reply_markup=main)


@router.message(F.text == 'Инструкция')
async def command_instruction(message: Message):
    #вывод инструкции к боту
    await message.answer('Инструкция к боту:\n Для того, чтобы взаимодействовать с ботом, необходимо зарегистрироваться. '
                         'Если вы пользуетесь ботом впервые, вам нужно ввести требуемые данные. '
                         'Сделать это можно по кнопке "Начать" -> "Зарегистрироваться/изменить данные"\n'
                         'Посмотреть свои данные можно нажав на кнопку "Мои данные" и выбрать интересующие данные. '
                         'Если вы хотите изменить данные, то сделать это можно также по кнопке '
                         '"Начать" -> "Зарегистрироваться/изменить данные."\n'
                         'Когда вы ввели ваши данные, можно приступать к отправке запроса нашему боту. '
                         'Для этого нужно нажать на кнопку "Начать" -> "Отправить запрос", '
                         'сформулировать своё пожелание и дождаться ответа\n')


@router.message(F.text == 'Начать')
async def command_start(message: Message):
    #регистрация/изменение данных, запрос
    await message.answer('Если вы еще не сообщали боту ваши данные, или хотите их поменять, '
                         'зарегистрируйтесь или измените данные. Если данные вас устраивают - отправьте запрос',
                         reply_markup=start)


@router.callback_query(F.data == 'registration')
async def register(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Register.name)
    await callback.answer()
    await callback.message.answer('Введите ваше имя')


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.city)
    await message.answer('Введите ваш город')


@router.message(Register.city)
async def register_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(Register.preff_prod)
    await message.answer('Введите ваши предпочтения по продуктам: что не стоит включать в список продуктов(Вам не нравится или у вас аллергия) или какие конкретно продукты вы любите(например, если сметана - то только брест-литовск)')


@router.message(Register.preff_prod)
async def register_city(message: Message, state: FSMContext):
    await state.update_data(preff_prod=message.text)
    await state.set_state(Register.preff_store)
    await message.answer('Введите ваши предпочтения по магазинам')


@router.message(Register.preff_store)
async def register_city(message: Message, state: FSMContext):
    await state.update_data(preff_store=message.text)
    data = await state.get_data()
    await message.answer(f'Ваше имя: {data["name"]}\nВаш город: {data["city"]}\n'
                         f'Ваши предпочтения по продуктам: {data["preff_prod"]}\n'
                         f'Ваши предпочтения по магазинам: {data["preff_store"]}')
    await set_new_user(message.from_user.id, str(data["name"]), str(data["city"]), str(data["preff_prod"]), str(data["preff_store"]))
    await message.answer(f'Ваши данные успешно сохранены')
    await state.clear()


@router.callback_query(F.data == 'request')
async def request_user(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id
    user = await get_user(tg_id)
    await callback.answer()
    try:
        if user:
            await state.set_state(Request.req)
            #await callback.answer()
            await callback.message.answer('Введите ваш запрос')
        else:
            await callback.message.answer('Вы не авторизованы')
    except Exception as e:
        await callback.message.answer(str(e))


@router.message(Request.req)
async def sent_requests(message: Message, state: FSMContext):
    await state.update_data(req=message.text)
    user_request_one = await state.get_data()
    user_request_two = user_request_one["req"]

    tg_id = message.from_user.id
    user = await get_user(tg_id)
    prefer_product = user.prefer_prod
    user_city = user.city

    requests_for_api = str(f"Запрос пользователя: {str(user_request_two)}; Предпочтения: соль поваренная, {str(prefer_product)}")
    city_for_api = str(user_city)

    answer_for_user = process(requests_for_api, city_for_api)

    await message.answer(answer_for_user)

    #await message.answer(f'Думаю, что запрос нейронке стоит отправить в таком виде: {requests_for_api}')
    await state.clear()


    """await message.answer(f'Ваше имя: {data["name"]}\nВаш город: {data["city"]}\n'
                         f'Ваши предпочтения по продуктам: {data["preff_prod"]}\n'
                         f'Ваши предпочтения по магазинам: {data["preff_store"]}')
    await set_new_user(message.from_user.id, str(data["name"]), str(data["city"]), str(data["preff_prod"]), str(data["preff_store"]))
    await message.answer(f'Ваши данные успешно сохранены')
    await state.clear()"""


@router.message(F.text == 'Мои данные')
async def command_my_data(message: Message):
    await message.answer('Выберите интересующие вас данные', reply_markup=my_data)


@router.callback_query(F.data == 'name')
async def city_of_user(callback: CallbackQuery):
    tg_id = callback.from_user.id
    user = await get_user(tg_id)
    await callback.answer()
    try:
        if user:
            await callback.message.answer(f'{user.name}')
        else:
            await callback.message.answer('Пользователь не найден')
    except Exception as e:
        await callback.message.answer(str(e))


@router.callback_query(F.data == 'city')
async def city_of_user(callback: CallbackQuery):
    tg_id = callback.from_user.id
    user = await get_user(tg_id)
    await callback.answer()
    try:
        if user:
            await callback.message.answer(f'{user.city}')
        else:
            await callback.message.answer('Пользователь не найден')
    except Exception as e:
        await callback.message.answer(str(e))


@router.callback_query(F.data == 'preferred_products')
async def city_of_user(callback: CallbackQuery):
    tg_id = callback.from_user.id
    user = await get_user(tg_id)
    await callback.answer()
    try:
        if user:
            await callback.message.answer(f'{user.prefer_prod}')
        else:
            await callback.message.answer('Пользователь не найден')
    except Exception as e:
        await callback.message.answer(str(e))


@router.callback_query(F.data == 'preferred_stores')
async def city_of_user(callback: CallbackQuery):
    tg_id = callback.from_user.id
    user = await get_user(tg_id)
    await callback.answer()
    try:
        if user:
            await callback.message.answer(f'{user.prefer_stor}')
        else:
            await callback.message.answer('Пользователь не найден')
    except Exception as e:
        await callback.message.answer(str(e))
