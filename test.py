from crossword import Crossword
import logging

logging.basicConfig(level=logging.DEBUG)


all_questions = []
all_questions.append(['КОТ', 'ТОК'])
all_questions.append(['БАР', 'БРА', 'РАБ'])
all_questions.append(['МУЖ', 'УЖ', 'УМ'])
all_questions.append(['ОПТ', 'ПОТ', 'ТОП'])
all_questions.append(['ДУХ', 'УХО', 'УХОД', 'ХОД'])
all_questions.append(['ЗАЛ', 'ЗОЛА', 'ЛАЗ'])
all_questions.append(['ДНО', 'ДОН', 'ФОН', 'ФОНД'])
all_questions.append(['МАРШ', 'ШАР', 'ШАРМ', 'ШРАМ'])
all_questions.append(['КОТ', 'СКОТ', 'СОК', 'СТОК', 'ТОК'])
all_questions.append(['ГРОМ', 'МОР', 'МОРГ', 'РОГ', 'РОМ'])
all_questions.append(['ЛЕС', 'ОСЕЛ', 'СЕЛО'])
all_questions.append(['ВОР', 'КРОВ', 'РОВ', 'РОК'])
all_questions.append(['БУК', 'КЛУБ', 'КУБ', 'ЛУК'])
all_questions.append(['РУИНА', 'РУНА', 'УРАН', 'УРНА'])
all_questions.append(['БЕС', 'БРУС', 'БУР', 'РЕБУС', 'СЕРБ', 'СРУБ'])
all_questions.append(['ДОМ', 'МОДА', 'ОДА'])
for i in range(len(all_questions)):
    words = all_questions[i]
    clues = words
    cw = Crossword(words, clues)

    tries = 20
    grid = cw.getSquareGrid(tries)
    # grid = cw.getGridWithMaximizedIntersections(10, tries)
    print("----------------------------------------", i, words)
    if None == grid:
        print(cw.getBadWords())
    else:
        for r in grid:
            print(",".join(r))
    print("----------------------------------------")

