import types

from databasesqlite3.database import *
from importi.importi import *
from keyboards.keyboards import *
API_TOKEN = "5167652549:AAGyl0koDoRjeBlZPtQd2GFQnVEYGngHB0Q"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage=MemoryStorage()
dp = Dispatcher(bot, storage = storage)

class apllication_for_admission(StatesGroup):
    name_and_surname = State()
    phone_number = State()
    addres_of_residence = State()
    name_and_surname_of_incomming_user = State()
    how_old_is_incomming = State()


numberslist = [0,1,2,3,4,5,6,7,8,9,0]


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
    await apllication_for_admission.name_and_surname.set()
    await message.answer("Введіть ваш ПІБ:")

@dp.message_handler(state=apllication_for_admission.name_and_surname)
async def responsenameandsurname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_and_surname'] = message.text
    for check_data in data['name_and_surname']:
        if check_data == numberslist:
            if len(data['name_and_surname'])<= 9 and len(data['name_and_surname']) >= 40:
                await message.answer("Введіть ще раз ")
                await apllication_for_admission.name_and_surname.reset()
    else:
        async with state.proxy() as data:
            data['name_and_surname'] = message.text
    await message.reply("Ваш ПІБ успішно записано")
    await apllication_for_admission.next()
    await message.answer("Введіть ваш номер телефону:\nЗаписувати у такому форматі: +380....\nПотрібно для того щоб ми змогли зв'язатися з вами")


@dp.message_handler(state=apllication_for_admission.phone_number)
async def responsephonenumber(message: types.Message, state = FSMContext):
    async with state.proxy() as data1:
        data1['phonenumber'] = message.text 
    replacephonenumber = data1['phonenumber'].replace("+380", '')
    lenphonenumber = len(replacephonenumber)
    print(replacephonenumber)
    numbers = [0,1,2,3,4,5,6,7,8,9]
    for check_nubmer in replacephonenumber:
        if check_nubmer==numbers:
            await message.reply("Ваш номер телефону успішно записано")
            await message.answer("Введіть вашу адресу проживання")
    else:
        await message.answer("Введіть корректно номер:\nПриклад:+380932439249239")
        await apllication_for_admission.phone_number.reset()
    await apllication_for_admission.next()


@dp.message_handler(state=apllication_for_admission.addres_of_residence)
async def requestlive(message: types.Message, state: FSMContext):
    async with state.proxy() as data2:
        data2['addres_of_residence'] = message.text
    lenadress = len(data2['addres_of_residence'])
    if lenadress >= 10 and lenadress <= 30:
        async with state.proxy() as data2:
            data2['addres_of_residence'] = message.text
        await message.reply("Записано в анкету успішно")
        await message.answer("Введіть ПІБ вступника:")
        await apllication_for_admission.next()
    else:
        apllication_for_admission.addres_of_residence.reset()
        await message.answer("Введіть адресу корректно")



@dp.message_handler(state=apllication_for_admission.name_and_surname_of_incomming_user)
async def requestincommingnameandsurname(message: types.Message, state: FSMContext):
    async with state.proxy() as data3:
        data3['name_and_surname_of_incomming_user'] = message.text
    for check_data in data3['name_and_surname_of_incomming_user']:
        if check_data == numberslist:
            if len(data3['name_and_surname_of_incomming_user']) <= 9:
                await message.answer("Введіть корректно ")
                await apllication_for_admission.name_and_surname_of_incomming_user.reset()
    else:
        async with state.proxy() as data:
            data3['name_and_surname_of_incomming_user'] = message.text
    await message.reply("ПІБ вступника записано")
    await message.answer('Введіть вік вступника\nПриклад: 15')
    await apllication_for_admission.next()


@dp.message_handler(state=apllication_for_admission.how_old_is_incomming)
async def requestoldincomminguser(message: types.Message, state: FSMContext):
    async with state.proxy() as data4:
        data4['how_old_is_incomming']  = message.text
    for check_data in data4['how_old_is_incomming']:
        if check_data != numberslist:
            if int(data4['how_old_is_incomming']) <= 5 and int(data4['how_old_is_incomming']) >= 25:
                await apllication_for_admission.how_old_is_incomming.reset()
                await message.answer('Введіть коректно вік\nПриклад: 15')
    else:
        async with state.proxy() as data4:
            data4['how_old_is_incomming'] = message.text
        await message.answer('Ви заповнили анкету\nАнкета відправлена до адміністраторів')
    await message.answer(f"Ваша анкета:\n1. Ваш ПІБ:{data4['name_and_surname']}"
                         f"\n2. Ваш номер телефону: {data4['phonenumber']}"
                         f"3. Ваше місце проживання: {data4['addres_of_residence']}"
                         f"4. ПІБ вступника: {data4['name_and_surname_of_incomming_user']}"
                         f"5. Вік вступника: {data4['how_old_is_incomming']}"
                         f'Допустили помилку в анкеті?,-просто нажміть на кнопку Змінити анкету',reply_markup=error_in_questionary())


@dp.message_handler(Text(equals='Змінити анкету'))
async def correct_questionary(message: types.Message):
    await message.reply('Виберіть який пункт хочете змінити',reply_markup=correct_answers())
@dp.message_handler(Text(equals='1'))
async def correct_1(message: types.Message):
    await apllication_for_admission.name_and_surname.set()
    await message.reply('Введіть ПІБ вступника')

@dp.message_handler(state=apllication_for_admission.name_and_surname)
async def correct_1_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
            data['name_and_surname'] = message.text
        for check_data in data['name_and_surname']:
            if check_data == numberslist:
                if len(data['name_and_surname']) <= 9 and len(data['name_and_surname']) >= 40:
                    await message.answer("Введіть ще раз ")
                    await apllication_for_admission.name_and_surname.reset()
        else:
            async with state.proxy() as data:
                data['name_and_surname'] = message.text
        await message.reply("Ваш ПІБ успішно змінено")

@dp.message_handler(Text(equals='2'))
async def correct_2(message: types.Message):
    await apllication_for_admission.phone_number.set()
    await message.reply('Введіть ваш номер телефону:\nЗаписувати у такому форматі: +380....')
@dp.message_handler(state=apllication_for_admission.phone_number)
async def responsephonenumber(message: types.Message, state = FSMContext):
    async with state.proxy() as data1:
        data1['phonenumber'] = message.text
    replacephonenumber = data1['phonenumber'].replace("+380", '')
    lenphonenumber = len(replacephonenumber)
    print(replacephonenumber)
    numbers = [0,1,2,3,4,5,6,7,8,9]
    for check_nubmer in replacephonenumber:
        if check_nubmer==numbers:
            await message.reply("Ваш номер телефону успішно змінено")
    else:
        await message.answer("Введіть корректно номер:\nПриклад:+380932439249239")
        await apllication_for_admission.phone_number.reset()
@dp.message_handler(Text(equals='3'))
@dp.message_handler(Text(equals='4'))
@dp.message_handler(Text(equals='5'))


# @dp.message_handler(apllication_for_admission.name_and_surname)
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
