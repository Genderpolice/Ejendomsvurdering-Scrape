FILES:

Scrape Script: Python code used to scrape the website. 

Transform Data: Python code used to transform the data. 

Tableau Dashboard: https://public.tableau.com/app/profile/anders.lind4378/viz/Ejendomsvurderingscrapepresentation/Dashboard2?publish=yes#WelcomeQuestionnaire

The idea came after the new evaluations for housing market in Denmark was published in 2023. No matter what address you would search for most of the URL would stay same only with a change in the ID number. I tried to change the ID to 1, 2, 3, 4, 5 to see if it would bring out a match, and it did. I’m not totally sure how the dictionary database has all the addresses stored. It seems like it goes from ID= 1 where 1 starts in the capital Copenhagen and my guess is it takes the surrounding cities from there. 

The information I wanted from the website was embedded in a HTML H1 tag. The H1 Tag itself containted the city, region, address, street, floor and number. The actual ejendomsværdi and grundværdi number were inside the tag under a DT and DD tag. These components were my target for the script. 
Since my expertise in scraping when starting this little project was close to none. I prompted my thought process to GPT, which through multiple trial and errors ended up with a script that could locate the tags and collect them into a CSV file thanks to beautifulsoup and pandas. Because this was my first time scraping anything I was a bit anxious. I’ve checked the websites robots.txt which didn’t state anything regarding the use of scraping. And tuned the script to take a break after every 10 URL requests. (no clue if it’s on the high or low end) 

Running the script for a little under a hour resulted in 1785 rows of data.

The format of the data needed a smaller transformation for it to be readable by tableau. The main issue was that the data inside the H1 tag got into the same cell. I needed to split it up into six different columns. And since the data wasn’t uniform tools like “text to column” or RIGHT, LEFT, MIDDEL, SEARCH, FIND functions wouldn’t work, or at least not without heavy modifications. Therefore, I prompted GPT with my thoughts of how I wanted it to look, and it gave me a script which did exactly that. Hackerman123, I know.

The data is now transformed and ready to be loaded into tableau. 
My first initial though was to make a heatmap showing Copenhagen and the streets my data represents, hovering over each street with the courser would pop up information regarding that specific streets / address’s ejendomsværdi or grundværdi, and correlate it to the average of the region. 
However, I quickly found out that such detailed map data isn’t just something you just paste in and volia! It works. No, you need specific spatial files that contains the correct map data for your actual map data. I’ve tried to make a workaround making a map that zoomed in onto the streets I knew were in my data with MapBox and connecting it to tableau with API, but still Map wouldn’t work as intended. 

Also, when I shuffled around with the data in tableau I quickly realized that the transformation made earlier on had some minor errors regarding the floor and number columns. This rather small errors give a huge amount of nulls in tableau (nice). Which meant that the actual useable data was over halved. (again, nice) This might be something I’ll take a deeper look into later on.

But nevertheless, I still think some useful insights came to light. Which is showcased in the tableau dashboard. Cheers. 




