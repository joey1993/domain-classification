# -*- coding: utf-8 -*-

import json
import string
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import numpy as np
import operator

stemmer = SnowballStemmer("english")
cachedStopWords = stopwords.words("english")
folder = 'results/'

def ks_optimization(ks_dic):
	for key,value in ks_dic.iteritems():
		ks_dic[key] = ks_normalization(value)
	return ks_dic


def ks_normalization(value_dic):
	value_max = float(max(value_dic.iteritems(), key=operator.itemgetter(1))[1])
	#print key," ",str(value_max)
	for key,value in value_dic.iteritems():
		value_dic[key] = value/value_max
	return value_dic


def clean(text):
	text = text.encode( "utf-8" )
	text = str(text)
	text = text.translate(None, string.punctuation)
	text = text.lower()
	text = ' '.join([text for text in text.split() if text not in cachedStopWords])
	return text

def ks_write(ks_dic,file_name):
	f = open(file_name,'w')
	ks = dict()
	for key,value in ks_dic.iteritems():
		ks[key] = sorted(value.items(), key=operator.itemgetter(1),reverse=True)
		line = '_'.join(key.split(' '))
		for word,freq in ks[key]:
			line = line + ' ' + word + ' ' + str(freq)
		f.write(line+'\n')
	f.close()


def main():
	with open('./data/rawdata_8-3') as data_file:    
		data = json.load(data_file)
		i = -1
		n = len(data["response"]["docs"])
		wordvecs = list()
		domain_list = list()
		domain_set = set()
		domain_dic = dict()
		domain_ind = dict()
		description_set = set()
		description_list = list()
		ks_dic = dict()
		f = open(folder+'input_all.dat','w')
		g = open(folder+'ground_truth_all.dat','w')
		num = 0
		for index in range(n):
			tool = data["response"]["docs"][index]
			if tool.has_key("domains") and tool.has_key("description"):

				domains = tool["domains"]
				description = tool["description"]
				description = clean(description)
				description_vec = description.split(' ')

				if len(description_vec) < 15: continue
				if description in description_set: continue
				if domains[0] == "": continue
				if "null" in domains: continue
				if "General" in domains: continue
				if "Computational Mathematics" in domains: continue
				if "Systems Biology" in domains: continue
				if "Chemistry(all)" in domains: continue
				if "Computer Science Applications" in domains: continue


				if "Epigenomics" not in domains and "Genomics" in domains and "Metagenomics" not in domains: domains.append("Genomics_sole")
				if "Metagenomics" in domains and "Genomics" not in domains: domains.append("Genomics")
				if "Epigenomics" in domains and "Genomics" not in domains: domains.append("Genomics")

				i += 1

				description_set.add(description)
				description_list.append(description)
				f.write(description+'\n')

				domains = tool["domains"]
				domain_vec = list()
				domain_num = list()

				for j in range(len(domains)):
					domain = domains[j]
					domain = str(domain.encode( "utf-8" )).lower()
					if domain == "systems biology": print description
					if domain == "genomics": continue

					domain_vec.append(domain)
					domain_set.add(domain)

					if not domain_ind.has_key(domain):
						domain_ind[domain] = num
						num += 1
					domain_num.append(str(domain_ind[domain]))

					if domain_dic.has_key(domain): 
						domain_dic[domain] += 1
					else: 
						domain_dic[domain] = 1
					
					if not ks_dic.has_key(domain):
						ks_dic[domain] = dict()
				
					for word in description_vec:
						if ks_dic[domain].has_key(word):
							ks_dic[domain][word] += 1
						else:
							ks_dic[domain][word] = 1

				domain_list.append(domain_num)
				#g.write(str(i)+': '+', '.join(domain_vec)+'\n')
				g.write(' '.join(domain_num)+'\n')

		f.close()
		g.close()

		print domain_dic
		print domain_ind
		#ks_write(ks_dic,"ks.dat")
		#ks_write(ks_optimization(ks_dic),"ks_opt.dat")

		length = len(description_list)
		np.random.seed(10)
		shuffle_indices = np.random.permutation(np.arange(length))
		
		description_list = np.array(description_list)
		domain_list = np.array(domain_list)

		x_shuffled = description_list[shuffle_indices]
		y_shuffled = domain_list[shuffle_indices]

		test_index = -1 * int(0.2 * float(length))
		x_train, x_test = x_shuffled[:test_index], x_shuffled[test_index:]
		y_train, y_test = y_shuffled[:test_index], y_shuffled[test_index:]

		print "training_num: ",len(x_train)
		print "testing_num: ",len(x_test)

		f = open(folder+'newdocs.dat','w')
		g = open(folder+'ground_truth_test.dat','w')

		for index,item in enumerate(x_train):
			f.write('['+' '.join(y_train[index]) + '] ' + item + '\n')
		for index,item in enumerate(x_test):
			f.write(item+'\n')
			g.write(' '.join(y_test[index])+'\n')


if __name__ == "__main__":
	main()














