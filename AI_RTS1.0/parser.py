
# parser.py
import re
import constants

def parse_llm_command(raw_text):
    """
    Parses the raw text pasted from the LLM and extracts the game commands.
    Returns a dictionary with 'status', 'target', 'action', and 'remarks'.
    """
    # Initialize the default response dictionary
    parsed_data = {
        "status": "error",
        "target": None,
        "action": None,
        "remarks": None,
        "message": ""
    }

    # Regex patterns 
    # We use flexible spacing (\s*) to catch formatting quirks from the LLM
    target_pattern = r"TARGET\s*UNIT:\s*(.+)"
    action_pattern = r"ACTION:\s*(.+)"
    # DOTALL allows the remarks regex to capture multiple lines of text
    remarks_pattern = r"REMARKS:\s*(.+)"

    try:
        # 1. Extract and format the Target Unit
        target_match = re.search(target_pattern, raw_text, re.IGNORECASE)
        if target_match:
            # Strip whitespace and force uppercase to match our constants
            parsed_data["target"] = target_match.group(1).strip().upper()
        else:
            parsed_data["message"] = "Error: Could not find 'TARGET UNIT'."
            return parsed_data

        # 2. Extract and validate the Action
        action_match = re.search(action_pattern, raw_text, re.IGNORECASE)
        if action_match:
            extracted_action = action_match.group(1).strip()
            
            # Create a lowercase list of valid actions for forgiving validation
            valid_actions_lower = [a.lower() for a in constants.VALID_ACTIONS]
            
            if extracted_action.lower() in valid_actions_lower:
                # Map it back to the exact constant string the engine expects
                index = valid_actions_lower.index(extracted_action.lower())
                parsed_data["action"] = constants.VALID_ACTIONS[index]
            else:
                parsed_data["message"] = f"Error: LLM hallucinated an invalid action: '{extracted_action}'"
                return parsed_data
        else:
            parsed_data["message"] = "Error: Could not find 'ACTION'."
            return parsed_data

        # 3. Extract the Remarks (Diary entry)
        remarks_match = re.search(remarks_pattern, raw_text, re.IGNORECASE | re.DOTALL)
        if remarks_match:
            # Clean up newlines so it renders nicely in our Pygame UI
            raw_remarks = remarks_match.group(1).strip()
            parsed_data["remarks"] = " ".join(raw_remarks.split())
        else:
            parsed_data["remarks"] = "No remarks provided by the Queen." # Fallback

        # If it passes all checks, flag it as a success for the game loop
        parsed_data["status"] = "success"
        parsed_data["message"] = "Command parsed and validated successfully."

    except Exception as e:
        parsed_data["message"] = f"Unexpected parsing error: {str(e)}"

    return parsed_data

# ==========================================
# QUICK TEST BLOCK (For your devs to verify)
# ==========================================
if __name__ == "__main__":
    sample_input = """
    TARGET UNIT: QUEEN
    ACTION: Produce Workers
    REMARKS: Our food
    storage is low. We should increase worker capacity to increase our
    chance of survival.
    """
    
    result = parse_llm_command(sample_input)
    print("Test Result:")
    for key, value in result.items():
        print(f"{key.capitalize()}: {value}")