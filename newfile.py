import telebot
from telebot import types

# ---------------------------------------------------------
# SOZLAMALAR (O'zingiznikiga almashtiring)
# ---------------------------------------------------------
BOT_TOKEN = "8949049815:AAFMjLMdR276r-y1S7WpG-gqPZz3-bInS-A"
ADMIN_ID = 5918117059        # Sizning Telegram ID raqamingiz
ADMIN_USERNAME = "@khabibulayev_o27"  # Telegramda ochgan yangi username profilingiz

bot = telebot.TeleBot(BOT_TOKEN)

# Foydalanuvchilar bazasi va vaqtincha buyurtma holati
users_db = {}
user_orders = {}

# XIZMATLAR VA ULARNING NARXLARI (1000 ta uchun so'mda)
PRICES = {
    # Telegram
    "tg_order1": {"name": "👤 Obunachi [ 🛑-Kafolatli 💯 ]", "price": 15000},
    "tg_order2": {"name": "👥 Arzon Obunachi [ 🔴-Kafolatsiz ]", "price": 8000},
    "tg_order3": {"name": "⭐ Premium Obunachi [ 🔴-Kafolatli ]", "price": 45000},
    "tg_order4": {"name": "🤖 Bot uchun /start-Obunachi", "price": 12000},
    "tg_order5": {"name": "📣 Premium Ovozlar [ 🔥-BOOST ]", "price": 30000},
    "tg_order6": {"name": "🩵 Bot uchun [ ⭐Premium Obunachi ]", "price": 40000},
    "tg_order7": {"name": "👀 Prasmotrlar [ ⚡-Tezkor ]", "price": 2000},
    "tg_order8": {"name": "👁️ Prasmotrlar [ ♻️-AvtoPost ]", "price": 5000},
    "tg_order9": {"name": "🇺🇿 O'zbek Xizmatlar [ Barchasi ]", "price": 25000},
    "tg_order10": {"name": "🥳 Reaksiyalar [ 🫀 Tezkor ]", "price": 3000},
    "tg_order11": {"name": "🤗 Reaksiyalar [ ♻️-AvtoPost ]", "price": 6000},
    "tg_order12": {"name": "📊 So'rovnomalar [ ⚡-OVOZ ]", "price": 4000},
    "tg_order13": {"name": "📥 Post Ulashish [ 📢Kanal uchun ]", "price": 10000},
    "tg_order14": {"name": "🔝 Post ulashish Share [ ♻️AvtoPost ]", "price": 15000},
    "tg_order15": {"name": "⭐️ Premium Obunachi [ Yangi Baza ]", "price": 38000},

    # Instagram
    "insta_order1": {"name": "👤 Obunachilar [ ⚡ Sifatli-Tezkor ]", "price": 18000},
    "insta_order2": {"name": "❤️ Likelar [ Sifatli Baza ]", "price": 6000},
    "insta_order3": {"name": " Aniq Prasmotr [ 👀 Ko'rishlar ]", "price": 3000},
    "insta_order4": {"name": "💬 Post Comentlar", "price": 12000},
    "insta_order5": {"name": "👀 Istoriya Prasmotrlar", "price": 4000},
    "insta_order6": {"name": "🚨 Jonli Efir Live [ 👁️ Prasmotr ]", "price": 35000},
    "insta_order7": {"name": "🇺🇿 O'zbek Xizmatlar [ Uzbekistan ]", "price": 28000},
    "insta_order8": {"name": "🔥 Coment LIKE 🔥", "price": 8000},

    # YouTube
    "yt_order1": {"name": "👤 Obunachilar", "price": 55000},
    "yt_order2": {"name": "👁️ Video Ko'rishlar", "price": 18000},
    "yt_order3": {"name": "❤️ Sifatli Like", "price": 8000},
    "yt_order4": {"name": "💬 YouTube Comments", "price": 15000},

    # TikTok
    "tt_order1": {"name": "👤 Obunachilar [ 🛑-Bezminus ]", "price": 24000},
    "tt_order2": {"name": "👁️ Prasmotr [👀-Ko'rishlar]", "price": 1500},
    "tt_order3": {"name": "❤️ Likelar [ Haqiqiy/Soxta ]", "price": 9000},
    "tt_order4": {"name": "👤 Obunachilar [ 👣-Arzon ]", "price": 14000},
    "tt_order5": {"name": "💾 Saqlash [ 💾-Yuklash ]", "price": 5000},
    "tt_order6": {"name": "⭕ Story xizmatlari [ Istoriya ]", "price": 7000},
    "tt_order7": {"name": "💬 TikTok Comments [ Komentlar ]", "price": 11000},
    "tt_order8": {"name": "♠️ PK Battle Poinst [ Achkolar ]", "price": 45000}
}

