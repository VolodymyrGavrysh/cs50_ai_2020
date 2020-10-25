from itertools import combinations, product
from random import randrange, choice

class Minesweeper():
    """
    Minesweeper game representation
    """
    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = randrange(height)
            j = randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """
        # Keep count of nearby mines
        count = 0
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count # num of mines

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.known_mines():
            self.cells.remove(cell)
            self.count -= 1
    
    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.known_safes():
            self.cells.remove(cell)

    def inference(self, new):
        """check if the centence is subset, else return None"""
        if new.cells.issubset(self.cells):
            return Sentence(self.cells - new.cells, self.count - new.count)
        elif self.cells.issubset(new.cells):
            return Sentence(new.cells - self.cells, new.count - self.count)
        else:
            return None

class MinesweeperAI():  
    """
    Minesweeper game player
    input: a cell in form (i, j) + self.count
    update: mines, safes, moves_made, knowledge
    """
    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width
        # Keep track of which cells have been clicked on
        self.moves_made = set()
        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()
        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1 mark the cell as a move that has been made
        self.moves_made.add(cell)
        # 2 mark the cell as safe
        self.mark_safe(cell)
        # 3 create new centence with list of neighboing cells
        sent_new = Sentence(self.neighboring_cell(cell), count)
        # check all the cells in new sentence if they are  mines
        for i in self.mines:
            sent_new.mark_mine(i)
        # check all cells in new sentenve if they are safe
        for i in self.mines:
            sent_new.mark_safe(i)
        # add knowledge to the knowledge base
        self.knowledge.append(sent_new)
        # 4 mark (save of mines) additional sells
        # add new sets 
        new_safe = set()
        new_mines = set()
        # iterate over sentence, mined and safe cells 
        for centence in self.knowledge:
            for cell in centence.known_mines():
                new_mines.add(cell)
            for cell in centence.known_safes():
                new_safe.add(cell)
        # mark them save / mines
        for cell in new_safe:
            self.mark_safe(cell)
        for cell in new_mines:
            self.mark_mine(cell)
        # 5 add new centences to the knowledge base if they can be infered from existing knowledge
        new_centence = []
        # loop over the combinations 
        for A, B in combinations(self.knowledge, 2):
            infer = A.inference(B)
            if infer is not None and infer not in self.knowledge:
                new_centence.append(infer)
        # extennd knowledge
        self.knowledge.extend(new_centence)
        # remove empty sentence
        for i in self.knowledge:
            if i == Sentence(set(), 0):
                self.knowledge.remove(i)

    def neighboring_cell(self, cell):
        '''func to find all the neighboring cells
        input - cell (i, j)
        output - list of neighboring cells 
        '''
        neighbors = set()
        # loop over all the sells
        for i in range(cell[0]-1, cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                # we don't need the cell itself
                if (i, j) == cell:
                    continue
                # add neightbor
                if 0 <= i < self.width and 0 <= j < self.height:
                    neighbors.add((i, j))
        return neighbors

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        move_left = list(self.safes - self.moves_made)
        # check it if it is None
        if len(move_left) == 0:
            return None
        else:
            return move_left[randrange(len(move_left))]

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves_left = set([(x, y) for x in self.width for y in self.height])
        moves_left = moves_left - self.mines - self.moves_made

        if moves_left:
            return choice(tuple(moves_left))
        else:
            return None