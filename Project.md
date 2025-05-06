# Project Report: LargeLanguageDungeon

**<u>Team</u>**: Bryan Caskey & Ian Timchak

**<u>Class</u>**: CMPSC441/GAME450

**<u>Due</u>**: 11:59PM, May 6

## 1: Base System Functionality

### This section details a comprehensive list of scenarios that our AI model is equipped to handle:

1. Generating and describing a setting in a fictional world for the players (the users) to interact with.

2. Handling dialogue with various spontaniously created NPCs as gameplay demands.

3. Generation of story/plot events for the players to follow along with.

4. Maintaining the story and state of the game.

5. Recalling previously mentioned information that may be relevent to the story or gameplay.

6. Performing dice rolls for skill checks, battles, and other such occurances in game.

7. Randomly generating new events for the players to interact with.

8. Creating new, interesting, and fleshed out NPCs.

9. Playing sounds and music for the players.

### The following sections will go into more detail about how some of the prior scenarios were implemented.

## 2: Prompt Engineering and Model Parameters

## 3: Tool Usage

- Scenario 5 was achieved through a pair of RAG implementation and a custom tool call. Using our RAG database that includes previous DM messages, we defined a tool call titled `retrieve_session_info` that queries the database for information relevant to the search string it provides. The effect of this is that the DM has an enhanced ability to recall prior information from earlier in a session.

## 4: Planning & Reasoning

## 5: RAG Implementation

- Scenario 5 was achieved through a pair of RAG implementation and a custom tool call. After the DM generates its message every turn, and before the DM sends out messages to the players' clients, its message is chunked and stored in a rag database. Internally, the ChromaDB client is a member object of the DungeonMaster object, and is labeled `DungeonMaster.rag`. Together with our retrieval tool call, this provides a long term memory to the DM.

## 6: Additional Tools or Innovations

For our additional innovation, we have a simple and easy to use UI for players to interact with the AI model. When you launch the app, it brings you first to a connection screen, where you can choose the server host and port information, as well as your name for the session. Once you connect, you will be in a sleek, scrollable, and readable chat window with the AI model.
