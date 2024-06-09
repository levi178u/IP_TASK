'''
*********************************************************************************
*
*        		===============================================
*           		        CYBORG OPENCV TASK 2
*        		===============================================
*
*
*********************************************************************************
'''

# Author Name:		[Anshuman Panda]
# Roll No:			[123CS0201]
# Filename:			task_2_{Anshuman}.py
# Functions:		detect_arena_parameters
# 					[ Comma separated list of functions in this file ]

#-------------------------COOK HERE----------------------------------
import cv2 as cv
import numpy as np

color_ranges = {
    'RED': ([0, 70, 50], [10, 255, 255]),  # Traffic signal
    'GREEN': ([35, 100, 100], [85, 255, 255]),  # Start node
}

# Mapping from column indices to letters
column_letters= 'ABCDEFG'

def bgr_to_colors(bgr_color):
    # Mapping BGR color values to color names
    color_map = {
        (0, 255, 255): 'YELLOW',
        (255, 0, 255): 'PURPLE',
        (0, 165, 255): 'ORANGE',
        (0, 255, 0): 'GREEN'
        (255, 0, 0): 'BLUE'
        (203, 192, 255):'PINK'
        
        
    }
    return color_map.get(tuple(bgr_color), 'Unknown')

def detect_arena_parameters(maze_image):

    arena_parameters = {
        'traffic_signals': [],
        'horizontal_roads_under_construction': [],
        'vertical_roads_under_construction': [],
        'medicine_packages_present': [],
        'start_node': []
    }

    hsv_image = cv.cvtColor(maze_image, cv.COLOR_BGR2HSV)
    gray_image = cv.cvtColor(maze_image, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray_image, 240, 255, cv.THRESH_BINARY_INV)

    
    # Traffic signals and start node
    #l=length or x0
    #b=bredth or y0
    #w=width or x1
    #h=height or y1
    #node_name =n_n 
    #color_name=c_n
    for c_n, (lower, upper) in color_ranges.items():
    #l_b= lower bound , u_b= upper bound
        l_b = np.array(lower)
        u_b = np.array(upper)
        mask = cv.inRange(hsv_image, l_b, u_b)
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for contour in contours:
   
            l, b, w, h = cv.boundingRect(contour)
          
            if c_n == 'RED' and cv.contourArea(contour) > 100:
                n_n= f"{column_letters[l // 100]}{b // 100 + 1}"
                arena_parameters['traffic_signals'].append(n_n)
            elif c_n == 'GREEN' and cv.contourArea(contour) > 100:
                n_n = f"{column_letters[l// 100]}{b // 100 + 1}"
                
             # Mentioning start node
                if len(arena_parameters['start_node']) == 0: 
                    arena_parameters['start_node'].append(n_n)

    # For roads under construction
    
    # road_name= r_n
    
    # Horizontal roads
    for i in range(7):
        for j in range(6):
            if np.mean(gray_image[i*100:(i+1)*100, j*100+50:j*100+51]) > 250:  # Missing links or spaces
                r_n = f"{column_letters[j]}{i+1}-{column_letters[j+1]}{i+1}"
                arena_parameters['horizontal_roads_under_construction'].append(r_n)

    # Vertical roads
    for i in range(6):
        for j in range(7):
            if np.mean(gray_image[i*100+50:i*100+51, j*100:(j+1)*100]) > 250:  # Missing links or spaces
                r_n = f"{column_letters[j]}{i+1}-{column_letters[j]}{i+2}"
                arena_parameters['vertical_roads_under_construction'].append(r_n)

    # Medicine packages
    color_shapes = {
        'Square':   [YELLOW,PINK,ORANGE,GREEN], 
        'Triangle': [YELLOW,PINK,ORANGE,GREEN],  
        'Circle':   [YELLOW,PINK,ORANGE,GREEN]   
    }

      # Shops
    for shape, colors in color_shapes.items():
        
        for color in colors:
            
            mask = cv.inRange(maze_image, np.array(color) - 10, np.array(color) + 10)
            contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                
                l,b,w, h = cv.boundingRect(contour)
                
                if cv.contourArea(contour) > 100: 
                    shop_num = i + 1  
                    centroid = [l + w//2, b + h//2]
                    color_name = bgr_to_colors(color)
                    arena_parameters['medicine_packages_present'].append(
                       [f'Shop_{shop_num}', color_name, shape, centroid])

    return arena_parameters

#------------------------COOKING DONE--------------------------------

file_name = "test_images/maze_0.png"

input_maze_image = cv.imread(f'{file_name}',1)

output_dict = detect_arena_parameters(input_maze_image)
print('Arena Parameters: ', output_dict)


output_params = ['traffic_signals',
                 'start_node',
                 'medicine_packages_present',
                 'horizontal_roads_under_construction',
                 'vertical_roads_under_construction']
maze_0_dict= {
          'traffic_signals': ['C5', 'D4', 'D6', 'G4'],
          'start_node': ['A7'],
          'horizontal_roads_under_construction': ['C5-D5', 'E7-F7', 'F5-G5'],
          'vertical_roads_under_construction': ['B2-B3', 'B3-B4', 'B6-B7', 'C5-C6', 'D5-D6', 'E5-E6', 'E6-E7', 'F6-F7'],
          'medicine_packages_present':
                                        [['Shop_1', 'Green', 'Square',  [130, 130]],
                                        ['Shop_2', 'Orange', 'Square',  [130, 170]],
                                        ['Shop_3', 'Pink',  'Square',   [170, 130]], 
                                        ['Shop_4', 'Skyblue', 'Square', [170, 170]],
                                        ['Shop_5', 'Green', 'Triangle', [270, 130]],
                                        ['Shop_6', 'Orange','Triangle', [270, 170]], 
                                        ['Shop_7', 'Green', 'Circle',   [630, 170]], 
                                        ['Shop_8', 'Pink',  'Circle',   [670, 170]],
                                        ['Shop_9', 'Skyblue','Circle', [670, 130]]]}


print()
passed = False
for i,param in enumerate(output_params):
    if i>2:
        break
    if maze_0_dict[param] == output_dict[param]:
        passed = True
    else:
        passed = False

