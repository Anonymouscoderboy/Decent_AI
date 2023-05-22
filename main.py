import pyrogram
from pyrogram import filters
from googletrans import Translator
import pymongo

# Initialize the translator
translator = Translator()

# Initialize the Pyrogram client
app = pyrogram.Client("my_bot", api_id=123456, api_hash="YOUR_API_HASH", bot_token="YOUR_BOT_TOKEN")

# Initialize MongoDB client and database
mongo_client = pymongo.MongoClient("YOUR_MONGODB_URL")
db = mongo_client["chatbot_db"]
collection = db["responses"]

# Handler for incoming messages
@app.on_message(filters.text)
def reply(client, message):
    # Detect the language of the incoming message
    detected_lang = translator.detect(message.text).lang

    # Translate the incoming message to English for processing
    translated_text = translator.translate(message.text, dest="en").text

    # Query the database for a response based on the translated message
    query = {"question": translated_text}
    response = collection.find_one(query)

    if response:
        # If a response is found, retrieve it and translate it to the detected language
        translated_response = translator.translate(response["answer"], dest=detected_lang).text
    else:
        # If no response is found, provide a default response
        translated_response = translator.translate("Sorry, I don't have an answer for that question.", dest=detected_lang).text

    # Send the translated response
    message.reply_text(translated_response)

# Start the bot
app.run()
