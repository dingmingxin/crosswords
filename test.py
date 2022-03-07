from crossword import Crossword
import logging

logging.basicConfig(level=logging.DEBUG)


#words = ['БУК', 'КЛУБ', 'КУБ', 'ЛУК']
#clues = ['БУК', 'КЛУБ', 'КУБ', 'ЛУК']

words = ['РЕБУС', 'БРУС', 'СЕРБ', 'СРУБ', 'БЕС', 'БУР']
clues = ['РЕБУС', 'БРУС', 'СЕРБ', 'СРУБ', 'БЕС', 'БУР']

words = ['ДУХ', 'УХО', 'УХОД', 'ХОД']
clues = ['ДУХ', 'УХО', 'УХОД', 'ХОД']
#words = ["ЛОТ","ОПТ","ОСЁЛ","ОТЁЛ","ПЛОТ","ПОЛ","ПОЛЁТ","ПОСТ","СТО","СТОЛ","СТОЛП","ТОП"]
#clues = ["ЛОТ","ОПТ","ОСЁЛ","ОТЁЛ","ПЛОТ","ПОЛ","ПОЛЁТ","ПОСТ","СТО","СТОЛ","СТОЛП","ТОП"]

cw = Crossword(words, clues)

tries = 10
grid = cw.getSquareGrid(tries)
print(grid)

