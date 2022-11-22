import math
import random
import multiprocessing as mp
from itertools import product
import time

# VARIABLE DECLARATION

lWords = []
lAllUserInputs = []
lPermutations = list(product('012', repeat=5))
cnt = 0

# FILE PARSING

with open("cuvinte_wordle.txt", "r") as wordleList:
    text = wordleList.read()
    lWords = [str(x) for x in text.split()]

# FUNCTIONS

def truncate_list(strargQueryWord, largPermutation, largWords):
    """
    Returneaza lista de cuvinte care pot fi folosite pentru 
    urmatoarele query-uri.
    """

    sReturn = set(largWords)

    for i in range(5):
        if int(largPermutation[i]) == 2:
            #verde
            for strWord in largWords:
                if strWord[i] != strargQueryWord[i]:
                    sReturn.discard(strWord)
        if int(largPermutation[i]) == 0:
            for strWord in largWords:
                if strargQueryWord[i] in strWord:
                    sReturn.discard(strWord)
        if int(largPermutation[i]) == 1:
            for strWord in largWords:
                if strargQueryWord[i] not in strWord or strargQueryWord[i] == strWord[i]:
                    sReturn.discard(strWord)
    
    lReturn = list(sReturn)
    lReturn.sort()

    return lReturn


def word_entropy(lArgWords, q):
    strNextQuery = ""

    maxEntropy = -1.0
    for strargWord in lArgWords:
        finalEntropy = 0.0
        word_prob = 0.0
        
        for tPerm in lPermutations:
            sPossibleQueries = set(lArgWords)
            var_word_information = 0.0
            
            #ALGORITM 2 
            
            for i in range(5):
                if int(tPerm[i]) == 2:
                    for strWord in lArgWords:
                        if strWord[i] != strargWord[i]:
                            sPossibleQueries.discard(strWord)
                if int(tPerm[i]) == 0:
                    for strWord in lArgWords:
                        if strargWord[i] in strWord:
                            sPossibleQueries.discard(strWord)
                if int(tPerm[i]) == 1:
                    for strWord in lArgWords:
                        if strargWord[i] not in strWord or strWord[i] == strargWord[i]:
                            sPossibleQueries.discard(strWord)
        
            
            if (len(sPossibleQueries) != 0):
                word_prob = len(sPossibleQueries) / len(lArgWords) 
                var_word_information = -(word_prob)*math.log2(word_prob)
            finalEntropy += var_word_information
        
        if (finalEntropy > maxEntropy):
            maxEntropy = finalEntropy
            strNextQuery = strargWord

    q.put(strNextQuery)


# WORDLE SOLVER

# Primul query va fi TAREI, deoarece are cea mai mare entropie
# din lista initiala de cuvinte. 
#  
# Pentru a consulta lista cu entropiile
# pentru primul query, vedeti fisierul entropii_toata_lista.txt

strUserInput = ""
lUserInput = list(strUserInput)

lRemainingList = lWords.copy()
strGuessWord = random.choice(lWords)
lGuessWord = list(strGuessWord)

if __name__ == "__main__":

    print("Bine ati venit in jocul Wordle!")
    strAns = input("Doriti sa jucati cu modul hint? (y/n) ").lower()
    varHelper = True if strAns == "y" else False
    if varHelper == True:
        print(f"Pentru aceasta runda, cuvantul ales de jocul wordle este {strGuessWord}!")
        print(f"De asemenea, pentru a minimiza numarul de incercari, recomandam TAREI drept prim query!")

    q = mp.JoinableQueue()
    lQueryPermutation = [0,0,0,0,0]

    while lUserInput != lGuessWord:

        strUserInput = input("Introduceti cuvantul: ").upper()
        if strUserInput not in lWords:
            print("Query-ul nu este valid!")
            continue

        lUserInput = list(strUserInput)
        print("In urma aplicarii, vom obtine:")
        print(*lUserInput)
        lAllUserInputs.append(strUserInput)
        
        # litera pe aceeasi pozitie 🟩 -> \U0001F7E9
        # litera nu e in pozitia corecta 🟨 -> \U0001F7E8
        # litera nu exista ⬜ -> \U00002B1C

        #array cu cifre bazat pe ce intoarce query-ul
        # 2 -> aceeasi pozitie
        # 1 -> undeva in cuvant
        # 0 -> nu este
        
        for i in range(5):
            if lUserInput[i] == lGuessWord[i]:
                lQueryPermutation[i] = 2
                print('\U0001F7E9', end='')
            elif lUserInput[i] in lGuessWord:
                lQueryPermutation[i] = 1
                print('\U0001F7E8', end='')
            else:
                lQueryPermutation[i] = 0
                print('\U00002B1C', end='')
        print()

        if varHelper == True:
            lRemainingList = truncate_list(strUserInput, lQueryPermutation, lRemainingList).copy()

            entropy_process = mp.Process(target=word_entropy, args=(lRemainingList, q,))
            entropy_process.start()
            entropy_process.join()

            bestWord = q.get()
            print(f"Urmatorul query pe care ar trebui sa il folosesti este {bestWord}!")
            entropy_process.close()

    else:
        print(f"Query-ul cu numarul {cnt} este {strUserInput}!")
        print("In urma aplicarii, vom obtine:")
        print(*list(strUserInput))
        print("\U0001F7E9\U0001F7E9\U0001F7E9\U0001F7E9\U0001F7E9")
        print(f"Ai gasit {strGuessWord}") 
        lAllUserInputs.append(strGuessWord)

    print(f"Felicitari, dragule! Ai luat sfantul 5 la A$C, din {len(lAllUserInputs)} incercari.")
    print(f"Istoricul query-urilor tale este: {lAllUserInputs}")