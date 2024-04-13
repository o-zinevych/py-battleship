class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        if start == end:
            self.decks = [Deck(*start)]
        else:
            self.decks = [Deck(*start), Deck(*end)]
            row_distance = end[0] - start[0]
            column_distance = end[1] - start[1]
            row_deck = []
            if row_distance >= 2:
                for i in range(1, row_distance):
                    row_deck.append(start[0] + i)
            elif column_distance >= 2:
                row_deck = [start[0]] * (column_distance - 1)
            column_deck = []
            if column_distance >= 2:
                for i in range(1, column_distance):
                    column_deck.append(start[1] + i)
            elif row_distance >= 2:
                column_deck = [start[1]] * (row_distance - 1)
            deck_coords = [(row_deck[i], column_deck[i])
                           for i in range(len(row_deck)) if row_deck]
            self.decks.extend([Deck(*deck) for deck in deck_coords])
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        hit_decks_count = 0
        deck = self.get_deck(row, column)
        deck.is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                break
            hit_decks_count += 1
        if hit_decks_count == len(self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            ship = Ship(*ship)
            ship_dict = {(ship.decks[i].row, ship.decks[i].column): ship
                         for i in range(len(ship.decks))}
            self.field.update(ship_dict)

    def fire(self, location: tuple) -> str:
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(*location)
        if self.field[location].is_drowned is False:
            return "Hit!"
        return "Sunk!"

    def print_field(self) -> None:
        rows = [["~"] * 10 for _ in range(10)]
        for location, ship in self.field.items():
            row = location[0]
            column = location[1]
            if ship.is_drowned:
                rows[row][column] = "x"
            elif not ship.get_deck(*location).is_alive:
                rows[row][column] = "*"
            else:
                rows[row][column] = u"\u25A1"
        joined_rows = ["    ".join(row) for row in rows]
        field = "\n".join(joined_rows)
        print(field)