def get_user_data(user_id):
    if user_id not in users_db:
        users_db[user_id] = {"balans": 0}
    return users_db[user_id]

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Xizmatlar & Buyurtma 🛒")
    btn2 = types.KeyboardButton("Profilim 👤")
    btn3 = types.KeyboardButton("Aloqa 📞")
    markup.add(btn1)
    markup.add(btn2, btn3)
    return markup

def social_networks_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_tg = types.InlineKeyboardButton("✈️ Telegram", callback_data="network_tg")
    btn_insta = types.InlineKeyboardButton("📸 Instagram", callback_data="network_insta")
    btn_yt = types.InlineKeyboardButton("🎥 YouTube", callback_data="network_yt")
    btn_tt = types.InlineKeyboardButton("🎵 TikTok", callback_data="network_tt")
    markup.add(btn_tg, btn_insta, btn_yt, btn_tt)
    return markup

# ---------------------------------------------------------
# COMMANDS
# ---------------------------------------------------------
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    get_user_data(user_id)
    welcome_text = "👋 Assalomu alaykum! SMM Service botimizga xush kelibsiz.\n\n🛒 Buyurtma berishni boshlash uchun quyidagi tugmalardan foydalaning."
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

@bot.message_handler(commands=['panel'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        try:
            parts = message.text.split()
            target_id = int(parts[1])
            amount = int(parts[2])
            get_user_data(target_id)
            users_db[target_id]["balans"] += amount
            bot.reply_to(message, f"✅ ID: {target_id} ga {amount} so'm qo'shildi!")
        except:
            bot.reply_to(message, "❌ Namuna: `/panel 5918117059 50000`", parse_mode="Markdown")

# ---------------------------------------------------------
# TEXT MESSAGES HANDLER
# ---------------------------------------------------------
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    text = message.text

    if text == "Xizmatlar & Buyurtma 🛒":
        bot.send_message(message.chat.id, "👇 Kerakli ijtimoiy tarmoqni tanlang:", reply_markup=social_networks_menu())

    elif text == "Profilim 👤":
        data = get_user_data(user_id)
        profile_text = f"👤 **Sizning Profilingiz:**\n\n🆔 ID: `{user_id}`\n💰 Balans: {data['balans']} so'm"
        bot.send_message(message.chat.id, profile_text, parse_mode="Markdown")

    elif text == "Aloqa 📞":
        bot.send_message(message.chat.id, f"👨‍💻 Savollar va balansni to'ldirish bo'yicha adminga yozing: {ADMIN_USERNAME}")

    # Link qabul qilish qadami
    elif user_id in user_orders and user_orders[user_id]["step"] == "get_link":
        user_orders[user_id]["link"] = text
        user_orders[user_id]["step"] = "get_amount"
        bot.send_message(message.chat.id, "🔢 Qancha buyurtma qilmoqchisiz? (Masalan: 1000)")

    # Miqdor qabul qilish qadami
    elif user_id in user_orders and user_orders[user_id]["step"] == "get_amount":
        try:
            amount = int(text)
            if amount <= 0:
                bot.send_message(message.chat.id, "❌ Iltimos, noldan katta miqdor kiriting!")
                return
                
            service_key = user_orders[user_id]["service"]
            price_per_1k = PRICES[service_key]["price"]
            total_cost = int((price_per_1k / 1000) * amount)
            
            user_data = get_user_data(user_id)
            if user_data["balans"] >= total_cost:
                user_data["balans"] -= total_cost
                
                # Adminga buyurtma haqida xabar yuborish
                admin_msg = (
                    f"🛒 **YANGI BUYURTMA KELDI!**\n\n"
                    f"👤 Kimdan: ID `{user_id}`\n"
                    f"📦 Xizmat: {PRICES[service_key]['name']}\n"
                    f"🔗 Havola (Link): {user_orders[user_id]['link']}\n"
                    f"🔢 Miqdori: {amount}\n"
                    f"💰 Yechilgan summa: {total_cost} so'm"
                )
                bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
                bot.send_message(message.chat.id, f"✅ Buyurtmangiz muvaffaqiyatli qabul qilindi!\n💰 Hisobingizdan {total_cost} so'm yechildi.\n👨‍💻 Admin tez orada buyurtmani bajaradi.")
            else:
                bot.send_message(message.chat.id, f"❌ Balansingizda yetarli mablag' mavjud emas!\n💵 Kerakli summa: {total_cost} so'm\n💳 Sizning balansingiz: {user_data['balans']} so'm")
            
            del user_orders[user_id]
        except:
            bot.send_message(message.chat.id, "❌ Iltimos, faqat butun raqam kiriting!")

# ---------------------------------------------------------
# CALLBACK HANDLERS
# ---------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    user_id = call.from_user.id

    # Telegram xizmatlari
    if call.data == "network_tg":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("👤 Obunachi [🛑-Kafolatli💯] - 15,000 so'm", callback_data="tg_order1"),
            types.InlineKeyboardButton("👥 Arzon Obunachi [🔴-Kafolatsiz] - 8,000 so'm", callback_data="tg_order2"),
            types.InlineKeyboardButton("⭐ Premium Obunachi [🔴-Kafolatli] - 45,000 so'm", callback_data="tg_order3"),
            types.InlineKeyboardButton("🤖 Bot uchun /start-Obunachi - 12,000 so'm", callback_data="tg_order4"),
            types.InlineKeyboardButton("👀 Prasmotrlar [⚡-Tezkor] - 2,000 so'm", callback_data="tg_order7"),
            types.InlineKeyboardButton("🥳 Reaksiyalar [🫀 Tezkor] - 3,000 so'm", callback_data="tg_order10"),
            types.InlineKeyboardButton("⏮️ Orqaga", callback_data="back_to_networks")
        )
        bot.edit_message_text("✈️ Telegram xizmatlari (Narxlar 1000 ta uchun):", chat_id, msg_id, reply_markup=markup)

    # Instagram xizmatlari
    elif call.data == "network_insta":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("👤 Obunachilar [⚡ Sifatli-Tezkor] - 18,000 so'm", callback_data="insta_order1"),
            types.InlineKeyboardButton("❤️ Likelar [Sifatli Baza] - 6,000 so'm", callback_data="insta_order2"),
            types.InlineKeyboardButton(" Aniq Prasmotr [👀 Ko'rishlar] - 3,000 so'm", callback_data="insta_order3"),
            types.InlineKeyboardButton("💬 Post Comentlar - 12,000 so'm", callback_data="insta_order4"),
            types.InlineKeyboardButton("⏮️ Orqaga", callback_data="back_to_networks")
        )
        bot.edit_message_text("📸 Instagram xizmatlari (Narxlar 1000 ta uchun):", chat_id, msg_id, reply_markup=markup)

    # YouTube xizmatlari
    elif call.data == "network_yt":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("👤 Obunachilar - 55,000 so'm", callback_data="yt_order1"),
            types.InlineKeyboardButton("👁️ Video Ko'rishlar - 18,000 so'm", callback_data="yt_order2"),
            types.InlineKeyboardButton("❤️ Sifatli Like - 8,000 so'm", callback_data="yt_order3"),
            types.InlineKeyboardButton("💬 YouTube Comments - 15,000 so'm", callback_data="yt_order4"),
            types.InlineKeyboardButton("⏮️ Orqaga", callback_data="back_to_networks")
        )
        bot.edit_message_text("🎥 YouTube xizmatlari (Narxlar 1000 ta uchun):", chat_id, msg_id, reply_markup=markup)

    # TikTok xizmatlari
    elif call.data == "network_tt":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("👤 Obunachilar [🛑-Bezminus] - 24,000 so'm", callback_data="tt_order1"),
            types.InlineKeyboardButton("👁️ Prasmotr [👀-Ko'rishlar] - 1,500 so'm", callback_data="tt_order2"),
            types.InlineKeyboardButton("❤️ Likelar [Haqiqiy/Soxta] - 9,000 so'm", callback_data="tt_order3"),
            types.InlineKeyboardButton("💬 TikTok Comments [Komentlar] - 11,000 so'm", callback_data="tt_order7"),
            types.InlineKeyboardButton("⏮️ Orqaga", callback_data="back_to_networks")
        )
        bot.edit_message_text("🎵 TikTok xizmatlari (Narxlar 1000 ta uchun):", chat_id, msg_id, reply_markup=markup)

    # Orqaga qaytish
    elif call.data == "back_to_networks":
        bot.edit_message_text("👇 Kerakli ijtimoiy tarmoqni tanlang:", chat_id, msg_id, reply_markup=social_networks_menu())

    # Har qanday xizmat tugmasi bosilganda
    elif call.data in PRICES:
        user_orders[user_id] = {"service": call.data, "step": "get_link"}
        bot.send_message(chat_id, f"📦 Siz tanladingiz: {PRICES[call.data]['name']}\n💵 Narxi (1000 ta uchun): {PRICES[call.data]['price']} so'm\n\n🔗 Iltimos, buyurtma havolasini (linkini) yuboring:")

if __name__ == "__main__":
    bot.infinity_polling()
