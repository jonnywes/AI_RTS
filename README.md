#AI SWARM: An LLM-Powered Autonomous Strategy Game

My goal was to create a game that my local LLM could "play", while I observe it and it keeps a journal.

This game is an experimental real-time/turn-based strategy game built in Python and Pygame. Instead of manually moving units or building structures, **you act as a strategic advisor to a Large Language Model (LLM)**. 

Powered by a local Ollama instance, the LLM analyzes the game state, reads threat reports, and sets high-level macro-objectives (Economy, Aggressive, Balanced) for its network of Queens. The Queens then autonomously execute those strategies to wipe out a hardcoded enemy faction.

I recommend reading the Journal.txt file after each game to see what the LLM was thinking.
## Key Features

* **Local LLM Integration:** Completely private and free AI decision-making using [Ollama](https://ollama.com/). By default, it uses the `llama3` model, but can be easily swapped.
* **Three-Tier Memory Architecture:** The AI agent learns and adapts using a sophisticated memory system:
    * *Ancestral Memory:* At the end of every game, the AI writes a post-mortem of its victory/defeat that is passed into the next game, creating an evolutionary learning loop.
    * *Long-Term Journal:* A persistent, turn-by-turn history of the AI's thoughts during the current match.
    * *Short-Term Buffer:* A rolling log of the last 5 turns to prevent strategic flip-flopping.
* **Human-in-the-Loop "Advisor" System:** Type strategic advice directly into the game UI to guide the AI's next move without directly controlling units.
* **Zero-Player Auto-Play:** Sit back and watch the AI fight. Includes a 3-strike failsafe system that automatically retries if the LLM hallucinates or breaks formatting.
* **Abstract Macro-Combat:** Complex math simplified into grand strategy, featuring an inherent "Defender's Advantage" to punish mindless zerg-rushes.
* **Custom Sprite Fallbacks:** Supports custom PNG graphics for Hives and maps, seamlessly falling back to clean geometric shapes if art assets are missing.

---

## Prerequisites

Before you begin, ensure you have met the following requirements:
1.  **Python 3.x** installed.
2.  **Ollama** installed and running on your local machine.
3.  An Ollama model pulled locally. (e.g., Run `ollama run llama3` in your terminal).

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/hive-mind-rts.git](https://github.com/yourusername/hive-mind-rts.git)
   cd hive-mind-rts

Create a Virtual Environment (Optional but recommended):
    Bash

    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

Install dependencies:
    Bash

    pip install -r requirements.txt

Run the simulation:
    Bash

    python main.py

🎮 How to Play

   Start the Engine: Ensure your local Ollama app is running in the background before launching the game.

   Auto-Play: Click the AUTO-PLAY: OFF button in the UI to toggle it ON. The game will automatically query the LLM, parse its commands, and execute turns.

   Advise the AI: Click inside the dark grey text box at the bottom right. Type advice like "Focus entirely on the Economy objective until we have 3 Queens," and hit Enter. The UI will update to show your current advice, which the LLM will read on its next turn.

   Victory/Defeat: The game ends when all Hives of one faction are destroyed. Do not close the window immediately—wait for the LLM to write its "Ancestral Memory" post-mortem so it can learn for your next session!

📁 Project Structure

    main.py: The core game loop, UI event handling, and Auto-Play logic.

    engine.py: The game state machine, combat math, and autonomous Queen AI rules.

    ui.py: Pygame rendering, UI components, and dynamic text wrapping.

    llm_api.py: The threaded Ollama connector, prompt generation, and memory file I/O.

    parser.py: Validates LLM output formatting and catches hallucinations.

    constants.py: Game balance variables, colors, and string enums.

🤝 Contributing

This is an MVP built to explore LLM capabilities in game environments. Feel free to fork the repo and experiment! Great areas for expansion include:

    Adding resource nodes or terrain modifiers to the map.

    Adding a Summarizer thread to compress the journal.txt file on matches that exceed 200 turns.

    Adding a second LLM to control the Red Faction.

📜 License

This project is open-source and available under the MIT License.
