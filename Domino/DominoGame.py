import DominoSet
import Player
import Snake
import random


class DominoGame:
    def __init__(self):
        self.domino_set = DominoSet.DominoSet()  # Corrected instantiation
        self.player = Player.Player("Player")  # Corrected instantiation
        self.computer = Player.Player("Computer")  # Corrected instantiation
        self.snake = Snake.Snake()  # Corrected instantiation
        self.current_player = None

        self.setup_game()

    def setup_game(self):
        # Assign 7 tiles to each player
        for _ in range(7):
            self.player.draw_tile(self.domino_set)
            self.computer.draw_tile(self.domino_set)

        # Determine starting piece and player
        self.determine_starting_piece()

    def determine_starting_piece(self):
        for i in range(6, -1, -1):
            double_tile = [i, i]
            if self.player.has_tile(double_tile):
                self.player.remove_tile(double_tile)
                self.snake.add_tile_right(double_tile)
                self.current_player = self.computer
                return
            elif self.computer.has_tile(double_tile):
                self.computer.remove_tile(double_tile)
                self.snake.add_tile_right(double_tile)
                self.current_player = self.player
                return
        self.setup_game()  # Reinitialize if no double tile is found

    def play(self):
        while True:
            self.print_game_state()
            if self.check_win():
                break
            if self.current_player == self.player:
                self.player_turn()
                self.current_player = self.computer
            else:
                self.computer_turn()
                self.current_player = self.player

    def print_game_state(self):
        print(70 * "=")
        print(f"Stock size: {self.domino_set.size()}")
        print(f"Computer pieces: {len(self.computer.hand)}\n")
        print(f"Snake: {self.snake.display()}")
        print("\nYour pieces:")
        for i, tile in enumerate(self.player.hand):
            print(f"{i + 1}: {tile}")

    def player_turn(self):
        print("\nStatus: It's your turn to make a move. Enter your command.")
        while True:
            try:
                choice = int(input())
                if -len(self.player.hand) <= choice <= len(self.player.hand):
                    self.make_move(self.player, choice)
                    break
                else:
                    print("Invalid input. Please try again.")
            except ValueError:
                print("Invalid input. Please try again.")

    def computer_turn(self):
        print("\nStatus: Computer is about to make a move. Press Enter to continue...")
        input()
        self.make_move(self.computer, random.choice(range(-len(self.computer.hand), len(self.computer.hand) + 1)))

    def make_move(self, player, choice):
        if choice == 0:
            player.draw_tile(self.domino_set)
        else:
            index = abs(choice) - 1
            tile = player.hand[index]
            if choice < 0 and (tile[1] == self.snake.left_end() or tile[0] == self.snake.left_end()):
                if tile[1] != self.snake.left_end():
                    tile.reverse()
                self.snake.add_tile_left(player.hand.pop(index))
            elif choice > 0 and (tile[0] == self.snake.right_end() or tile[1] == self.snake.right_end()):
                if tile[0] != self.snake.right_end():
                    tile.reverse()
                self.snake.add_tile_right(player.hand.pop(index))
            else:
                print("Illegal move. Please try again.")
                self.player_turn() if player == self.player else self.computer_turn()

    def check_win(self):
        if not self.player.hand:
            print("\nStatus: The game is over. You won!")
            return True
        elif not self.computer.hand:
            print("\nStatus: The game is over. The computer won!")
            return True
        elif self.snake.left_end() == self.snake.right_end():
            count = sum(tile.count(self.snake.left_end()) for tile in self.snake.tiles)
            if count == 8:
                print("\nStatus: The game is over. It's a draw!")
                return True
        return False


if __name__ == "__main__":
    game = DominoGame()
    game.play()