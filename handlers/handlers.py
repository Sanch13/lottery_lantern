from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from init_bot import router

from keyboards.keyboards import get_inline_keyboard_enter_data, get_inline_keyboard_yes_no
from middleware.middleware import check_subscribe


class Registration(StatesGroup):
    waiting_for_consent = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = get_inline_keyboard_enter_data()
    await message.answer(
        text=f"Рады приветствовать Вас на розыгрыше умного проектора\n"
             f"Пожалуйста, проверьте вашу подписку на наш корпоративный Telegram-канал\n"
             f"Для регистрации введите ваши ФИО",
        reply_markup=keyboard
    )


@check_subscribe
@router.callback_query(lambda c: c.data == "waiting_for_consent")
async def process_ask_for_consent(callback_query: CallbackQuery, state: FSMContext):
    keyboard = get_inline_keyboard_yes_no()
    await state.set_state(Registration.waiting_for_consent)
    await callback_query.message.answer("Я согласен на обработку персональных данных",
                                        reply_markup=keyboard)
    await callback_query.answer()
