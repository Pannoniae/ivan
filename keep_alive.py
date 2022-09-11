from flask import Flask
from threading import Thread
import subprocess
import time
import sys

app = Flask('')



@app.route('/')
def main():
  return 'Bot works!'



def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()