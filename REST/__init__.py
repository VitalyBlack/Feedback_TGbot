from flask import Flask

app = Flask(__name__)

from REST import routes
