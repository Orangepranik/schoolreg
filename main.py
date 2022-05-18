
from importi.importi import *
API_TOKEN = ""
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)

today = datetime.datetime.today()
time = today.strftime("%Y-%m-%d-%H.%M.%S")

@dp.message_handler(commads="start")
async def welcome_user(message: types.Message):
    await message.answer()
