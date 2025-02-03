from aiogram.types import Message
from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from config import Config, load_config

BOT_TOKEN: str = Config.tg_bot.token
bot=Bot(BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

channel = InlineKeyboardButton(
    text='Канал-спонсор',
    url='https://t.me/svetochek069',
    callback_data='channel_button_pressed'
)

channels = InlineKeyboardMarkup(
    inline_keyboard=[[channel]]
)

play = InlineKeyboardButton(
    text='Проверить подписку',
    callback_data='play_button_pressed'
)

play= InlineKeyboardMarkup(
    inline_keyboard=[[play]]
)

@dp.message(F.text.lower() == "/start")
async def process_start_command(message: Message):
    await message.answer(
        text='Нажми на кнопку ниже для участия в позыгрыше',
        reply_markup=play
)

@dp.callback_query(F.data == 'play_button_pressed')
async def check_subs(callback: CallbackQuery, bot: Bot):
    user_channel_status_1 = await bot.get_chat_member(chat_id='@svetochek069', user_id=callback.from_user.id)
    # user_channel_status_2 = await bot.get_chat_member(chat_id='@durov_russia', user_id=callback.from_user.id)
    if user_channel_status_1.status != 'left':
        await callback.message.edit_text(
                text = 'Вы участвуете в розыгрыше',
            )
        
    else:
        await callback.message.edit_text(
                text = 'Для участия в розыгрышах вам необходимо подписаться на следующие каналы:',
                reply_markup=channels
            )

if __name__ == '__main__':
    dp.run_polling(bot)
