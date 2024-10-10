from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from .models import User
# newsapi
from newsapi import NewsApiClient
import requests

views = Blueprint('views', __name__)
@views.route('/')
def index():
    return render_template("index.html", user=current_user)


@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('wala naman to laman eh', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('nalagay ko na note mo', category='success')
            
    return render_template("notes.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

# this is test
@views.route('/darkMode', methods=['POST'])
def darkLightMode():
    if request.method == 'POST':
        print(current_user.darkLight)
        if current_user.id:
            current_user.darkLight = 'dark'
            db.session.commit()
    return render_template("index.html", user=current_user)

@views.route('/lightMode', methods=['POST'])
def lightMode():
    if request.method == 'POST':
        print(current_user.darkLight)
        if current_user.id:
            current_user.darkLight = 'light'
            db.session.commit()
    return render_template("index.html", user=current_user)

# profile
@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)


# test navbar
@views.route('/rick')
def rick():
    return render_template("rick.html", user=current_user)


# news route
@views.route('/news')
def news():
    newsapi = NewsApiClient(api_key='a15726cbda154abe8bffed22843a3a0c')
    # top_headlines = newsapi.get_top_headlines(sources="google-news", country='ph')
    # articles = top_headlines['articles']

    response = requests.get('https://newsapi.org/v2/top-headlines?country=ph&apiKey=a15726cbda154abe8bffed22843a3a0c')

    # Convert the response to JSON
    data = response.json()

    # Extract the articles
    articles = data['articles']
    datta = [len(articles)]
    # Extract and print the sources
    for article in articles:
        datta.append(article)

    # print(datta)
    return render_template('newsCurrent.html',user=current_user, data=datta)


# GAMES SECTOR
@views.route('/games')
def game():
    return render_template("games.html", user=current_user)

@views.route('/snakegame')
def snakegame():
    return render_template("/games/snakegame.html")

@views.route('/bolidegame')
def bolidegame():
    return render_template("/games/bolidegame.html")

@views.route('/puzzlemaker')
def puzzlemaker():
    return render_template("/games/puzzlemaker.html")

@views.route('/trigonium')
def trigonium():
    return render_template("/games/trigonium.html")

@views.route('/checkers')
def checkers():
    return render_template("/games/checkers.html")

@views.route('/tetris')
def tetris():
    return render_template("/games/tetris.html")
    
@views.route('/xo')
def xo():
    return render_template("/games/xo.html")

@views.route('/pingpong')
def pingpong():
    return render_template("/games/pingpong.html")

@views.route('/breakout')
def breakout():
    return render_template("/games/breakout.html")
