import csv 
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
import itertools
import operator

paneldump_path='paneldump/'
volt_val = 1000/110 # kW/V to A conversion fraction
curr_val = 0 # current value 
c_list = [] # list of current values
f_list = []
onlyfiles = [f for f in listdir(paneldump_path) if isfile(join(paneldump_path, f)) and f.startswith( "paneldump" )]
def paneldumpparse(f_name) : 
	curr_list = []
	curr_list_for_print = []
	house_curr = {}
	house_dict = {} # {house_# : { timestamp : power }}
	time_dict = {} # {timestamp : { house : power }}
	with open(paneldump_path+f_name, newline='') as csvfile : 
		fr = csv.reader(csvfile, delimiter=',', quotechar='|')
		next(fr)
		for row in fr :
			curr_val = float(row[3])*volt_val
			if not time_dict : # first line of dictionary
				time_dict[row[0]] = {row[1]:curr_val}
			else : 
				if row[0] in time_dict : # check if timestamp is in list 
					if row[1] in time_dict[row[0]].keys() : # check if timestamp is in the list
						time_dict[row[0]][row[1]] = float(time_dict[row[0]][row[1]])+curr_val
					else : #add new house key
						time_dict[row[0]][row[1]]=curr_val
				else : #timestamp not in list
					time_dict[row[0]]={row[1]:curr_val}
	#Swapping keys between timestamp and house
	# Gather k2-k1-v2
	g = ((k2,k1,v2) for k1,v1 in time_dict.items() for k2,v2 in v1.items())
	# Sort by k2
	sg = sorted(g)
	# Group by k2
	gsg = itertools.groupby(sg, key=operator.itemgetter(0))
	# Turn it into a dict of dicts
	house_dict = {k: {ksk[1]: ksk[2] for ksk in group} for (k, group) in gsg}
	# print(b['house_97_ELEC'])
	# print(max(b['house_97_ELEC'].iteritems(), key=operator.itemgetter(1))[0])
	for house in house_dict : 
		curr_list_for_print.append([house,max(house_dict[house].items(), key=operator.itemgetter(1))[0],max(house_dict[house].items(), key=operator.itemgetter(1))[1]])
		curr_list.append(max(house_dict[house].items(), key=operator.itemgetter(1))[1])
	return curr_list 

# Variables for plotting
y_plt = []
x_label = ['50', '100', '150', '200', '200+']
x_plt = np.arange(len(x_label))
x_shift = np.NaN
for file_name in onlyfiles : 
	c_list = []
	panel_50 = 0
	panel_100 = 0
	panel_150 = 0
	panel_200 = 0
	panel_large = 0
	c_list = (paneldumpparse(file_name))
	for val in c_list : 
		if val < 40 : 
			panel_50 = panel_50+1; 
		elif val >= 40 and val < 80 : 
			panel_100 = panel_100+1;
		elif val >= 80 and val < 120 :
			panel_150 = panel_150+1; 
		elif val >= 120 and val < 160 :
			panel_200 = panel_200+1; 
		else : 
			panel_large = panel_large+1;
	y_plt = [panel_50, panel_100, panel_150, panel_200, panel_large]
	plt.bar(x_plt, y_plt, align='center', label=file_name[10:])
plt.xticks(x_plt, x_label)
plt.ylabel('Number of Houses')
plt.xlabel('Electrical Panel Size (A)')
plt.legend()
plt.tight_layout()
plt.show()
plt.savefig('output/panel_histogram.png')
