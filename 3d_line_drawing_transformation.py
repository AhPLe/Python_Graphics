#Project 2
#Written by Arthur LeBlanc for class 6810
#Cohen-Sutherland algorithm source in comments at ComputeCode
import tkinter as tk
import argparse
import numpy as np
import re
import copy
from threading import Thread

verbose = False

INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

window = tk.Tk()
win_height = 750
win_width = 750

line_canvas = tk.Canvas(window, bg = "white", height = win_height, width = win_width)

lines = 50
length = 100
seed = 42
bresenham = False

xEye = 0
yEye = 0
zEye = 0

worldToEye = np.identity(4)
screenDistance = 2.5 # cm - defined by project description
screenSize = 100 #cm, defined by project description

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
    return datalines, count

def InputLines3d(datalines, num: int = -1, text = ''):
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
        line_arr = line_arr.reshape(2, 3)
        datalines.append(line_arr)
        if verbose:
            print(line_arr)
        count += 1
    datalines = np.array(datalines)
    
    return datalines, count

def OutputLines(datalines, num):
    #prints the contents of datalines to a specified file
    file_str = input('Please type the name of the output file: ')
    datalines = np.array(datalines, dtype = int)
    #np.savetxt might be a bit quicker
    with open(file_str, 'w') as f:
        for i in range(min(len(datalines), num)):
            arr = datalines[i]
            string = ''
            for j in range(len(arr)):
                for k in range(len(arr[j])):
                    string += str(arr[j][k]) + ' '
            f.write(string[:-1] + '\n')

def OutputLines3d(datalines, num):
    #both this and normal outputlines are the same, there is no real difference
    
    #prints the contents of datalines to a specified file
    file_str = input('Please type the name of the output file: ')
    datalines = np.array(datalines, dtype = int)
    #np.savetxt might be a bit quicker
    with open(file_str, 'w') as f:
        for i in range(min(len(datalines), num)):
            arr = datalines[i]
            string = ''
            for j in range(len(arr)):
                for k in range(len(arr[j])):
                    string += str(arr[j][k]) + ' '
            if verbose:
                print('writing array:', string[:-1])
            f.write(string[:-1] + '\n')

def ApplyTransformation(matrix, datalines):
    #applies the transformation matrix to all points in datalines
    matrix = np.array(matrix)
    initiallines = np.array(datalines)
    
    finallines = copy.deepcopy(initiallines)
    for line in finallines:
        for i in range(len(line)):
            templine = np.concatenate((line[i], np.array([1])), axis = 0)
            templine = np.matmul(templine, matrix)
            line[i] = templine[:len(line[i])]
    if verbose:
        print('applying transformation:')
        print(finallines)
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

def DisplayPixels(datalines, num):
    #sends the Datalines coordinates to draw_line
    #this function is the proper method to implement 3D line clipping if necessary
    x1 = x2 = y1 = y2 = 0
    if num == -1:
        num = len(datalines)
    for i in range(num):
        
        x1 = datalines[i][0][0]
        y1 = datalines[i][0][1]
        x2 = datalines[i][1][0]
        y2 = datalines[i][1][1]
        draw_line(x1, y1, x2, y2)
        if verbose:
            print('should be drawing line with coords ({}, {}) to ({}, {})'.format(\
            x1, y1, x2, y2))

def WorldtoEye():
    #beginning coding of function to change from world to eye coordinates
    worldToEye = Basic3DTranslate(xEye, yEye, zEye)
    #rotation about the x axis
    xRotate = np.array([[1, 0, 0, 0], [0, 0, -1, 0], \
                        [0, 1, 0, 0], [0, 0, 0, 1]])
    worldToEye = np.matmul(worldToEye, xRotate)
    #y-rotation
    denominatorYRotate = np.sqrt(xEye*xEye + yEye*yEye)
    xEyeYRotate = xEye/denominatorYRotate
    yEyeYRotate = yEye/denominatorYRotate
    print(xEyeYRotate)
    yRotate = np.array([[-xEyeYRotate, 0, yEyeYRotate, 0], [0, 1, 0, 0],\
                        [-yEyeYRotate, 0, -xEyeYRotate, 0], [0, 0, 0, 1]])
    worldToEye = np.matmul(worldToEye, yRotate)
    #z-rotation
    denominatorZRotate = np.sqrt(zEye*zEye + denominatorYRotate*denominatorYRotate)
    xyEyeZRotate = denominatorYRotate/denominatorZRotate
    zEyeZRotate = zEye/denominatorZRotate
    zRotate = np.array([[1, 0, 0, 0], [0, xyEyeZRotate, zEyeZRotate, 0],\
                        [0, -zEyeZRotate, xyEyeZRotate, 0], [0, 0, 0, 1]])
    worldToEye = np.matmul(worldToEye, zRotate)
    #final z reorientation
    zReorient = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0],\
                          [0, 0, 0, 1]])
    worldToEye = np.matmul(worldToEye, zReorient)
    return worldToEye

