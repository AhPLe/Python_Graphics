#Project 2
#Written by Arthur LeBlanc for class 6810
#Cohen-Sutherland algorithm source in comments at ComputeCode
import tkinter as tk
import argparse
import numpy as np
import re
import copy
from threading import Thread

INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

window = tk.Tk()
win_height = 500
win_width = 500

line_canvas = tk.Canvas(window, bg = "white", height = win_height, width = win_width)

lines = 50
length = 100
seed = 42
bresenham = False

def InputLines(datalines, num: int = -1, text = ''):
    #collects all datalines from file up to num
    #   or all lines from file if num == -1
    #if num == -1, all lines are read
    if text == '':
        file_str = input('input name of data file: ')
    else:
        file_str = text
    #np.loadtxt might be quicker
    with open(file_str, 'r') as f:
        output = f.read()
    lines = output.split('\n')
    datalines = []
    count = 0
    for line in lines:
        line_arr = (np.fromstring(line[0:], dtype = np.float, sep = ' '))
        if line_arr.size < 1:
            continue
        elif num >= 0 and count >= num: #allows user to specify the number of lines to input
            break
        line_arr = np.expand_dims(line_arr, axis = 0)
        line_arr = line_arr.reshape(2, 2)
        datalines.append(line_arr)
        count += 1
    datalines = np.array(datalines)
    #Old function - based on formatting [num, num, num]
    # for line in lines:
    #     line_arr = (np.fromstring(line[1:-1], dtype = np.int, sep = ', '))
    #     if line_arr.size < 1:
    #         continue
    #     elif num >= 0 and count == num: #allows user to specify the number of lines to input
    #         break
    #     if count < 1:
    #         datalines = line_arr
    #     else:
    #         datalines = np.vstack((datalines, line_arr))
    #     count += 1
    return datalines, count

def ApplyTransformation(matrix, datalines):
    #print('untested feature apply transformation')
    #applies the transformation matrix to all points in datalines
    matrix = np.array(matrix)
    initiallines = np.array(datalines)
    
    finallines = copy.deepcopy(initiallines)
    for line in finallines:
        for i in range(len(line)):
            templine = np.concatenate((line[i], np.array([1])), axis = 0)
            templine = np.matmul(templine, matrix)
            line[i] = templine[:len(line[i])]
    return finallines

#cohen-sutherland code from:
#https://codingee.com/computer-graphics-program-to-implement-cohen-sutherland-line-clipping-algorithm/
def ComputeCode(x_min, x_max, y_min, y_max, x, y):
    code = INSIDE
    if x < x_min:      # left of rectangle
        code |= LEFT
    elif x > x_max:    # right of rectangle
        code |= RIGHT
    if y < y_min:      # below
        code |= BOTTOM
    elif y > y_max:    # above
       code |= TOP
    return code

def CohenSutherlandClip(x_min, x_max, y_min, y_max, x1, y1, x2, y2):
    #see above for link to cohen-sutherland code source
    code1 = ComputeCode(x_min, x_max, y_min, y_max, x1, y1)
    code2 = ComputeCode(x_min, x_max, y_min, y_max, x2, y2)
    accept = False
    while True:
     
        if code1 == 0 and code2 == 0:
            accept = True
            break
         
        elif (code1 & code2) != 0:
            break
         
        else:
         
            x = 1.0
            y = 1.0
            if code1 != 0:
                code_out = code1
            else:
                code_out = code2
          
            if code_out & TOP:
         
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif code_out & BOTTOM:
         
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif code_out & RIGHT:
                 
        
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif code_out & LEFT:
        
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min
         
            if code_out == code1:
                x1 = x
                y1 = y
                code1 = ComputeCode(x_min, x_max, y_min, y_max, x1, y1)
            else:
                x2 = x
                y2 = y
                code2 = ComputeCode(x_min, x_max, y_min, y_max, x2, y2)
    return accept, x1, y1, x2, y2

