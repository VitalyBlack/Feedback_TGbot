from rest import app
from bot.bot import runBot
from threading import Thread


thread = Thread(target=runBot, daemon=True)
thread.start()
app.run(host="localhost", port=4067)
