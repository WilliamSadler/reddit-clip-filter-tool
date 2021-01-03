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

   print(request.form['post1'])
   print(request.form['post2'])
   print(request.form['post3'])

   urls = [request.form['post1'], request.form['post2'], request.form['post3']]

   for i in range(0, len(urls)):
      url = urls[i]
      download_reddit_video(url)

@app.route('/reset_folders', methods = ['POST'])
def reset_folder():
   print("Resetting Folders...")
   setup()

@app.route('/download_video', methods = ['POST'])
def download_video():
   print("Downloading Video...")
   url = request.form['post_url']

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

   #remove old videos
   try:
      os.remove(os.getcwd() + "\\static\\videos\\"+str(counter-3)+".mp4")
   except:
      print("Failed trying to delete old video.")

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
