# -*- coding: utf-8 -*-

import operator

thresholds = [0.1, 0.2, 0.3]
folder = 'results/'

for threshold in thresholds:
	f = open(folder+'model.theta','r')
	g = open(folder+'ground_truth_test.dat','r')
	h = open(folder+'results_'+str(threshold)+'.dat','w')
	ground_truth = g.readlines()
	contents = f.readlines()
	training_num = len(contents) - len(ground_truth)
	contents = contents[training_num:]
	#print "training_num: ",training_num
	#print "testing_num: ",len(contents)

	for i,item in enumerate(ground_truth): 
		ground_truth[i] = item.replace('\n','').split(' ')

	dic = dict()
	count1 = 0
	count2 = 0

	for i,line in enumerate(contents):

		truth = ground_truth[i]
		line = line.replace('\n','')
		vec = line.split(' ')
		for item in vec: 
			try:
				temp = item.split(':')
				dic[temp[0]] = float(temp[1])
			except:
				pass
		sorted_dic = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
		j = 0
		result = list()
		for (key,value) in sorted_dic:
			if j == 0:
				result.append(key)
				previous_value = value
			else:
				if (previous_value-value)/value < threshold:
					result.append(key)
			j += 1
		for item in result:
			if item in truth:
				count2 += 1
				break
		h.write(' '.join(result)+'\n')
		count1 += 1

	f.close()
	g.close()
	h.close()

	print "threshold: ",threshold
	print "we have ", count1, " documents."
	print "in which ", count2, " are predicted correctly."
	print "the accuracy is ", float(count2)/count1





