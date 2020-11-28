import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def index_in_list(self, n, nlist): # help function 1
        '''find a index of the word in the list of words'''
        l = []
        for index, value in enumerate(nlist):
            if value == n:
                l.append(index)
        return l

    def remove_words_not_consistent(self, d, ndict): # help fuction 2
        '''return only words that in index list'''
        l = set()
        for index, value in enumerate(ndict):
            if index in d:
                l.add(value)
        return l

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # get the list of leght of words 
        for i in self.domains.values():
            lenth_of_words = [len(d) for d in i]
            break # count one time
        
        # iterate over dict items 
        for i, values in self.domains.items():

            self.domains[i] = self.remove_words_not_consistent(self.index_in_list(i.length, lenth_of_words), self.domains[i])

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.
        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # start with false 
        # revised = False
        # # empty list
        # update_words = []
        # # check if words overlap in assigment
        # if self.crossword.overlaps[x, y] is not None:
        #     # iterate over x and y values
        #     for word1 in self.domains[x]:
        #         for word2 in self.domains[y]:
        #             # 1 words should not be the same
        #             # 2 the lengh of them must be more that letters of overlap
        #             # 3 check if i-th value of x not equal to the j-th value of y
        #             if word1 != word2 \
        #             and len(word1) >= (self.crossword.overlaps[x, y][0] + 1)\
        #             and len(word2) >= (self.crossword.overlaps[x, y][1] + 1) \
        #             and word1[self.crossword.overlaps[x, y][0]] != word2[self.crossword.overlaps[x, y][1]]:
        #                 # change status of revised
        #                 revised = True
        #                 # add to the list
        #                 update_words.append(word1)
        # # itetare of the NOT acr consistem words of x and remome them
        # for word in set(update_words):
        #     # pop the values of x from domain
        #     self.domains[x].remove(word)
        # #return the status 
        # return revised

        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap:
            a, b = overlap
            domains_to_remove = set()
            for x_domain in self.domains[x]:
                overlap_possible = False
                for y_domain in self.domains[y]:
                    if x_domain != y_domain and x_domain[a] == y_domain[b]:
                        overlap_possible = True
                        break
                # no value in y.domain satifies the constraints
                if not overlap_possible:
                    domains_to_remove.add(x_domain)
            if domains_to_remove:
                self.domains[x] -= domains_to_remove
                revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.
        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # check if named agrs is None
        if arcs is None:
            quere = []
            # iterate over each member of overlaping 
            for member in self.crossword.overlaps:
                # add to the quere if memeber is not None
                if self.crossword.overlaps[member] is not None:
                    quere.append(member)
        else:
            # otherwise make a copy
            quere = arcs.copy()
        # pop elements from quere untill it is empty
        while len(quere) > 0:
            x, y = quere.pop()
            # check consistency of X in Y domain 
            if self.revise(x, y):
                if not self.domains[x] == 0:
                    return False
                # iterate over and add combination that is consistent
                for z in self.crossword.neighbors(x) - self.domains[y]:
                    quere.append((z, x))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # for word in self.crossword.variables:
        #     if word not in assignment.keys() and assignment[word] not in self.crossword.words:
        #         return False
        # return True 

        for variable in self.crossword.variables:
            if variable not in assignment.keys():
                return False
            if assignment[variable] not in self.crossword.words:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # consistent = True
        # # check unique values of assigment and add to dict
        # values_words = {}
        # for word in assignment.values():
        #     values_words = word
        # # check one time uniqueness of word in 
        # for value in assignment.values():
        #     if value != values_words:
        #         consistent = False
        # # check the lenth of the words
        # for key, value in assignment.items():
        #     # print(key.length, [len(n) for n in value])
        #     # iterate over every len(word) 
        #     for num in [len(n) for n in value]:
        #         # check the lenght of word in assiment and word in the list
        #         if num != key.length:
        #             consistent = False
        # # no confilict with neightboring
        # # find all overlaps or not
        # values = self.crossword.overlaps #self
        # # select words that overplas (by not None value)
        # values_constrains = [i for i in values if values[i] is not None]
        # # set of value constrains
        # temp_set_1 = set()
        # for var, ind in values_constrains:
        #     temp_set_1.add(ind)
        # temp_set_2 = set()
        # for pair in creator.crossword.variables:
        #     temp_set_2.add(pair)
        # # check the is the two sets are equal
        # if temp_set_2 == temp_set_1:
        #     consistent = False
        # return consistent

        for x in assignment:
            word1 = assignment[x]
            if x.length != len(word1):
                return False

            for y in assignment:
                word2 = assignment[y]
                if x != y:
                    if word1 == word2:
                        return False

                    overlap = self.crossword.overlaps[x, y]
                    if overlap:
                        a, b = overlap
                        if word1[a] != word2[b]:
                            return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbors = self.crossword.neighbors(var)
        for i in assignment:
            if i in neighbors:
                neighbors.remove(i)

        result = []
        for val in self.domains[var]:
            total_ruled_out = 0
            for var2 in neighbors:
                for val2 in self.domains[var2]:
                    overlap = self.crossword.overlaps[var, var2]
                    if overlap:
                        a, b = overlap
                        if val[a] != val2[b]:
                            total_ruled_out += 1
            result.append([val, total_ruled_out])
        result.sort(key=lambda x: (x[1]))
        return [i[0] for i in result]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        list_of_variables = []
        for var in self.crossword.variables:
            if var not in assignment:
                list_of_variables.append([var, len(self.domains[var]), len(self.crossword.neighbors(var))])

        if list_of_variables:
            list_of_variables.sort(key=lambda x: (x[1], -x[2]))
            return list_of_variables[0][0]
        return None
                
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            new_assigment = assignment.copy()
            new_assigment[var] = val
            if self.consistent(new_assigment):
                result = self.backtrack(new_assigment)
                if result:
                    return result
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
