from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))


from util.base import Player
import eel

# Set web files folder
eel.init('web')
eel.browsers.set_path('electron', 'node_modules/electron/dist/electron.exe')

#Player instance
player = None

# Expose a function to JavaScript
@eel.expose
def say_hello_py(x):
    print(f"Calling JavaScript function from Python with argument: {x}")
    eel.addAiMessage(x);

# Send the AI response 
def send_ai_response(response):
    print(f"Sending AI response: {response}")
    eel.addAiMessage(response)

#send user response
@eel.expose
def send_user_response(response):
    print(f"Sending user response: {response}")
    player.take_turn(response)

# Build the player client connection. Set the host and port and name to the server and initiates the joining process
@eel.expose
def connect_player(host, port, name):
    try:
        global player 
        player = Player(name)
        player.set_connection(host, int(port))
        player.connect()
        player.add_subscriber(send_ai_response)
        print(f"Player {name} connected to server at {host}:{port}")
        
    except Exception as e:  
        print(f"Error connecting player: {e}")

#player = Player("Goredawn the Gladiator")


#player.connect()
#player.add_subscriber(send_ai_response)

# Start the application
eel.start('index.html', mode='electron')

