import pygame
import clingo
from tkinter import Tk  # not advisable to import everything with *
from tkinter import filedialog
from ast import literal_eval # To parse the clingo output
import threading

def update():
    pygame.display.update()

def drawTable(nrows, ncols, width, height, background_color):    
    pygame.init()
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Heyawake solver by Arturo Pérez Sánchez")
    win.fill(background_color)

    # Table dimensions
    gridWidth = width - 350
    gridHeight = height- 50
    cellWidth = (gridWidth)/(ncols+1)
    cellHeight = (gridWidth)/(nrows+1)

    # Columns
    for i in range(0, ncols +1):
        pygame.draw.line(win, 'black', (50 + cellWidth*i, 50), (50 + cellWidth*i, 50 + cellHeight*nrows), 2)

    # Rows
    for i in range(0, nrows +1):
        pygame.draw.line(win, 'black', (50, 50 + cellHeight*i), (50+cellWidth*ncols, 50 + cellHeight*i), 2)


    pygame.display.update()
    return win, cellWidth, cellHeight

def drawBoxes(win, boxes, cellWidth, cellHeight, nrows):
    for box in boxes:
        #Left
        pygame.draw.line(win, 'black', (50 + cellWidth*(box[1]-1), 50 + cellHeight*(nrows-box[2]+1)), 
                                       (50 + cellWidth*(box[1]-1), 50 + cellHeight*(nrows-box[4])),5)
        #Top
        pygame.draw.line(win, 'black', (50 + cellWidth*(box[1]-1), 50 + cellHeight*(nrows-box[2]+1)), 
                                        (50 + cellWidth*(box[3]), 50 + cellHeight*(nrows-box[2]+1)),5)
        #Right
        pygame.draw.line(win, 'black', (50 + cellWidth*(box[3]), 50 + cellHeight*(nrows-box[2]+1)), 
                                        (50 + cellWidth*(box[3]), 50 + cellHeight*(nrows-box[4])),5)
        #Bottom
        pygame.draw.line(win, 'black', (50 + cellWidth*(box[1]-1), 50 + cellHeight*(nrows-box[4])), 
                                        (50 + cellWidth*(box[3]), 50 + cellHeight*(nrows-box[4])),5)

def drawNumbers(win, boxes, numbers, cellWidth, cellHeight, nrows, fontFamily, fontSize):
    myfont = pygame.font.SysFont(fontFamily, fontSize)
    for number in numbers:
        for box in boxes:
            if (number[0] == box[0]):
                if(number[1] != -1):
                    text = myfont.render(str(number[1]), True, 'black')
                    win.blit(text, (50 + (cellWidth - text.get_width())/2 + cellWidth*(box[1]-1), 50 + (cellHeight - text.get_height())/2 + (cellHeight*(nrows-box[4]))))
                break
    pygame.display.update()

def drawButtons(win, width, height, fontFamily, buttonsFontSize):
    myfont = pygame.font.SysFont(fontFamily, buttonsFontSize)

    b1 = [width-300,height*0.1, 250, 50]
    # LOAD FILE BUTTON
    pygame.draw.rect(win,'lightgreen',b1)
    text1 = myfont.render("LOAD FILE", True, 'black')
    text1_width = text1.get_width()
    text1_height = text1.get_height()
    win.blit(text1, ((150 - text1_width)/2 + width-250, (50 - text1_height)/2 + height*0.1))

    b2 = [width-300,height*0.3, 250, 50]
    # SOLVE BUTTON
    pygame.draw.rect(win,'orange',b2)
    text2 = myfont.render("SOLVE", True, 'black')
    text2_width = text2.get_width()
    text2_height = text2.get_height()
    win.blit(text2, ((150 - text2_width)/2 + width-250, (50 - text2_height)/2 + height*0.3))

    b3 = [width-325,height*0.47, 50, 50]
    image = pygame.image.load('images/logoUS.png')
    win.blit(image, b3)

    pygame.display.update()

    return b1, b2

def select_file():
    root = Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(filetypes=(("Clingo Files", ".lp"), ("All Files", "*.*")))
    root.destroy()
    return filename

def read_file(filename):
    f = open(filename, "r")
    text = ''

    # Remove comments
    inComment = False
    for x in f:
        if('%*' in x):
            inComment = True
        if('%*' in x and '*%' in x):
            if(x.rfind('*%') > x.rfind('%*')):
                inComment = False
                pass
            else:
                inComment = True
        elif('*%' in x):
            inComment = False
            pass

        if(inComment or '%' in x):
            pass
        else:
            text +=x

    # Remove white spaces and separate each instruction
    text = text.replace(" ", "")
    text = text.split('.')

    # add each instruction params to boxes or numbers array
    boxes = []
    numbers = []
    ncols = 0
    nrows = 0
    for i in text:
        if ('room(' in i):
            i = i.replace("room(", "").replace(")", "")
            boxes.append([int(j) for j in i.split(',')])
        elif ('has(' in i):
            i = i.replace("has(", "").replace(")", "")
            numbers.append([int(j) for j in i.split(',')])
    nboxes = len(boxes)
    for box in boxes:
        if (box[1] > ncols):
            ncols = box[1]
        if (box[3] > ncols):
            ncols = box[3]
        if (box[2] > nrows):
            nrows = box[2]
        if (box[4] > nrows):
            nrows = box[4]
    return boxes, numbers, ncols, nrows, nboxes

