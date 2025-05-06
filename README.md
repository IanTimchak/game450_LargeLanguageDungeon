# Large Language Dungeons

## Description
Large Language Dungeons is an AI-based dungeon master client that uses large language models to generate and manage text-based role-playing games. The client allows users to create and customize their own adventures, characters, and settings, while the AI provides dynamic storytelling and gameplay experiences.

## Features

- **AI Dungeon Master**: The AI generates storylines, quests, and NPCs based on user input and preferences.
- **Character Creation**: Users can create and customize their own characters, including attributes, skills, and backgrounds.
- **Dynamic Storytelling**: The AI adapts the story based on player choices and actions, providing a unique experience for each session.
- **Multi-player Support**: Players can join the same game session and interact with each other in real-time.
- **Customizable Settings**: Users can choose from various genres, themes, and settings for their adventures.



## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/IanTimchak/LLD.git
2. Install necessary dependencies
   ```bash
   npm install
   pip install ollama, chromadb, langchain, eel
3. Install [Ollama](https://ollama.com/), if it is not already on your system.
4. Pull the necessary models from Ollama.
   ```bash
   ollama pull llama3.2:latest nomic-embed-text
   ```

## Running the application
### Starting the Game Server
In order to start the game server, run `game.py` in a dedicated terminal.
Once it is running, a countdown will begin for all players to connect to
the server.

### Starting the Player Client
To start the player client, run `app.py` in a dedicated terminal. This will
launch an electron application to host the UI for interacting with the
LLM server. Input the host and port of the server (found in `dndnetwork.py`)
and your player name for the session. Do this within the server countdown, and
you will join the LLM server.
   