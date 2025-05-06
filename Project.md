# Project Report: LargeLanguageDungeon

**<u>Team</u>**: Bryan Caskey & Ian Timchak

**<u>Class</u>**: CMPSC441/GAME450

**<u>Due</u>**: 11:59PM, May 6

## 1: Base System Functionality

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

The following sections will go into more detail about how some of the prior scenarios were implemented.

## 2: Prompt Engineering and Model Parameters

Our project has 3 templates, with 1 being the main DM and the other 2 being called upon with tool calls. The templates are as follows:



**MAIN_DM_TEMPLATE**

- Purpose: This template is the main DM instance, and is what the players will be interacting with. It is in charge of driving the plot, responding to player input, making calls to tools when necessary, and handling input from those tool calls.

- Parameters:
  
  - temerature: We set the temperature value to a low `0.2`. We felt that a low temperature makes sence for this template, as it is both in charge of keeping track of the story and, more importantly, making tool calls that require a structured format.

- Prompts:
  
  - The prompt for the main DM template covers the many duties that the DM is supposed to handle, and addresses many problems that the DM consistantly displayed over the course of the project. Here is a breakdown of the prompt:
  
  - First, It tells the DM to intruduce itself as the DM and ask the players for introductions, and remember those as the players that will be playing in the session. 
  
  - For our team, the DM had a habit of hallucinating extra players, so the next portion of the system prompt addresses this problem.
  
  - Next, we tell the DM not to value any one player's response over another's.
  
  - Following that, we reinforce the idea that the DM is narrating a fictional setting, because toward the end of the project the llama3.2 model's sensitive content filter starting acting much more aggressively and wouldn't allow anything it considered "violent," such as Dungeon's and Dragon's combat.
  
  - After addressing all of those problems, the next section focuses on defining a three section format for the DM's output.
  
  - Finally, the last portion of the system prompt (after the newlines) focuses on the tool calls that the model can make.

**event_generator**

- Purpose: this template is 

## 3: Tool Usage

- Scenario 5 was achieved through a pair of RAG implementation and a custom tool call. Using our RAG database that includes previous DM messages, we defined a tool call titled `retrieve_session_info` that queries the database for information relevant to the search string it provides. The effect of this is that the DM has an enhanced ability to recall prior information from earlier in a session.

- Scenario 6 can be accomplished using the `roll_dice` tool call. The DM model has access to the `player`, `max_roll`, `min_roll`, `quantity`, and `modifier` parameters. These control who the roll is for (in the case of multiple players), the highest and lowest values on the die, the amount of dice being rolled, and the modifier to the roll if any (such as a silver sword doing +1 damage against vampires).

- Scenario 7 is possible through a tool call simply named `generate_event`. This event activates a separate LLM template, and asks it to generate a new event based upon a context string passed to it by the DM and a desired complexity level.

- In the same fashion as 7, scenario 8 is accomplished through the tool call `generate_npc`. This function calls another separate LLM template designed for creating new NPCs, and asks it to generate one based off of the NPCs intended role (such as warrior, chef, villain, king, etc.) and a background to refine the model's output.

- Scenario 9 is handled by the tool call `play_sound_effect`, which gives the DM the ability to select a sound file, and control the relative volume of it as well as if it should loop or not.

## 4: Planning & Reasoning

## 5: RAG Implementation

- Scenario 5 was achieved through a pair of RAG implementation and a custom tool call. After the DM generates its message every turn, and before the DM sends out messages to the players' clients, its message is chunked and stored in a rag database. Internally, the ChromaDB client is a member object of the DungeonMaster object, and is labeled `DungeonMaster.rag`. Together with our retrieval tool call, this provides a long term memory to the DM.

## 6: Additional Tools or Innovations

For our additional innovation, we have a simple and easy to use UI for players to interact with the AI model. When you launch the app, it brings you first to a connection screen, where you can choose the server host and port information, as well as your name for the session. Once you connect, you will be in a sleek, scrollable, and readable chat window with the AI model.

We also have our audio tool call, which allows the DM to play sound effects that fit the current situation of the game. These sound effects play on the players' client machines when the DM sends out its response.
