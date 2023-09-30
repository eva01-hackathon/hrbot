from huggingface_hub import snapshot_download
from llama_cpp import Llama

from config import logger


SYSTEM_PROMPT = "Ты — помощник для HR отдела компании, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им во всех вопросах, связанных с делами компании."
SYSTEM_TOKEN = 1788
USER_TOKEN = 1404
BOT_TOKEN = 9225
LINEBREAK_TOKEN = 13


ROLE_TOKENS = {
    "user": USER_TOKEN,
    "bot": BOT_TOKEN,
    "system": SYSTEM_TOKEN
}


def get_message_tokens(model, role, content):
    message_tokens = model.tokenize(content.encode("utf-8"))
    message_tokens.insert(1, ROLE_TOKENS[role])
    message_tokens.insert(2, LINEBREAK_TOKEN)
    message_tokens.append(model.token_eos())
    return message_tokens


def get_system_tokens(model):
    system_message = {"role": "system", "content": SYSTEM_PROMPT}
    return get_message_tokens(model, **system_message)


repo_name = "IlyaGusev/saiga2_13b_gguf"
model_name = "model-q4_K.gguf"

snapshot_download(repo_id=repo_name, local_dir=".", allow_patterns=model_name)

model = Llama(
    model_path=model_name,
    n_ctx=2048,
    n_parts=1,
    n_gqa=8,
    # f16_kv=True,
    # verbose=True,
)

max_new_tokens = 1500


def generate(
    history,
    system_prompt,
    top_p,
    top_k,
    temp
):
    tokens = get_system_tokens(model)[:]
    tokens.append(LINEBREAK_TOKEN)

    for user_message, bot_message in history[:-1]:
        message_tokens = get_message_tokens(model=model, role="user", content=user_message)
        tokens.extend(message_tokens)
        if bot_message:
            message_tokens = get_message_tokens(model=model, role="bot", content=bot_message)
            tokens.extend(message_tokens)

    last_user_message = history[-1][0]
    message_tokens = get_message_tokens(model=model, role="user", content=last_user_message)
    tokens.extend(message_tokens)

    role_tokens = [model.token_bos(), BOT_TOKEN, LINEBREAK_TOKEN]
    tokens.extend(role_tokens)
    logger.info("Generating response...")
    generator = model.generate(
        tokens,
        top_k=top_k,
        top_p=top_p,
        temp=temp
    )
    partial_text = ""
    for i, token in enumerate(generator):
        if token == model.token_eos() or (max_new_tokens is not None and i >= max_new_tokens):
            break
        partial_text += model.detokenize([token]).decode("utf-8", "ignore")
        history[-1][1] = partial_text
        yield history