def EyetoClip():
    #function to return the clipping matrix
    D = screenDistance
    S = screenSize/2
    clipConstant = D/S
    clipMatrix = [[clipConstant, 0, 0, 0], [0, clipConstant, 0, 0],\
                  [0, 0, 1, 0], [0, 0, 0, 1]]
    return clipMatrix

def DatalinetoClip(datalines, num):
    #beginning function to change from world to clip coordinates
    clipMatrix = EyetoClip()
    transformationMatrix = np.matmul(worldToEye, clipMatrix)
    
    ApplyTransformation(transformationMatrix, datalines[0:num])
    if verbose:
        print(datalines)
    return datalines

def EyeDatalinetoClip(datalines, num):
    #function to apply the clipping matrix to all datalines
    clipMatrix = EyetoClip()
    datalines = ApplyTransformation(clipMatrix, datalines)
    if verbose:
        print(datalines)
    return datalines

def EyetoScreen(xEye, yEye, zEye):
    #function to calculate one 2d coordinate from one 3d eye coordinate
    S = screenSize/2 # cm, dimension distance
    D = screenDistance
    xCenter = win_width/2
    yCenter = win_height/2
    if zEye != 0:
        xScreen = D*xEye/(S*zEye)*(win_width/2) + xCenter
        yScreen = D*yEye/(S*zEye)*(win_height/2) + yCenter
    else:
        xScreen = 4294967295
        yScreen = 4294967295
    return xScreen, yScreen
    
def LinesEyetoScreen(datalines, num):
    #function to change 3d eye coordinates to 2d coordinates
    x = 0
    y = 1
    z = 2
    datalines2d = []
    for i in range(num):
        coords2dStart = [EyetoScreen(datalines[i][0][x], datalines[i][0][y], datalines[i][0][z])]
        coords2dEnd = [EyetoScreen(datalines[i][1][x], datalines[i][1][y], datalines[i][1][z])]
        coords2d = np.concatenate((np.array(coords2dStart),\
                                   np.array(coords2dEnd)), axis = 0)
        datalines2d.append(coords2d)

    datalines2d = np.stack(tuple(datalines2d))
    if verbose:
        print(datalines2d)
    return datalines2d

def Display3DPixels(datalines, num):
    #beginning function to display the world coordinate functions
    datalines = DatalinetoClip(datalines, num)
    datalines2d = LinesEyetoScreen(datalines, num)
    DisplayPixels(datalines2d, num)

def DisplayEye3DPixels(datalines, num):
    #correct use of defined program function to display the coordinates
    datalines2d = LinesEyetoScreen(datalines, num)
    DisplayPixels(datalines2d, num)

def Basic3DTranslate(Tx, Ty, Tz):
    #creates a 3d matrix for translation
    matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [Tx, Ty, Tz, 1]])
    return matrix

def Basic3DScale(Sx, Sy, Sz):
    #creates a 3d matrix for scale
    matrix = np.array([[Sx, 0, 0, 0], [0, Sy, 0, 0], [0, 0, Sz, 0], [0, 0, 0, 1]])
    return matrix

