from crossword import Crossword


words = ['БУК', 'КЛУБ', 'КУБ', 'ЛУК']
clues = ['БУК', 'КЛУБ', 'КУБ', 'ЛУК']

cw = Crossword(words, clues)

tries = 10; 
grid = cw.getSquareGrid(tries)
print(grid)
