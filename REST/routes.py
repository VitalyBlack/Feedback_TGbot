import asyncio
from BOT.bot import startPollForUser
from REST import app

@app.route('/')
def index():
    asyncio.run(startPollForUser())
    print("/")
    return "Hello, World!"
