from flask import Flask, render_template
from threading import Thread

web = Flask('')

app = Flask(__name__)

@web.route('/')
def home():
   return render_template('index.html')
if __name__ == '__main__':
   app.run()

def run():
  web.run(host='0.0.0.0',port=8080)

def keep_alive():
   run_thread = Thread(target=run)
   run_thread.start()


