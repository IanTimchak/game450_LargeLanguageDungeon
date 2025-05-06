
from util.llm_utils import tool_tracker

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
    
    #Tool
    def retrieve_session_info(self, query: str = "search") -> str:
        print(f'[DEBUG] retrieve_session_info called with query: {query}')
        documents = self.network_model.rag.query(query, 1)
        print(f'[DEBUG] Retrieved documents: {documents}')
        return "\n".join(documents[0])

    #Tool
    def default(self):
        print(f'[DEBUG] default tool called')
        return ""



    