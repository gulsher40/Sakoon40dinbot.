import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
from threading import Thread

# ===== FLASK - BOT KO ZINDA RAKHNE KE LIYE =====
app = Flask('')
@app.route('/')
def home(): return "Sakoon40dinbot Zinda Hai! Alhamdulillah"
def run(): app.run(host='0.0.0.0',port=10000)
def keep_alive(): Thread(target=run).start()
# ===============================================

TOKEN = os.environ['BOT_TOKEN']

# ===== PAID SYSTEM SETTINGS =====
UPI_ID = "nottoworkapi@ybl"
PRICE = 99
ADMIN_USERNAME = "@didiknowyt"
# ================================

# ===== HAR DIN KI TASBEEH =====
TASBEEH = {
    1: {"zikr": "Ya Saboor", "target": 7},
    2: {"zikr": "Alhamdulillah", "target": 33},
    3: {"zikr": "Hasbiyallahu la ilaha illa Huwa alaihi tawakkaltu", "target": 7},
    4: {"zikr": "Allahummaghfir li", "target": 11},
    5: {"zikr": "Astaghfirullah", "target": 100}
    # Din 6-40 ke liye baad mein add kar dena
}
# ==============================

SABAQ = {
    1: """Din 1: Sabr - Allah Ke Sath Baithna

Qissa: Ek sahabi jungle mein rasta bhool gaye. Na paani na khana. 3 din tak bhookay rahe. Teesre din sirf itna kaha: "Ya Allah, Tu janta hai main koshish kar raha hun." Thodi der mein ek kaafila udhar se guzra aur unhe bacha liya.

Ilm: Sabr ka matlab haath pe haath rakh ke bethna nahi. Sabr ka matlab hai koshish karte rehna aur shikayat na karna. Allah ke faislay pe raazi rehna.

Aaj Ke 3 Kaam:
1. Kisi ek baat pe shikayat nahi karni, chahe dil kare.
2. 5 min aankh band karke sirf "Alhamdulillah" bolna.
3. Raat ko sone se pehle 3 cheez likhna jinke liye shukr hai.

Dua: "Ya Saboor, mujhe apna sabr ata farma." 7 baar""",

    2: """Din 2: Shukr - Nazar Ka Chashma Badalna

Qissa: Ek fakir ke paas sirf ek kambal tha. Sardi thi. Aadhi raat ko utha, dekha ek shakhs ke paas kambal bhi nahi. Fakir ne apna kambal aadha phaad kar use de diya. Bola: "Shukr hai mere paas aadha to tha."

Ilm: Shukr nahi hai to sab kuch hote hue bhi fakiri hai. Shukr hai to kuch na hote hue bhi ameeri hai. Shukr Allah ko pasand hai aur wo nashukri se nafrat karta hai.

Aaj Ke 3 Kaam:
1. Khaana khane se pehle aur baad mein dil se Alhamdulillah kehna.
2. Kisi ek insaan ko uski madad ke liye "JazakAllah" bolna.
3. Apne jism ka koi ek hissa dekh kar shukr karna. Jaise "Ya Allah shukr hai aankh di."

Dua: "Allahumma a'inni ala zikrika wa shukrika wa husni ibadatik" 3 baar""",

    3: """Din 3: Tawakkul - Allah Pe Bharosa

Qissa: Ek musafir ka oont gum ho gaya. Pareshan hua. Ek buzurg ne poocha: "Oont baandha tha?" Musafir bola: "Nahi, main Allah pe tawakkul karta hun." Buzurg ne kaha: "Pehle oont baandho, phir tawakkul karo."

Ilm: Tawakkul ka matlab kaam chhod dena nahi hai. Tawakkul ka matlab hai apni poori koshish karna, phir nateeja Allah pe chhod dena. Mehnat tumhari, fal Allah ka.

Aaj Ke 3 Kaam:
1. Aaj ka sabse mushkil kaam Bismillah padh ke shuru karna.
2. Koshish ke baad jo nateeja nikle, uspe "Alhamdulillah ala kulli haal" kehna.
3. Raat ko sone se pehle apni saari fikar Allah ke hawale kar ke sona.

Dua: "Hasbiyallahu la ilaha illa Huwa alaihi tawakkaltu" 7 baar"""
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear() # Tasbeeh reset
    keyboard = [
        [InlineKeyboardButton("Din 1 Chahiye", callback_data='din_1')],
        [InlineKeyboardButton(f"🌟 Premium Access ₹{PRICE}", callback_data='buy_now')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Assalamualaikum! Sakoon ke 40 Din mein khush amdeed.\n\nDin 1-3 Free hain. Din 4-40 Premium hain.', reply_markup=reply_markup)

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""🌟 SAKOON40DIN - Premium Access 🌟

Ruhani Safar Start kijiye - Sirf ₹{PRICE} mein

Din 4 se 40 tak ke khaas sabaq paane ke liye:

1. Neeche diye QR pe ₹{PRICE} bhejiye
2. UPI ID: `{UPI_ID}`
3. Payment ka screenshot {ADMIN_USERNAME} pe bhejein
4. 12 ghante mein aapko Premium access mil jayega

"Jo Allah ki raah mein kharch karta hai, Allah uske maal mein 700 guna barkat deta hai" """
    try:
        await update.message.reply_photo(photo=open('qr.png', 'rb'), caption=text, parse_mode='Markdown')
    except:
        await update.message.reply_text(text + f"\n\nNote: QR load nahi hua. UPI ID: {UPI_ID} pe bhej dein.")

async def din_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text
    din_number = int(command.replace('/din', ''))
    context.user_data['current_din'] = din_number
    context.user_data[f'tasbeeh_{din_number}'] = 0 # Counter reset
    await send_din(update, context, din_number)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'buy_now':
        await buy(query, context)
        return

    if query.data.startswith('tasbeeh_'):
        din_number = int(query.data.split('_')[1])
        key = f'tasbeeh_{din_number}'
        context.user_data[key] = context.user_data.get(key, 0) + 1
        count = context.user_data[key]
        zikr_data = TASBEEH.get(din_number, {"zikr": "SubhanAllah", "target": 33})

        if count >= zikr_data["target"]:
            text = f"🎉 Mubarak! {zikr_data['target']} baar mukammal!\n\n'{zikr_data['zikr']}'\n\nAllah qubool kare. Ameen."
            keyboard = [[InlineKeyboardButton(f"Din {din_number + 1} Chahiye", callback_data=f'din_{din_number + 1}')]]
        else:
            text = f"📿 Tasbeeh: {zikr_data['zikr']}\n\nCount: {count}/{zikr_data['target']}\n\nPadhte raho..."
            keyboard = [[InlineKeyboardButton(f"📿 Dabaya: {count}", callback_data=f'tasbeeh_{din_number}')]]

        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    din_number = int(query.data.replace('din_', ''))
    context.user_data['current_din'] = din_number
    context.user_data[f'tasbeeh_{din_number}'] = 0
    await send_din(update, context, din_number, query)

async def send_din(update, context, din_number, query=None):
    message_target = query.message if query else update.message

    if din_number > 3:
        keyboard = [[InlineKeyboardButton(f"₹{PRICE} mein Premium Khareedein", callback_data='buy_now')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message_target.reply_text(f"🔒 Din {din_number}: Ye Premium Sabaq hai.\n\nDin 4-40 ka access lene ke liye neeche dabayein.", reply_markup=reply_markup)
        return

    if din_number in SABAQ:
        text = SABAQ[din_number]
        zikr_data = TASBEEH.get(din_number, {"zikr": "SubhanAllah", "target": 33})

        keyboard = [
            [InlineKeyboardButton(f"📿 Tasbeeh Shuru: 0/{zikr_data['target']}", callback_data=f'tasbeeh_{din_number}')],
            [InlineKeyboardButton(f"Din {din_number + 1} Chahiye", callback_data=f'din_{din_number + 1}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message_target.reply_text(text, reply_markup=reply_markup)
    else:
        await message_target.reply_text("Ye sabaq abhi likha nahi gaya.")

def main():
    keep_alive()
    app_tele = Application.builder().token(TOKEN).build()
    app_tele.add_handler(CommandHandler("start", start))
    app_tele.add_handler(CommandHandler("buy", buy))
    for i in range(1, 41):
        app_tele.add_handler(CommandHandler(f"din{i}", din_handler))
    app_tele.add_handler(CallbackQueryHandler(button))
    print("Bot is running...")
    app_tele.run_polling()

if __name__ == '__main__':
    main()
