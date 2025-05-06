# Player Sheets Guide

## Overview
Player sheets are an essential part of the game, allowing you to track each player's stats, inventory, and skills. These sheets are stored as JSON files in the `player_sheets` folder. However, if you do not plan to use character sheets for each player or do not wish to maintain them throughout the game, **ensure that the `player_sheets` folder is empty**.

## Using Character Sheets
1. **File Naming**:
   - Each player's character sheet should be saved as a JSON file in the `player_sheets` folder.
   - Use a clear and unique name for each file (e.g., `player1.json`, `wizard.json`).

2. **Maintaining Sheets**:
   - Update the character sheets regularly to reflect changes in stats, inventory, or skills during the game.
   - Ensure that the JSON structure matches the expected format for proper functionality.

3. **No Character Sheets**:
   - If you do not plan to use character sheets, simply leave the `player_sheets` folder empty.
   - The game will not function correctly if there is a mismatch between the data in character sheets and the player names in the application.

## Using the Template
A template file, `empty_sheet.json`, is provided in the `templates` folder to help you create new character sheets. Follow these steps to use it:
1. Navigate to the `templates` folder and locate the `empty_sheet.json` file.
2. Copy the file into the `player_sheets` folder.
3. Rename the file to match the player's character name or identifier.
4. Open the file in a text editor and fill in the necessary details (e.g., stats, inventory, skills).
