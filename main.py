from flask import Flask, render_template, request, redirect, url_for, session, send_file
import time
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
@app.route('/')
def main():
  return render_template('index.html', btn='generate', tip='Generated lyrics will appear here:')

import requests


API_TOKEN = os.environ['API_TOKEN']
API_URL = "https://api-inference.huggingface.co/models/yuzhiliu8/Songlyricsgenerator"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
  response = requests.post(API_URL, headers=headers, json=payload)
  return response.json()



@app.route('/generated', methods=['POST'])
def index():
  lyrics=request.form['input']
  output = query({
    "inputs": lyrics,
    "options":{
              "wait_for_model": True
            }
  })
  while True:
    try:
      print(output[0])
    except KeyError:
      time.sleep(1)
    else:
      return render_template('index.html', input=lyrics, output=output[0]['generated_text'].replace('.','\n'), btn='regenerate', tip='Click the "regenerate" button to try again!')

@app.route('/about', methods=['GET'])
def about():
  return render_template("about.html")

@app.route('/meet_the_team', methods=['GET'])
def meet_the_team():
  return render_template("team.html")


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)


