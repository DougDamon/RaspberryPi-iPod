my_dict = {'a': 1, 'b': 2, 'c': 3}

#for index, (key, value) in enumerate(reversed(list(my_dict.items()))):
#    print(index, key, value)

maxIndex = len(my_dict) -1
for index, dict in enumerate(reversed(my_dict)):
    print(type(dict))
    if index == maxIndex:
        firstSong = dict
        
print(firstSong)
    
#for index, dict in reversed(enumerate(my_dict)):
#    print(index, dict)
