import logging
import os.path
import random
import pytube
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandHelp, Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

TOKEN = "6292304045:AAHwl_UXBwk2xfNoe9wtvGLB2aFxvc7QcaM"

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



class DownloadVideoStates(StatesGroup):
    sending_video_url = State()
    sending_music_url = State()

inline_btn = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Developer", url=("https://t.me/RasulDeveloper")))

option_btn = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton("📽Download Video"), KeyboardButton("🎶Download Music")).add(KeyboardButton("info")).row(KeyboardButton("Raqamni jonatish", request_contact=True), KeyboardButton("Lokatsia tashlash", request_location=True))


@dp.message_handler(commands=['start'])
async def on_start(msg: types.Message):
    await bot.send_message(msg.from_user.id,"""Asalomu aleykum 👋\nYoutube site dan video 🎥 \nLarni tez va oson yuklab\nBeruvchi botga 🤖 Hush kelibsiz\n\nBotdan foydalanish uchun 💻\n\n
👨‍💻 /start - start bot
👨‍💻/help - help to down""", reply_markup=option_btn)


@dp.message_handler(Text(equals='info', ignore_case=True))
async def get__info(msg: types.Message):
    await bot.send_message(msg.from_user. id, 'Salom mening ismim RasulBek', reply_markup=inline_btn)



@dp.message_handler(commands=['info'])
async def getInfo(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Salom Mening Ismim RasulBek')




@dp.message_handler(Text(equals='📽Download Video', ignore_case=True))
async def get_video(msg: types.Message):
    await DownloadVideoStates.sending_video_url.set()
    await bot.send_message(msg.from_user.id, "Iltimos menga video yuklash uchun  yutube link yuboring ✓")

@dp.message_handler(Text(equals='🎶Download Music', ignore_case=True))
async def get_music(msg: types.Message):
    await DownloadVideoStates.sending_music_url.set()
    await bot.send_message(msg.from_user.id, "Youtubedan ▶\nVideoni 🎥 Musiqasini 🎵\nYuklash ✔ uchun \nMenga Video ni link 🔗 ni yuboring")


@dp.message_handler(state=DownloadVideoStates.sending_video_url)
async def upload_video(message: types.Message, state: FSMContext):
    file_name = str(random.randint(0, 100000))
    await bot.send_message(message.chat.id, 'Yuklan moqda 1-5 m ...')

    try:
        yt = pytube.YouTube(message.text)

        yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        path = './videos'
        if not os.path.exists(path):
            os.makedirs(path)
        file_name += '.mp4'
        yt.download(path, filename=file_name)

        logging.info(f'Started processing {file_name}')
        with open(os.path.join(path, file_name), 'rb') as file:
            await bot.send_video(message.chat.id, file, disable_notification=True, reply_markup=inline_btn)

        await bot.send_message(message.chat.id, 'Yakunlandi ✓')
    except Exception as ex:
        print(ex)
        await bot.send_message(message.chat.id, 'Hatolik yuz berdi uzur')
    finally:
        await state.finish()




@dp.message_handler(state=DownloadVideoStates.sending_music_url)
async def upload_music(message: types.Message, state: FSMContext):
    file_name = str(random.randint(0, 100000))
    await bot.send_message(message.chat.id, 'Yuklan moqda 1-5 m ...')

    try:
        yt = pytube.YouTube(message.text)
        yt = yt.streams.filter(only_audio=True, file_extension='mp4').first()

        path = './Videos'
        if not os.path.exists(path):
            os.makedirs(path)
        file_name += '.mp4'
        yt.download(path, filename=file_name)

        logging.info(f'Started processing {file_name}')
        with open(os.path.join(path, file_name), 'rb') as file:

            await bot.send_audio(message.chat.id, file, disable_notification=True)
        await bot.send_message(message.chat.id, 'Yakun landi ✓ ')

    except Exception as ex:
        print(ex)
        await bot.send_message(message.chat.id, 'Hatolik yuz berdi uzur')
    finally:
        await state.finish()


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer("Youtube")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)
