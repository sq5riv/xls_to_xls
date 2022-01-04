import datetime

class gauge_block_model(object):
    '''model of gaugeblock. It contains all measurements
    of block and has checker of calibration properety'''

    
    def __init__(self, form_file):
        '''makes all fields as {nick:[meas1,meas2]} format'''

        try:
            form_nick_file = open(form_file)
            lst = form_nick_file.readlines()
            form_nick_file.close()    
        except IOError:
            
            print("Brak pliku z danymi formularza, znajdź plik formularza \
i uruchom program jeszcze raz")
            input('')
            exit()
        for item in lst:
            item = item[:-1]
            data = item.split(', ')
            self.__dict__.update({data[1]:[]})

    def cd_list(self):
        '''returns list of center deviations'''

        return self.center_length_deviation
    
    def __repr__(self):
        '''representation of gauge'''

        b = ('gaugeblock LN = %s, SN = %s, deviation = %s, wringed_side = %s'
                %(self.nom_len, self.gauge_serial_number, self.center_length_deviation, self.ws()))
            
        return b
    
    def recog(self, nom_len = 0, gauge_serial_number = 0):
        '''returns True if nominal lengtr and serial number is the same as in object. '''
        ret = False
        if len(self.nom_len) != 0:
            if (float(nom_len) == float(self.nom_len[0]) and
            str(gauge_serial_number) == str(self.gauge_serial_number[0])):
                #print('1')
                ret = True
            else:
                #print('2')
                ret = False
        return ret
    def  recog_show(self):
        '''returns nominal length and serial number of gaugeblock. To compare gaugeblock'''

        if len(self.nom_len) != 0:
            #print('test')
            ret_dict = {'nom_len':self.nom_len[0],'gauge_serial_number':self.gauge_serial_number[0]}
        else:
            ret_dict = {}
        return ret_dict
    
    def update(self, **data):
        '''fills data list of numerous measurements'''

        for key, val in data.items():
            self.__dict__[key].append(val)
            
    def mean_dd(self):
        '''returns mean central length deviation and add field do object'''
        mean = 0
        try:
            mean = sum(self.center_length_deviation)/len(self.center_length_deviation)
        except ZeroDivisionError:
            print('no data in gauge_block_model')
            mean = 0
        finally:
            self.mean_dd = mean
            return mean
        
    def date_show(self):
        '''returns date of measurement as datetime.date instance'''

        #print('--------------------------------------------------------------------------')
        #print(self.__dict__)
        print(self.measurement_date[0])
        o = (self.measurement_date[0].split('.'))
        
        o = [int(i) for i in o]
        return datetime.date(o[-1],o[-2],o[0])
        

    def t_gauge_show(self):
        '''returns tuple of min, max temperature of gauge block'''

        
        mn = min(min(self.ch8G_C), min(self.ch9G_C), min(self.ch8R_C), min(self.ch9R_C))
        
        mx = max(max(self.ch8G_C), max(self.ch9G_C), max(self.ch8R_C), max(self.ch9R_C))
        
        return (mn, mx)

    def show_me(self):
        '''returns data in usable fomat of dict'''
        if len(self.gauge_serial_number) != 0:
            ret = {'LN':self.nom_len[0],'SN':self.gauge_serial_number[0],'res':self.center_length_deviation, 'side':self.ws()}
        else:
            ret = {'LN':self.nom_len[0],'SN':' ','res':self.center_length_deviation, 'side':self.ws()}
        return ret

    def ws(self):
        '''returns list of wringed side Afor left and B for right'''

        ws = []
        for s in self.wringed_side:

            
            if s == 'A' or s.find('ewa') != -1:
                ws.append('A')
            elif s == 'B' or s.find('rawa') != -1:
                ws.append('B')
            else:
                ws.append('X')
        self.wringed_side_list = ws
        return ws
    
if __name__ == '__main__':
    b = gauge_block_model('W_02_S6_data_net.txt')
    
    di = {'gauge_serial_number':'123', 'ch8R_R': 12.123, 'nom_len':'500', 'ch8R_C':20.00, 'ch9R_C':21.00,
          'ch8G_C':19.00, 'ch9G_C':18, 'center_length_deviation':1.5, 'wringed_side': 'lewa'}
    b.update(**di)
    do = {'center_length_deviation':5, 'wringed_side':'Prawa'}
    b.update(**do)
    #print(b.__dict__)
    #print(b)
    #print(b.gauge_serial_number)
    print(b.mean_dd())
    print(b.wringed_side)
    print(b.cd_list())
    print(b.ws())
    #print(b.H_G_True)
    #print(b.t_gauge_show())
    #print(b.recog_show())
    #print(b.recog(500,123))
