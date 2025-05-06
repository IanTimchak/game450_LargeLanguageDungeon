

from util.dndnetwork import DungeonMasterServer, PlayerClient
from util.llm_utils import TemplateChat
from util.ragu import ChromaDBClient as chroma, OllamaEmbeddingFunction
from util.tool_handler import ToolHandler


class DungeonMaster:
    def __init__(self):
        self.game_log = ['START']
        self.server = DungeonMasterServer(self.game_log, self.dm_turn_hook)
        self.chat = TemplateChat.from_file('util/templates/dm_bryan.json', 
                                           sign='hellogamers',
                                           process_response=TemplateChat.process_response,
                                           dungeon_master=self)
        self.start = True
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

        # Process the DM's message and update the game log
        self.rag.add_documents([
            {
                'id': 'dm_message_' + str(len(self.game_log)),
                'text': dm_message,
                'metadata': {'role': 'dm'}
            }
        ])

        # print(f"[DEBUG] session_info: {self.rag.peek()}")

        # Return a message to send to the players for this turn
        return dm_message 

    # @tool_tracker
    # def process_function_call(self, function_call):
    #     name = function_call.name
    #     args = function_call.arguments

    #     if hasattr(self, name):
    #         method = getattr(self, name)  # Get the method by name
    #         return method(**args)  # Call the method with the provided arguments
    #     else:
    #         raise AttributeError(f"Method '{name}' not found in DungeonMaster.")
    
    #Tool
    # def retrieve_session_info(self, query: str = "search") -> str:
    #     print(f'[DEBUG] retrieve_session_info called with query: {query}')
    #     documents = self.rag.query(query, 3)
    #     print(f'[DEBUG] Retrieved documents: {documents}')
    #     return "\n".join(documents[0])
    #     pass

    # #Tool
    # def default(self):
    #     print(f'[DEBUG] default tool called')
    #     return ""
    #     pass



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
    
    def add_subscriber(self, subscriber):
        self.client.add_subscriber(subscriber)

    def take_turn(self, message):
        self.client.send_message(message)
