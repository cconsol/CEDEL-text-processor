from lexical_diversity import lex_div as ld
import glob, re
import math
import pickle
import os

def splitter(input_string): #presumes that the list is tab-delimitted
	output_list = []

	for x in input_string.split("\n")[1:]: #iterate through sample string split by "\n", skip header row
		cols = x.split("\t") #split the item by "\t"
		word = cols[0] #the first item will be the word
		freq = cols[1] #the second will be the frequency value
		output_list.append([word,freq]) #append the [word, freq] list to the output list

	return(output_list)

def splitter2(input_string): #presumes that the list is tab-delimitted
	output_list = []
	
	for x in input_string.split("\n")[1:]: 
		cols = x.split("\t") 
		pair = cols[0] 
		delta_p_lr = cols[1] 
		delta_p_rl = cols[2]
		mi_score = cols[3]
		t_score = cols[4]
		raw_freq_score = cols[5]
		output_list.append([pair,delta_p_lr,delta_p_rl,mi_score,t_score,raw_freq_score]) 

	return(output_list)

def freq_dicter(input_list):
	output_dict = {}

	for x in input_list: #iterate through list
		word = x[0] #word is the first item
		freq = float(x[1]) #frequency is second item (convert to float using float())
		output_dict[word] = freq #assign key:value pair

	return(output_dict)

def file_freq_dicter(filename):
	spreadsheet = open(filename, errors = 'ignore').read() #open and read the file here
	split_ss = splitter(spreadsheet) #split the string into rows
	out_dict = freq_dicter(split_ss) #iterate through the rows and assign the word as the key and the frequency as the value

	return(out_dict)


escow_freq = pickle.load(open("corp_raw_freq_escow_ax01_2021-04-28.pickle","rb"))


def safe_divide(numerator,denominator): #this function has two arguments
	if denominator == 0: #if the denominator is 0
		output = 0 #the the output is 0
	else: #otherwise
		output = numerator/denominator 

	return(output) 


def word_counter(low): 
	nwords = len(low)
	return(nwords)


def frequency_count(tok_text,freq_dict):
	
	freq_sum = 0
	word_sum = 0
	for x in tok_text:
		
		if x in freq_dict: #if the word is in the frequency dictionary
			freq_sum += math.log(freq_dict[x]) #add the (logged) frequency value to the freq_sum counter
			word_sum += 1  #add one to the word_sum counter
		else:
			continue 

	return(safe_divide(freq_sum,word_sum)) #return average (logged) frequency score for words in the text

def word_frequency(tok_text, freq_dict):
	word_freqs = {}
	for word in tok_text:
		if word in freq_dict:
			word_freqs[word] = freq_dict[word]
		else:
			continue
	return word_freqs


def bigram_soa_count(tok_text,bigram_soa_dict,soatype):
	deltalr_sum = 0
	bigram_sum = 0
	for x in tok_text:
		if x in bigram_soa_dict:
			deltalr_sum += bigram_soa_dict[x][soatype]
			bigram_sum += 1 
		else:
			continue 

	return(safe_divide(deltalr_sum,bigram_sum)) 

def cover_check(tok_text,freq_dict):
	total_words = 0
	words_infreq = 0
	for x in tok_text:
		if x in freq_dict:
			total_words += 1
			words_infreq += 1
		else:
			total_words +=1 
	return(safe_divide(words_infreq,total_words))


def bigram_dicter(inputlist):
	bigram_dict = {}
	for x in inputlist: 
		pair = x[0]
		deltalr= float(x[1]) 
		deltarl= float(x[2])
		miscore = float(x[3])
		tscore = float(x[4])
		raw_f = float(x[5])
		log_f = math.log(float(x[5]))
		bigram_dict[pair] = {'delta_lr':deltalr, 'delta_rl':deltarl,'MI':miscore,'T':tscore,'raw_f':raw_f, 'log_f': log_f} 
		
	return(bigram_dict)


def file_bigram_dicter(filename):
	spreadst = open(filename, errors = 'ignore').read() 
	splited_spreadst = splitter2(spreadst)
	out_dictionary = bigram_dicter(splited_spreadst)
	return(out_dictionary)
	
			
escow_soa = file_bigram_dicter("escowax01_bi_soa_raw.txt")

for x in escow_soa:
	print(x)
	
def tokenize(input_string):
	tokenized = [] 

	punct_list = [".", "?","!","¡",",","'","‘","’",'"','“','”',"%","/",";","¿","-",":","(",")","&quot;","&quot","&apos","&amp","&gt","&lt","»","[","]","*","º","•","+","<",">","&","´","—"] #the ones after "+" probably need to be removed when processing ESCOW data

	replace_list = ["\n","\t"]

	ignore_list = [".", "?","!","¡",",","'","‘","’",'"','“','”',"%","/",";","¿","-",":","(",")","&quot;","&quot","&apos","&amp","&gt","&lt","»","[","]","*","º","•","+","<",">","&","´","—"] #the ones after "+" probably need to be removed when processing ESCOW data

	for x in punct_list:
		input_string = input_string.replace(x," " + x + " ")

	for x in replace_list:
		input_string = input_string.replace(x," ")

	input_string = input_string.lower()

	input_list = input_string.split(" ")

	for x in input_list:
		if x not in ignore_list: 
			tokenized.append(x) 

	return(list(filter(None, tokenized)))



def grammificator(token_list, gram_size, separator = "-"):
	ngrammed = [] 

	for idx, x in enumerate(token_list): 

		ngram = token_list[idx:idx+gram_size] 

		if len(ngram) == gram_size: 
			ngrammed.append(separator.join(ngram)) 

	return(ngrammed) 


