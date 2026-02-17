# llm_api.py
import threading
import requests
import constants

class OllamaConnector:
    def __init__(self, model_name="llama3"): # Change to whichever model you have pulled in Ollama
        self.model_name = model_name
        self.url = "http://localhost:11434/api/generate"
        self.is_generating = False
        self.response_data = None
        self.error_message = None

    def generate_prompt(self, queen):
        """Constructs the prompt dynamically using current game state."""
        prompt = f"""WARNING: Your response is being read by a Pygame engine parser. You must follow these guidelines strictly, or the game loop will fail. Do not return any other dialogue or conversational filler outside of the requested format.

You are a Hive Mind. You control a growing network of Hives. Your goal is to manage your resources (Food), grow your population, and expand your territory.

CURRENT GAME STATE:
Awaiting orders for Queen {queen.queen_id}.
Hive {queen.hive.hive_id} Stats:
- Food Storage: {queen.hive.food}
- Workers: {queen.hive.workers} (Produce 2 food per turn. Cost: {constants.COST_WORKER})
- Warriors: {queen.hive.warriors} (Cost: {constants.COST_WARRIOR})
- Queens: {len(queen.hive.queens)} (Cost: {constants.COST_QUEEN})

VALID ACTIONS (Choose exactly ONE):
* {constants.ACTION_GATHER_FOOD}
* {constants.ACTION_PRODUCE_WORKERS}
* {constants.ACTION_PRODUCE_WARRIORS}
* {constants.ACTION_PRODUCE_QUEEN}

REQUIRED OUTPUT FORMAT:
TARGET UNIT: QUEEN
ACTION: [Insert exactly one valid action]
REMARKS: [Your diary. State your strategic thoughts here.]
"""
        return prompt

    def _make_request(self, prompt):
        """The blocking HTTP call that runs in the background thread."""
        self.is_generating = True
        self.response_data = None
        self.error_message = None
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False # We wait for the full response for the MVP
        }
        
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            data = response.json()
            self.response_data = data.get("response", "")
        except Exception as e:
            self.error_message = f"Ollama Connection Error: {str(e)}"
        finally:
            self.is_generating = False

    def request_action(self, queen):
        """Triggered by the UI button. Spawns a thread so Pygame doesn't freeze."""
        if self.is_generating:
            return # Prevent spam-clicking the button
            
        prompt = self.generate_prompt(queen)
        
        # Start the API call in a daemon thread
        thread = threading.Thread(target=self._make_request, args=(prompt,))
        thread.daemon = True 
        thread.start()