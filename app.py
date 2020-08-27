from flask import Flask, render_template, url_for, request
import os
from os import listdir
from os.path import isfile, join
from tdidf import search
import string


app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST" and str(request.form["searchQuery"])!= "":
        resultList = search((request.form["searchQuery"]))
        return render_template("index.html", results=resultList, playSound=True)
    else:
        return render_template("index.html",playSound=False)

@app.route('/files')
def method_name():
    path = "files/"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    print(onlyfiles)
    # q = input(str("\nQuery? : "))
    listen = []
    return render_template("index.html", files=onlyfiles)





@app.route('/page/<pageTitle>', methods=["GET","POST"])
def filePage(pageTitle):
    title = (str(pageTitle)[0]).upper()+ str(pageTitle)[1:-4]
    f = open("files/"+pageTitle, "r")
    body=""
    for lines in f:
        body+= lines+"\n"
    print(body)
    return render_template("page.html", title=title.replace("_"," "), body=body)



# Removes the cache of the CSS on the flask development server
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == "__main__":
    app.run(debug=True)