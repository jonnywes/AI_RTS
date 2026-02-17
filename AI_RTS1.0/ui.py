# ui.py
import pygame
import constants
import pyperclip

class UIManager:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("LLM RTS - MVP")
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        
        self.font_main = pygame.font.SysFont('Consolas', 14)
        self.font_large = pygame.font.SysFont('Consolas', 18, bold=True)
        
        self.input_text = ""
        self.input_rect = pygame.Rect(
            constants.MAP_WIDTH + 10, 
            constants.SCREEN_HEIGHT - constants.INPUT_BOX_HEIGHT, 
            constants.TERMINAL_WIDTH - 20, 
            constants.INPUT_BOX_HEIGHT - 10
        )
        self.input_active = False
        
        self.cursor_visible = True
        self.cursor_timer = 0
        
        # --- NEW: Ollama Button State ---
        self.ollama_btn_rect = pygame.Rect(
            constants.MAP_WIDTH + 10,
            constants.SCREEN_HEIGHT - constants.INPUT_BOX_HEIGHT - 45, # Positioned right above the text box
            constants.TERMINAL_WIDTH - 20,
            35
        )
        self.ollama_btn_hover = False

    def handle_events(self, events):
        """
        Now returns a tuple: (submitted_text, action_signal)
        action_signal will be "OLLAMA_CLICK" if the new button is pressed.
        """
        submitted_text = None
        action_signal = None
        
        # Check mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        self.ollama_btn_hover = self.ollama_btn_rect.collidepoint(mouse_pos)
        
        for event in events:
            if event.type == pygame.QUIT:
                return "QUIT", None
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    # Check if Ollama button was clicked
                    if self.ollama_btn_rect.collidepoint(event.pos):
                        action_signal = "OLLAMA_CLICK"
                        
                    # Check text box focus
                    if self.input_rect.collidepoint(event.pos):
                        self.input_active = True
                    else:
                        self.input_active = False
                
            if event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL or event.mod & pygame.KMOD_META):
                    paste_text = pyperclip.paste()
                    if paste_text:
                        self.input_text += paste_text
                        
                elif event.key == pygame.K_RETURN:
                    submitted_text = self.input_text
                    self.input_text = ""
                    
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                    
                else:
                    if event.unicode and event.unicode.isprintable():
                        self.input_text += event.unicode
                        
        return submitted_text, action_signal

    def draw(self, engine, prompt_message, error_message="", is_generating=False):
        """Now accepts is_generating to change the UI while Ollama thinks."""
        self.screen.fill(constants.COLOR_BG_MAP)
        
        self._draw_map(engine)
        self._draw_terminal(prompt_message, error_message, engine, is_generating)
        
        pygame.display.flip()

    def _draw_map(self, engine):
        turn_surface = self.font_large.render(f"TURN: {engine.turn_number}", True, constants.COLOR_TEXT)
        self.screen.blit(turn_surface, (20, 20))
        
        for hive in engine.map.hives:
            pygame.draw.rect(self.screen, constants.COLOR_HIVE, (hive.x, hive.y, 40, 40))
            
            id_text = self.font_main.render(f"HIVE {hive.hive_id}", True, constants.COLOR_HIGHLIGHT)
            food_text = self.font_main.render(f"Food: {hive.food}", True, constants.COLOR_TEXT)
            pop_text = self.font_main.render(f"Wkr:{hive.workers} War:{hive.warriors} Qn:{len(hive.queens)}", True, constants.COLOR_TEXT)
            
            self.screen.blit(id_text, (hive.x, hive.y - 45))
            self.screen.blit(food_text, (hive.x, hive.y - 30))
            self.screen.blit(pop_text, (hive.x, hive.y - 15))

    def _draw_terminal(self, prompt_message, error_message, engine, is_generating):
        terminal_rect = pygame.Rect(constants.MAP_WIDTH, 0, constants.TERMINAL_WIDTH, constants.SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, constants.COLOR_BG_TERMINAL, terminal_rect)
        pygame.draw.line(self.screen, constants.COLOR_HIGHLIGHT, (constants.MAP_WIDTH, 0), (constants.MAP_WIDTH, constants.SCREEN_HEIGHT), 2)

        y_offset = 20
        
        # --- NEW: Dynamic Prompt for Loading State ---
        if is_generating:
            display_prompt = "Hive Mind is thinking... (Please wait)"
            prompt_color = (255, 200, 50) # Yellow warning color
        else:
            display_prompt = prompt_message
            prompt_color = constants.COLOR_HIGHLIGHT
            
        prompt_surface = self.font_large.render(display_prompt, True, prompt_color)
        self.screen.blit(prompt_surface, (constants.MAP_WIDTH + 10, y_offset))
        y_offset += 30

        if error_message:
            error_surface = self.font_main.render(error_message, True, (255, 100, 100))
            self.screen.blit(error_surface, (constants.MAP_WIDTH + 10, y_offset))
            y_offset += 25

        y_offset += 10
        recent_diaries = []
        for hive in engine.map.hives:
            recent_diaries.extend(hive.diaries)
        
        for log in recent_diaries[-5:]:
            for line in log.split('\n'):
                log_surface = self.font_main.render(line, True, constants.COLOR_TEXT)
                self.screen.blit(log_surface, (constants.MAP_WIDTH + 10, y_offset))
                y_offset += 15
            y_offset += 10

        # --- NEW: Draw Ollama Button ---
        # Change color based on hover or if currently generating
        if is_generating:
            btn_color = (100, 100, 100) # Greyed out
        else:
            btn_color = constants.COLOR_HIGHLIGHT if self.ollama_btn_hover else (80, 120, 80)
            
        pygame.draw.rect(self.screen, btn_color, self.ollama_btn_rect)
        btn_text = self.font_large.render("Ask Hive Mind (Ollama)", True, (10, 10, 10))
        text_rect = btn_text.get_rect(center=self.ollama_btn_rect.center)
        self.screen.blit(btn_text, text_rect)

        # Draw Input Box Background
        pygame.draw.rect(self.screen, constants.COLOR_INPUT_BG, self.input_rect)
        border_color = constants.COLOR_HIGHLIGHT if self.input_active else (80, 80, 80)
        pygame.draw.rect(self.screen, border_color, self.input_rect, 2)
        
        self._draw_multiline_text_with_cursor(self.input_text, self.input_rect.x + 5, self.input_rect.y + 5, self.input_rect.width - 10)

    def _draw_multiline_text_with_cursor(self, text, x, y, max_width):
        words = text.replace('\n', ' \n ').split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            if word == '\n':
                lines.append(current_line)
                current_line = ""
                continue
                
            test_line = current_line + word + " "
            if self.font_main.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        
        for i, line in enumerate(lines):
            text_surface = self.font_main.render(line, True, constants.COLOR_TEXT)
            self.screen.blit(text_surface, (x, y + (i * 18)))

        if self.input_active:
            self.cursor_timer += 1
            if self.cursor_timer >= constants.FPS // 2:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
                
            if self.cursor_visible:
                cursor_x = x + self.font_main.size(lines[-1])[0]
                cursor_y = y + ((len(lines) - 1) * 18)
                cursor_surface = self.font_main.render("_", True, constants.COLOR_HIGHLIGHT)
                self.screen.blit(cursor_surface, (cursor_x, cursor_y))
        else:
            self.cursor_timer = 0
            self.cursor_visible = True