def DisplayPixels(datalines, num, VPx1, VPx2, VPy1, VPy2):
    #print('unimplemented feature display pixels - viewport unimplemented')
    #Displays the pixels within the defined VP (viewport) coordinates
    draw = True
    x1 = x2 = y1 = y2 = 0
    for i in range(num):
        draw, x1, y1, x2, y2 = CohenSutherlandClip(\
                VPx1, VPx2, VPy1, VPy2, datalines[i][0][0], \
                datalines[i][0][1], datalines[i][1][0], datalines[i][1][1])
        if draw:
            draw_line(x1, y1, x2, y2)
    

def OutputLines(datalines, num):
    #print('untested feature output lines')
    #prints the contents of datalines to a specified file
    file_str = input('Please type the name of the output file: ')
    datalines = np.array(datalines, dtype = int)
    #np.savetxt might be a bit quicker
    with open(file_str, 'w') as f:
        for i in range(min(len(datalines), num)):
            arr = datalines[i]
            #string = ''.join((' '.join(str(arr[j])))for j in range(1, len(arr) - 1))
            
            #puts the string into the expected format
            string = ''
            for j in range(len(arr)):
                for k in range(len(arr[j])):
                    string += str(arr[j][k]) + ' '
            f.write(string[:-1] + '\n')
            #old method, based on format [num, num, num]
            # f.write('[' + arr[0])
            # f.write(', '.join(arr[j]))  for j in range(1, len(arr) - 1
            # f.write(arr[len(arr) - 1] + ']')

def BasicTranslate(Tx, Ty):
    #print('untested feature basic translate')
    #Creates a matrix to move the array by Tx in the x direction, 
    #   and Ty in the y direction
    matrix = np.array([[1, 0, 0], [0, 1, 0], [Tx, Ty, 1]])
    return matrix

def BasicScale(Sx, Sy):
    #print('untested feature basic scale')
    #Creates a matrix to scale the array by Sx and Sy
    matrix = np.array([[Sx, 0, 0], [0, Sy, 0], [0, 0, 1]])
    return matrix

def BasicRotate(angle):
    #Creates a matrix to rotate the array by angle degrees
    #print('untested feature basic rotate')
    radians = angle*2*np.pi/360
    matrix = np.array([[np.cos(radians), -np.sin(radians), 0], \
                       [np.sin(radians), np.cos(radians), 0], [0, 0, 1]])
    return matrix

def Scale(Sx, Sy, Cx, Cy):
    #print('untested feature scale')
    initialTranslate = BasicTranslate(-Cx, -Cy)
    scaleMatrix = BasicScale(Sx, Sy)
    finalTranslate = BasicTranslate(Cx, Cy)
    matrix = np.matmul(initialTranslate, scaleMatrix)
    matrix = np.matmul(matrix, finalTranslate)
    return matrix

def Rotate(angle, Cx, Cy):
    #implemented in degrees
    #print('untested feature rotate')
    initialTranslate = BasicTranslate(-Cx, -Cy)
    rotateMatrix = BasicRotate(angle)
    finalTranslate = BasicTranslate(Cx, Cy)
    matrix = np.matmul(initialTranslate, rotateMatrix)
    matrix = np.matmul(matrix, finalTranslate)
    return matrix

def quit():
    window.destroy()

def key(event):
    print("quitting")
    quit()

def handle_keypress(event):
    pass

def neg(x):
    return -x

def straight(x):    
    return x

def invert_coor(x, y):
    return y, x

def straight_coor(x, y):
    return x, y

def draw_line(x_initial, y_initial, x_final, y_final):
    x_initial = int(x_initial)
    y_initial = int(y_initial)
    x_final = int(x_final)
    y_final = int(y_final)
    
    x_change = x_final - x_initial
    y_change = y_final - y_initial
    
    if y_change < 0:
        y_funct = neg
        y_initial = -y_initial
        y_change = -y_change
    else:
        y_funct = straight
    
    if x_change < 0:
        x_funct= neg
        x_initial = -x_initial
        x_change = -x_change
    else:
        x_funct = straight

    if y_change > x_change:
        coor_funct = invert_coor
        
        temp_initial = x_initial
        temp_change = x_change
        temp_funct = x_funct
        x_initial = y_initial
        x_change = y_change
        x_funct = y_funct
        y_initial = temp_initial
        y_change = temp_change
        y_funct = temp_funct
        
    else:
        coor_funct = straight_coor
    
    #these were the only values not changed in the above code
    #this reassigns them instead of modifying them within the loop
    y_final = y_change + y_initial
    x_final = x_change + x_initial
    
    draw_line_bresenham(line_canvas, x_initial, x_final, y_initial, y_final, coor_funct, x_funct, y_funct)
    
    

