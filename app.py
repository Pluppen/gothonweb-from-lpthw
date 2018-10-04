from flask import Flask, session, flash, redirect, url_for, escape, request
from flask import render_template
from gothonweb import planisphere
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True)


app = Flask(__name__)

def increase_highscore(target_usr):

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([target_usr]))
    result = query.first()

    result.highscore += 1

    s.commit()

    return result.highscore

def login_mechanics(target_usr, target_psswd):
    
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([target_usr]), User.password.in_([target_psswd]) )
    result = query.first()
    
    if result:
        session['current_user'] = result.username
        session['current_user_highscore'] = result.highscore
        session['logged_in'] = True
    else:
        print('wrong password!')


@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        session['room_name'] = planisphere.START
        return redirect(url_for("game"))


@app.route("/game", methods=['GET', 'POST'])
def game():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        room_name = session.get('room_name') 
        current_user = session.get('current_user')
        if request.method == "GET":
            if room_name:
                room = planisphere.load_room(room_name)
                lvl = room.lvl
                
                if lvl > session['current_user_highscore']:
                    session['current_user_highscore'] = increase_highscore(current_user)                    
                
                return render_template("show_room.html", room=room, session=session)
        else:
            action = request.form.get('action')
            if room_name and action:
                room = planisphere.load_room(room_name)
                next_room = room.go(action)

                if next_room == None:
                    death = planisphere.load_room('generic_death')
                    session['room_name'] = planisphere.name_room(death)
                else:
                    session['room_name'] = planisphere.name_room(next_room)

            return redirect(url_for("game"))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "GET":
        if not session['logged_in']:
            return render_template("login.html")
        else:
            return index()
    else:
        post_username = str(request.form['username'])
        post_password = str(request.form['password'])
        
        login_mechanics(post_username, post_password)
        return index()

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "GET":
        if not session.get('logged_in'):
            return render_template("signup.html")
        else:
            return index()
    else:
        post_username = str(request.form['username'])
        post_password = str(request.form['password'])

        Session = sessionmaker(bind=engine)
        s = Session()

        user = User(post_username, post_password)
        s.add(user)

        s.commit()

        login_mechanics(post_username, post_password)
            
    return index()


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return index()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()
