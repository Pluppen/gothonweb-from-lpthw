from sys import exit

class Room(object):

    def __init__(self, name, description, lvl):
        self.name = name
        self.description = description
        self.paths = {} # Creates an empty paths dict.
        self.lvl = lvl
        self.help = []

    def add_help(self, command):
        self.help.append(command)

    def go(self, direction):
        return self.paths.get(direction, None)
        # See's if the value of direction is in the paths dict.
        # If not it will return None
        
    def add_paths(self, paths):
        self.paths.update(paths) # Add a new path to the paths dict.

central_corridor = Room("Central Corridor", 
"""
The Gothons of Planet Percal #25 have invaded your ship and destroyed
your entire crew. You are the last surviving member and your last
mission is to get the neutron destruct bomb from the Weapons Armory, put
it in the bridge, and blow the ship up after getting into an escape pod.

You're running down the central corridor to the Weapons Armory when a
Gothon jumps out, red scaly skin, dark grimy teeth, and evil clown
costume flowing around his hate filled body. He's blocking the door to
the Armory and about to pull a weapon to blast you.
""", 1)

laser_weapon_armory = Room("Laser Weapon Armory",
"""
Lucky for you they made you learn Gothon insults in the academy. You
tell the one Gothon joke you know: Lbhe zbgure vf fb sng, jura fur fvgf
ebhaq gur ubhfr, fur fvgf nebhaq gur ubhfr. The Gothon stops, tries
not to laugh, then busts out laughing and can't move. While he's
laughing you run up and shoot him square in the head putting him down,
then jump through the Weapon Armory door.

You do a dive roll into the Weapon Armory, crouch and scan the room for
more Gothons that might be hiding. It's dead quiet, too quiet. You
stand up and run to the far side of the room and find the neutron bomb
in its container. There's a keypad lock on the box and you need the
code to get the bomb out. If you get the code wrong 10 times then the
lock closes forever and you can't get the bomb. The code is 3 digits.
""", 2)

the_bridge = Room("The Bridge",
"""
The container clicks open and the seal breaks, letting gas out. You
grab the neutron bomb and run as fast as you can to the bridge where you
must place it in the right spot.

You burst onto the Bridge with the netron destruct bomb under your arm
and surprise 5 Gothons who are trying to take control of the ship. Each
of them has an even uglier clown costume than the last. They haven't
pulled their weapons out yet, as they see the active bomb under your arm
and don't want to set it off.
""", 3)

escape_pod = Room("Escape Pod",
"""
You point your blaster at the bomb under your arm and the Gothons put
their hands up and start to sweat. You inch backward to the door, open
it, and then carefully place the bomb on the floor, pointing your
blaster at it. You then jump back through the door, punch the close
button and blast the lock so the Gothons can't get out. Now that the
bomb is placed you run to the escape pod to get off this tin can.

You rush through the ship desperately trying to make it to the escape
pod before the whole ship explodes. It seems like hardly any Gothons
are on the ship, so your run is clear of interference. You get to the
chamber with the escape pods, and now need to pick one to take. Some of
them could be damaged but y
""", 4)

the_end_winner = Room("The End",
"""
You jump into pod 2 and hit the eject button. The pod easily slides out
into space heading to the planet below. As it flies to the planet, you
look back and see your ship implode then explode like a bright star,
taking out the Gothon ship at the same time. You won!
""", 5)

the_end_loser = Room("The End",
"""
You jump into a random pod and hit the eject button. The pod escapes
out into the void of space, then implodes as the hull ruptures, crushing
your body into jam jelly.
""", 0)

escape_pod.add_paths({
    '2': the_end_winner,
    '*': the_end_loser
}) # Adding paths to the escape_pod paths dict

escape_pod.add_help('A number between 0-9 ex: 7')

generic_death = Room("Death", "You died.", 0)

the_bridge.add_paths({
    'throw the bomb': generic_death,
    'slowly place the bomb': escape_pod
}) 

the_bridge.add_help('throw the bomb')
the_bridge.add_help('slowly place the bomb')

laser_weapon_armory.add_paths({
    '0132': the_bridge,
    '*': generic_death
})

laser_weapon_armory.add_help('A four digit code ex: 1234')

central_corridor.add_paths({
    'shoot!': generic_death,
    'dodge!': generic_death,
    'tell a joke': laser_weapon_armory
})

central_corridor.add_help('shoot!')
central_corridor.add_help('dodge!')
central_corridor.add_help('tell a joke')

START = 'central_corridor'

def load_room(name):
    whitelist = [
        "central_corridor", "laser_weapon_armory", "the_bridge", "escape_pod",
        "the_end_winner", "the_end_loser", "generic_death"
    ]    
    if name in whitelist:
        return globals().get(name) # Checks for the global variable with the name
    else:
        exit(0)


def name_room(room):
    whitelist = [
        central_corridor, laser_weapon_armory, the_bridge, escape_pod,
        the_end_winner, the_end_loser, generic_death
    ]        
    if room in whitelist:
        for key, value in globals().items():
            if value == room:
                return key
    else:
        exit(0)