def draw_point(line_canvas, x, y, coor_funct, xfunct, yfunct):
    x, y = coor_funct(xfunct(x), yfunct(y))
    line_canvas.create_rectangle((x, y)*2)

    
def draw_line_bresenham(line_canvas, x_initial, x_final, y_initial, y_final, coor_funct, xfunct, yfunct):
    delta_y = y_final - y_initial
    delta_x = x_final - x_initial
    big_e = 2*delta_y - delta_x
    inc1 = 2*delta_y
    inc2 = 2*(delta_y - delta_x)
    y = y_initial
    x = x_initial
    
    while (x < x_final):
        
        draw_point(line_canvas, x, y, coor_funct, xfunct, yfunct)
        if big_e < 0:
            big_e = big_e + inc1
        else:
            y = y + 1
            big_e = big_e + inc2
        x = x + 1
        
def DisplayVars(datalines, num, matrix):
    print('datalines:')
    print(datalines)
    print('num:', num)
    print('matrix:')
    print(matrix)

def ChangeNum(newNum):
    return newNum
    

def InstructionLoop(window, line_canvas):
    # define initial, possibly error-giving options
    select = -1;
    angle = Dx = Dy = Cx = Cy = 'i'
    num = -1
    datalines = np.array([])
    matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    #dictionary to select from, it's a small step towards
    #total integration of possible commands with the switch statement
    selectDict = {0: DisplayVars,
                  1: InputLines,
                  2: OutputLines,
                  3: DisplayPixels,
                  4: ApplyTransformation,
                  5: BasicTranslate,
                  6: BasicScale,
                  7: BasicRotate,
                  8: Scale,
                  9: Rotate,
                  10: ChangeNum
                  
        }
    #selectionData[select]() #perform function - if numbers are completely integrated
    
    #allow easy manipulation of the dictionary into a working, useful prompt
    #this defines a re that replaces the dictionary value with
    #a string that is easy to see for the user
    #example dictionary value is <Function Blargh at 0x89498126349>
    stringDict = str(selectDict)
    found = re.findall(r'(<\w+ (\w+) at \d\w+>)', stringDict, re.MULTILINE)
    for i in range(len(found)):
        stringDict = stringDict.replace(found[i][0], found[i][1])
    
    repeat = True
    #datalines, num = selectDict[1](datalines, num, 'd.txt')
    #window.update()
    while (repeat):
        print('available selections:', stringDict)
        select = input('Please input a selection or any other key to end: ')
        #apparently match case will be implemented in 3.10 python
        #so instead of working out a way to use it with dicts, I'll use if/else
        if select.isnumeric():
            select = int(select)
            
        if select == 1: #InputLines
            datalines, num = selectDict[select](datalines, num)
            
        elif select == 2:#OutputLines
            selectDict[select](datalines, num)
            
        elif select == 3:#DisplayPixels
            line_canvas.delete('all')
            Dx = input('Please input a number for Viewport x1 or '\
                       + 'anything for max window size: ')
            if str.isnumeric(Dx):
                Dx = int(Dx)
                Cx = int(input('Please input a number for Viewport x2: '))
                Dy = int(input('Please input a number for Viewport y1: '))
                Cy = int(input('Please input a number for Viewport y2: '))
            else:
                print('using max size for window')
                Dx = 0
                Cx = win_width
                Dy = 0
                Cy = win_height
            selectDict[select](datalines, num, VPx1 = Dx, VPx2 = Cx, VPy1 = Dy, VPy2 = Cy)
            #line_canvas.update()

        elif select == 4:#ApplyTransformation
            datalines = selectDict[select](matrix, datalines)
            
        elif select == 5:#BasicTranslate
            Dx = int(input('Please input a number for Translation x: '))
            Dy = int(input('Please input a number for Translation y: '))
            matrix = selectDict[select](Tx = Dx, Ty = Dy)
            
        elif select == 6:#BasicScale
            Dx = float(input('Please input a number for Scale x: '))
            Dy = float(input('Please input a number for Scale y: '))
            matrix = selectDict[select](Sx = Dx, Sy = Dy)
            
        elif select == 7:#BasicRotate
            angle = float(input('Please input a number for the angle: '))
            matrix = selectDict[select](angle = angle)
            
        elif select == 8:#Scale
            Dx = float(input('Please input a number for Scale x: '))
            Dy = float(input('Please input a number for Scale y: '))
            Cx = int(input('Please input a number for Center x: '))
            Cy = int(input('Please input a number for Center y: '))
            matrix = selectDict[select](Sx = Dx, Sy = Dy, Cx = Cx, Cy = Cy)
            
        elif select == 9:#Rotate
            angle = float(input('Please input a number for the angle: '))
            Cx = int(input('Please input a number for Center x: '))
            Cy = int(input('Please input a number for Center y: '))
            matrix = selectDict[select](angle = angle, Cx = Cx, Cy = Cy)
            
        elif select == 0:#displayVars
            selectDict[select](datalines, num, matrix)
        
        elif select == 10:
            newNum = int(input('Please input the number of lines to compute: '))
            num = selectDict[select](newNum)
            
        else:
            repeat = False
            
        #line_canvas.update()
    #window.destroy()
    #sys.exit()
    
    

