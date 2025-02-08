import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Tokenni o'zingizning bot tokeningizga almashtiring
TOKEN = "7925929707:AAE_NeRoegYWfIIqW-g0NQfaNnljIG0tijE"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Logger qo'shamiz
logging.basicConfig(level=logging.INFO)

# 500 ta savol va javoblar
questions = [
    {"savol": "O‘zbekiston poytaxti qaysi shahar?", "javob": ["toshkent", "ташкент"]},
    {"savol": "Yerning sun’iy yo‘ldoshi nima?", "javob": ["oy", "луна"]},
    {"savol": "Eng katta okean qaysi?", "javob": ["tinch okeani", "тихий океан"]},
    {"savol": "5 × 5 nechiga teng?", "javob": ["25"]},
    {"savol": "Tesla kompaniyasining asoschisi kim?", "javob": ["ilon mask", "илон маск"]},
    {"savol": "Dunyodagi eng baland tog‘ qaysi?", "javob": ["everest", "эверест"]},
    {"savol": "Dunyodagi eng uzun daryo qaysi?", "javob": ["nil", "нил"]},
    {"savol": "O‘zbekistonning eng katta viloyati qaysi?", "javob": ["navoiy", "навоий"]},
    {"savol": "Dunyodagi eng kichik davlat qaysi?", "javob": ["vatikan", "ватикан"]},
    {"savol": "Futbol bo‘yicha eng ko‘p jahon chempioni bo‘lgan davlat?", "javob": ["braziliya", "бразилия"]},
    {"savol": "Yerning markazidagi issiq suyuq qatlam nima deb ataladi?", "javob": ["magma", "магма"]},
    {"savol": "Eng katta sayyora qaysi?", "javob": ["yupiter", "юпитер"]},
    {"savol": "Eng katta qit’a qaysi?", "javob": ["osiyo", "азия"]},
    {"savol": "Samolyotni kim ixtiro qilgan?", "javob": ["rayt aka-uka", "райт ака-ука"]},
    {"savol": "Albert Eynshteyn qaysi fan sohasida mashhur?", "javob": ["fizika", "физика"]},
    {"savol": "Eng tez yuguruvchi hayvon?", "javob": ["gepard", "гепард"]},
    {"savol": "Hindistonning poytaxti qaysi shahar?", "javob": ["dehli", "дели"]},
    {"savol": "Elektr toki birligini ayting?", "javob": ["amper", "ампер"]},
    {"savol": "Fransiyaning poytaxti qaysi?", "javob": ["parij", "париж"]},
    {"savol": "Suvning kimyoviy formulasi qanday?", "javob": ["h2o"]},
    {"savol": "Yerning qobig‘idagi eng qattiq mineral qaysi?", "javob": ["olmos", "алмаз"]},
    {"savol": "Marsa sayyorasining boshqa nomi nima?", "javob": ["qizil sayyora", "красная планета"]},
    {"savol": "Dunyodagi eng yirik texnologik kompaniyalardan biri?", "javob": ["apple", "эппл"]},
    {"savol": "Eng mashhur o‘zbek yozuvchilaridan biri?", "javob": ["abdulla qodiriy", "абдулла қодирий"]},
    {"savol": "Eng sovuq qit’a qaysi?", "javob": ["antarktida", "антарктида"]},
    {"savol": "Dunyodagi eng katta orol qaysi?", "javob": ["gronlandiya", "гренландия"]},
    {"savol": "Eng mashhur fizik nazariyasi qaysi?", "javob": ["nisbiylik", "относительность"]},
    {"savol": "Eng tez harakatlanadigan narsa nima?", "javob": ["yorug‘lik", "свет"]}
]
random.shuffle(questions)  # Savollar tartibini aralashtiramiz

# Foydalanuvchilar ma'lumotlari
players = {}

@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    chat_id = message.chat.id
    players[chat_id] = {"score": 0, "current_question": 0}
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("🤖 Aqilni Sinag o‘yini boshlandi!\n❓ Savollarga javob bering!", reply_markup=keyboard)
    await ask_question(message)

async def ask_question(message):
    chat_id = message.chat.id
    player = players.get(chat_id)

    if player and player["current_question"] < len(questions):
        savol = questions[player["current_question"]]["savol"]
        await message.answer(f"❓ {savol}")
    else:
        await message.answer("🎉 Siz barcha savollarga to‘g‘ri javob berdingiz! 👏")
        await end_game(message)

@dp.message_handler()
async def check_answer(message: types.Message):
    chat_id = message.chat.id
    player = players.get(chat_id)

    if player:
        current_question = player["current_question"]
        togri_javoblar = questions[current_question]["javob"]
        if message.text.lower() in togri_javoblar:
            player["score"] += 1
            player["current_question"] += 1
            await ask_question(message)
        else:
            correct_answer = ', '.join(togri_javoblar)
            await message.answer(f"❌ Noto‘g‘ri! ✅ To‘g‘ri javob: {correct_answer}\n🎯 Siz {player['score']} ball to‘pladingiz.")
            await end_game(message)

async def end_game(message):
    chat_id = message.chat.id
    players.pop(chat_id, None)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🔄 Qayta o‘ynash uchun /start bosing!"))
    await message.answer("🔄 Qayta o‘ynash uchun /start tugmasini bosing!", reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)