from aiogram import types


from config import dp, ratings_db


LIKE = "like"
DISLIKE = "dislike"


rate_buttons = types.InlineKeyboardMarkup(2).add(
    types.InlineKeyboardButton("👎", callback_data=DISLIKE),
    types.InlineKeyboardButton("👍", callback_data=LIKE),
)


async def rate(query: types.CallbackQuery, liked: bool) -> None:
    reply = query.message.reply_to_message
    question = reply.text if reply else ""
    await ratings_db.insert_one({
        "answer": query.message.text,
        "question": question,
        "liked": liked
    })
    await query.message.delete_reply_markup()
    await query.answer("Спасибо ❤️")


@dp.callback_query_handler(lambda call: call.data == LIKE)
async def send_like(query: types.CallbackQuery) -> None:
    await rate(query, True)
    

@dp.callback_query_handler(lambda call: call.data == DISLIKE)
async def send_dislike(query: types.CallbackQuery) -> None:
    await rate(query, False)

