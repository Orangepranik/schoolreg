from databasesqlite3.database import *
from importi.importi import *
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
    checkuserid = cur.execute(f"SELECT * FROM users WHERE userid==('{iduser}')").fetchone()
    if checkuserid is None:
        cur.execute("INSERT INTO users(username, userid, userbio, timestart) VALUES(?, ?, ?, ?)", (username, iduser, biouserget, datainvite))
    else:
        pass
    base.commit()
    await message.answer("Вітаємо вас,")

# base.execute("CREATE TABLE IF NOT EXISTS users(username VARCHAR(256),userid VARCHAR(300),phonenumber VARCHAR(30), userbio VARCHAR(150),timestart VARCHAR(100), timerequest VARCHAR(100)")
# base.commit()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)