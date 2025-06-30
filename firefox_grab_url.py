from flask import Flask, request
from flask_cors import CORS
import threading
import time

current_url = None
last_update_time = 0

app = Flask(__name__)
CORS(app)

@app.route('/update-url', methods=['POST'])
def update_url():
  global current_url, last_update_time
  data = request.json
  current_url = data.get("url")
  last_update_time = time.time()
  return '', 200

def run_server():
  app.run(port=5001)

#Background thread for Flask server
threading.Thread(target=run_server, daemon=True).start()

def get_current_browser_url():
  return current_url