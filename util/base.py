from util.dndnetwork import DungeonMasterServer, PlayerClient
from util.llm_utils import TemplateChat
from util.ragu import ChromaDBClient as chroma, OllamaEmbeddingFunction
from util.tool_handler import ToolHandler
import os, json
from threading import Thread


# This function is responsible for compiling the sounds from the web/sounds directory
# It returns a string representation of the list of sound names (without extensions)
# This is used to send the sounds to the template for use in the game
def compile_sounds():
    sounds = []
    for filename in os.listdir('web/sounds'):
        if filename.endswith('.wav') or filename.endswith('.mp3'):
            sound_name = filename[:-4]  # Remove the extension
            sounds.append(sound_name)
    return str(sounds)[1:-1]

#Load the json file in utils tool_list and dump it/stringify it to sent to the template
def stringify_tools():
    with open('util/tool_list.json', 'r') as file:
        tools = json.load(file)
    return json.dumps(tools, indent=0)


class DungeonMaster:
    def __init__(self):
        self.game_log = ['START']
        self.server = DungeonMasterServer(self.game_log, self.dm_turn_hook)
        self.chat = TemplateChat.from_file('util/templates/MAIN_DM_TEMPLATE.json', 
                                           sign='hellogamers',
                                           process_response=TemplateChat.process_response,
                                           #provide a reference to the server for TemplateChat to use
                                           dungeon_master=self,
                                           sounds=compile_sounds(),
                                           tool_definitions=stringify_tools())
        self.start = True
        # Initialize the ChromaDB client as a member variable
        self.rag = chroma(
            collection_name='session_info',
            embedding_function=OllamaEmbeddingFunction(model_name='nomic-embed-text')
        )
        
        #Initialize the tool handler
        self.tool_handler = ToolHandler(self)


    def start_server(self):
        self.server.start_server()

    def dm_turn_hook(self):
        dm_message = ''
        # Do DM things here. You can use self.game_log to access the game log
        if self.start:
            dm_message = self.chat.start_chat()
            self.start = False
        else: 
            #Combine all of the strings in the action stack into a single string, non-list
            turn_string = ''
            for action in self.server.action_stack:
                turn_string += action + " "
            self.server.clear_action_stack()
            
            dm_message = self.chat.send(turn_string)

        # Adding the DM's message to the session_info collection
        # This is done in a separate thread to avoid blocking the main thread
        def add_to_rag(game_log, dm_message):
            self.rag.add_documents([
                {
                    'id': 'dm_message_' + str(len(game_log)),
                    'text': dm_message,
                    'metadata': {'role': 'dm'}
                }
            ]) 
        Thread(target=add_to_rag, args=(self.game_log, dm_message)).start()

        # print(f"[DEBUG] session_info: {self.rag.peek()}")

        # Return a message to send to the players for this turn

        #If the dm_message is an empty string, return the second to last message in the templatechat's messages
        if dm_message == '':
            dm_message = self.chat.messages[-2]['content']

        return dm_message 


class Player:
    def __init__(self, name):
        self.name = name
        self.client = PlayerClient(self.name)

    def connect(self):
        self.client.connect()

    def set_connection(self, host, port):
        self.client.set_connection(host, port)

    def unjoin(self):
        self.client.unjoin()
    
    def add_subscriber(self, subscriber, name):
        self.client.add_subscriber(subscriber, name)

    def take_turn(self, message):
        self.client.send_message(message)
