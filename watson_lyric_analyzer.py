from __future__ import print_function
import requests
import json
from os.path import join, dirname
from watson_developer_cloud import ToneAnalyzerV3

import config
from bs4 import BeautifulSoup

base_url = "http://api.genius.com"
headers = {'Authorization': ('Bearer ' + config.GENIUS_BEARER_TOKEN)}


"""
Call Genius API with song data and scrape site to get lyrics
Input: Path to URL for getting to lyrics page
"""

# Adapted from https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/
def lyrics_from_song_api_path(song_api_path):
  song_url = base_url + song_api_path
  response = requests.get(song_url, headers=headers)
  json = response.json()
  path = json["response"]["song"]["path"]
  page_url = "http://genius.com" + path
  page = requests.get(page_url)

  # Web Scraping section
  html = BeautifulSoup(page.text, "html.parser")
  #remove script tags that they put in the middle of the lyrics
  [h.extract() for h in html('script')]

  lyrics = html.find("div", class_= "lyrics").get_text()
  return lyrics


"""
Save lyrics to doc 'lyrics.txt'
input: string containing lyrics
"""
def lyrics_to_doc(lyrics):
    split_lyrics = lyrics.splitlines()
    with open('lyrics.txt', 'w') as the_file:
        for line in split_lyrics:
            line = line.strip()
            if ']' in line:
                continue
            the_file.write(line + '\n')

        the_file.close()

"""
Get analysis from Watson on lyrics_to_doc
"""
# Adapted from IBM Watson Tone Analyzer tutorial: https://www.ibm.com/watson/developercloud/tone-analyzer/api/v3/?cm_mc_uid=70738413429015075187085&cm_mc_sid_50200000=1515616067&cm_mc_sid_52640000=1515617306#post-tone
def watson_analyze():
    tone_analyzer = ToneAnalyzerV3(
        username="366078ad-95b5-4ac0-b5c6-66fcf8a53953",
        password="8xj5T5OJSSZN",
        version='2017-09-26')


    with open(join(dirname(__file__), 'lyrics.txt')) as tone_json:
        tone = tone_analyzer.tone(tone_json.read(), content_type="text/plain")

    return tone


"""
Print results from analysis
Input: ToneAnalysis object
"""
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
