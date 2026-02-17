# main.py
import pygame
import constants
from engine import GameEngine
from ui import UIManager
from parser import parse_llm_command
from llm_api import OllamaConnector

def main():
    # Initialize the core modules
    engine = GameEngine()
    ui = UIManager()
    
    # Initialize the Ollama Connector (Ensure your local model name matches)
    ollama = OllamaConnector(model_name="llama3") 
    
    clock = pygame.time.Clock()
    
    running = True
    error_message = ""
    
    # Kick off the very first turn
    engine.start_turn()

    while running:
        prompt_message = ""
        current_queen = None
        
        # 1. Check the State Machine
        if engine.active_queens_queue:
            current_queen = engine.active_queens_queue[0]
            prompt_message = f"Turn {engine.turn_number}: Awaiting orders for Queen {current_queen.queen_id} (Hive {current_queen.hive.hive_id})"
        else:
            engine.end_turn()
            engine.start_turn()
            error_message = "" 
            continue 

        # 2. Handle UI Events
        # We now unpack TWO variables from handle_events
        submitted_text, action_signal = ui.handle_events(pygame.event.get())
        
        if submitted_text == "QUIT":
            running = False
            
        # 3. Trigger Ollama Call
        elif action_signal == "OLLAMA_CLICK" and current_queen and not ollama.is_generating:
            # Clears any old errors and starts the background thread
            error_message = "" 
            ollama.request_action(current_queen)

        # 4. Check for Ollama Thread Completion
        if ollama.response_data:
            # Ollama finished! Treat its output exactly like pasted text.
            parsed_data = parse_llm_command(ollama.response_data)
            
            if parsed_data["status"] == "success":
                engine.process_queen_command(current_queen, parsed_data)
                engine.active_queens_queue.pop(0)
                error_message = ""
            else:
                error_message = parsed_data["message"]
                
            # Clear the response data so we don't process it twice
            ollama.response_data = None
            
        # Catch connection errors from the API thread
        if ollama.error_message:
            error_message = ollama.error_message
            ollama.error_message = None

        # 5. Handle Manual Text Submission (Fallback/Override)
        if submitted_text is not None and current_queen and not ollama.is_generating:
            parsed_data = parse_llm_command(submitted_text)
            
            if parsed_data["status"] == "success":
                engine.process_queen_command(current_queen, parsed_data)
                engine.active_queens_queue.pop(0)
                error_message = ""
            else:
                error_message = parsed_data["message"]

        # 6. Render the Screen
        # Pass the is_generating flag so the UI knows to draw the "Thinking..." state
        ui.draw(engine, prompt_message, error_message, is_generating=ollama.is_generating)
        
        # 7. Tick the Clock
        clock.tick(constants.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()