# GAME 450 Final Project
## Bryan Caskey, 3/27/25

### List of Base System Functionality, Requirement 1
- Scene Description
- Plot Generation
  - Ultimate Goal for Adventures; Win Condition
- Trading/Merchants
- NPC Dialogue
- Rudimentary Combat System 
  - Needs Defined Further, may be axed due to limitations of LLMs
- Inventory Management
- UI
- Session/Plot Persistance
- Monster Manual 
  - Enemy Database with RAG
- Reading the Player's Character Sheet
  - Stored as an external file the player can edit.
- 

### Requirements 2-7
- Needs to implement **RAG**
  
- Needs to implement **multi-step reasoning**
  
- Needs to implement **Tool usage**
  - [ ] Template Loading Tool
    - PARAMS: Template Name, Context, tbd.
  - [ ] Image Generation Tool
  - [x] Dice Rolling Tool / Skill Check Tool
  - [x] Story Recall Tool (RAG)
  - [x] Add chunk to RAG database
  - [ ] Enemy/Player information lookup
  - [x] session info loading
  - [x] session summary generation
  - [x] side quest/event generator
  - [ ] text to speech
  - [ ] loot generator
  - [ ] Rule quereying
    - PURPOSE: Query the D&D rule book for information and rules found in D&D5e
  
- Needs to implement **An additional thing**
  
- Needs well structured code as well as understandable and efficient promt engineering and model parameters.





Can't force user client to quit.
Infinite loop of attempting to do an operation on something that is not a socket WIN ERROR 1038


## Notes for next session
- Since the LLM favours the most recent message to act upon, the player who goes last will receive more attention. Look into a way of combining the inputs to avoid this problem. 

- [Found a monster manual](https://gist.github.com/tkfu/9819e4ac6d529e225e9fc58b358c3479)

- Implement tool calls defined in `dm_bryan.json`
- Fill out report found in `Project.md`
- Fill out Readme instructions for running the project.
- Add documentation where necessary.
- Find a way to implement multi-step reasoning.
- Fine tune model parameters and prompt
- Clean up repository root (including removing this file before submission)
- 



## Project Files
### game.py

- imports `base.py`
- initialize DM (imported from `base.py`)
- start server

### base.py

- imports `dndnetwork.py` & `llm_utils.py`
- Defines DungeonMaster class
  - start_server()
    - Called in `game.py`, implemented in `dndnetwork.py`
  - dm_turn_hook()
    - this is where the AI processes happen.
    - self.chat is defined in `llm_utils.py`
- Defines Player class
  - 




Update Readme.md so that it includes known errors that we know about and workarounds to some issues
  -> Game not being able to be force closed
      S: close the terminal it is running in.

  -> whatever else u can think of to cover our app

Finalize project.md, go over the system prompt and notice what I changed for prompt engineering. 

Clean up repo

Make sure everything is working so it works on submission