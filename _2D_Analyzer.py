# NOTE: This file is not currently in use! It is a script version of the Notebook "2D Grapher.ipynb"

import pandas as pd
import numpy as np
import _2D_Utils


#Camera constants
num_pixels = 1024
nm_per_pixel = 0.125
nm_in_half = (num_pixels/2) * nm_per_pixel


#Convert nm to cm-1 or vice versa
def nm_cm(to_convert):
	return 10000000/to_convert


xml_file, data_file = _2D_Utils.get_files()
xml_tree = _2D_Utils.get_tree(xml_file)
xml_root = xml_tree.getroot()

#Read scan settings
scan_start = float(xml_root[2][2][1].text)
scan_stop = float(xml_root[2][4][1].text)
scan_step = float(xml_root[2][3][1].text)
nsteps = int(xml_root[2][5][1].text)
offset = float(xml_root[3][2][1].text)

#Calculate graph center and offset for y-axis
fluor_center = nm_cm(scan_start - offset)
fluor_offset = fluor_center - nm_in_half

steps = np.around(np.linspace(scan_start, scan_stop, nsteps), 2)
fluor_steps = (np.around(np.linspace((fluor_center - nm_in_half), (fluor_center + nm_in_half), num_pixels), 2))

data = pd.read_csv(data_file, delimiter='\t', header=None)
data.index = steps
data.columns = fluor_steps
data_transposed = data.transpose()

while True:
	arg = input("Enter command: ")
	
	match arg:
		case "g" | "graph":
			print("Displaying graph...\n")
			_2D_Utils.show_graph(data_transposed)

		case "f" | "fig" | "image":
			image_file = _2D_Utils.save_image(data_transposed, data_file)
			print(f'Saved image as {image_file}\n')

		case "q" | "quit":
			print("Exiting...\n")
			break

		case _:
			print("Invalid command.\n")
