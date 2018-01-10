from __future__ import print_function
import requests
import json
from os.path import join, dirname
from watson_developer_cloud import ToneAnalyzerV3

import config
from bs4 import BeautifulSoup

base_url = "http://api.genius.com"
headers = {'Authorization': ('Bearer ' + config.GENIUS_BEARER_TOKEN)}



# {
#   "url": "https://gateway.watsonplatform.net/tone-analyzer/api",
#   "username": "366078ad-95b5-4ac0-b5c6-66fcf8a53953",
#   "password": "8xj5T5OJSSZN"
# }

def lyrics_from_song_api_path(song_api_path):
  song_url = base_url + song_api_path
  response = requests.get(song_url, headers=headers)
  json = response.json()
  path = json["response"]["song"]["path"]
  #gotta go regular html scraping... come on Genius
  page_url = "http://genius.com" + path
  page = requests.get(page_url)
  html = BeautifulSoup(page.text, "html.parser")
  #remove script tags that they put in the middle of the lyrics
  [h.extract() for h in html('script')]
  #at least Genius is nice and has a tag called 'lyrics'!
  lyrics = html.find("div", class_= "lyrics").get_text() #updated css where the lyrics are based in HTML
  return lyrics

def lyrics_to_doc(lyrics):
    split_lyrics = lyrics.splitlines()
    with open('lyrics.txt', 'w') as the_file:
        for line in split_lyrics:
            line = line.strip()
            if ']' in line:
                continue
            print(line)
            the_file.write(line + '\n')

        the_file.close()

def watson_analyze():
    tone_analyzer = ToneAnalyzerV3(
        username="366078ad-95b5-4ac0-b5c6-66fcf8a53953",
        password="8xj5T5OJSSZN",
        version='2017-09-26')


    with open(join(dirname(__file__), 'lyrics.txt')) as tone_json:
        tone = tone_analyzer.tone(tone_json.read(), content_type="text/plain")

    return tone

def display_watson_results(tone):

    print('\nLyrical Lines Analysis:\n')
    for line in tone['sentences_tone']:
        if (len(line['text']) < 2):
            continue
        print("Line: [ " + line['text'] + ' ]')

        for emotion in line['tones']:
            print('Tone: ' + emotion['tone_name'])
            print('Score: ' + str(emotion['score']))
        print('-------------------')

    print('\nOverall Analysis:\n')

    if len(tone['document_tone']['tones']) < 1:
        print('No major tones detected\n')

    else:
        for emotion in tone['document_tone']['tones']:
            print('Tone: ' + emotion['tone_name'])
            print('Score: ' + str(emotion['score']) +'\n')


if __name__ == "__main__":
  search_url = base_url + "/search"
  print('\n*********************************')
  print('* Watson + Genius Tone Analyzer *')
  print('*********************************\n')

  running = True
  while running:

      print('Please input song and artist information. input "q" at anytime to quit\n')

      song_title = input("Song Title: ")
      if song_title.strip() == 'q':
          running = False
          break
      artist_name = input("Artist Name: ")
      if artist_name.strip() == 'q':
          running = False
          break

      print('\nSearching song...\n')

      data = {'q': song_title}
      response = requests.get(search_url, params=data, headers=headers)
      json = response.json()
      song_info = None

      for hit in json["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"].lower() == artist_name.lower():
          song_info = hit
          break

      if song_info:
            song_api_path = song_info["result"]["api_path"]
            lyrics = lyrics_from_song_api_path(song_api_path)
            lyrics_to_doc(lyrics)

            print('\nANALYZING...\n')
            tone = watson_analyze()

            print('Watson analysis for "' + song_title + '" by ' + artist_name +':\n')

            display_watson_results(tone)

            print('***')

      else:
            print('\nHmm, looks like we had trouble finding that song. Make sure the song and artist spellings are correct.\n')
