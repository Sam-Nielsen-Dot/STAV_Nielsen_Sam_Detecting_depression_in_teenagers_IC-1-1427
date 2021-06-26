from flask import Flask, url_for
from flask import render_template, redirect, send_file, send_from_directory
app = Flask(__name__)
import flask

from flask import request
from datetime import datetime
import csv
import json

from depressionAnalysis.depressionAnalysis import analyse_user, check_dir, get_all_posts_for_user, save_dict, classify, get_classifier

#app.secret_key = 'super secret key'
#app.config['SERVER_NAME'] = 'https://fhakfhalskdjfhalsdkfjahsdlkfjhfasd.dev:5000'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        user = request.form['username']
        return redirect(url_for('user', username=user))
    return render_template('index.html')

@app.route('/text', methods=['GET', 'POST'])
def text_analyse():
    if request.method == "POST":
        d = request.form.to_dict()
        text=d["text_fill"]
        classifier = get_classifier(96)
        classification = classify(text, mode="int", classifier=classifier)
        depressed = (classification == 1)
        classification_probabilities = classify(text, mode="probabilities", classifier=classifier)
        return render_template('text.html', text=text, depressed=depressed, positive_likelihood=classification_probabilities[1][1], negative_likelihood=classification_probabilities[0][1])

    return redirect(url_for('index'))
    #return render_template('index.html')

@app.route('/user/<string:username>')
def user(username):

    try:
        user_posts = get_all_posts_for_user(username, limit=10)
    except:
        return redirect(url_for("index"))

    print("posts gotten")

    if check_dir(f"static\\data\\{username}") == False:
        
        user_stats = analyse_user(username, posts=user_posts, save_as="json", filename=f"static\\data\\{username}\\{username}")
        print("saved as json")
        save_dict(username, "csv", user_stats, filename=f"static\\data\\{username}\\{username}")
        print("saved as csv")
        save_dict(username, "xlsx", user_stats, filename=f"static\\data\\{username}\\{username}")
        print("saved as xlsx")
    else:
        user_stats = analyse_user(username, posts=user_posts)


    return render_template('user.html', username=username, user_stats=user_stats, data=json.dumps(user_stats), posts=sorted(user_stats["posts"], key=lambda x:x["positive_likelihood"], reverse=True), json=f"{username}.json", csv=f"{username}.csv", xlsx=f"{username}.xlsx", xlsx_post=f"{username}_posts.xlsx")
        
@app.route('/download/<string:username>/<path:filename>', methods=['GET', 'POST'])
def download(username, filename):    
    try:
        return send_from_directory(directory=f'static\\data\\{username}', filename=filename)
    except:
        return redirect(url_for('index'))


#flask run --host=0.0.0.0