# hack-a-thing-watson

## Watson + Genius Song Analyzer 

### Purpose
The application takes a song title and artist name from the user and accesses the lyrics using the Genius API and basic web scraping. The lyrics are then placed through IBM Watson's tone analyzer, which detects scores for emotions: Aner, Fear, Joy, Sadness, Analytical, Confident, and Tentative.

Tones and scores are displayed for the overall song, as well as for each lyrical line.

### To Run
To run the application, Python 3 is required. The following packages must be installed:
* Watson Python SDK: `pip install --upgrade watson-developer-cloud`
* Beautiful Soup: `pip install beautifulsoup4`

### Config File
* The application uses API Keys, secret tokens, and login credentials that are stored in a config.py file not displayed in github. Please feel free to contact me via email, canvas, or slack to get the file.
