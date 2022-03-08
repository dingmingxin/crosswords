import random
import math
import logging

GRID_EMPTY_CELL = "."

class CrosswordCell(object):
    def __init__(self, letter):
        self.char = letter
        self.across = None
        self.down = None
    def set_direction_node(self, direction, cell_node):
        if direction == "across":
            self.across = cell_node
        else:
            self.down = cell_node
    def __repr__(self):
        return self.char

class CrosswordCellNode(object):
    def __init__(self, is_start_of_word, index):
        self.is_start_of_word = is_start_of_word
        self.index = index 

class WordElement(object):
    def __init__(self, word, index):
        self.word = word 
        self.index = index 
    def __repr__(self):
        return self.word

GRID_ROWS = 50
GRID_COLS = 50

class Crossword(object):
    def __init__(self, words_in, clues_in):
        self.char_index = {}
        self.bad_words = []

        # constructor
        #if(len(words_in) < 2) throw "A crossword must have at least 2 words"
        #if(len(words_in) != len(clues_in)) throw "The number of words must equal the number of clues"

        self.grid = [None] * GRID_ROWS
        for i in range(GRID_ROWS):
            self.grid[i] = [None] * GRID_COLS

        # sorting idea from http:#stackoverflow.com/questions/943113/algorithm-to-generate-a-crossword/1021800#1021800
        words_in.sort(key = len, reverse=True)
        self.word_elements = []
        for i in range(len(words_in)):
            self.word_elements.append(WordElement(words_in[i], i))
        self.word_list = words_in

    def getSquareGrid(self, max_tries, only_words=True):
        best_grid = None
        best_ratio = 0

        for i in range(max_tries):
            a_grid = self.getGrid(1)
            if a_grid == None:
                continue
            ratio = min(len(a_grid), len(a_grid[0])) * 1.0 / max(len(a_grid), len(a_grid[0]))
            if ratio > best_ratio:
                best_grid = a_grid
                best_ratio = ratio
            if best_ratio == 1:
                break
        # logging.debug("getSquareGrid %s", self.word_list)
        # logging.debug("getSquareGrid %s", best_grid)
        return self.pretty_grid(best_grid, only_words)

    def getGrid(self, max_tries):
        if not self.word_elements[0]:
            return None
        for tries in range(max_tries):
            self.clear() 

            start_dir = self.randomDirection()
            r = math.floor(len(self.grid) / 2)
            c = math.floor(len(self.grid[0]) / 2)
            word_element = self.word_elements[0]
            if start_dir == "across":
                c -= math.floor(len(word_element.word)/2)
            else:
                r -= math.floor(len(word_element.word)/2)

            if self.canPlaceWordAt(word_element.word, r, c, start_dir) != False:
                self.placeWordAt(word_element.word, word_element.index, r, c, start_dir)
            else:
                self.bad_words = [word_element]
                return None

            groups = []
            groups.append(self.word_elements[1:])
            for g in range(len(groups)):
                word_has_been_added_to_grid = False
                for i in range(len(groups[g])):
                    word_element = groups[g][i]
                    best_position = self.findPositionForWord(word_element.word)

                    if not best_position: 
                        if len(groups) - 1 == g:
                            groups.append([])
                        groups[g+1].append(word_element)
                    else: 
                        r = best_position["row"]
                        c = best_position["col"]
                        dir = best_position['direction']
                        self.placeWordAt(word_element.word, word_element.index, r, c, dir)
                        word_has_been_added_to_grid = True
                if not word_has_been_added_to_grid:
                    break
            if  word_has_been_added_to_grid:
                return self.minimizeGrid()

        self.bad_words = groups[len(groups) - 1]
        return None

    def getBadWords(self):
        return self.bad_words

    def getLegend(self, grid):
        groups = {"across" : [], "down" : []}
        position = 1
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                cell = grid[r][c]
                increment_position = False
                for k in groups:
                    if cell and cell[k] and cell[k]['is_start_of_word']:
                        index = cell[k]['index']
                        groups[k].append({"position" : position, "index" : index, "clue" : clues_in[index], "word" : words_in[index]})
                        increment_position = True

                if increment_position:
                    position += 1
        return groups

    def minimizeGrid(self):
        r_min = GRID_ROWS-1
        r_max = 0
        c_min = GRID_COLS-1
        c_max = 0

        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                cell = self.grid[r][c]
                if cell != None:
                    if r < r_min:
                        r_min = r
                    if r > r_max:
                        r_max = r
                    if c < c_min: 
                        c_min = c
                    if c > c_max:
                        c_max = c

        rows = r_max - r_min + 1
        cols = c_max - c_min + 1
        new_grid = [None] * rows
        for r in range(rows):
            for c in range(cols):
                new_grid[r] = [None] * cols

        r = r_min
        for r2 in range(rows):
            c = c_min
            for c2 in range(cols):
                new_grid[r2][c2] = self.grid[r][c]
                c += 1
            r += 1

        return new_grid

    def addCellToGrid(self, word, index_of_word_in_input_list, index_of_char, r, c, direction):
        char = word[index_of_char:index_of_char+1]
        if self.grid[r][c] == None:
            self.grid[r][c] = CrosswordCell(char)

            if not char in self.char_index:
                self.char_index[char] = []

            self.char_index[char].append({"row" : r, "col" : c})

        is_start_of_word = 0
        index_of_char == 0

        #logging.debug("addcellToGrid %s %s %s", self.grid[r][c], word, direction)
        self.grid[r][c].set_direction_node(direction, CrosswordCellNode(is_start_of_word, index_of_word_in_input_list))

    def placeWordAt(self, word, index_of_word_in_input_list, row, col, direction):
        if direction == "across":
            i = 0
            for c in range(col, col+len(word)):
                self.addCellToGrid(word, index_of_word_in_input_list, i, row, c, direction)
                i += 1
        elif direction == "down":
            i = 0
            for r in range(row, row+len(word)):
                self.addCellToGrid(word, index_of_word_in_input_list, i, r, col, direction)
                i += 1
        else: 
            pass
    def canPlaceCharAt(self, char, row, col, word_intersections):
        word_cell = self.grid[row][col]
        if None == word_cell:
            return 0
        if word_cell.char == char:
            across_word_index = None 
            down_word_index = None
            if word_cell.across != None:
                across_word_index = word_cell.across.index
            if word_cell.down != None:
                down_word_index = word_cell.down.index

            if across_word_index != None and across_word_index in word_intersections:
                return -1

            if down_word_index != None and down_word_index in word_intersections:
                return -1

            word_intersections[across_word_index] = True
            word_intersections[down_word_index] = True
            return 1
        return -1

    def canPlaceWordAt(self, word, row, col, direction):
        #logging.debug("canPlaceCharAt == %s %i %i %s", word, row, col, direction)
        if row < 0 or row >= len(self.grid) or col < 0 or col >= len(self.grid[row]):
            return False

        word_intersections = {}

        if direction == "across":
            if col + len(word) > len(self.grid[row]):
                return False
            if col - 1 >= 0 and self.grid[row][col - 1] != None:
                return False
            if col + len(word) < len(self.grid[row]) and self.grid[row][col+len(word)] != None:
                return False

            i = 0
            r = row - 1
            for c in range(col, col+len(word)):
                if r<0:
                    break
                is_empty = self.grid[r][c] == None
                is_intersection = self.grid[row][c] != None and self.grid[row][c].char == word[i:i+1]
                can_place_here = is_empty or is_intersection
                if not can_place_here:
                    return False
                i += 1

            i = 0
            r = row + 1
            for c in range(col, col+len(word)):
                if r>=len(self.grid):
                    break
                is_empty = self.grid[r][c] == None
                is_intersection = self.grid[row][c] != None and self.grid[row][c].char == word[i:i+1]
                can_place_here = is_empty or is_intersection
                if not can_place_here:
                    return False
                i += 1

            intersections = 0
            i = 0
            for c in range(col, col+len(word)):
                result = self.canPlaceCharAt(word[i:i+1], row, c, word_intersections)
                if result == -1:
                    return False
                intersections += result
                i += 1

        elif direction == "down":
            if row + len(word) > len(self.grid):
                return False
            if row - 1 >= 0 and self.grid[row - 1][col] != None:
                return False
            if row + len(word) < len(self.grid) and self.grid[row+len(word)][col] != None:
                return False

            i = 0
            c = col - 1
            for r in range(row, row+len(word)):
                if c<0:
                    break
                is_empty = self.grid[r][c] == None
                is_intersection = self.grid[r][col] != None and self.grid[r][col].char == word[i:i+1]
                can_place_here = is_empty or is_intersection
                if not can_place_here:
                    return False
                i += 1

            i = 0
            c = col + 1
            for r in range(row, row+len(word)):
                if c>=len(self.grid[r]):
                    break
                is_empty = self.grid[r][c] == None
                is_intersection = self.grid[r][col] != None and self.grid[r][col].char == word[i:i+1]
                can_place_here = is_empty or is_intersection
                if not can_place_here:
                    return False
                i += 1


            intersections = 0
            i = 0
            for r in range(row, row+len(word)):
                result = self.canPlaceCharAt(word[i:i+1], r, col, word_intersections)
                if result == -1:
                    return False
                intersections += result
                i += 1

        else:
            pass
        if intersections == len(word):
            return False
        else:
            return True

    def randomDirection(self):
        if math.floor(random.random()*2) == 0:
            return "across"
        else: 
            return "down"

    def findPositionForWord(self, word):
        bests = []
        for i in range(len(word)):
            char = word[i:i+1]
            if char in self.char_index:
                possible_locations_on_grid = self.char_index[word[i:i+1]]
            else:
                continue

            for j in range(len(possible_locations_on_grid)):
                point = possible_locations_on_grid[j]
                r = point['row']
                c = point['col']
                intersections_across = self.canPlaceWordAt(word, r, c - i, "across")
                intersections_down = self.canPlaceWordAt(word, r - i, c, "down")

                if intersections_across != False:
                    bests.append({"intersections" : intersections_across, "row" : r, "col" : c - i, "direction" : "across"})
                if intersections_down != False:
                    bests.append({"intersections" : intersections_down, "row" : r - i, "col" : c, "direction" : "down"})

        if len(bests) == 0:
            return False

        best = bests[math.floor(random.random()*len(bests))]

        return best

    def clear(self):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                self.grid[r][c] = None
        self.char_index = {}

    def pretty_grid(self, grid, raw = True):
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if grid[r][c] == None:
                    grid[r][c] = GRID_EMPTY_CELL
                elif raw:
                    grid[r][c] = grid[r][c].char
        return grid
        


