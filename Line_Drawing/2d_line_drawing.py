import tkinter as tk
import argparse
import random
import math
import datetime

window = tk.Tk()

win_height = 500
win_width = 500


line_canvas = tk.Canvas(window, bg = "white", height = win_height, width = win_width)

lines = 50
length = 100
seed = 42
berenheim = False #yeah, it's a typo. I changed it in the report
#code is less about correct spelling and more about correct logic

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

def draw_line(line_canvas, x, y, coor_funct, xfunct, yfunct):
    x, y = coor_funct(xfunct(x), yfunct(y))
    line_canvas.create_rectangle((x, y)*2)

def draw_line_normal(line_canvas, x_initial, y_initial, slope_normal, length, coor_funct, xfunct, yfunct):
    x = x_initial
    for i in range(length):
        x = x_initial + i
        y = y_initial + math.floor(i*slope_normal)
        draw_line(line_canvas, x, y, coor_funct, xfunct, yfunct)
    
def configured_lines(line_canvas, bresenheim):
    #defining all necessary lines
    line1 = [10, 10, 30, 10]
    line2 = [10, 10, 10, 30]
    line3 = [30, 10, 10, 10]
    line4 = [10, 30, 10, 10]
    line5 = [10, 10, 20, 30]
    line6 = [10, 30, 20, 10]
    line7 = [20, 30, 10, 10]
    line8 = [20, 10, 10, 30]
    #converting them into an easy to use format:
    lines = [line1, line2, line3, line4, line5, line6, line7, line8]
    #converting lines to slope format as expected in the program:
    for line in lines:
        #while this should be a function, it is mirrored with the code in the random loop
        
        x_initial = line[0]
        y_initial = line[1]
        x_final = line[2]
        y_final = line[3]
        
        x_change = line[2] - line[0]
        y_change = line[3] - line[1]
        
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
        
        slope = y_change/x_change
        
        #instead of modifying the above to reflect the change
        #I opted to change y_final/x_final it like it does in the random program itself
        y_final = y_change + y_initial
        x_final = x_change + x_initial

        if berenheim:
            draw_line_berenheim(line_canvas, x_initial, x_final, y_initial, y_final, coor_funct, x_funct, y_funct)
        else:
            draw_line_normal(line_canvas, x_initial, y_initial, slope, int(x_change), coor_funct, x_funct, y_funct)

    
def draw_line_berenheim(line_canvas, x_initial, x_final, y_initial, y_final, coor_funct, xfunct, yfunct):
    delta_y = y_final - y_initial
    delta_x = x_final - x_initial
    big_e = 2*delta_y - delta_x
    inc1 = 2*delta_y
    inc2 = 2*(delta_y - delta_x)
    y = y_initial
    x = x_initial
    
    while (x < x_final):
        
        draw_line(line_canvas, x, y, coor_funct, xfunct, yfunct)
        if big_e < 0:
            big_e = big_e + inc1
        else:
            y = y + 1
            big_e = big_e + inc2
        x = x + 1

def start_lines(lines, seed, line_canvas, length, berenheim):
    #defines the initial setup
    seed = random.seed(seed)
    x_min = 0
    x_max= win_width
    y_min = 0
    y_max = win_height
    length = length
    start_time = datetime.datetime.now()
    for i in range(lines):
        #defines where they start
        x_initial = random.randint(x_min, x_max)
        y_initial = random.randint(y_min, y_max)
        #defines the 1/2 unit length changes - corrected later
        x_change_1 = random.random() - 0.5
        y_change_1 = random.random() - 0.5
        
        if y_change_1 < 0:
            y_funct = neg
            y_initial = -y_initial
            y_change_1 = -y_change_1
        else:
            y_funct = straight
        
        if x_change_1 < 0:
            x_funct= neg
            x_initial = -x_initial
            x_change_1 = -x_change_1
        else:
            x_funct = straight

        if y_change_1 > x_change_1:
            coor_funct = invert_coor
            
            temp_initial = x_initial
            temp_change_1 = x_change_1
            temp_funct = x_funct
            x_initial = y_initial
            x_change_1 = y_change_1
            x_funct = y_funct
            y_initial = temp_initial
            y_change_1 = temp_change_1
            y_funct = temp_funct
            
        else:
            coor_funct = straight_coor
        
        slope = y_change_1/x_change_1
        print(y_funct(x_funct(slope)))
        
        #1/2 unit length changes corrected to normal lengths
        y_change = slope * length
        x_change = math.sqrt(length*length - y_change*y_change)
        
        y_final = y_change + y_initial
        x_final = x_change + x_initial        
        
        if berenheim:
            draw_line_berenheim(line_canvas, x_initial, x_final, y_initial, y_final, coor_funct, x_funct, y_funct)
        else:
            draw_line_normal(line_canvas, x_initial, y_initial, slope, int(x_change), coor_funct, x_funct, y_funct)
    end_time = datetime.datetime.now()
    return start_time, end_time
        
        #to be able to equate both methods, all variables must be computed
        #before either function starts, and the computations should be identical
        
        #this should insure an even time based field once the function starts
        #in java and c++ the compiler may throw out useless variables
        #but I believe that is not the case for python (this may be false)

parser = argparse.ArgumentParser()
#the user can specify the number of lines and the seed for the program through the command line
parser.add_argument('-n', action = "store", dest = "arg_lines",  #the number of lines
                    default = lines,   type = int)
parser.add_argument('-l', action = "store", dest = "arg_length",  #the number of lines
                    default = length,   type = int)
parser.add_argument('-s', action = "store", dest = "arg_seed",  #the seed
                    default = seed,   type = int)
parser.add_argument('-b', action = "store_true", #which algorithm
                    dest = "berenheim", default = berenheim)
                    #default False - declared at the top
parser.add_argument('-t', action = "store_true", #which algorithm
                    dest = "table", default = False)
parser.add_argument('-cf', action = "store_true", #which algorithm
                    dest = "configured", default = False)

args = parser.parse_args()
lines = args.arg_lines
length = args.arg_length
seed = args.arg_seed
berenheim = args.berenheim
table_gen = args.table

line_canvas.focus_set()
line_canvas.bind("q", key)

line_canvas.pack()

line_canvas.focus_set()
if (args.configured):
    configured_lines(line_canvas, berenheim)
else:
    if table_gen:
        nums = [1, 10, 100, 1000, 5000]
        times = []
        for j in range(len(nums)):
            st, et = start_lines(nums[j], seed, line_canvas, length, berenheim)
            times.append(et-st)
        print(times)
    else:
        start_lines(lines, seed, line_canvas, length, berenheim)
window.mainloop()


