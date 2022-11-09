from itertools import product

with open("cuvinte_wordle.txt", "r") as wordleList:
    sAux = wordleList.read()
    lQueryWords = [str(x) for x in sAux.split()]
wordleList.close()

def read_permutation_file():
    """
    Reads the rez_query.txt file, in which 5 digits are written,
    describing the wordle game's response to the last given query

    The feedback is returned by the function as a list
    """
    with open("rez_query.txt", "r") as rezQuery:
        sAux = rezQuery.read()
        lPermutation = [int(x) for x in sAux.split()]

    return lPermutation

def generate_entropy_dictionary():
    """
    returns a dictionary where the key is a word and the value is the
    information said word would return if chosen as a query
    """

lPermutations = []


L = read_permutation_file()
print(L)

def word_information(word):

    generate_entropy_dictionary()

    return

    #TODO check the dictionary for words that can be valid queries
    #based on the permutation returned by the wordle game

    #TODO ceva

lPermutations = list(product('012', repeat=5))
#for x in cuvinte:
   # for i in range (243):
    #    for j in range (5):
     #        aux = i
     #        permutari=aux%3
     #        aux=aux//3   
print(lPermutations)
print('\U00002B1C')
print('\U0001F7E8')
print('\U0001F7E9')
#def temp1():
