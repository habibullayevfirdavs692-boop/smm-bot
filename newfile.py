import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# --- SOZLAMALAR ---
BOT_TOKEN = "8949049815:AAFMjLMdR276ruNmtF09bet7-vJiPZsgLZY"
ADMIN_ID = 5918117059  # Sizning ID raqamingiz muvaffaqiyatli qo'yildi

# SMM Panel API sozlamalari
SMM_API_URL = "https://smmpanel-sayti.com/api/v2" 
SMM_API_KEY = "SMM_PANELDAN_OLINGAN_API_KEY"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

users_db = {} 

class OrderState(StatesGroup):
    waiting_for_link = State()
    waiting_for_quantity = State()

class AdminState(StatesGroup):
    waiting_for_ad = State()

def main_keyboard():
    kb = [
        [types.KeyboardButton(text="Xizmatlar & Buyurtma 🛒")],
        [types.KeyboardButton(text="Profilim 👤"), types.KeyboardButton(text="Aloqa 📞")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def admin_keyboard():
    kb = [
        [types.KeyboardButton(text="Statistika 📊"), types.KeyboardButton(text="Reklama Jo'natish 📢")],
        [types.KeyboardButton(text="Asosiy Menyu ↩️")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    if user_id not in users_db:
        users_db[user_id] = {"name": message.from_user.full_name, "balance": 50000}
    
    await message.answer(
        f"Salom {message.from_user.full_name}!\nSMM avtomatlashtirilgan botiga xush kelibsiz.",
        reply_markup=main_keyboard()
    )

@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Admin paneliga xush kelibsiz:", reply_markup=admin_keyboard())
    else:
        await message.answer("Siz admin emassiz!")

@dp.message(F.text == "Profilim 👤")
async def profile_cmd(message: types.Message):
    user_id = message.from_user.id
    balance = users_db.get(user_id, {}).get("balance", 0)
    await message.answer(f"👤 **Profilingiz:**\n\n🆔 ID: `{user_id}`\n💰 Balans: {balance:,} so'm", parse_mode="Markdown")

@dp.message(F.text == "Aloqa 📞")
async def contact_cmd(message: types.Message):
    await message.answer("👨‍💻 Savollar bo'yicha adminga yozing: @SizningUsername")

@dp.message(F.text == "Asosiy Menyu ↩️")
async def back_to_main(message: types.Message):
    await message.answer("Asosiy menyudasiz:", reply_markup=main_keyboard())

SERVICES = {
    "1": {"name": "TG Obunachi (Arzon)", "id": 102, "price": 12000},
    "2": {"name": "Insta Obunachi (Sifatli)", "id": 205, "price": 18000}
}

@dp.message(F.text == "Xizmatlar & Buyurtma 🛒")
async def services_cmd(message: types.Message):
    inline_kb = []
    for key, value in SERVICES.items():
        inline_kb.append([types.InlineKeyboardButton(text=f"{value['name']} - {value['price']} so'm", callback_data=f"buy_{key}")])
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=inline_kb)
    await message.answer("Kerakli xizmatni tanlang:", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("buy_"))
async def process_service_choice(callback: types.CallbackQuery, state: FSMContext):
    service_key = callback.data.split("_")[1]
    await state.update_data(chosen_service=service_key)
    await callback.message.answer("Ajoyib! Endi buyurtma havolasini (link) yuboring:")
    await state.set_state(OrderState.waiting_for_link)
    await callback.answer()

@dp.message(OrderState.waiting_for_link)
async def process_link(message: types.Message, state: FSMContext):
    await state.update_data(link=message.text)
    await message.answer("Qancha buyurtma qilmoqchisiz? (Faqat raqam kiriting):")
    await state.set_state(OrderState.waiting_for_quantity)

@dp.message(OrderState.waiting_for_quantity)
async def process_quantity(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, faqat raqam kiriting!")
        return
        
    quantity = int(message.text)
    user_data = await state.get_data()
    service_info = SERVICES[user_data['chosen_service']]
    user_id = message.from_user.id
    
    total_price = int((service_info['price'] / 1000) * quantity)
    user_balance = users_db.get(user_id, {}).get("balance", 0)
    
    if user_balance < total_price:
        await message.answer(f"Mablag' yetarli emas! ❌\nBalansingizda: {user_balance} so'm bor.")
        await state.clear()
        return

    payload = {
        'key': SMM_API_KEY,
        'action': 'add',
        'service': service_info['id'],
        'link': user_data['link'],
        'quantity': quantity
    }
    
    await message.answer("Buyurtma yuborilmoqda...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(SMM_API_URL, data=payload) as response:
                result = await response.json()
                
                if "order" in result:
                    users_db[user_id]["balance"] -= total_price
                    await message.answer(
                        f"Buyurtma qabul qilindi! ✅\n\nID: {result['order']}\nSarflandi: {total_price} so'm",
                        reply_markup=main_keyboard()
                    )
                else:
                    await message.answer(f"Xatolik yuz berdi: Nomalum xato")
    except:
        await message.answer("SMM xizmatiga ulanishda xato bo'ldi, lekin botingiz ishlayapti!")
    
    await state.clear()

@dp.message(F.text == "Statistika 📊")
async def admin_stat(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(f"📊 Jami foydalanuvchilar: {len(users_db)} ta")

@dp.message(F.text == "Reklama Jo'natish 📢")
async def admin_ad_start(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Reklama xabarini kiriting:")
        await state.set_state(AdminState.waiting_for_ad)

@dp.message(AdminState.waiting_for_ad)
async def admin_send_ad(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        count = 0
        for user_id in users_db.keys():
            try:
                await message.copy_to(chat_id=user_id)
                count += 1
                await asyncio.sleep(0.05)
            except:
                pass
        await message.answer(f"Reklama {count} kishiga ketdi!", reply_markup=admin_keyboard())
        await state.clear()

async def main():
    print("SMM Bot ishlamoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
