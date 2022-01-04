import xlrd
import xls_imp as imp

class cell_obj(object):
    '''Obiekt komórki'''
    def __init__(self, **data):
        self.nick_name = 'no_data'
        self.coords = 'no_data'
        self.coords_x = 'no_data'
        self.coords_y = 'no_data'
        self.format = 'no_data'
        self.value = 'no_data'
        self.borders = 'no_data'
        self.expected_value_type = 'no_data'

        for key, val in data.items():
            if key in self.__dict__:
                self.__dict__[key] = val
            else:
                print('nie ma wartości %s' %key)
        if self.coords != 'no_data' and self.coords_x == 'no_data':
            
            self.coords_x , self.coords_y = imp.to_num(self.coords)
        if self.coords_x != 'no_data' and self.coords == 'no_data':
            self.coords = imp.to_let_num(self.coords_x, self.coords_y)

       
    def ch_val(self, **data):
        '''Zmienia wartość zmiennych tylko zainicjowanych w obiekcie'''
        
        for key, val in data.items():
            if key in self.__dict__:
                self.__dict__[key] = val

                
    def __repr__(self):
        '''Zwraca zmienne które zostały zmienione. \
        Nie zwraca zmiennych nie zmienionych.'''
        
        loc_dict = {}
        for key, val in self.__dict__.items():
            if val != 'no_data':
                #print('key: %s have value: %s' %(key,val))
                loc_dict.update({key:val})
        return str(loc_dict)+'\n'
    
    def ret_data_dict(self):
        '''Returns dict with data'''
        
        loc_dict = {}
        for key, val in self.__dict__.items():
            if val != 'no_data':
                #print('key: %s have value: %s' %(key,val))
                loc_dict.update({key:val})
        return loc_dict

    def ret_data(self):
        '''Returns dict nick_name : value'''

        tmp_dict = {self.nick_name : self.value}
        return tmp_dict
    def hook_coords(self):
        return (int(self.coords_x), int(self.coords_y))


    def update_data(self, data):
        self.value = data
        
if __name__ =='__main__':
    d={'coords_x':'1', 'coords_y':'2'}
    b=cell_obj(**d)
    print(type(b.coords), b.coords)
    c, d = b.hook_coords()
    print( 'c = %s, d = %s' %(c,d))