parser = argparse.ArgumentParser()
#the user can specify the number of lines and the seed for the program through the command line
parser.add_argument('-n', action = "store", dest = "arg_lines",  #the number of lines
                    default = lines,   type = int)
parser.add_argument('-l', action = "store", dest = "arg_length",  #the number of lines
                    default = length,   type = int)
parser.add_argument('-s', action = "store", dest = "arg_seed",  #the seed
                    default = seed,   type = int)
parser.add_argument('-b', action = "store_true", #which algorithm
                    dest = "bresenham", default = bresenham)
                    #default False - declared at the top
parser.add_argument('-t', action = "store_true", #which algorithm
                    dest = "table", default = False)
parser.add_argument('-cf', action = "store_true", #which algorithm
                    dest = "configured", default = False)

args = parser.parse_args()
lines = args.arg_lines
length = args.arg_length
seed = args.arg_seed
bresenham = args.bresenham
table_gen = args.table

line_canvas.focus_set()

line_canvas.pack()

line_canvas.focus_set()

keyQuit = 'q'

class WindowThread(Thread):
    def run(self):
        window.mainloop()
        print('%s finished' % self.name)

class LoopThread(Thread):
    def run(self):
        InstructionLoop(window, line_canvas)
        # try:
            
        # except:
        #     #on error, attempting to make sure the program will close all windows
        #     window.destroy()
        #     raise
        print('%s finished' % self.name)
        print('press %s to end ' % keyQuit)


loopT = LoopThread()
loopT.name = 'loop thread'
loopT.start()
line_canvas.bind(keyQuit, key)

window.mainloop()
loopT.join()

# windowT = WindowThread()
# windowT.name = 'window thread'
# windowT.start()

#InstructionLoop(windowT, window, line_canvas)
#windowT.join()
#window.destroy()
print('program finished')
#


# if (args.configured):
#     configured_lines(line_canvas, bresenham)
# else:
#     if table_gen:
#         nums = [1, 10, 100, 1000, 5000]
#         times = []
#         for j in range(len(nums)):
#             st, et = start_lines(nums[j], seed, line_canvas, length, bresenham)
#             times.append(et-st)
#         print(times)
#     else:
#         start_lines(lines, seed, line_canvas, length, bresenham)

# def draw_line_normal(line_canvas, x_initial, y_initial, slope_normal, length, coor_funct, xfunct, yfunct):
#     x = x_initial
#     for i in range(length):
#         x = x_initial + i
#         y = y_initial + math.floor(i*slope_normal)
#         draw_point(line_canvas, x, y, coor_funct, xfunct, yfunct)
    
