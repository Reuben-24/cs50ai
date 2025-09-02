import sys

from crossword import *


class CrosswordCreator:

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
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
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            words_copy = self.domains[variable][:]
            for word in words_copy:
                if not len(word) == variable.length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False

        if (x, y) in self.crossword.overlaps:
            x_index = self.crossword.overlaps[x, y][0]
            y_index = self.crossword.overlaps[x, y][1]

            # iterate across x's domain
            x_words_copy = self.domains[x][:]
            for x_word in x_words_copy:
                satisfies = False
                for y_word in self.domains[y]:
                    if x_word[x_index] == y_word[y_index]:
                        satisfies = True
                        break

                if not satisfies:
                    self.domains[x].remove(x_word)
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
        # Initialise queue
        queue = []
        if arcs:
            queue.extend(arcs)
        else:
            # Populate queue with all arcs in CSP
            for x, y in self.crossword.overlaps:
                queue.append((x, y))
                queue.append((y, x))

        while queue:
            (x, y) = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                x_neighbours_to_enqueue = self.crossword.neighbors(x) - {y}
                for z in x_neighbours_to_enqueue:
                    queue.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Assignment complete if it contains all the variables from CSP
        return set(assignment.keys()) == self.crossword.variables

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check all values distinct
        if not len(assignment.values()) == len(set(assignment.values())):
            return False

        for variable in assignment:
            # Check all values correct length
            if not len(assignment[variable]) == variable.length:
                return False

        # Check all values don't conflict
        overlaps = self.crossword.overlaps
        for x, y in overlaps:
            if x in assignment and y in assignment:
                (x_index, y_index) = overlaps[x, y]
                if not assignment[x][x_index] == assignment[y][y_index]:
                    return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Get neighbours for var
        neighbors = self.crossword.neighbors(var)

        word_rules_out_dict = {}

        # For each word in vars domain, check how many values it would rule out for it's neighbours
        for var_word in self.domains[var]:
            word_rules_out_dict[var_word] = 0
            for neighbor in neighbors:
                # Skip neighbors that are already assigned
                if neighbor in assignment:
                    continue

                # Assume there is an overlap between neighbors
                overlap = self.overlaps.get((var, neighbor))
                if not overlap:
                    overlap = self.overlaps.get((neighbor, var))
                    var_index, neighbor_index = overlap[1], overlap[0]  # swap
                else:
                    var_index, neighbor_index = overlap

                for neighbor_word in self.domains[neighbor]:
                    # Rule out if the var_index of the overlap does not equal neighbour_index
                    if not var_word[var_index] == neighbor_word[neighbor_index]:
                        word_rules_out_dict[var_word] += 1

        return sorted(self.domains[var], key=lambda word: word_rules_out_dict[word])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Get variable with smallest domain
        unassigned_domains = {
            var: self.domains[var] for var in self.domains if var not in assignment
        }
        min_size = min(len(domain) for domain in unassigned_domains.values())
        mrv_variables = [
            var for var, domain in unassigned_domains.items() if len(domain) == min_size
        ]
        if len(mrv_variables) == 1:
            return mrv_variables[0]

        mrv_variables_degree_dict = {}

        for var in mrv_variables:
            unassigned_neighbors = [
                n for n in self.crossword.neighbors(var) if n not in assignment
            ]
            degree = len(unassigned_neighbors)
            mrv_variables_degree_dict[var] = degree

        mrv_variables_by_degree_desc = sorted(
            mrv_variables, key=lambda var: mrv_variables_degree_dict[var], reverse=True
        )

        return mrv_variables_by_degree_desc[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


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
