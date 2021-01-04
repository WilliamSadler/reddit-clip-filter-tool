import os
import glob
import shutil
import requests
import urllib

from bs4 import BeautifulSoup

from redvid import Downloader

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__, static_folder='static')
counter = 0
default_directory = os.getcwd()

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/initial_download', methods=['POST'])
def initial_download():
   global counter
   global default_directory

   print("Downloading First Few Videos...")

   print(request.form['post1'])
   print(request.form['post2'])
   print(request.form['post3'])

   urls = [request.form['post1'], request.form['post2'], request.form['post3']]

   for i in range(0, len(urls)):
      os.chdir(default_directory)
      url = urls[i]
      if "reddit.com" in url:
         download_reddit_video(url)
      elif "tiktok.com" in url:
         download_tiktok_video_via_musicallydown(url, os.getcwd() + "\\static\\videos\\"+str(counter)+".mp4")
         

      #remove old videos
      try:
         os.remove(os.getcwd() + "\\static\\videos\\"+str(counter-3)+".mp4")
      except:
         print("Failed trying to delete old video.")

      counter = counter + 1

@app.route('/reset_folders', methods = ['POST'])
def reset_folder():
   print("Resetting Folders...")
   setup()

@app.route('/download_video', methods = ['POST'])
def download_video():
   global default_directory
   global counter
   print("Downloading Video...")
   url = request.form['post_url']
   os.chdir(default_directory)

   if "reddit.com" in url:
      download_reddit_video(url)
   elif "tiktok.com" in url:
      download_tiktok_video_via_musicallydown(url, os.getcwd() + "\\static\\videos\\"+str(counter)+".mp4")

   #remove old videos
   try:
      os.remove(os.getcwd() + "\\static\\videos\\"+str(counter-3)+".mp4")
   except:
      print("Failed trying to delete old video.")

   counter = counter + 1

   return ("nothing")

def download_reddit_video(url):
   global counter
   dd = os.getcwd()

   reddit = Downloader(max_q=True)
   reddit.path = os.getcwd() + "/static/videos/dl"
   reddit.url = url
   try:
      reddit.download()

      os.chdir(dd)

      v = glob.glob(os.getcwd() + "\\static\\videos\\dl\\*.mp4")[0]
      os.rename(v, os.getcwd() + "/".join(v.split("/")[:-1]) + "\\static\\videos\\"+str(counter)+".mp4")
   except:
      print("Could not download reddit video...")

def download_tiktok_video_via_musicallydown(url, dest):
   session = requests.Session()
   resp = session.get("https://musicallydown.com/")
   soup = BeautifulSoup(resp.text, "html.parser")

   form = soup.find("form", {"id" : "submit-form"})

   inputs = form.findAll("input")
   tiktok_key = inputs[0]["name"]
   secret_key = inputs[1]["name"]
   secret_value = inputs[1]["value"]

   payload = {
      tiktok_key : url,
      secret_key: secret_value,
      "verify" : 1,
      "watermark" : 1
   }


   resp = session.post("https://musicallydown.com/download", data=payload)

   soup = BeautifulSoup(resp.text, "html.parser")
   row = soup.find("div", {"class" : "col s12 l8 left-align"})

   a_list = row.findAll("a", {"class" : "btn"}, href=True)

   direct_link = a_list[0]["href"]
   download_link = a_list[1]["href"]

   download_video(download_link, dest)

def download_video(url, dest):
   """General function to download an mp4 (or other video file) from a given url
   url: the url to the video
   dest: Destination folder for which the video will be downloaded to"""
   #urllib.request.urlretrieve(url, dest + '/v%d.mp4' %time.time())
   urllib.request.urlretrieve(url, dest)

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
