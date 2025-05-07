# Large Language Dungeons

## Description
Large Language Dungeons is an AI-based dungeon master client that uses large language models to generate and manage text-based role-playing games. The client allows users to create and customize their own adventures, characters, and settings, while the AI provides dynamic storytelling and gameplay experiences.

## Base System Functionality

This section details a comprehensive list of scenarios that our AI model is equipped to handle:

1. Generating and describing a setting in a fictional world for the players (the users) to interact with.
  
2. Handling dialogue with various spontaniously created NPCs as gameplay demands.
  
3. Generation of story/plot events for the players to follow along with.
  
4. Maintaining the story and state of the game.
  
5. Recalling previously mentioned information that may be relevent to the story or gameplay.
  
6. Performing dice rolls for skill checks, battles, and other such occurances in game.
  
7. Randomly generating new events for the players to interact with.
  
8. Creating new, interesting, and fleshed out NPCs.
  
9. Playing sounds for the players.
  

Naturally, our system preserves the properties and interactions that you would expect when interacting with a LLM.



## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/IanTimchak/game450_LargeLanguageDungeon.git
2. Install necessary dependencies  
   Ensure that the latest versions of python(3.12.9) and node(20.13.1) are installed.
   ```bash
   npm install
   pip install -r requirements.txt
3. Install [Ollama](https://ollama.com/), if it is not already on your system.
4. Pull the necessary models from Ollama.
   ```bash
   ollama pull llama3.2:latest
   ollama pull nomic-embed-text
   ollama pull qwen3:1.7b
   ```

## Running the application
1. Ensure that the working directory in your terminal is set to be the true root of the application, where `app.py` and `game.py` are in the highest level folder. The app will not run correctly if you are trying to initiate these scripts from another directory.
1. Run `app.py` in a dedicated terminal.
   - This will launch an electron application that brings you to the server connection screen. Input the server host and port (defined in `dndnetwork.py`) and your player name for the session.
   - **DON'T click join yet**.
2. Run `game.py` in a dedicated terminal.
   - This starts up the game server which hosts the LLM and all other game logic. Once this starts up, a countdown begins for all players to join the game.
   - To change the host and port the server runs on, update the host and port information in line 20 of `dndnetwork.py`. If you are attempting to play with people from other networks and devices, you must ensure that your network is properly port forwarded.
3. Return to the app and click **JOIN**.
   - The server connection screen will be replaced by the chat window where you interact with the Dungeon Master LLM. Once the countdown ends, the DM will make its first response.

## Character Sheets

Our app allows the players to maintain their own character sheets that will be referenced throughout the course of the story. For more information on how to use these, please refer to the [README](player_sheets/templates/README.md) file in the player_sheets folder. It is important to note that if you won't be maintaining character sheets throughout your gameplay, there must be no character sheets within the player_sheets folder, as it will overwrite the character information you introduce with the AI agent.

## Known Issues and Workarounds

1. Game server not ending correctly
   - When the clients completely disconnect from the server, there are some errors that prevent the process from being force killed from the terminal, or naturally ending. This is a limitation of the original server code that we never got around to fixing. 
     - To end the game server process, please fully close the terminal from VSCode, or however else it is being run.
2. Host refusing to connect to the client
   - If your client does not recieve messages from the server after attempting to join and you are recieving an error that says the host refused connection, try changing the port that the server is being hosted on.