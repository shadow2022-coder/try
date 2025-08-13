# make sure you have pygame to run this program.
# To install pygame you can use: 
# pip install pygame
import random
import sys
import pygame
from pygame.locals import *

# Game Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
FPS = 32

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 215, 0)
RED = (220, 20, 60)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (211, 211, 211)

class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird - Enhanced Edition')
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Game state
        self.game_state = "START"  # START, PLAYING, GAME_OVER
        self.score = 0
        self.high_score = 0
        
        # Bird properties
        self.bird_x = WINDOW_WIDTH // 5
        self.bird_y = WINDOW_HEIGHT // 2
        self.bird_velocity = 0
        self.bird_width = 40
        self.bird_height = 30
        
        # Pipe properties
        self.pipes = []
        self.pipe_width = 60
        self.pipe_gap = 200
        self.pipe_velocity = -4
        
        # Ground
        self.ground_y = WINDOW_HEIGHT - 100
        
        self.create_initial_pipes()

    def create_initial_pipes(self):
        """Create initial set of pipes"""
        self.pipes = []
        for i in range(3):
            pipe_height = random.randint(100, WINDOW_HEIGHT - self.pipe_gap - 200)
            self.pipes.append({
                'x': WINDOW_WIDTH + i * 300,
                'top_height': pipe_height,
                'bottom_y': pipe_height + self.pipe_gap,
                'passed': False
            })

    def draw_button(self, text, x, y, width, height, color, text_color, border_color=None):
        """Draw a button with text"""
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.window, color, button_rect)
        
        if border_color:
            pygame.draw.rect(self.window, border_color, button_rect, 3)
        
        text_surface = self.font_medium.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.window.blit(text_surface, text_rect)
        
        return button_rect

    def draw_start_screen(self):
        """Draw the start screen with instructions"""
        # Background gradient effect
        for y in range(WINDOW_HEIGHT):
            color_value = int(135 + (y / WINDOW_HEIGHT) * 50)
            color = (max(0, min(255, color_value)), 206, 250)
            pygame.draw.line(self.window, color, (0, y), (WINDOW_WIDTH, y))

        # Title
        title_text = self.font_large.render("FLAPPY BIRD", True, WHITE)
        title_shadow = self.font_large.render("FLAPPY BIRD", True, BLACK)
        
        # Shadow effect
        self.window.blit(title_shadow, (WINDOW_WIDTH//2 - title_text.get_width()//2 + 3, 83))
        self.window.blit(title_text, (WINDOW_WIDTH//2 - title_text.get_width()//2, 80))

        # Instructions box
        instructions_rect = pygame.Rect(50, 200, WINDOW_WIDTH-100, 300)
        pygame.draw.rect(self.window, WHITE, instructions_rect)
        pygame.draw.rect(self.window, BLACK, instructions_rect, 3)

        # Instructions text
        instructions = [
            "HOW TO PLAY:",
            "",
            "• Press SPACE or UP ARROW to flap",
            "• Avoid hitting the pipes",
            "• Fly through gaps to score points",
            "• Try to beat your high score!",
            "",
            f"High Score: {self.high_score}"
        ]

        y_offset = 220
        for line in instructions:
            if line == "HOW TO PLAY:":
                text = self.font_medium.render(line, True, RED)
            elif line.startswith("High Score:"):
                text = self.font_medium.render(line, True, ORANGE)
            else:
                text = self.font_small.render(line, True, BLACK)
            
            self.window.blit(text, (70, y_offset))
            y_offset += 30

        # Start button
        start_button = self.draw_button("START GAME", WINDOW_WIDTH//2 - 100, 520, 200, 50, 
                                      GREEN, WHITE, DARK_GREEN)
        
        # Quit button
        quit_button = self.draw_button("QUIT", WINDOW_WIDTH//2 - 75, 580, 150, 40, 
                                     RED, WHITE, (150, 0, 0))

        return start_button, quit_button

    def draw_bird(self):
        """Draw an enhanced bird"""
        # Bird body (ellipse)
        pygame.draw.ellipse(self.window, YELLOW, 
                          (self.bird_x, self.bird_y, self.bird_width, self.bird_height))
        
        # Bird outline
        pygame.draw.ellipse(self.window, BLACK, 
                          (self.bird_x, self.bird_y, self.bird_width, self.bird_height), 2)
        
        # Eye
        eye_x = self.bird_x + self.bird_width - 15
        eye_y = self.bird_y + 8
        pygame.draw.circle(self.window, WHITE, (eye_x, eye_y), 6)
        pygame.draw.circle(self.window, BLACK, (eye_x, eye_y), 6, 2)
        pygame.draw.circle(self.window, BLACK, (eye_x + 2, eye_y), 3)
        
        # Beak
        beak_points = [
            (self.bird_x + self.bird_width, self.bird_y + self.bird_height//2),
            (self.bird_x + self.bird_width + 10, self.bird_y + self.bird_height//2 - 3),
            (self.bird_x + self.bird_width + 10, self.bird_y + self.bird_height//2 + 3)
        ]
        pygame.draw.polygon(self.window, ORANGE, beak_points)

    def draw_pipes(self):
        """Draw enhanced pipes"""
        for pipe in self.pipes:
            # Top pipe
            top_rect = pygame.Rect(pipe['x'], 0, self.pipe_width, pipe['top_height'])
            pygame.draw.rect(self.window, GREEN, top_rect)
            pygame.draw.rect(self.window, DARK_GREEN, top_rect, 3)
            
            # Top pipe cap
            cap_rect = pygame.Rect(pipe['x'] - 5, pipe['top_height'] - 30, self.pipe_width + 10, 30)
            pygame.draw.rect(self.window, GREEN, cap_rect)
            pygame.draw.rect(self.window, DARK_GREEN, cap_rect, 3)
            
            # Bottom pipe
            bottom_rect = pygame.Rect(pipe['x'], pipe['bottom_y'], self.pipe_width, 
                                    WINDOW_HEIGHT - pipe['bottom_y'])
            pygame.draw.rect(self.window, GREEN, bottom_rect)
            pygame.draw.rect(self.window, DARK_GREEN, bottom_rect, 3)
            
            # Bottom pipe cap
            cap_rect = pygame.Rect(pipe['x'] - 5, pipe['bottom_y'], self.pipe_width + 10, 30)
            pygame.draw.rect(self.window, GREEN, cap_rect)
            pygame.draw.rect(self.window, DARK_GREEN, cap_rect, 3)

    def draw_background(self):
        """Draw enhanced background"""
        # Sky gradient
        for y in range(self.ground_y):
            ratio = y / self.ground_y
            r = int(135 + ratio * 50)
            g = int(206 - ratio * 50)
            b = 250
            color = (max(0, min(255, r)), max(0, min(255, g)), b)
            pygame.draw.line(self.window, color, (0, y), (WINDOW_WIDTH, y))
        
        # Ground
        ground_rect = pygame.Rect(0, self.ground_y, WINDOW_WIDTH, WINDOW_HEIGHT - self.ground_y)
        pygame.draw.rect(self.window, (139, 69, 19), ground_rect)
        
        # Ground texture lines
        for i in range(0, WINDOW_WIDTH, 20):
            pygame.draw.line(self.window, (101, 67, 33), 
                           (i, self.ground_y), (i, WINDOW_HEIGHT), 2)

    def draw_score(self):
        """Draw score with shadow effect"""
        score_text = str(self.score)
        score_surface = self.font_large.render(score_text, True, WHITE)
        score_shadow = self.font_large.render(score_text, True, BLACK)
        
        x = WINDOW_WIDTH // 2 - score_surface.get_width() // 2
        y = 50
        
        # Shadow
        self.window.blit(score_shadow, (x + 2, y + 2))
        # Main text
        self.window.blit(score_surface, (x, y))

    def draw_game_over_screen(self):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.window.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        x = WINDOW_WIDTH // 2 - game_over_text.get_width() // 2
        self.window.blit(game_over_text, (x, 200))
        
        # Score info
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        x = WINDOW_WIDTH // 2 - score_text.get_width() // 2
        self.window.blit(score_text, (x, 280))
        
        high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, YELLOW)
        x = WINDOW_WIDTH // 2 - high_score_text.get_width() // 2
        self.window.blit(high_score_text, (x, 320))
        
        # Buttons
        restart_button = self.draw_button("PLAY AGAIN", WINDOW_WIDTH//2 - 100, 400, 200, 50,
                                        GREEN, WHITE, DARK_GREEN)
        
        menu_button = self.draw_button("MAIN MENU", WINDOW_WIDTH//2 - 100, 460, 200, 50,
                                     BLUE, WHITE, (0, 0, 150))
        
        quit_button = self.draw_button("QUIT", WINDOW_WIDTH//2 - 75, 520, 150, 40,
                                     RED, WHITE, (150, 0, 0))
        
        return restart_button, menu_button, quit_button

    def reset_game(self):
        """Reset game to initial state"""
        self.bird_y = WINDOW_HEIGHT // 2
        self.bird_velocity = 0
        self.score = 0
        self.create_initial_pipes()

    def update_bird(self):
        """Update bird physics"""
        # Apply gravity
        self.bird_velocity += 0.5
        self.bird_y += self.bird_velocity
        
        # Limit velocity
        if self.bird_velocity > 10:
            self.bird_velocity = 10

    def update_pipes(self):
        """Update pipe positions and add new ones"""
        for pipe in self.pipes:
            pipe['x'] += self.pipe_velocity
            
            # Check if bird passed the pipe
            if not pipe['passed'] and pipe['x'] + self.pipe_width < self.bird_x:
                pipe['passed'] = True
                self.score += 1
        
        # Remove pipes that are off screen
        self.pipes = [pipe for pipe in self.pipes if pipe['x'] > -self.pipe_width]
        
        # Add new pipe if needed
        if len(self.pipes) < 3:
            last_pipe_x = max(pipe['x'] for pipe in self.pipes) if self.pipes else WINDOW_WIDTH
            pipe_height = random.randint(100, self.ground_y - self.pipe_gap - 100)
            self.pipes.append({
                'x': last_pipe_x + 300,
                'top_height': pipe_height,
                'bottom_y': pipe_height + self.pipe_gap,
                'passed': False
            })

    def check_collision(self):
        """Check for collisions"""
        bird_rect = pygame.Rect(self.bird_x, self.bird_y, self.bird_width, self.bird_height)
        
        # Ground collision
        if self.bird_y + self.bird_height >= self.ground_y or self.bird_y <= 0:
            return True
        
        # Pipe collision
        for pipe in self.pipes:
            pipe_rect_top = pygame.Rect(pipe['x'], 0, self.pipe_width, pipe['top_height'])
            pipe_rect_bottom = pygame.Rect(pipe['x'], pipe['bottom_y'], self.pipe_width,
                                         WINDOW_HEIGHT - pipe['bottom_y'])
            
            if bird_rect.colliderect(pipe_rect_top) or bird_rect.colliderect(pipe_rect_bottom):
                return True
        
        return False

    def handle_click(self, pos):
        """Handle mouse clicks"""
        if self.game_state == "START":
            start_button, quit_button = self.draw_start_screen()
            if start_button.collidepoint(pos):
                self.game_state = "PLAYING"
                self.reset_game()
            elif quit_button.collidepoint(pos):
                return False
                
        elif self.game_state == "GAME_OVER":
            restart_button, menu_button, quit_button = self.draw_game_over_screen()
            if restart_button.collidepoint(pos):
                self.reset_game()
                self.game_state = "PLAYING"
            elif menu_button.collidepoint(pos):
                self.game_state = "START"
            elif quit_button.collidepoint(pos):
                return False
        
        return True

    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key in (K_SPACE, K_UP):
                        if self.game_state == "PLAYING":
                            self.bird_velocity = -8
                        elif self.game_state == "START":
                            self.game_state = "PLAYING"
                            self.reset_game()
                        elif self.game_state == "GAME_OVER":
                            self.reset_game()
                            self.game_state = "PLAYING"
                
                elif event.type == MOUSEBUTTONDOWN:
                    if not self.handle_click(event.pos):
                        running = False
                    elif self.game_state == "PLAYING":
                        self.bird_velocity = -8

            # Game logic
            if self.game_state == "PLAYING":
                self.update_bird()
                self.update_pipes()
                
                if self.check_collision():
                    if self.score > self.high_score:
                        self.high_score = self.score
                    self.game_state = "GAME_OVER"

            # Drawing
            if self.game_state == "START":
                self.draw_start_screen()
            elif self.game_state == "PLAYING":
                self.draw_background()
                self.draw_pipes()
                self.draw_bird()
                self.draw_score()
            elif self.game_state == "GAME_OVER":
                self.draw_background()
                self.draw_pipes()
                self.draw_bird()
                self.draw_score()
                self.draw_game_over_screen()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run()
