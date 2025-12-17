import random
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

# ---------- CUSTOM POKÉMON ----------
CUSTOM_POKEMON = [
    {
        "name": "noop poop",
        "image": "https://i.imgur.com/6XGQxQp.png"
    },
    {
        "name": "golden mewtwo",
        "image": "https://i.imgur.com/0gZ7K7F.png"
    }
]

user_answer = {}

# ---------- COMMANDS ----------
def start(update, context):
    update.message.reply_text(
        "🎮 Pokémon Guess Bot\n\n"
        "Use /guess to guess the Pokémon name!"
    )

def guess(update, context):
    use_custom = random.choice([True, False])

    if use_custom:
        poke = random.choice(CUSTOM_POKEMON)
        name = poke["name"]
        image = poke["image"]
    else:
        pid = random.randint(1, 151)
        data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pid}").json()
        name = data["name"]
        image = data["sprites"]["other"]["official-artwork"]["front_default"]

    user_answer[update.effective_user.id] = name.lower()

    update.message.reply_photo(
        photo=image,
        caption="❓ Guess the Pokémon name!"
    )

def check_answer(update, context):
    uid = update.effective_user.id
    if uid not in user_answer:
        return

    if update.message.text.lower() == user_answer[uid]:
        update.message.reply_text("✅ Correct! 🎉")
        del user_answer[uid]
    else:
        update.message.reply_text("❌ Wrong, try again!")

# ---------- MAIN ----------
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("guess", guess))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_answer))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