class Context:
     def id(self, x):
         return x
     def seq(self, x, y):
         return [x, y]

def on_finish(sat):
    if(sat.unsatisfiable):
        print('Instancia insatisfacible')

def on_model(win, cellWidth, cellHeight, nrows, numbers, boxes, model):
    solution = parseSolution(str(model))
    displaySolution(win, cellWidth, cellHeight, nrows, numbers, boxes, solution)

def solve(win, cellWidth, cellHeight, nrows, ncols, nboxes, instance, numbers, boxes, solver='solver.lp'):
    ctl = clingo.Control("1")
    ctl.load(instance)
    tableSizes = "col(1.." + str(ncols) + "). row(1.." + str(nrows) + "). num(0.." + str(nboxes-1) + ")."
    ctl.load(solver)
    ctl.add("base", [], tableSizes + "#show black/2.")
    ctl.ground([("base", [])], context=Context())
    ctl.solve(on_finish=on_finish, on_model=lambda m: on_model(win, cellWidth, cellHeight, nrows, numbers, boxes,m))

def parseSolution(text):
    text = text.replace(" ", "")
    text = text.split('black')
    items = list(filter(None, text))
    res = []
    for i in items:
        res.append(literal_eval(i))
    return res

def displaySolution(win, cellWidth, cellHeight, nrows, numbers, boxes, solution, fontFamily='Comic Sans MS', fontSize=22):
    myfont = pygame.font.SysFont(fontFamily, fontSize)
    
    for x,y in solution:
        # Draw de black cells
        pygame.draw.rect(win, 'black', (50 + cellWidth*(x-1) +1, 50 + (cellHeight*(nrows-y) + 1), cellWidth, cellHeight))

        # Cambiamos el color de las letras que tapamos
        myfont = pygame.font.SysFont(fontFamily, fontSize)
        for number in numbers:
            for box in boxes:
                if (number[0] == box[0] and number[1] != -1 and box[1] ==x and box[4] ==y):
                    text = myfont.render(str(number[1]), True, 'white')
                    win.blit(text, (50 + (cellWidth - text.get_width())/2 + cellWidth*(box[1]-1), 50 + (cellHeight - text.get_height())/2 + (cellHeight*(nrows-box[4]))))
                    break
    pygame.display.update()

def main(nrows=10, ncols=10, nboxes=10, width=850, height=550, background_color='#cccccc', fontFamily='Comic Sans MS', fontSize=22, buttonsFontSize=26, filename=''):
    # Initialization
    win, cellWidth, cellHeight = drawTable(nrows, ncols, width, height, background_color)
    b1, b2 = drawButtons(win, width, height, fontFamily, buttonsFontSize)
    numbers = []
    boxes = []
    # Main loop
    while True:
        t = threading.Thread(target = update)
        t.start()
        for event in pygame.event.get():
            # Close windows event
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            # Buttons functionality
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # load file button
                if(b1[0] < x < (b1[0] + b1[2]) and b1[1] < y < (b1[1] + b1[3])):
                    # Open the file explorer folder
                    filename = select_file()
                    if(filename):
                        # Reads and parse the selected file
                        boxes, numbers, ncols, nrows, nboxes = read_file(filename)

                        # Redraw de screen to refresh the data
                        win, cellWidth, cellHeight = drawTable(nrows, ncols, width, height, background_color)
                        b1, b2 = drawButtons(win, width, height, fontFamily, buttonsFontSize)

                        # Draw the new game instance
                        drawBoxes(win, boxes,  cellWidth, cellHeight, nrows)
                        drawNumbers(win, boxes, numbers, cellWidth, cellHeight, nrows, fontFamily, fontSize)
                    
                # solve button
                elif((b2[0] < x < (b2[0] + b2[2]) and b2[1] < y < (b2[1] + b2[3])) and filename):
                    solve(win, cellWidth, cellHeight, nrows, ncols, nboxes, filename, numbers, boxes)

            # Buttons hover effect
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if((b1[0] < x < (b1[0] + b1[2]) and b1[1] < y < (b1[1] + b1[3])) or (b2[0] < x < (b2[0] + b2[2]) and b2[1] < y < (b2[1] + b2[3]))):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

if __name__ == "__main__":

    # Hyperparameters
    nrows=10 # Number of rows
    ncols=10 # Number of columns
    nboxes = 10 # number of boxes
    width=850 # Screen width
    height=550 # Screen height
    background_color='white' # Background color
    fontFamily='Comic Sans MS' # Font family
    fontSize=22 # Size of the font
    buttonsFontSize=26 # Size of the buttons font
    filename=''

    # Main loop call
    main(nrows, ncols, nboxes, width, height, background_color, fontFamily, fontSize, buttonsFontSize, filename)
