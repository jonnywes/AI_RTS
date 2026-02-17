# engine.py
import constants

class Queen:
    def __init__(self, hive, queen_id):
        self.hive = hive
        self.queen_id = queen_id
        self.action_queued = None

class Hive:
    def __init__(self, hive_id, x, y):
        self.hive_id = hive_id
        self.x = x
        self.y = y
        self.food = constants.STARTING_FOOD
        self.workers = constants.STARTING_WORKERS
        self.warriors = constants.STARTING_WARRIORS
        self.queens = []
        self.gathering_modifier = 1.0
        self.diaries = []  # Stores the LLM "Remarks" for the UI to display

class Map:
    def __init__(self):
        self.hives = []

class GameEngine:
    def __init__(self):
        self.map = Map()
        self.turn_number = 1
        self.active_queens_queue = [] # Queens waiting for LLM input this turn
        self._next_hive_id = 1
        self._next_queen_id = 1
        
        # Initialize the MVP starting state
        self._create_initial_hive()

    def _create_initial_hive(self):
        # Place the first hive roughly in the center of the map panel
        first_hive = Hive(self._next_hive_id, constants.MAP_WIDTH // 2, constants.MAP_HEIGHT // 2)
        self._next_hive_id += 1
        
        first_queen = Queen(first_hive, self._next_queen_id)
        self._next_queen_id += 1
        
        first_hive.queens.append(first_queen)
        self.map.hives.append(first_hive)

    def start_turn(self):
        """Phase 1: Maintenance and Setup"""
        self.active_queens_queue.clear()
        
        for hive in self.map.hives:
            # 1. Calculate and deduct upkeep
            total_upkeep = (len(hive.queens) * constants.UPKEEP_QUEEN) + \
                           (hive.warriors * constants.UPKEEP_WARRIOR) + \
                           (hive.workers * constants.UPKEEP_WORKER)
            
            hive.food -= total_upkeep
            
            # Dev Note: MVP starvation logic - simply clamp to 0 for now. 
            # Later, we can add logic to kill units if food < 0.
            if hive.food < 0:
                hive.food = 0
            
            # 2. Reset modifiers
            hive.gathering_modifier = 1.0
            
            # 3. Queue queens for the Action Phase
            for queen in hive.queens:
                self.active_queens_queue.append(queen)

    def process_queen_command(self, queen, parsed_data):
        """Phase 2: Queue the validated LLM action and save the diary."""
        queen.action_queued = parsed_data['action']
        
        # Format the diary entry for the UI log
        log_entry = f"Turn {self.turn_number} | Hive {queen.hive.hive_id} | Action: {parsed_data['action']}\nRemarks: {parsed_data['remarks']}"
        queen.hive.diaries.append(log_entry)

    def end_turn(self):
        """Phase 3: Resolution - Execute actions, gather resources, spawn units."""
        for hive in self.map.hives:
            for queen in hive.queens:
                action = queen.action_queued
                
                # Execute Action based on Enums
                if action == constants.ACTION_GATHER_FOOD:
                    # Apply a math multiplier for the gathering phase below
                    hive.gathering_modifier = constants.GATHER_RATE_BOOSTED
                    
                elif action == constants.ACTION_PRODUCE_WORKERS:
                    if hive.food >= constants.COST_WORKER:
                        hive.food -= constants.COST_WORKER
                        hive.workers += 1
                        
                elif action == constants.ACTION_PRODUCE_WARRIORS:
                    if hive.food >= constants.COST_WARRIOR:
                        hive.food -= constants.COST_WARRIOR
                        hive.warriors += 1
                        
                elif action == constants.ACTION_PRODUCE_QUEEN:
                    if hive.food >= constants.COST_QUEEN:
                        hive.food -= constants.COST_QUEEN
                        # MVP: Spawn a new Hive nearby to represent expansion
                        new_hive = Hive(self._next_hive_id, hive.x + 80, hive.y + 80)
                        self._next_hive_id += 1
                        
                        new_queen = Queen(new_hive, self._next_queen_id)
                        self._next_queen_id += 1
                        
                        new_hive.queens.append(new_queen)
                        self.map.hives.append(new_hive)
                
                # Clear the action for the next turn
                queen.action_queued = None

            # Gather Food (Base * Count * Modifier)
            gathered_food = hive.workers * (constants.GATHER_RATE_BASE + hive.gathering_modifier)
            hive.food += int(gathered_food)
            hive.gathering_modifier = 0 # Reset modifier after gathering

        # Increment turn counter
        self.turn_number += 1
