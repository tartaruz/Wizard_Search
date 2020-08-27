# TF-IDF
An easy and simple TF-IDF to see the real "numbers" in action.
The programs has a folder with dummy data. The files are the wikipedia page with only the text.
The basic concept used here is the TF-IDF, term frequency and inverted document frequency. [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
 
## Run the program
 
Simple, just run it as all other python scripts.
 
```bash
python3 TF-IDF.py
```
OR 

You can run the search engine page created for this project called _Wizard Search_. The python framework called **Flask** is used to run and host the page.

```bash
    export FLASK_APP=app.py
    flask run
```
It runs in port :5000

## Usage
 
It will ask for the query.
 
```bash
Query? :
```
Insert what you want to search for and the TD-IDF will do it's magic!
 
## Example
 
This will be an example with the query "light ball in space"
 
```bash
Query? : light ball in space
Name           Result
-----------  --------
tv.txt       1.03163
norway.txt   0.727054
clouds.txt   1.23145
rainbow.txt  1.13365
sun.txt      1.80236
Document "sun.txt" is the most relevant
```
The results will be presented as a table with the total sum of the weights. The last sentence will be the name of the most relevant file.


## Possible to add more data
Use the command "data+" to add content to files from wikipedia :)


---
This is the magic spell, TF-IDF: 

![Figure 1-1](https://wikimedia.org/api/rest_v1/media/math/render/svg/cb8cdf7f351b63973cee045cc98c9efcde04203a?raw=true "Figure 1-1")
 
 
