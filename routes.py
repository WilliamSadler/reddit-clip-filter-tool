import os
import glob
import shutil

from redvid import Downloader

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__, static_folder='static')
counter = 0

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/initial_download', methods=['POST'])
def initial_download():
   print("Downloading First Few Videos...")

   urls = ["https://www.reddit.com/r/perfectlycutscreams/comments/cvt1s9/nword_ticket/",
            "https://www.reddit.com/r/perfectlycutscreams/comments/hkyiz5/i_dont_think_he_has_a_gf_anymore/",
            "https://www.reddit.com/r/perfectlycutscreams/comments/ehmr54/i_peaked_in_terms_of_laziness_last_night/"]

   for i in range(0, len(urls)):
      url = urls[i]
      download_reddit_video(url)

@app.route('/download_video', methods = ['POST'])
def download_video():
   print("Downloading Video...")

   url = request.form['post_urls']

   download_reddit_video(url)

   return ("nothing")

def download_reddit_video(url):
   global counter
   dd = os.getcwd()

   reddit = Downloader(max_q=True)
   reddit.path = os.getcwd() + "/static/videos/dl"
   reddit.url = url
   reddit.download()

   os.chdir(dd)

   v = glob.glob(os.getcwd() + "\\static\\videos\\dl\\*.mp4")[0]
   os.rename(v, os.getcwd() + "/".join(v.split("/")[:-1]) + "\\static\\videos\\"+str(counter)+".mp4")
   counter = counter + 1

def setup():
   print("Setting up folders...")
   try:
      shutil.rmtree(os.getcwd() + '/static/videos')
   except:
      print("Could not delete")

   os.mkdir(os.getcwd() + '/static/videos')
   os.mkdir(os.getcwd() + '/static/videos/dl')

if __name__ == '__main__':
   setup()
   app.run(port=6969)
