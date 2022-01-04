'''Few func to change xls coords from A1 type to 00 and backwards'''

def to_num(coords):
    ''' It takes coords of cell in 'A1' format and return (0,0) format'''
    
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N', \
               'O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK']
    start = True
    i = 1
    while(coords[:i].isalpha() == True):
        i = i+1
        #print(i)
    
    return (int(coords[i-1:])-1, letters.index(coords[:i-1]))

def to_let_num(x, y):
    ''' It takes coords of cell in (0,0) format and return it in 'A1' format'''
    x = int(x)
    y = int(y+1)
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N', \
               'O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK']
    
    return str(letters[x])+str(y)

def range_to_num(start, stop):
    '''retutns list of all fields in range between start and stop'''

    x1, y1 = to_num(start)
    x2, y2 = to_num(stop)
    ret_list = []
    for ding in range(x1, x2+1):
        for dong in range(y1,y2+1):
            ret_list.append((ding, dong))
            
    return ret_list
def col_to_num(x):
    '''returns number of column'''
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N', \
               'O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK']

    return letters.index(x)
    
if __name__ ==  '__main__':
    print(col_to_num('S'))


'''    
    for f in range_to_num('A1', 'C3'):
        print(to_let_num(f[0],f[1]))

        #print(type(to_num('A11')))
        print(to_let_num(5, 3))
        a, b =to_num('AB11')
        print('a = %s, b = %s' %(a,b))
        a, b =to_num('A11')
        print('a = %s, b = %s' %(a,b))
'''
