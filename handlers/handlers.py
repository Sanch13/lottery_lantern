from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import settings
from init_bot import router, bot

from keyboards.keyboards import (
    get_inline_keyboard_enter_data,
    get_inline_keyboard_yes_no,
    get_inline_keyboard_check_user_state,
    get_inline_keyboard_get_number_of_ticket,
    get_inline_keyboard_link_to_bot_registration
)
from utils.utils import get_data_user
from validators.validators import validate_string
from utils.utils_for_db import (
    is_exists_user,
    check_user_ticket,
    create_ticket, get_user_by_telegram_id, save_user
)


class Registration(StatesGroup):
    check_user_state = State()
    waiting_for_consent = State()
    last_name = State()
    first_name = State()
    middle_name = State()
    get_number_of_ticket = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = get_inline_keyboard_check_user_state()
    await message.answer(
        text=f"Рады приветствовать Вас на розыгрыше умного проектора\n"
             f"Пожалуйста, проверьте вашу подписку на наш корпоративный Telegram-канал\n"
             f'Для проверки нажмите кнопку "Проверка подписки"',
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data == "check_user_state")
async def process_check_user_state(callback_query: CallbackQuery, state: FSMContext):
    keyboard = get_inline_keyboard_get_number_of_ticket()
    await state.set_state(Registration.check_user_state)

    user_id = callback_query.from_user.id
    status = await bot.get_chat_member(
        chat_id=settings.CHANNEL_ID_MIRAN,
        user_id=user_id,
        request_timeout=10
    )
    print(f"status---------------{status}---------------")

    if status.status in ('member', 'creator', 'administrator'):
        if await is_exists_user(telegram_id=user_id):
            print(f"---------------Юзер подписан и есть в БД---------------")
            await state.set_state(Registration.get_number_of_ticket)
            await callback_query.message.answer(
                'Мы успешно проверили вашу подписку.\nЧтобы получить номер для участия в розыгрыше умного проектора нажмите на "Получить номер":',
                reply_markup=keyboard)
        else:
            print("---------------Юзер подписан на канал, но его нет в БД---------------")
            keyboard_input_data = get_inline_keyboard_enter_data()
            await callback_query.message.answer(
                'Для участия в розыгрыше умного проектора введите ваши ФИО',
                reply_markup=keyboard_input_data)

    else:
        print("---------------Юзера нет на канале и нет в БД (Абсолютно новый "
              "пользователь)---------------")
        keyboard_with_link_to_bot_registration = get_inline_keyboard_link_to_bot_registration()
        await callback_query.message.answer(
            'Вы не подписаны на наш канал. Пожалуйста, зарегистрируйтесь по кнопки ниже, '
            'чтобы принять участие в розыгрыше.',
            reply_markup=keyboard_with_link_to_bot_registration
        )

    await callback_query.answer()


@router.callback_query(lambda c: c.data == "waiting_for_consent")
async def process_ask_for_consent(callback_query: CallbackQuery, state: FSMContext):
    keyboard = get_inline_keyboard_yes_no()
    await state.set_state(Registration.waiting_for_consent)
    await callback_query.message.answer("Я согласен на обработку персональных данных",
                                        reply_markup=keyboard)
    await callback_query.answer()


@router.callback_query(Registration.waiting_for_consent, lambda c: c.data in ["yes", "no"])
async def process_choose_yes_or_no(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "yes":
        await state.set_state(Registration.last_name)
        await callback_query.message.answer("Введите вашу фамилию (только русские символы):")
        await callback_query.answer()

    else:
        await callback_query.message.delete()
        await callback_query.message.answer(
            f"Очень жаль. Надеемся, Вы передумаете.",
            reply_markup=get_inline_keyboard_enter_data()
            )
        await callback_query.answer()
        await state.clear()


@router.message(Registration.last_name)
async def process_input_last_name(message: Message,  state: FSMContext):
    if not await validate_string(message):
        await message.answer("только русские символы.")
        return

    await state.update_data(last_name=message.text.strip())
    await state.set_state(Registration.first_name)
    await message.answer("Введите ваше имя (только русские символы.):")


@router.message(Registration.first_name)
async def process_input_first_name(message: Message,  state: FSMContext):
    if not await validate_string(message):
        await message.answer("только русские буквы.")
        return

    await state.update_data(first_name=message.text.strip())
    await state.set_state(Registration.middle_name)
    await message.answer("Введите ваше отчество (только русские символы.):")


@router.message(Registration.middle_name)
async def process_input_middle_name(message: Message,  state: FSMContext):
    if not await validate_string(message):
        await message.answer("только русские буквы.")
        return

    await state.update_data(middle_name=message.text.strip())
    data = await state.get_data()
    telegram_id, full_name, full_name_from_tg, username = await get_data_user(message, data)

    user = await get_user_by_telegram_id(telegram_id=telegram_id)
    print(f"---------------user---------------{user}---------------")
    if not user:
        await save_user(
            telegram_id=telegram_id,
            full_name=full_name,
            full_name_from_tg=full_name_from_tg,
            username=username
        )
        print(f"---------------Save User---------------")

    keyboard = get_inline_keyboard_get_number_of_ticket()
    await message.answer('Благодарим за информацию\nЧтобы получить номер для участия в '
                         'розыгрыше умного проектора '
                         'нажмите на "Получить номер":',
                         reply_markup=keyboard)
    await state.clear()


@router.callback_query(lambda c: c.data == "get_number_of_ticket")
async def process_get_number_of_ticket(callback_query: CallbackQuery, state: FSMContext):
    telegram_id = callback_query.from_user.id

    has_ticket = await check_user_ticket(
        telegram_id=telegram_id,
        lottery_name=settings.LOTTERY_NAME
    )
    print(f"has_ticket------------------{has_ticket}------------------")

    if has_ticket:
        await callback_query.message.answer("Вы уже участвуете в лотерее.")
    else:
        ticket_number = await create_ticket(
            telegram_id=telegram_id,
            lottery_name=settings.LOTTERY_NAME
        )
        await callback_query.message.answer(f"Ваш номер участия: {ticket_number}")

    await state.clear()
    await callback_query.answer()
