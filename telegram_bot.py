# pip install pyTelegramBotAPI
# python telegram_bot.py

import telebot
from telebot import types

# ─── KONFIGURACJA ──────────────────────────────────────────────────
BOT_TOKEN = "8850495118:AAFEHfuZC9M_ZUpDSR1Sdbd-ljcwS6fz0b8"

TWOJ_TELEGRAM = "@PaulinaKoch_xoxo"

LINK_PLATNOSCI_BLIK    = "Przelew BLIK na numer: 796066335"
LINK_PLATNOSCI_PAYPAL  = "https://paypal.me/twojlink"
LINK_PLATNOSCI_REVOLUT = "https://revolut.me/twojlink"

# ─── PAKIETY ───────────────────────────────────────────────────────
PAKIETY = {
    "normal": {
        "nazwa": "NORMAL",
        "cena":  "50 zl",
        "opis":  "10 zdj lifestyle\nRozdzielczosc HD\nDostawa w 24h\nJednorazowe uzycie",
        "emoji": "P",
    },
    "pro": {
        "nazwa": "PRO",
        "cena":  "100 zl",
        "opis":  "25 zdj tematycznych\nRozdzielczosc Full HD\nDostawa w 12h\n1 motyw do wyboru\nMozliwosc 1 rewizji",
        "emoji": "S",
    },
    "vip": {
        "nazwa": "VIP",
        "cena":  "200 zl",
        "opis":  "50 zdj ekskluzywnych\nRozdzielczosc 4K\nDostawa w 6h\n3 motywy do wyboru\nNielimitowane rewizje\nDostep do archiwum",
        "emoji": "V",
    },
}

# ─── BOT ───────────────────────────────────────────────────────────
bot = telebot.TeleBot(BOT_TOKEN)

def menu_glowne():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        types.KeyboardButton("NORMAL - 50 zl"),
        types.KeyboardButton("PRO - 100 zl"),
        types.KeyboardButton("VIP - 200 zl"),
        types.KeyboardButton("Jak to dziala?"),
        types.KeyboardButton("Kontakt"),
    )
    return markup

def przyciski_pakietu(klucz):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Zamawiam!", callback_data="zamow_" + klucz),
        types.InlineKeyboardButton("Wroc",      callback_data="powrot"),
    )
    return markup

def przyciski_platnosci(klucz):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("BLIK",    callback_data="platnosc_blik_"    + klucz),
        types.InlineKeyboardButton("PayPal",  callback_data="platnosc_paypal_"  + klucz),
        types.InlineKeyboardButton("Revolut", callback_data="platnosc_revolut_" + klucz),
        types.InlineKeyboardButton("Wroc",    callback_data="szczegoly_"        + klucz),
    )
    return markup


# ─── KOMENDY ───────────────────────────────────────────────────────

@bot.message_handler(commands=["start"])
def start(message):
    imie = message.from_user.first_name or "hej"
    bot.send_message(
        message.chat.id,
        "Czesc " + imie + "!\n\nJestem Twoim botem do zamawiania ekskluzywnych zdj.\n\nWybierz pakiet ktory Cie interesuje!",
        reply_markup=menu_glowne(),
    )

@bot.message_handler(commands=["menu"])
def pokaz_menu(message):
    bot.send_message(message.chat.id, "Wybierz pakiet:", reply_markup=menu_glowne())


MAPA_KLAWISZY = {
    "NORMAL - 50 zl": "normal",
    "PRO - 100 zl":   "pro",
    "VIP - 200 zl":   "vip",
}

@bot.message_handler(func=lambda m: m.text in MAPA_KLAWISZY)
def pokaz_pakiet(message):
    klucz = MAPA_KLAWISZY[message.text]
    p = PAKIETY[klucz]
    tekst = "Pakiet " + p["nazwa"] + " - " + p["cena"] + "\n\n" + p["opis"] + "\n\nKliknij Zamawiam! aby wybrac metode platnosci."
    bot.send_message(message.chat.id, tekst, reply_markup=przyciski_pakietu(klucz))

@bot.message_handler(func=lambda m: m.text == "Jak to dziala?")
def jak_dziala(message):
    bot.send_message(
        message.chat.id,
        "Jak to dziala?\n\n1. Wybierz pakiet\n2. Oplacam zamowienie (BLIK / PayPal / Revolut)\n3. Wyslij potwierdzenie przelewu\n4. Otrzymujesz link do zdj\n\nWszystkie zdjecia sa oryginalne i wysylane tylko Tobie.",
        reply_markup=menu_glowne(),
    )

@bot.message_handler(func=lambda m: m.text == "Kontakt")
def kontakt(message):
    bot.send_message(
        message.chat.id,
        "Mozesz napisac do mnie bezposrednio: " + TWOJ_TELEGRAM + "\n\nOdpowiadam zazwyczaj w ciagu kilku godzin.",
        reply_markup=menu_glowne(),
    )


# ─── INLINE CALLBACKS ──────────────────────────────────────────────

@bot.callback_query_handler(func=lambda c: c.data.startswith("szczegoly_"))
def pokaz_szczegoly(call):
    klucz = call.data.replace("szczegoly_", "")
    p = PAKIETY[klucz]
    tekst = "Pakiet " + p["nazwa"] + " - " + p["cena"] + "\n\n" + p["opis"] + "\n\nKliknij Zamawiam! aby wybrac metode platnosci."
    bot.edit_message_text(tekst, call.message.chat.id, call.message.message_id, reply_markup=przyciski_pakietu(klucz))

@bot.callback_query_handler(func=lambda c: c.data == "powrot")
def powrot(call):
    bot.edit_message_text("Wybierz pakiet:", call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Wybierz pakiet:", reply_markup=menu_glowne())

@bot.callback_query_handler(func=lambda c: c.data.startswith("zamow_"))
def zamow(call):
    klucz = call.data.replace("zamow_", "")
    p = PAKIETY[klucz]
    bot.edit_message_text(
        "Wybierz metode platnosci dla pakietu " + p["nazwa"] + " (" + p["cena"] + "):",
        call.message.chat.id, call.message.message_id,
        reply_markup=przyciski_platnosci(klucz),
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("platnosc_"))
def platnosc(call):
    czesci = call.data.split("_")
    metoda = czesci[1]
    klucz  = czesci[2]
    p      = PAKIETY[klucz]

    if metoda == "blik":
        info = "Platnosc BLIK\n\n" + LINK_PLATNOSCI_BLIK + "\n\nKwota: " + p["cena"]
    elif metoda == "paypal":
        info = "Platnosc PayPal\n\nLink: " + LINK_PLATNOSCI_PAYPAL + "\n\nKwota: " + p["cena"]
    else:
        info = "Platnosc Revolut\n\nLink: " + LINK_PLATNOSCI_REVOLUT + "\n\nKwota: " + p["cena"]

    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        info + "\n\nPo dokonaniu platnosci wyslij mi zrzut ekranu potwierdzenia.\nMozesz tez napisac bezposrednio: " + TWOJ_TELEGRAM,
        reply_markup=menu_glowne(),
    )


@bot.message_handler(func=lambda m: True)
def nieznana(message):
    bot.send_message(message.chat.id, "Nie rozumiem tej komendy. Skorzystaj z menu ponizej.", reply_markup=menu_glowne())


if __name__ == "__main__":
    print("Bot uruchomiony. Nacisnij Ctrl+C aby zatrzymac.")
    bot.infinity_polling()
