from Analyze2DHelper import *

if __name__ == '__main__':
	xml_file, txt_file = get_filenames()
	params = get_params(xml_file)
	df = get_df(txt_file, params)
	print(df.head())
	print(df.tail())
	graph_df(df)
