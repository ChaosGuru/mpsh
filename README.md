## This site was developed for plast (Ukrainian scout organization) event.

[Web site](http://mpsh.herokuapp.com)

Event was held in format of team competition.
The site should have had the following functions: 
1. display ranking of each team in real time
2. display for each team its completed tasks
3. instructors can add scores for teams
4. teams can scan qr codes to answer theoretical questions

I have chosen the folowing stack Flask, sqlalchemy, sqlite (later I regretted it) and heroku.

Generally users were pretty satisfied except minor issues.
If someone interested I developed the site from zero in 22 hours.

### Mistakes
Here is mistakes which I have made.

1. Do not use sqlite and heroku together. Every 24 hours heroku refresh your app so all data on sqlite will be wiped. That was the most severe issue wich I have seen a few hours before event, lucky I managed to fix it and it leads to a next mistake.
2. Lack of testing. Yes, you need to thoroughly test it. There are always bugs which you can not even imagine.
3. Lack of user guides. Preferably visual guides because they will not understand if you try to explain.

### Lessons and advices
1. First discuss with client your system and make sure that you understand all functionality. Then design database scheme, it will make your life a lot easier. Then just relax and develop.
2. Create automatic database data inserting in case you need to change database scheme.
3. Read documentation. I often read documentation if I do not know how to do some things but if you know does not mean you know correctly. (Hosting sqlite on heroku (facepalm))
4. Periodically show your progress to your client. It keeps you and your client motivated.