def Basic3DRotate(angle, axis = 'x'):
    #creates a 3d matrix for rotatation
    radians = angle*2*np.pi/360
    if axis == 'x':
        matrix = np.array([[1, 0, 0, 0], [0, np.cos(radians), np.sin(radians), 0], \
                [0, -np.sin(radians), np.cos(radians), 0], [0, 0, 0, 1]])
    elif axis == 'y':
        matrix = np.array([[np.cos(radians), 0, -np.sin(radians), 0], \
                [0, 1, 0, 0], [np.sin(radians), 0, np.cos(radians), 0], [0, 0, 0, 1]])
    elif axis == 'z':
        matrix = np.array([[np.cos(radians), np.sin(radians), 0, 0], \
                [-np.sin(radians), np.cos(radians), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    else:
        print('no matching coordinate system, returning identity matrix')
        matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    return matrix

def BasicTranslate(Tx, Ty):
    #Creates a matrix to move the array by Tx in the x direction, 
    #   and Ty in the y direction
    matrix = np.array([[1, 0, 0], [0, 1, 0], [Tx, Ty, 1]])
    return matrix

def BasicScale(Sx, Sy):
    #Creates a matrix to scale the array by Sx and Sy
    matrix = np.array([[Sx, 0, 0], [0, Sy, 0], [0, 0, 1]])
    return matrix

def BasicRotate(angle):
    #Creates a matrix to rotate the array by angle degrees
    radians = angle*2*np.pi/360
    matrix = np.array([[np.cos(radians), -np.sin(radians), 0], \
                       [np.sin(radians), np.cos(radians), 0], [0, 0, 1]])
    return matrix

def Scale(Sx, Sy, Cx, Cy):
    #creates a matrix for scale with center
    initialTranslate = BasicTranslate(-Cx, -Cy)
    scaleMatrix = BasicScale(Sx, Sy)
    finalTranslate = BasicTranslate(Cx, Cy)
    matrix = np.matmul(initialTranslate, scaleMatrix)
    matrix = np.matmul(matrix, finalTranslate)
    return matrix

def Rotate(angle, Cx, Cy):
    #creates a matrix that rotates an object with defined center
    #implemented in degrees
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

def ChangeScreenDistance(newDistance):
    global screenDistance 
    screenDistance = newDistance
    
def ChangeScreenSize(newSize):
    global screenSize
    screenSize = newSize

def InstructionLoop3D(window, line_canvas):
    # define initial, possibly error-giving options
    select = -1;
    axis = angle = Dx = Dy = Dz = 'i'
    num = -1
    datalines = np.array([])
    matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    #WorldtoEye()
    
    #dictionary to select from, it's a small step towards
    #total integration of possible commands with the switch statement
    selectDict = {0: DisplayVars,
                  1: InputLines3d,
                  2: OutputLines3d,
                  3: DisplayEye3DPixels,
                  4: ApplyTransformation,
                  5: Basic3DTranslate,
                  6: Basic3DScale,
                  7: Basic3DRotate,
                  8: ChangeNum,
                  9: ChangeScreenDistance,
                  11: ChangeScreenSize
                  
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
    while (repeat):
        print('available selections:', stringDict)
        select = input('Please input a selection or any other key to end: ')
        #apparently match case will be implemented in 3.10 python
        #so instead of working out a way to use it with dicts, I'll use if/else
        if select.isnumeric():
            select = int(select)
            print('selection:', select)

        if select == 0:#displayVars
            selectDict[select](datalines, num, matrix)        
            
        elif select == 1: #InputLines3d
            datalines, num = selectDict[select](datalines, num)
            
        elif select == 2:#OutputLines3d
            selectDict[select](datalines, num)
            
        elif select == 3:#Display3DEyePixels
            line_canvas.delete('all')
            selectDict[select](datalines, num)
            
        elif select == 4:#ApplyTransformation
            datalines = selectDict[select](matrix, datalines)

        elif select == 5:#Basic3DTranslation
            Dx = float(input('Please input a number for x Translation: '))
            Dy = float(input('Please input a number for y Translation: '))
            Dz = float(input('Please input a number for z Translation: '))
            matrix = selectDict[select](Tx = Dx, Ty = Dy, Tz = Dz)
            
        elif select == 6:#Basic3DScale
            Dx = float(input('Please input a number for Scale x: '))
            Dy = float(input('Please input a number for Scale y: '))
            Dz = float(input('Please input a number for Scale z: '))
            matrix = selectDict[select](Sx = Dx, Sy = Dy, Sz = Dz)
            
        elif select == 7:#Basic3DRotation
            axis = input('Please input a character for the axis to rotate around:')
            angle_input = input('Please input an angle to rotate on axis {}:'.format(axis))
            angle = int(angle_input)
            matrix = selectDict[select](angle, axis)
            
        elif select == 8: #changing num
            newNum = int(input('Please input the number of lines to compute: '))
            num = selectDict[select](newNum)

        elif select == 9: #changing screen distance
            newNum = float(input('Please input the new screen distance: '))
            selectDict[select](newNum)
        
        elif select == 11: #changing screen size
            newNum = float(input('Please input the new screen Size: '))
            selectDict[select](newNum)    
        
        else:
            repeat = False    

#parser = argparse.ArgumentParser()
datalines = []

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
        InstructionLoop3D(window, line_canvas)
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

print('program finished')

