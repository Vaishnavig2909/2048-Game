import pygame

class Game2048GUI:
    def _init_(self, size=4, square_size=100, margin=10):
        self.size = size
        self.square_size = square_size
        self.margin = margin
        self.width = (size * square_size) + (margin * (size + 1))
        self.height = (size * square_size) + (margin * (size + 1))
        self.screen = pygame.display.set_mode((self.width, self.height + 100))
        pygame.display.set_caption("2048")

    def draw_board(self, matrix):
        for i in range(self.size):
            for j in range(self.size):
                x = self.margin + j * (self.square_size + self.margin)
                y = self.margin + i * (self.square_size + self.margin)
                value = matrix[i][j]
                color = self.get_color(value)
                pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size))
                pygame.draw.rect(self.screen, (75, 75, 75), (x, y, self.square_size, self.square_size), 2)

                if value != 0:
                    font = pygame.font.Font(None, self.square_size // 3)
                    text_surface = font.render(str(value), True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(x + self.square_size // 2, y + self.square_size // 2))
                    self.screen.blit(text_surface, text_rect)

    def get_color(self, value):
        if value == 0:
            return (150, 150, 150)
        colors = {
            2: (238, 148, 138),
            4: (237, 104, 100),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46)
        }
        return colors.get(value, (0, 0, 0))

    def draw_scoreboard(self, score, best_score):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        best_score_text = font.render(f"Best Score: {best_score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.width // 4, self.height + 50))
        best_score_rect = best_score_text.get_rect(center=(3 * self.width // 4, self.height + 50))
        self.screen.blit(score_text, score_rect)
        self.screen.blit(best_score_text, best_score_rect)

    def draw_menu(self):
        font = pygame.font.Font(None, 36)
        new_game_text = font.render("New Game (N)", True, (255, 255, 255))
        speed_text = font.render("Animation Speed (1, 2, 3)", True, (255, 255, 255))
        new_game_rect = new_game_text.get_rect(center=(self.width // 2, self.height + 20))
        speed_rect = speed_text.get_rect(center=(self.width // 2, self.height + 80))
        self.screen.blit(new_game_text, new_game_rect)
        self.screen.blit(speed_text, speed_rect)

    def update(self, matrix, score, best_score):
        self.screen.fill((119, 110, 101))
        self.draw_scoreboard(score, best_score)
        self.draw_menu()
        self.draw_board(matrix)
        pygame.display.flip()

    def show_game_over(self):
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()

    def show_game_won(self):
        font = pygame.font.Font(None, 72)
        game_won_text = font.render("You Won!", True, (0, 255, 0))
        game_won_rect = game_won_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(game_won_text, game_won_rect)
        pygame.display.flip()

    def quit_game(self):
        pygame.quit()

    def is_game_over(self, matrix):
        for i in range(self.size):
            for j in range(self.size):
                if matrix[i][j] == 0:
                    return False
                if j < self.size - 1 and matrix[i][j] == matrix[i][j + 1]:
                    return False
                if i < self.size - 1 and matrix[i][j] == matrix[i + 1][j]:
                    return False
        return True

    def is_game_won(self, matrix):
        for i in range(self.size):
            for j in range(self.size):
                if matrix[i][j] == 2048:
                    return True
        return False
    def wait_and_quit(self):
        pygame.time.wait(3000)  
        self.quit_game()

pygame.init()

gui = Game2048GUI()

example_matrix = [
    [2, 256, 512, 8],
    [4, 128, 1024, 2],
    [8, 64, 2, 16],
    [16, 32, 128, 4]
]

score = 128
best_score = 256

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if gui.is_game_over(example_matrix):
        gui.show_game_over()
        gui.wait_and_quit()
        running = False
    elif gui.is_game_won(example_matrix):
        gui.show_game_won()
        gui.wait_and_quit()
        running = False
    else:
        gui.update(example_matrix, score, best_score)

gui.quit_game()
