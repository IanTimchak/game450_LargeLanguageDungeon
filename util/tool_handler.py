
from util.llm_utils import tool_tracker, generate_single_response
import random, os, json
class ToolHandler:
    def __init__(self, DungeonMaster):
        self.network_model = DungeonMaster #Carries the DM Server variables and functions, such as rag

    @tool_tracker
    def process_function_call(self, function_call):
        name = function_call.name
        args = function_call.arguments

        if hasattr(self, name):
            method = getattr(self, name)  # Get the method by name
            return method(**args)  # Call the method with the provided arguments
        else:
            raise AttributeError(f"Method '{name}' not found in DungeonMaster.")
    
    #RAG
    def retrieve_session_info(self, query: str = "search") -> str:
        print(f'[DEBUG] retrieve_session_info called with query: {query}')
        documents = self.network_model.rag.query(query, 3)
        print(f'[DEBUG] Retrieved documents: {documents}')
        return "\n".join(documents[0])

    #Default run tool if no other tool is called, prevents the LLM from spamming tool calls
    def default(self):
        print(f'[DEBUG] default tool called')
        return ""
    
    #Roll dice
    def roll_dice(self, player: str, max_roll: int, min_roll: int = 1, quantity: int = 1, modifier: int = 0) -> dict:
        """
        Simulates rolling dice for skill checks, combat, or other game mechanics.

        Args:
            max_roll (int): The maximum roll value.
            min_roll (int): The minimum roll value (default is 1).
            quantity (int): The number of dice to roll (default is 1).
            modifier (int): A modifier to add or subtract from the total roll (default is 0).

        Returns:
            dict: A dictionary containing the individual rolls, total roll, and modifier.
        """
        if min_roll > max_roll:
            return "invalid input parameters. Please disregard this message and prompt the players for clarification."
        if quantity < 1:
            return "invalid input parameters. Please disregard this message and prompt the players for clarification."

        rolls = [random.randint(min_roll, max_roll) for _ in range(quantity)]
        total = sum(rolls) + modifier

        print(f'[DEBUG] roll_dice called with max_roll={max_roll}, min_roll={min_roll}, quantity={quantity}, modifier={modifier}')
        print(f'[DEBUG] Rolls: {rolls}, Total (with modifier): {total}')

        #Return a string that includes the player and the rolled value.
        return f"Player '{player}' rolled {quantity}d{max_roll} with a modifier of {modifier}. Rolls: {rolls}, Final total: {total}"
    
    #generate event
    def generate_event(self, prompt: str, complexity: int) -> str:
        """
        Generates a unique event or scenario based on the provided input prompt.

        Args:
            prompt (str): A brief description or idea to base the event on.
            complexity (int): The complexity level of the event (e.g., 1 for simple, 5 for highly detailed).

        Returns:
            str: A generated event description.
        """
        if complexity < 1 or complexity > 5:
            return "invalid input parameters. Please disregard this message and prompt the players for clarification."

        print(f'[DEBUG] generate_event called with prompt="{prompt}" and complexity={complexity}')

        # Use the network model to generate the event
        event = generate_single_response(
            template_file='util/templates/event_generator.json',
            prompt=prompt,
            complexity=str(complexity),
        )
        #print(f'[DEBUG] Generated event: {event}')

        return event


    #generate_new_npc
    def generate_new_npc(self, role: str, background: str) -> str:
        """
        Generates a random NPC description with personality traits, appearance, and role.

        Args:
            role (str): The role of the NPC (e.g., 'merchant', 'villager', 'warrior').
            background (str): A brief background or story for the NPC.

        Returns:
            str: A generated NPC description.
        """
        if not role or not background:
            return "invalid input parameters. Please provide both role and background."

        print(f'[DEBUG] generate_new_npc called with role="{role}" and background="{background}"')
        


        # Use the network model to generate the NPC
        npc_description = generate_single_response(
            template_file='util/templates/npc_generator.json',
            prompt="Please give me a response.",
            role=role,
            background=background,
        )
        print(f'[DEBUG] Generated NPC: {npc_description}')

        return npc_description
    
    #retrieve_active_player_sheets
    def retrieve_active_player_sheets(self, include_inventory: bool, include_stats: bool, include_skills: bool) -> str:
        """
        Retrieves all active player character sheets for the current session.

        Args:
            include_inventory (bool): Whether to include the players' inventory details.
            include_stats (bool): Whether to include the players' stats.
            include_skills (bool): Whether to include the players' skills.

        Returns:
            str: A stringified JSON containing the filtered player sheets.
        """
        player_sheets_folder = 'player_sheets'  # Folder containing player sheet JSON files
        player_sheets_data = []

        print(f'[DEBUG] retrieve_active_player_sheets called with include_inventory={include_inventory}, include_stats={include_stats}, include_skills={include_skills}')

        # Iterate through all JSON files in the player_sheets folder
        for filename in os.listdir(player_sheets_folder):
            if filename.endswith('.json'):
                file_path = os.path.join(player_sheets_folder, filename)
                with open(file_path, 'r') as file:
                    player_data = json.load(file)

                    # Filter the data based on the parameters
                    filtered_data = {}
                    if include_inventory and 'inventory' in player_data:
                        filtered_data['inventory'] = player_data['inventory']
                    if include_stats and 'stats' in player_data:
                        filtered_data['stats'] = player_data['stats']
                    if include_skills and 'skills' in player_data:
                        filtered_data['skills'] = player_data['skills']

                    # Add the filtered data to the result list
                    player_sheets_data.append({
                        "player_meta": player_data["player_meta"],
                        "data": filtered_data
                    })

        # Convert the result to a stringified JSON
        result = json.dumps(player_sheets_data, indent=2)
        print(f'[DEBUG] Retrieved player sheet data: {result}')

        return result
    
    #play_sound_effect
    def play_sound_effect(self, sound_name: str, volume: int = 5, loop: bool = False) -> str:
        """
        Plays a sound effect on the user client.

        Args:
            sound_name (str): The name or identifier of the sound effect to play (e.g., 'dice_roll', 'sword_clash').
            volume (int): The volume level of the sound effect (e.g., 1 for low, 10 for maximum). Default is 5.
            loop (bool): Whether the sound effect should loop continuously. Default is False.

        Returns:
            str: A confirmation message indicating the sound effect was broadcasted.
        """
        if not sound_name:
            return "invalid input parameters. Please provide a valid sound_name."

        if volume < 1 or volume > 10:
            return "invalid input parameters. Volume must be between 1 and 10."

        print(f'[DEBUG] play_sound_effect called with sound_name="{sound_name}", volume={volume}, loop={loop}')

        # Prepare the instruction to broadcast to all clients
        instruction = {
            "action": "play_sound_effect",
            "parameters": {
                "sound_name": sound_name,
                "volume": volume,
                "loop": loop
            }
        }

        # Use the network model to broadcast the instruction
        self.network_model.server.broadcast_event(instruction)

        print(f'[DEBUG] Sound effect instruction broadcasted: {instruction}')

        return f"Sound effect '{sound_name}' with volume {volume} and loop={loop} broadcasted successfully."

# # #generate new npc
# tool_handler = ToolHandler(None)
# tool_handler.generate_new_npc(role="merchant", background="a mysterious traveler from the east")