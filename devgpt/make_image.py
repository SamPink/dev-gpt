import openai
from base64 import b64decode
from devgpt.prompts.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

response = openai.Image.create(
    prompt="meme", n=1, size="256x256", response_format="b64_json",
)

image_data = b64decode(response["data"][0]["b64_json"])

with open("image.png", "wb") as png:
    png.write(image_data)

