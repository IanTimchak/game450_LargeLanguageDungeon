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
        player.add_subscriber(send_ai_response, "send_ai_response")
        player.add_subscriber(play_sound_effect, "play_sound_effect")
        print(f"Player {name} connected to server at {host}:{port}")
        
    except Exception as e:  
        print(f"Error connecting player: {e}")


@eel.expose
def play_sound_effect(sound_name, volume=5, loop=False):
    """
    Plays a sound effect on the client's end through the Electron app.

    Args:
        sound_name (str): The name or identifier of the sound effect to play.
        volume (int): The volume level of the sound effect (1 to 10). Default is 5.
        loop (bool): Whether the sound effect should loop continuously. Default is False.
    """
    print(f"[DEBUG] play_sound_effect called with sound_name='{sound_name}', volume={volume}, loop={loop}")

    # Call the JavaScript function in the Electron app to play the sound
    eel.playSoundEffect(sound_name, volume, loop)

#player = Player("Goredawn the Gladiator")


#player.connect()
#player.add_subscriber(send_ai_response)

# Start the application
eel.start('index.html', mode='electron')

