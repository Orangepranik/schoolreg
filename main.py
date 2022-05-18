import types

from databasesqlite3.database import *
from importi.importi import *
from keyboards.keyboards import *
API_TOKEN = "5167652549:AAGyl0koDoRjeBlZPtQd2GFQnVEYGngHB0Q"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage=MemoryStorage()
dp = Dispatcher(bot, storage = storage)

today = datetime.datetime.today()
time = today.strftime("%Y-%m-%d-%H.%M.%S")

@dp.message_handler(commands="start")
async def welcome_user(message: types.Message):
    iduser = message.from_user.id
    username = message.from_user.username
    biouser = await bot.get_chat(iduser)
    biouserget = biouser.bio
    datainvite = time
    checkuserid = cur.execute(f"SELECT * FROM users WHERE userid = ?",(iduser,)).fetchone()
    if checkuserid is None:
        cur.execute("INSERT INTO users(username, userid, userbio, timestart) VALUES(?, ?, ?, ?)", (username, iduser, biouserget, datainvite))
    else:
        pass
    base.commit()
    await message.answer("Вітаємо вас!\n В цьому боті ви можете взнати актуальну інформацію про шкільний заклад під назвою 'ЛУЦЬКИЙ НВК №26'\n Щоб дізнатися інформацію про школу введіть або нажміть кнопку 'Інформація про школу'",
                         reply_markup = start_keyboard())


@dp.message_handler(Text(equals = 'Інформація про школу'))
async def infoforshool(message: types.Message):
    await message.answer()


@dp.message_handler(Text(equals = 'Профіль'))
async def give_profile(message: types.Message):
    info_give_profile = cur.execute("SELECT * FROM users WHERE userid=(?)", (message.from_user.id,)).fetchone()
    await message.reply(f"Ваше ім`я в телеграммі: {info_give_profile[0]}\n Дата коли ви звернулися перший раз до цього бота: {info_give_profile[4]}", reply_markup = returntomenu())


@dp.message_handler(Text(equals = 'Повернутися назад'))
async def returnback(message: types.Message):
    await message.answer("Добре",reply_markup = start_keyboard())


@dp


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)