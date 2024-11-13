# Player.py
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_tile(self, domino_set):
        tile = domino_set.draw_tile()
        if tile:
            self.hand.append(tile)

    def has_tile(self, tile):
        return tile in self.hand

    def remove_tile(self, tile):
        if tile in self.hand:
            self.hand.remove(tile)
