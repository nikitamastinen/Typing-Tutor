from game import Game

if __name__ == '__main__':
    with open('words.txt', 'r') as f:
        text = f.read()
        new_game = Game(text)
        new_game.init_game()
        new_game.play()



