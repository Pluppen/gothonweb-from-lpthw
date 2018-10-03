from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
from gothonweb import planisphere

app = Flask(__name__)

@app.route("/")
def index():
    # this is used to "setup" the session with starting values
    session['room_name'] = planisphere.START # Setting a starting point
    return redirect(url_for("game")) # Redirects to the game function

@app.route("/game", methods=['GET', 'POST']) # Sets the route for game() to /game and acceots both GET and POST requests.
def game():
    # Set the var room_name to the 'room_name's value in the session dict
    room_name = session.get('room_name') 

    # Checks if the request message is GET or POST
    if request.method == "GET": # Evaluates true if it's a GET req
        if room_name: # True if room_name is defined
            room = planisphere.load_room(room_name) # Sets the room var to return we get from the load room with the arg room_name
            return render_template("show_room.html", room=room) # Loads our show_room.html with the data room
    else: # POST req method
        action = request.form.get('action') # Gets the value from the form and assigns action to it
        if room_name and action: # Checks if both room_name and action has a val
            room = planisphere.load_room(room_name) # Calls the load_room func with the arg as room_name variable
            next_room = room.go(action) # Calls the go func on the current room
                                        # and passes in the arg as action 

            if not next_room: # True if the next room dosen't have any value
                session['room_name'] = planisphere.name_room(room) # Calls the name_room func with the arg room
            else:
                session['room_name'] = planisphere.name_room(next_room) # Calls the name_room func with the arg next_room
            
        return redirect(url_for("game")) # Runs the game function again

# YOU SHOULD CHANGE THIS IF YOU PUT ON THE INTERNET
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run()
