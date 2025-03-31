import numpy as np
import random as r

class Movement:
    def __init__(self, matrix):
        self.matrix = matrix
        self.moved = False 
        self.score = 0
        self.merged = [[False] * 4 for _ in range(4)]  

    def move_up(self):
        for j in range(4):
            for i in range(1, 4):
                if self.matrix[i][j] != 0:
                    k = i
                    while k > 0 and (self.matrix[k-1][j] == 0 or (self.matrix[k-1][j] == self.matrix[k][j])):
                        if self.matrix[k-1][j] == 0:
                            self.matrix[k-1][j] = self.matrix[k][j]
                            self.matrix[k][j] = 0
                            self.moved = True
                        elif self.matrix[k-1][j] == self.matrix[k][j] and not self.merged[k-1][j]:
                            self.matrix[k-1][j] *= 2
                            self.score += self.matrix[k-1][j]
                            self.matrix[k][j] = 0
                            self.moved = True
                            self.merged[k-1][j] = True
                            break
                        k -= 1
        return self.moved, self.score

    def move_down(self):
        for j in range(4):
            for i in range(2, -1, -1):
                if self.matrix[i][j] != 0:
                    k = i
                    while k < 3 and (self.matrix[k+1][j] == 0 or (self.matrix[k+1][j] == self.matrix[k][j])):
                        if self.matrix[k+1][j] == 0:
                            self.matrix[k+1][j] = self.matrix[k][j]
                            self.matrix[k][j] = 0
                            self.moved = True
                        elif self.matrix[k+1][j] == self.matrix[k][j] and not self.merged[k+1][j]:
                            self.matrix[k+1][j] *= 2
                            self.score += self.matrix[k+1][j]
                            self.matrix[k][j] = 0
                            self.moved = True
                            self.merged[k+1][j] = True
                            break
                        k += 1
        return self.moved, self.score

    def move_left(self):  
        for i in range(4):
            for j in range(1, 4):
                if self.matrix[i][j] != 0:
                    k = j
                    while k > 0 and (self.matrix[i][k-1] == 0 or (self.matrix[i][k-1] == self.matrix[i][k])):
                        if self.matrix[i][k-1] == 0:
                            self.matrix[i][k-1] = self.matrix[i][k]
                            self.matrix[i][k] = 0
                            self.moved = True
                        elif self.matrix[i][k-1] == self.matrix[i][k] and not self.merged[i][k-1]:
                            self.matrix[i][k-1] *= 2
                            self.score += self.matrix[i][k-1]
                            self.matrix[i][k] = 0
                            self.moved = True
                            self.merged[i][k-1] = True
                            break
                        k -= 1
        return self.moved, self.score

    def move_right(self):
        for i in range(4):
            for j in range(2, -1, -1):
                if self.matrix[i][j] != 0:
                    k = j
                    while k < 3 and (self.matrix[i][k+1] == 0 or (self.matrix[i][k+1] == self.matrix[i][k])):
                        if self.matrix[i][k+1] == 0:
                            self.matrix[i][k+1] = self.matrix[i][k]
                            self.matrix[i][k] = 0
                            self.moved = True
                        elif self.matrix[i][k+1] == self.matrix[i][k] and not self.merged[i][k+1]:
                            self.matrix[i][k+1] *= 2
                            self.score += self.matrix[i][k+1]
                            self.matrix[i][k] = 0
                            self.moved = True
                            self.merged[i][k+1] = True
                            break
                        k += 1
        return self.moved, self.score

class Game:
    def __init__(self, max_undo_redo_size=10):
        self.matrix = np.zeros((4, 4), dtype=int)
        self.undo_stack = []  
        self.redo_stack = []  
        self.max_undo_redo_size = max_undo_redo_size
        self.generate_random_tiles(2)  

    def generate_random_tiles(self, num_tiles):
        for _ in range(num_tiles):
            while True:
                i, j = r.randint(0, 3), r.randint(0, 3)
                if self.matrix[i][j] == 0:
                    self.matrix[i][j] = r.choices([2, 4], weights=[0.9, 0.1])[0]
                    break

    def save_state(self):
        """Save the current game state."""
        self.undo_stack.append(np.copy(self.matrix))
        if len(self.undo_stack) > self.max_undo_redo_size:
            self.undo_stack.pop(0)

    def undo(self):
       if len(self.undo_stack) > 1:
            current_state = self.undo_stack[-1]
            self.redo_stack.append(np.copy(self.matrix))
            self.matrix = current_state

    def redo(self):
        if self.redo_stack:
            current_state = self.redo_stack.pop()
            self.undo_stack.append(np.copy(self.matrix))
            self.matrix = current_state

    def print_board(self):
        for row in self.matrix:
            print(" ".join(map(str, row)))

    def is_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    return False
                if i < 3 and self.matrix[i][j] == self.matrix[i+1][j]:
                    return False
                if j < 3 and self.matrix[i][j] == self.matrix[i][j+1]:
                    return False
        return True

    def move_and_merge(self, direction):
        movement = Movement(self.matrix)
        if direction == "up":
            moved, score = movement.move_up()
        elif direction == "down":
            moved, score = movement.move_down()
        elif direction == "left":
            moved, score = movement.move_left()
        elif direction == "right":
            moved, score = movement.move_right()
        else:
            print("Invalid direction! Please enter 'up', 'down', 'left', or 'right'.")
            return False, 0
        if moved:
            self.save_state()
            self.generate_random_tiles(1)
        else:
            print("Invalid move! Please try again.")
        return moved, score

game = Game()
while not game.is_game_over():
    game.print_board()
    direction = input("Enter direction (up/down/left/right), u for undo, r for redo: ").lower()
    if direction == 'u':
        game.undo()
        print("Undo performed.")
        continue
    elif direction == 'r':
        game.redo()
        print("Redo performed.")
        continue
    moved, score = game.move_and_merge(direction)
    if moved:
        print("Moved! Score:", score)
    else:
        print("Could not move.")
print("Game over!")
