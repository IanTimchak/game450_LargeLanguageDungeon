# Large Language Dungeons

## Description
Large Language Dungeons is an AI-based dungeon master client that uses large language models to generate and manage text-based role-playing games. The client allows users to create and customize their own adventures, characters, and settings, while the AI provides dynamic storytelling and gameplay experiences.

## Features

- **AI Dungeon Master**: The AI generates storylines, quests, and NPCs based on user input and preferences.
- **Character Creation**: Users can create and customize their own characters, including attributes, skills, and backgrounds.
- **Dynamic Storytelling**: The AI adapts the story based on player choices and actions, providing a unique experience for each session.
- **Multi-player Support**: Players can join the same game session and interact with each other in real-time.



## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/IanTimchak/game450_LargeLanguageDungeon.git
2. Install necessary dependencies
   ```bash
   npm install
   pip install -r requirements.txt
3. Install [Ollama](https://ollama.com/), if it is not already on your system.
4. Pull the necessary models from Ollama.
   ```bash
   ollama pull llama3.2:latest nomic-embed-text
   ```

## Running the application
1. Run `app.py` in a dedicated terminal.
   - This will launch an electron application that brings you to the server connection screen. Input the server host and port (defined in `dndnetwork.py`) and your player name for the session.
     - To change the host and port the server runs on, update the host and port information in line 20 of `dndnetwork.py`.
   - **DON'T click join yet**.
2. Run `game.py` in a dedicated terminal.
   - This starts up the game server which hosts the LLM and all other game logic. Once this starts up, a countdown begins for all players to join the game.
3. Return to the electron app and click **JOIN**.
   - The server connection screen will be replaced by the chat window where you interact with the Dungeon Master LLM. Once the countdown ends, the DM will make its first response.