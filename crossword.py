import random
import math
import logging

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
        self.index = index # use to map this node to its word or clue

class WordElement(object):
    def __init__(self, word, index):
        self.word = word # the actual word
        self.index = index # use to map this node to its word or clue
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

        # build the grid
        self.grid = [None] * GRID_ROWS
        for i in range(GRID_ROWS):
            self.grid[i] = [None] * GRID_COLS

        # build the element list (need to keep track of indexes in the originial input arrays)
        words_in.sort(key = len, reverse=True)
        self.word_elements = []
        for i in range(len(words_in)):
            self.word_elements.append(WordElement(words_in[i], i))

        # I got this sorting idea from http:#stackoverflow.com/questions/943113/algorithm-to-generate-a-crossword/1021800#1021800
        # seems to work well
        #self.word_elements.sort(key=len)

    def getSquareGrid(self, max_tries):
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
        return best_grid

    def getGrid(self, max_tries):
        if not self.word_elements[0]:
            return None
        for tries in range(max_tries):
            self.clear() # always start with a fresh grid and char_index
            # place the first word in the middle of the grid
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
                bad_words = [word_element]
                return None

            # start with a group containing all the words (except the first)
            # as we go, we try to place each word in the group onto the grid
            # if the word can't go on the grid, we add that word to the next group 
            groups = []
            groups.append(self.word_elements[1:])
            for g in range(len(groups)):
                word_has_been_added_to_grid = False
                # try to add all the words in this group to the grid
                for i in range(len(groups[g])):
                    word_element = groups[g][i]
                    best_position = self.findPositionForWord(word_element.word)

                    if not best_position: 
                        # make the new group (if needed)
                        if len(groups) - 1 == g:
                            groups.append([])
                        # place the word in the next group
                        groups[g+1].append(word_element)
                    else: 
                        r = best_position["row"]
                        c = best_position["col"]
                        dir = best_position['direction']
                        self.placeWordAt(word_element.word, word_element.index, r, c, dir)
                        word_has_been_added_to_grid = True
                # if we haven't made any progress, there is no point in going on to the next group
                if not word_has_been_added_to_grid:
                    break
            # no need to try again
            if  word_has_been_added_to_grid:
                return self.minimizeGrid()

        bad_words = groups[len(groups) - 1]
        return None

    # returns the list of WordElements that can't fit on the crossword
    def getBadWords(self):
        return bad_words

    # get two arrays ("across" and "down") that contain objects describing the
    # topological position of the word (e.g. 1 is the first word starting from
    # the top left, going to the bottom right), the index of the word (in the
    # original input list), the clue, and the word itself
    def getLegend(self, grid):
        groups = {"across" : [], "down" : []}
        position = 1
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                cell = grid[r][c]
                increment_position = False
                # check across and down
                for k in groups:
                    # does a word start here? (make sure the cell isn't None, first)
                    if cell and cell[k] and cell[k]['is_start_of_word']:
                        index = cell[k]['index']
                        groups[k].append({"position" : position, "index" : index, "clue" : clues_in[index], "word" : words_in[index]})
                        increment_position = True

                if increment_position:
                    position += 1
        return groups

    # move the grid onto the smallest grid that will fit it
    def minimizeGrid(self):
        # find bounds
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

        # initialize new grid
        rows = r_max - r_min + 1
        cols = c_max - c_min + 1
        new_grid = [None] * rows
        for r in range(rows):
            for c in range(cols):
                new_grid[r] = [None] * cols

        # copy the grid onto the smaller grid
        r = r_min
        for r2 in range(rows):
            c = c_min
            for c2 in range(cols):
                new_grid[r2][c2] = self.grid[r][c]
                c += 1
            r += 1

        return new_grid

    # helper for placeWordAt()
    def addCellToGrid(self, word, index_of_word_in_input_list, index_of_char, r, c, direction):
        char = word[index_of_char:index_of_char+1]
        if self.grid[r][c] == None:
            self.grid[r][c] = CrosswordCell(char)

            # init the char_index for that character if needed
            if not char in self.char_index:
                self.char_index[char] = []

            # add to index
            self.char_index[char].append({"row" : r, "col" : c})

        is_start_of_word = 0
        index_of_char == 0

        #logging.debug("addcellToGrid %s %s %s", self.grid[r][c], word, direction)
        self.grid[r][c].set_direction_node(direction, CrosswordCellNode(is_start_of_word, index_of_word_in_input_list))

    # place the word at the row and col indicated (the first char goes there)
    # the next chars go to the right (across) or below (down), depending on the direction
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
            #todo 
            #throw "Invalid Direction"

    # you can only place a char where the space is blank, or when the same
    # character exists there already
    # returns False, if you can't place the char
    # 0 if you can place the char, but there is no intersection
    # 1 if you can place the char, and there is an intersection
    def canPlaceCharAt(self, char, row, col):
        # no intersection
        if self.grid[row][col] == None:
            return 0
        # intersection!
        if self.grid[row][col].char == char:
            return 1
        return -1

    # determines if you can place a word at the row, column in the direction
    def canPlaceWordAt(self, word, row, col, direction):
        #logging.debug("canPlaceCharAt == %s %i %i %s", word, row, col, direction)
        # out of bounds
        if row < 0 or row >= len(self.grid) or col < 0 or col >= len(self.grid[row]):
            return False

        if direction == "across":
            # out of bounds (word too long)
            if col + len(word) > len(self.grid[row]):
                #logging.debug("canplayce word at return none 1")
                return False
            # can't have a word directly to the left
            if col - 1 >= 0 and self.grid[row][col - 1] != None:
                #logging.debug("canplayce word at return none 2")
                return False
            # can't have word directly to the right
            if col + len(word) < len(self.grid[row]) and self.grid[row][col+len(word)] != None:
                #logging.debug("canplayce word at return none 3")
                return False

            # check the row above to make sure there isn't another word
            # running parallel. It is ok if there is a character above, only if
            # the character below it intersects with the current word
            i = 0
            r = row - 1
            for c in range(col, col+len(word)):
                if r<0:
                    break
                is_empty = self.grid[r][c] == None
                is_intersection = self.grid[row][c] != None and self.grid[row][c].char == word[i:i+1]
                can_place_here = is_empty or is_intersection
                if not can_place_here:
                    #logging.debug("canplayce word at return none 4")
                    return False
                i += 1

            # same deal as above, we just search in the row below the word
            i = 0
            r = row + 1
            for c in range(col, col+len(word)):
                if r>=len(self.grid):
                    break
                is_empty = self.grid[r][c] == None
                is_intersection = self.grid[row][c] != None and self.grid[row][c].char == word[i:i+1]
                can_place_here = is_empty or is_intersection
                if not can_place_here:
                    #logging.debug("canplayce word at return none 5")
                    return False
                i += 1

            # check to make sure we aren't overlapping a char (that doesn't match)
            # and get the count of intersections
            intersections = 0
            i = 0
            for c in range(col, col+len(word)):
                result = self.canPlaceCharAt(word[i:i+1], row, c)
                if result == -1:
                    #logging.debug("canplayce word at return none 6 %s", result)
                    return False
                intersections += result
                i += 1

        elif direction == "down":
            # out of bounds
            if row + len(word) > len(self.grid):
                return False
            # can't have a word directly above
            if row - 1 >= 0 and self.grid[row - 1][col] != None:
                return False
            # can't have a word directly below
            if row + len(word) < len(self.grid) and self.grid[row+len(word)][col] != None:
                return False

            # check the column to the left to make sure there isn't another
            # word running parallel. It is ok if there is a character to the
            # left, only if the character to the right intersects with the
            # current word
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

            # same deal, but look at the column to the right
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


            # check to make sure we aren't overlapping a char (that doesn't match)
            # and get the count of intersections
            intersections = 0
            i = 0
            for row in range(row, row+len(word)):
                result = self.canPlaceCharAt(word[i:i+1], r, col)
                if result == -1:
                    return False
                intersections += result
                i += 1

        else:
            pass
            # todo
            #throw "Invalid Direction"
        #logging.debug("canPlaceWordAt --- %i", intersections)
        return True

    def randomDirection(self):
        if math.floor(random.random()*2) == 0:
            return "across"
        else: 
            return "down"

    def findPositionForWord(self, word):
        # check the char_index for every letter, and see if we can put it there in a direction
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
                # the c - i, and r - i here compensate for the offset of character in the word
                intersections_across = self.canPlaceWordAt(word, r, c - i, "across")
                intersections_down = self.canPlaceWordAt(word, r - i, c, "down")

                if intersections_across != False:
                    bests.append({"intersections" : intersections_across, "row" : r, "col" : c - i, "direction" : "across"})
                if intersections_down != False:
                    bests.append({"intersections" : intersections_down, "row" : r - i, "col" : c, "direction" : "down"})

        if len(bests) == 0:
            return False

        # find a good random position
        best = bests[math.floor(random.random()*len(bests))]

        return best

    def clear(self):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                self.grid[r][c] = None
        self.char_index = {}

