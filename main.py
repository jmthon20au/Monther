import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# أدخل رمز API الذي حصلت عليه من BotFather
API_TOKEN = "7365835096:AAExXLCGjQuHJ2VyE8J22p8bnl_7NJJVwDU"

bot = telebot.TeleBot(API_TOKEN)

# قائمة بالكلمات المحظورة
banned_words = ['كسمك','كسعمتك','كسختك','عيري','اير','عير','زب','زوب','كسي','طيز','امك','خالتك','مص','كسك','مصلي','موطه','موطة','موطلي','انيج امك','كسختك','عير باختك','عير بامك','عير بيك','بلاع','نيج','نيجني','انيجك','امك الكحبه','اختك الكحبه','تيل بيك','تيل','اه','سكسي','سكس','sex','+18','نيجه','مصه','كحبه','كحبه','امك تنيج','اختك تنيج','خالتك الشكرا','خالتك الشكره','خالتك الشكرة','وردي','ما اتحمل','كله لو بس الراس','مصيلي','ااه','اهه','🍑'"كسك","نجب","ابن الكحبه","انيجك","كواد","بربوك","زربان","سكس","كسكوس","امك","اختك","عير","عيري","ايري","امك انيجها","نيجها","طيزي","طيزك","طيزج","ولج بربوك"," انيجج","متبربكه","كواده","ابو العيوره","ام العيوره"]

# قائمة معرفات المطورين (يمكنك إضافة معرفات المطورين هنا)
DEVELOPERS_CHAT_IDS =  [6429513266,663985495 ,1882860421]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    developer_button = InlineKeyboardButton(text="المطور 🧑🏼‍💻", url="https://t.me/i_qq_q")
    markup = InlineKeyboardMarkup().add(developer_button)
    bot.reply_to(message, "مرحبا بك في بوت حماية المعهد. هذا البوت خاص بالمعهد النجاح والتطور فقط.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def check_message(message):
    text = message.text.lower()

    # الردود على الرسائل المحددة
    if "السلام عليكم" in text:
        bot.reply_to(message, "وعليكم السلام ورحمة الله 💖")
    elif "شلونكم شباب" in text:
        bot.reply_to(message, "الحمدلله وانت؟")
    elif "شلونكم" in text:
        bot.reply_to(message, "زينين وانت؟")
    elif "المطور" in text:
        developer_button = InlineKeyboardButton(text="المطور 🧑🏼‍💻", url="https://t.me/ZK_HK")
        markup = InlineKeyboardMarkup().add(developer_button)
        bot.send_message(message.chat.id, "اسم المطور : حسين\nيوزر المطور : @i_qq_q", reply_markup=markup)
    elif "السورس" in text:
        developer_button = InlineKeyboardButton(text="المطور 🧑🏼‍💻", url="https://t.me/ZK_HK")
        markup = InlineKeyboardMarkup().add(developer_button)
        bot.send_message(message.chat.id, "عزيزي لايوجد سورس لكن هذا البوت تمت برمجتهُ من قبل حسين", reply_markup=markup)

    # التحقق من الكلمات المحظورة (فقط في المجموعات)
    banned_word_found = next((word for word in banned_words if word in text), None)
    if message.chat.type in ["group", "supergroup"] and banned_word_found:
        try:
            bot.delete_message(message.chat.id, message.message_id)
            
            # إعداد زر شفاف مع اسم المستخدم ورابط الملف الشخصي
            user_profile_url = f"tg://user?id={message.from_user.id}"
            user_button = InlineKeyboardButton(text=message.from_user.first_name, url=user_profile_url)
            markup = InlineKeyboardMarkup().add(user_button)
            
            bot.send_message(message.chat.id, 'تم حذف الرسالة لاحتوائها على كلمة محظورة.', reply_markup=markup)

            # إرسال تنبيه للمطورين
            alert_message = (
                f"ستاذي هاي اكو واحد كاعد يكتب كلمات محظورة شو تعال شوفه شيريد:\n"
                f"{message.from_user.first_name} ({message.from_user.id})\n"
                f"الكلمة المحظورة: {banned_word_found}"
            )
            for dev_id in DEVELOPERS_CHAT_IDS:
                forgive_button = InlineKeyboardButton(text="يلا نسامحه", callback_data=f"forgive_{message.chat.id}_{message.from_user.id}")
                ban_button = InlineKeyboardButton(text="اطرده", callback_data=f"ban_{message.chat.id}_{message.from_user.id}")
                user_button = InlineKeyboardButton(text=message.from_user.first_name, url=user_profile_url)
                alert_markup = InlineKeyboardMarkup().add(forgive_button, ban_button).add(user_button)
                bot.send_message(dev_id, alert_message, reply_markup=alert_markup)

        except Exception as e:
            print(f"Error: {e}")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    action, chat_id, user_id = call.data.split('_')
    if action == "forgive":
        bot.answer_callback_query(call.id, "تم مسامحة المستخدم.")
    elif action == "ban":
        try:
            bot.kick_chat_member(chat_id, user_id)
            bot.answer_callback_query(call.id, "تم طرد المستخدم.")
        except Exception as e:
            bot.answer_callback_query(call.id, f"فشل في طرد المستخدم: {e}")

bot.polling()
