import re
import os
import sys
import json
import urllib, urllib2
#import requests

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

port = int(sys.argv[1])
vcap_host = os.environ.get('VCAP_APP_HOST')

#vcap_services = json.loads(os.environ['VCAP_SERVICES'])
#mysql_srv = vcap_services['mysql-5.1'][0]

# port = int(8000)


def read_twit_file():

    twit_raw = []
    twit_decoded = []

    twit_file = open("output.txt")
    for twit_line in twit_file.readlines():
      twit_json = json.loads(twit_line)
      if (twit_json.has_key("entities")):
        if twit_json["entities"]["hashtags"] != []:
          for txr_word in twit_json["entities"]["hashtags"]:
            if txr_word["text"].isalnum():
              twit_raw.append (txr_word["text"])
            
    tmp_tweets = {}
    for twit in twit_raw:
      if twit in tmp_tweets:
        tmp_tweets[twit] += 1
      else:
        tmp_tweets[twit] = 1

    myTopTen = []
    for twt in sorted(tmp_tweets, key=tmp_tweets.get, reverse=True):
      myTopTen.append((twt, tmp_tweets[twt]))
    myTopTen = myTopTen[0:10]

    twit_file.close() 

    return myTopTen


def read_twit_file_freq():

    twit_raw = []
    twit_decoded = []

    twit_file = open("output.txt")
    for twit_line in twit_file.readlines():
      twit_json = json.loads(twit_line)
      if twit_json.has_key("text"):
        twit_raw.append(twit_json["text"])
		
    for twit_line in twit_raw:
      twit_decoded.append(twit_line.encode("utf-8"))

    twit_file.close() 

    return twit_decoded

def calculate(twit_list):
  word_list = dict()
  tot_num_words = 0
  for tweet_line in twit_list:
    for twit_word in tweet_line.split():
      if twit_word in word_list:
        word_list[twit_word] += 1
      elif twit_word.isalnum():
        word_list[twit_word] = 1

  return word_list

def read_sentiment_info_file():

    sent_file = open("AFINN-111.txt")
    sent_file_lines = sent_file.readlines()

    x = dict()
    for line in sent_file_lines:
      term, score = line.split("\t")
      x[term] = int(score)

    sent_file.close()
    return x


    #load twitter file
def read_twit_file_sentiment():

    twit_raw = []
    twit_decoded = []

    twit_file = open("output.txt")
    for twit_line in twit_file.readlines():
      twit_json = json.loads(twit_line)
      if twit_json.has_key("text"):
        twit_raw.append(twit_json["text"])
		
    for twit_line in twit_raw:
      twit_decoded.append(twit_line.encode("utf-8"))

    twit_file.close() 

    return twit_decoded


def calculate_sentiment(sent_list, twit_list):
  
  for tweet_line in twit_list:
    score = 0.00
    for key in sent_list:
      if key in tweet_line:
        score += float(sent_list[key])

    print score


class requestHandler(BaseHTTPRequestHandler):
    def do_POST(s):
        os._exit(0)
 
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html>")
        s.wfile.write("<head><title>Python on Cloud Foundry.</title></head>")
        s.wfile.write("<body><p>Port:")
        s.wfile.write("%s" % port)
        s.wfile.write("</p></body>")
        s.wfile.write("<body><p>Sentiment analysis:      [URL]/sent</p></body>")
        s.wfile.write("<body><p>Top ten twitter handles: [URL]/tt</p></body>")
        s.wfile.write("<body><p>Distinct word count:     [URL]/freq</p></body>")
        s.wfile.write("<form action=\"demo.asp\"><button type=\"submit\" formmethod=\"post\" formaction=\"kill.asp\">Kill</button </form>")


        if s.path[1] == "t" and s.path[2] == "t" :
          myTopTen = read_twit_file()
          for (a, b) in myTopTen:
            s.wfile.write("<body><p>")
            s.wfile.write("%s      :" % a)
            s.wfile.write("%s" % b)
            s.wfile.write("</p></body>")

        if s.path[1] == "f" and s.path[2] == "r" and s.path[3] == "e" and s.path[4] == "q" :
          tweet_list = read_twit_file_freq()
          word_list = calculate(tweet_list)
          for word in word_list:
            print word, word_list[word]
            s.wfile.write("<body><p>")
            s.wfile.write("%s      :" % word)
            s.wfile.write("%s" % word_list[word])
            s.wfile.write("</p></body>")

        if s.path[1] == "s" and s.path[2] == "e" and s.path[3] == "n" and s.path[4] == "t" :
          sent_list = list()
          sent_list = read_sentiment_info_file()
          tweet_list = read_twit_file_sentiment()
          count = 0

          for tweet_line in tweet_list:
            pattern = re.compile('([^\s\w]|_)+')
            tweet_string = re.sub(pattern, '', tweet_line)
            if len(tweet_string) > 0:
              score = 0.00
              for key in sent_list:
                if key in tweet_string:
                  score += float(sent_list[key])

              if score > 0:
                  s.wfile.write("<body><p>")
                  s.wfile.write("%s      :\t" % score)
                  s.wfile.write("%s" % tweet_string)
                  s.wfile.write("</p></body>")

                  if count < 200:
                    myURL =  str(score)
                    myURL =  myURL   + "     \t" + tweet_string
                    quoted_query = urllib.quote(myURL)
                    host = 'http://cf-go-martini-unchafed-coryph.cfapps.io/set/data=%s' % (quoted_query)
                    req = urllib2.Request(host)
                    req.add_header('User-Agent', 'Mozilla/5.0')
                    response = urllib2.urlopen(req)
                    count += 1



        s.wfile.write("</html>")
        return

web_server = HTTPServer(('0.0.0.0', port), requestHandler)
print 'Started on port', port
web_server.serve_forever()
