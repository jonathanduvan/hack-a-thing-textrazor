# hack-a-thing-watson

## Watson + Genius Song Analyzer 

### Purpose
The application takes a song title and artist name from the user and accesses the lyrics using the Genius API and basic web scraping. The lyrics are then placed through IBM Watson's tone analyzer, which detects scores for emotions: Anger, Fear, Joy, Sadness, Analytical, Confident, and Tentative. The scores reflect the percentage of confidence Watson has in the matching the tone with the song/line.

Tones and scores are displayed for the overall song, as well as for each lyrical line.

### To Run
To run the application, Python 3 is required. The following packages must be installed:
* Watson Python SDK: `pip install --upgrade watson-developer-cloud`
* Beautiful Soup: `pip install beautifulsoup4`

### Config File
* The application uses API Keys, secret tokens, and login credentials that are stored in a config.py file not displayed in github. Please feel free to contact me via email, canvas, or slack to get the file.

### Examples
Song Title: Out of the Woodwork
Artist Name: Courtney Barnett

~~~
ANALYZING...

Watson analysis for "Out of the Woodwork" by Courtney Barnett:

Lyrical Lines Analysis:

Line: [ I was busy underwater ]
-------------------
Line: [ Seeing how long I could hold my breath ]
Tone: Tentative
Score: 0.88939
-------------------
Line: [ A drowning flower caught my eye and I ]
Tone: Sadness
Score: 0.55602
-------------------
Line: [ Had to come on up for air ]
Tone: Confident
Score: 0.898327
-------------------
Line: [ Just because you’re older than me ]
Tone: Sadness
Score: 0.916667
Tone: Tentative
Score: 0.946222
-------------------
Line: [ Doesn’t mean you have to be so condescending ]
Tone: Confident
Score: 0.866237
-------------------
Line: [ I still see the same things that you see ]
-------------------
Line: [ I’m a little shady on my history ]
-------------------
.
.
.
Line: [ Jump up on your horse and tell me, how’s the view? ]
-------------------
Line: [ (She's so easy) ]
Tone: Joy
Score: 0.851351
-------------------
Line: [ Look over my shoulder when I talk to you ]
-------------------
Line: [ (She's so easy) ]
Tone: Joy
Score: 0.851351
-------------------
Line: [ Where’s the more important person in the room? ]
-------------------

Overall Analysis:

Tone: Fear
Score: 0.773737
~~~

Song Title: Freedom is free
Artist Name: Chicano Batman

~~~
ANALYZING...

Watson analysis for "Freedom is free" by Chicano Batman:


Lyrical Lines Analysis:

Line: [ Nobody likes you nobody cares ]
Tone: Sadness
Score: 0.506538
-------------------
Line: [ Nobody wants you nobody cares ]
-------------------
Line: [ To extend a greeting, a connecting glance ]
-------------------
Line: [ Life is just a jaded game to them ]
Tone: Joy
Score: 0.676002
Tone: Tentative
Score: 0.88939
-------------------
Line: [ They won't give it a chance ]
Tone: Tentative
Score: 0.946222
-------------------
Line: [ But you know and I know ]
Tone: Analytical
Score: 0.955445
-------------------
Line: [ That the galaxies are all around us ]
-------------------
Line: [ And life will flow on ]
Tone: Joy
Score: 0.836063
-------------------
Line: [ As long as the grass grows and the water runs ]
Tone: Analytical
Score: 0.762356
-------------------
Line: [ And while I'm here on earth ]
-------------------
.
.
.
-------------------
Line: [ Freedom is Free ]
-------------------
Line: [ Freedom is Free ]
-------------------
Line: [ Freedom is Free ]
-------------------

Overall Analysis:

Tone: Joy
Score: 0.782302

Tone: Tentative
Score: 0.530083
~~~
