# Snake.py
class Snake:
    def __init__(self):
        self.tiles = []

    def add_tile_left(self, tile):
        self.tiles.insert(0, tile)

    def add_tile_right(self, tile):
        self.tiles.append(tile)

    def left_end(self):
        return self.tiles[0][0] if self.tiles else None

    def right_end(self):
        return self.tiles[-1][1] if self.tiles else None

    def display(self):
        return " ".join(str(tile) for tile in self.tiles)
