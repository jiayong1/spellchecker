
# coding: utf-8

# In[71]:


#Created by Jiayong Lin
import numpy as np
import pandas as pd
import difflib
import scipy.sparse

#Compare two words and decide type of misspelling.
def difference(incorrect,correct):
    if len(incorrect) <= len(correct): 
        for i,s in enumerate(difflib.ndiff(incorrect, correct)):
            if s[0] == '+':
                return correct[i], "-"
                break
            if s[0] == '-':
                return correct[i], incorrect[i]
                break
    else:
        for i,s in enumerate(difflib.ndiff(incorrect, correct)):
            if s[0] != ' ':
                return "-", incorrect[i]
                break


f = open("misspelling.txt", "r")
letters = "abcdefghijklmnopqrstuvwxyz"
correct = ""
scorematrix = np.zeros((26, 26))
incorrectisspace = 0
correctisspace = 0
j = 0

#go through the misspelling dataset, compare each pair of words and count the scroe.
for i in f:
    
    if i[0] =="$":
        correct = i[1:].lower()
    else:
        j+=1
        if(i.lower() != correct):
            x, y = difference(i.lower(),correct)
            
            if x == "-" or x == "_" :
                correctisspace+=1
            elif y == "-" or y == "_":
                incorrectisspace+=1
            elif y in letters and x in letters and y != x:
                scorematrix[letters.index(y), letters.index(x)]+=1    

scorematrix = scorematrix.astype(int)
#pd.scorematrix(scorematrix).to_csv("score.csv")


scorematrix2 = np.array(scorematrix, copy=True)  


scorematrix[scorematrix <= 1] = -5
scorematrix[scorematrix == 2] = -4
scorematrix[(scorematrix >= 3) & (scorematrix <= 50)] = -3
scorematrix[(scorematrix > 50) & (scorematrix <= 80)] = -2
scorematrix[(scorematrix > 80) & (scorematrix <= 90)] = -1
scorematrix[(scorematrix > 90) & (scorematrix <= 100)] = 0


scorematrix[(scorematrix > 100) & (scorematrix <= 150)] = 1
scorematrix[(scorematrix > 150) & (scorematrix <= 200)] = 2
scorematrix[(scorematrix > 200) & (scorematrix <= 250)] = 3
scorematrix[(scorematrix > 250) & (scorematrix <= 300)] = 4
scorematrix[(scorematrix > 300)] = 5



#Based on English word letter frequency to create the pairing score.
scorematrix[0,0] = 11
scorematrix[1,1] = 6
scorematrix[2,2] = 7
scorematrix[3,3] = 8
scorematrix[4,4] = 11
scorematrix[5,5] = 7
scorematrix[6,6] = 7
scorematrix[7,7] = 9
scorematrix[8,8] = 10
scorematrix[9,9] = 6
scorematrix[10,10] = 6
scorematrix[11,11] = 8
scorematrix[12,12] = 7
scorematrix[13,13] = 9
scorematrix[14,14] = 10
scorematrix[15,15] = 6
scorematrix[16,16] = 6
scorematrix[17,17] = 9
scorematrix[18,18] = 9
scorematrix[19,19] = 11
scorematrix[20,20] = 7
scorematrix[21,21] = 6
scorematrix[22,22] = 7
scorematrix[23,23] = 6
scorematrix[24,24] = 7
scorematrix[25,25] = 6
 

letterFrequence = np.array([0.082, 0.015, 0.028, 0.042, 0.127, 0.022, 0.02, 0.061, 0.07, 0.001, 0.008,0.04,0.024, 0.068,0.075, 0.02, 0.001,0.06, 0.062,0.09,0.028,0.01,0.024, 0.001, 0.02,0.001 ]).reshape(26,1)
letterFrequenceMatrix = letterFrequence * letterFrequence.T


# check if the score matrix has a Negative Expected Score
print( np.sum( np.multiply(letterFrequenceMatrix , scorematrix )))
print(scorematrix)
np.save("scorematrix", scorematrix)


    
    

