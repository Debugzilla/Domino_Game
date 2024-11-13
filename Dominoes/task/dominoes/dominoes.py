import random
import sys

# Define constants
DOMINOS = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
           [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
           [2, 2], [2, 3], [2, 4], [2, 5], [2, 6],
           [3, 3], [3, 4], [3, 5], [3, 6],
           [4, 4], [4, 5], [4, 6],
           [5, 5], [5, 6],
           [6, 6],
           ]


def main():
    domino_set = reset(DOMINOS)
    player_hand, computer_hand, domino_set = assign(domino_set)
    player_hand, computer_hand, snake, status = determine(player_hand, computer_hand)
    if status is None:
        main()
    while True:
        print_field(domino_set, computer_hand, snake, player_hand)
        check_win(player_hand, computer_hand, snake)
        if status == "player":
            print(f"\nStatus: It's your turn to make a move. Enter your command.")
            status = player_move(player_hand, snake, domino_set)
        else:
            print("\nStatus: Computer is about to make a move. Press Enter to continue...")
            input()
            status = computer_move(computer_hand, snake, domino_set)


def reset(domino_set):
    """creates a new list of all the domino pieces, shuffles and then returns it"""

    shuffle = domino_set[:]
    random.shuffle(shuffle)
    return shuffle


def assign(domino_set):
    """Assigns 7 domino pieces to each player and returns each players set of tiles and the list of remaining tiles"""

    player_hand = []
    computer_hand = []
    for _ in range(7):
        player_hand += [domino_set.pop()]
        computer_hand += [domino_set.pop()]
    return player_hand, computer_hand, domino_set


def determine(player_hand, computer_hand):
    """Determines who has the highest double tile, puts it as starting tile and defines starting player"""

    start_piece = []
    state = None
    for i in range(7):
        check_piece = [6 - i, 6 - i]
        if check_piece in player_hand:
            player_hand.remove(check_piece)
            start_piece.append(check_piece)
            state = "computer"
            break
        elif check_piece in computer_hand:
            computer_hand.remove(check_piece)
            start_piece.append(check_piece)
            state = "player"
            break
    return player_hand, computer_hand, start_piece, state


def print_field(stock, com_pieces, snake_tiles, player_pieces):
    """Prints out the current snake in appropriate format"""

    print(70 * "=")
    print("Stock size:", len(stock))
    print("Computer pieces:", len(com_pieces), "\n")
    if len(snake_tiles) < 7:
        print("".join(map(str, snake_tiles)))
    else:
        print("".join(map(str, snake_tiles[0:3])) + "..." + "".join(map(str, snake_tiles[-3:])))
    print("\nYour pieces:")
    for i in range(len(player_pieces)):
        print(f"{i + 1}:{player_pieces[i]}")


def player_move(player_hand, snake, domino_set):
    """Handles the players Move"""

    proper_input = False
    while not proper_input:
        cmd = input()
        try:
            choice = int(cmd)
        except ValueError:
            print("Invalid input. Please try again.")
        except TypeError:
            print("Invalid input. Please try again.")
        else:
            if -len(player_hand) <= abs(choice) <= len(player_hand):
                index = abs(choice)-1
                if choice == 0:
                    if len(domino_set) > 0:
                        random.shuffle(domino_set)
                        player_hand.append(domino_set.pop())
                    return "computer"
                elif choice < 0:
                    if snake[0][0] in player_hand[index]:
                        if player_hand[index][1] == snake[0][0]:
                            snake.insert(0, player_hand.pop(index))
                        else:
                            player_hand[index].reverse()
                            snake.insert(0, player_hand.pop(index))
                        return "computer"
                    else:
                        print("Illegal move. Please try again.")
                elif choice > 0:
                    if snake[-1][1] in player_hand[index]:
                        if player_hand[index][0] == snake[-1][1]:
                            snake.append(player_hand.pop(index))
                        else:
                            player_hand[index].reverse()
                            snake.append(player_hand.pop(index))
                        return "computer"
                    else:
                        print("Illegal move. Please try again.")
            else:
                print("Invalid input. Please try again.")


def computer_move(computer_hand, snake, domino_set):
    """Handles the computers move"""

    random.shuffle(computer_hand)
    start_right = random.randint(0, 1)
    if start_right:
        if com_append_right(computer_hand, snake):
            return "player"
        else:
            if com_append_left(computer_hand, snake):
                return "player"
            else:
                com_pick_piece(computer_hand, domino_set)
                return "player"
    else:
        if com_append_left(computer_hand, snake):
            return "player"
        else:
            if com_append_right(computer_hand, snake):
                return "player"
            else:
                com_pick_piece(computer_hand, domino_set)
                return "player"


def com_append_right(computer_hand, snake):
    """Tries to append a domino piece from the computer to the right of the snake"""

    for domino in computer_hand:
        domino_index = computer_hand.index(domino)
        if snake[-1][1] in domino:
            if domino[0] == snake[-1][1]:
                snake.append(computer_hand.pop(domino_index))
                return True
            else:
                computer_hand[domino_index].reverse()
                snake.append(computer_hand.pop(domino_index))
                return True
        else:
            continue
    return False


def com_append_left(computer_hand, snake):
    """Tries to append a domino piece from the computer to the left of the snake"""

    for domino in computer_hand:
        domino_index = computer_hand.index(domino)
        if snake[0][0] in domino:
            if domino[1] == snake[0][0]:
                snake.insert(0, computer_hand.pop(domino_index))
                return True
            else:
                computer_hand[domino_index].reverse()
                snake.insert(0, computer_hand.pop(domino_index))
                return True
    return False


def com_pick_piece(computer_hand, domino_set):
    """Adds a piece from the pile to the computers stock"""

    if len(domino_set) > 0:
        random.shuffle(domino_set)
        computer_hand.append(domino_set.pop())


def check_win(player, computer, snake_tiles):
    """Checks if one of the players won or if the game can not be won anymore"""

    if len(player) == 0:
        print("\nStatus: The game is over. You won!")
        sys.exit()
    elif len(computer) == 0:
        print("\nStatus: The game is over. The computer won!")
        sys.exit()
    elif snake_tiles[0][0] == snake_tiles[-1][1]:
        counter = 0
        for tile in snake_tiles: c 
            counter += tile.count(snake_tiles[0][0])
            if counter == 8:
                print("\nStatus: The game is over. It's a draw!")
                sys.exit()


if __name__ == "__main__":
    main()

