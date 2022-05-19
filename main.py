import types

from databasesqlite3.database import *
from importi.importi import *
from keyboards.keyboards import *
API_TOKEN = "5167652549:AAGyl0koDoRjeBlZPtQd2GFQnVEYGngHB0Q"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage=MemoryStorage()
dp = Dispatcher(bot, storage = storage)


class apllicationforadmission(StatesGroup):
    name_and_surname = State()
    phonenumner = State()


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


@dp.message_handler(Text(equals = 'Подати заявку на вступ'))
async def inforequest(message: types.Message):
    await message.answer("При поданні заявки ви погоджуєтися з цими правилами\nПравила: ....\nВведіть 'Так' або 'Ні'", reply_markup=yesornorequest())

@dp.message_handler(Text(equals= ['Так', 'так']))
async def requestyes(message: types.Message):
    await apllicationforadmission.name_and_surname.set()
    await message.answer("Введіть ваш ПІБ:")

@dp.message_handler(apllicationforadmission.name_and_surname)
async def responsenameandsurname(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['name_and_surname'] = message.text
    if len(data['name_and_surname'])>= 9:
        await message.answer("Введіть ще раз ")
        await state.finish()
    elif len(data['name_and_surname'])<= 9:
        async with state.proxy() as data:
            data['name_and_surname'] = message.text
    await apllicationforadmission.next()
    await message.answer("Введіть ваш номер телефону:\nЗаписувати у такому форматі: +380....\nПотрібно для того щоб ми змогли зв'язатися з вами")


@dp.message_handler(apllicationforadmission.phonenumner)
async def responsephonenumber(message: types.Message, state = FSMContext):
    async with state.proxy() as data1:
        data1['phonenumber'] = message.text
    replacephonenumber = data1['phonenumber'].replace("+380", '')
    lenphonenumber = len(replacephonenumber)
    if lenphonenumber <= 10 and lenphonenumber >= 13:
        await state.finish()
        await message.answer("Введіть корректно номер:\nПриклад:+380932439249239")
    else:
        await message.answer("alo")

# @dp.message_handler(apllicationforadmission.name_and_surname)
# async def responsenameandsurname(message: types.Message, state = FSMContext)
#     if len(data['name_and_surname'])>= 9:
#         await message.answer("Введіть ще раз ")
#     else
#         await state.update(name_and_surname=message.text}
#         await state.set_state()


@dp.message_handler(Text(equals= ['Ні', 'ні']))
async def requestno(message: types.Message):
    await message.answer("Повертаю назад", reply_markup=start_keyboard())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)