# def configured_lines(line_canvas, bresenham):
#     #defining all necessary lines
#     line1 = [10, 10, 30, 10]
#     line2 = [10, 10, 10, 30]
#     line3 = [30, 10, 10, 10]
#     line4 = [10, 30, 10, 10]
#     line5 = [10, 10, 20, 30]
#     line6 = [10, 30, 20, 10]
#     line7 = [20, 30, 10, 10]
#     line8 = [20, 10, 10, 30]
#     #converting them into an easy to use format:
#     lines = [line1, line2, line3, line4, line5, line6, line7, line8]
#     #converting lines to slope format as expected in the program:
#     for line in lines:
#         #while this should be a function, it is mirrored with the code in the random loop
        
#         x_initial = line[0]
#         y_initial = line[1]
#         x_final = line[2]
#         y_final = line[3]
        
#         x_change = line[2] - line[0]
#         y_change = line[3] - line[1]
        
#         if y_change < 0:
#             y_funct = neg
#             y_initial = -y_initial
#             y_change = -y_change
#         else:
#             y_funct = straight
        
#         if x_change < 0:
#             x_funct= neg
#             x_initial = -x_initial
#             x_change = -x_change
#         else:
#             x_funct = straight

#         if y_change > x_change:
#             coor_funct = invert_coor
            
#             temp_initial = x_initial
#             temp_change = x_change
#             temp_funct = x_funct
#             x_initial = y_initial
#             x_change = y_change
#             x_funct = y_funct
#             y_initial = temp_initial
#             y_change = temp_change
#             y_funct = temp_funct
            
#         else:
#             coor_funct = straight_coor
        
#         slope = y_change/x_change
        
#         #instead of modifying the above to reflect the change
#         #I opted to change y_final/x_final like it does in the random program itself
#         y_final = y_change + y_initial
#         x_final = x_change + x_initial

#         if bresenham:
#             draw_line_bresenham(line_canvas, x_initial, x_final, y_initial, y_final, coor_funct, x_funct, y_funct)
#         else:
#             draw_line_normal(line_canvas, x_initial, y_initial, slope, int(x_change), coor_funct, x_funct, y_funct)

# def start_lines(lines, seed, line_canvas, length, bresenham):
#     #defines the initial setup
#     seed = random.seed(seed)
#     x_min = 0
#     x_max= win_width
#     y_min = 0
#     y_max = win_height
#     length = length
#     start_time = datetime.datetime.now()
#     for i in range(lines):
#         #defines where they start
#         x_initial = random.randint(x_min, x_max)
#         y_initial = random.randint(y_min, y_max)
#         #defines the 1/2 unit length changes - corrected later
#         x_change_1 = random.random() - 0.5
#         y_change_1 = random.random() - 0.5
        
#         if y_change_1 < 0:
#             y_funct = neg
#             y_initial = -y_initial
#             y_change_1 = -y_change_1
#         else:
#             y_funct = straight
        
#         if x_change_1 < 0:
#             x_funct= neg
#             x_initial = -x_initial
#             x_change_1 = -x_change_1
#         else:
#             x_funct = straight

#         if y_change_1 > x_change_1:
#             coor_funct = invert_coor
            
#             temp_initial = x_initial
#             temp_change_1 = x_change_1
#             temp_funct = x_funct
#             x_initial = y_initial
#             x_change_1 = y_change_1
#             x_funct = y_funct
#             y_initial = temp_initial
#             y_change_1 = temp_change_1
#             y_funct = temp_funct
            
#         else:
#             coor_funct = straight_coor
        
#         slope = y_change_1/x_change_1
#         print(y_funct(x_funct(slope)))
        
#         #1/2 unit length changes corrected to normal lengths
#         y_change = slope * length
#         x_change = math.sqrt(length*length - y_change*y_change)
        
#         y_final = y_change + y_initial
#         x_final = x_change + x_initial        
        
#         if bresenham:
#             draw_line_bresenham(line_canvas, x_initial, x_final, y_initial, y_final, coor_funct, x_funct, y_funct)
#         else:
#             draw_line_normal(line_canvas, x_initial, y_initial, slope, int(x_change), coor_funct, x_funct, y_funct)
#     end_time = datetime.datetime.now()
#    return start_time, end_time
        
        #to be able to equate both methods, all variables must be computed
        #before either function starts, and the computations should be identical
        
        #this should insure an even time based field once the function starts
        #in java and c++ the compiler may throw out useless variables
        #but I believe that is not the case for python (this may be false)

#def InputPrompt():

#def InputLinesFunct(select):