def text_extractor(text): #text is a string
	meta_d = {}
	lines = text.split("\n")
	text_check = False
	for line in lines:
		if text_check == True and ":" not in line:
			meta_d["Text"] = meta_d["Text"] + line
		items = line.split(": ") #split on ": "
		if len(items) < 2: #check for empty lines
			continue
		if len(items) == 2:
			meta_d[items[0]] = items[1]
		if len(items) > 2:
			meta_d[items[0]] = " ".join(items[1:])
		if items[0] == "Text":
			text_check = True
	return(meta_d)


#process entire files
def CEDEL_Processor(folder,outname): #folder name, name of output file
	outf = open(outname,"w") #create output file
	outf.write("\t".join(["Participant","Placement_test","Task","Age","Proficiency","Nwords","MATTR", "HDD", "MTLD", "Av_Freq", "Stay Abroad", "Medium", "Location", "Resources", "Age of exposure", "Years studying", "Coverage", "Delta_lr", "Delta_rl","MI","T","raw_fre_bigram","log_fre_bigram"])) #write header
	filenames = glob.glob(folder + "/*") #get filenames in folder
	
	for filename in filenames: #iterate through filenames
		simple_fname = filename.split("/")[-1] #get last part of filename
		if "Icon" in simple_fname: continue #skip weirdness
		text = open(filename, encoding='utf-8').read() #read file
		text_d = text_extractor(text) #create text dictionary
		text_d["tokenized"] = tokenize(text_d["Text"])
		text_d["nwords"] = word_counter(text_d["tokenized"]) #calculate number of words
		text_d["av_freq"] = frequency_count(text_d["tokenized"],escow_freq)
		text_d["Coverage"] = cover_check(text_d["tokenized"],escow_freq)
		text_d["MATTR"] = ld.mattr(text_d["tokenized"]) #lexical diversity
		text_d["HDD"] = ld.hdd(text_d["tokenized"]) #lexical diversity
		text_d["MTLD"] = ld.mtld(text_d["tokenized"]) #lexical diversity
		text_d["bigramificated"] = grammificator(text_d["tokenized"],2) 
		text_d["deltalr"] = bigram_soa_count(text_d["bigramificated"],escow_soa,"delta_lr")
		text_d["deltarl"] = bigram_soa_count(text_d["bigramificated"],escow_soa,"delta_rl")
		text_d["mi"] = bigram_soa_count(text_d["bigramificated"],escow_soa,"MI")
		text_d["t"] = bigram_soa_count(text_d["bigramificated"],escow_soa,"T")
		text_d["rawfreq"] = bigram_soa_count(text_d["bigramificated"],escow_soa,"raw_f")
		text_d["logfreq"] = bigram_soa_count(text_d["bigramificated"],escow_soa,"log_f")
		out_line = [simple_fname,text_d["Placement test score (%)"],text_d["Task number"],text_d["Age"],text_d["Proficiency"],str(text_d["nwords"]),str(text_d["MATTR"]),str(text_d["HDD"]),str(text_d["MTLD"]),str(text_d["av_freq"]),text_d["Stay abroad (months)"],text_d["Writting/audio details"],text_d["Where the task was done"],text_d["Resources used"],text_d["Age of exposure to Spanish"],text_d["Years studying Spanish"],str(text_d["Coverage"]),str(text_d["deltalr"]),str(text_d["deltarl"]),str(text_d["mi"]),str(text_d["t"]),str(text_d["rawfreq"]),str(text_d["logfreq"])] #create line for output, make sure to turn any numbers to strings
		outf.write("\n" + "\t".join(out_line)) #write line
	
	outf.flush() #flush buffer
	outf.close() #close_file


CEDEL_Processor("cleancedeldesc2","results_cleancedeldesc2_20210713c.txt")

#process entire files
def file_outputter(folder): #folder name, name of output file
    filenames = glob.glob(folder + "/*") #get filenames in folder
    path = os.path.join(os.getcwd(), "output")
    if not os.path.exists(path):
        os.mkdir(path)
    for filename in filenames: #iterate through filenames
        simple_fname = filename.split("/")[-1] #get last part of filename
        if "Icon" in simple_fname: continue #skip weirdness
        text = open(filename, encoding='utf-8').read() #read file
        wordout = open(path + "/" + simple_fname + "-out.txt", "w")
        wordout.write("\t".join(["Word", "Frequency", "\n"]))
        text_d = text_extractor(text) #create text dictionary
        text_d["tokenized"] = tokenize(text_d["Text"])
        text_d["word_freq"] = word_frequency(text_d["tokenized"], escow_freq)
        word_out_line = "".join(str(k) +"\t" + str(v) + "\n" for k,v in text_d["word_freq"].items())
        wordout.write(word_out_line)
        wordout.flush()
        wordout.close()


file_outputter("cleancedeldesc2")

def missing_check(tok_text,freq_dict):
	missing_words = []
	for x in tok_text:
		if x in freq_dict:
			continue
		else:
			missing_words.append(x)
	return(missing_words)

def missing_file(folder,outfile):
	outf = open(outfile,"w")
	outf.write("\t".join(["Missing"]))
	filenames = glob.glob(folder + "/*")

	for filename in filenames: #iterate through filenames
		simple_fname = filename.split("/")[-1] #get last part of filename
		if "Icon" in simple_fname: continue #skip weirdness
		text = open(filename, encoding='utf-8').read() #read file
		text_d = text_extractor(text) #create text dictionary
		text_d["tokenized"] = tokenize(text_d["Text"])
		text_d["Missing"] = missing_check(text_d["tokenized"], escow_freq)
		out_line = [simple_fname,str(text_d["Missing"])]
		outf.write("\n" + "\t".join(out_line)) #write line
	
	outf.flush() #flush buffer
	outf.close() #close_file


missing_file("cleancedeldesc2","missinglist.txt")