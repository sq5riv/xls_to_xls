import in_xls_model as in_m
from gauge_block_model import gauge_block_model as g_b_m
import sys
import os

sys.argv[0] = os.getcwd()


class set_cal_model(object):
    '''Class of calibration series. '''

    def __init__(self, directory, conf_file):

        
        self.directory = directory
        self.meas_series = [] #list of in_xls_model
        self.propper_meas =[] #list of propper meas
##        self.gauge_block_model = [] #list of gauge blocks
        self.data_file_list = [] #list of data files

        self.list_of_gauge = [] # list of all gauge block with all measurements.
        self.help_list = [] #list of nominal length and serial number
                                #of gauge blocks. Sorted the same as list of gauge

        #set config data to object
        f = open(conf_file)
        data = f.readlines()
        for d in data:
            t_lst = d.split(' ')
            self.__dict__[t_lst[0]] = t_lst[1]
        
        self.file_walker(self.directory) #looking for data files
        
        self.data_picker(self.directory) #peak data from files

        self.meas_filter() #filters bad data.

        self.meas_sorter() #sort data to gaugeblock objects

        self.min_max_temp() #returns min max temp of gauge

        self.min_max_date() #returns min and max date

        #to do
        #list of gauge block update
        
    def file_walker(self, walk_dir):
        '''Update data file list from dir'''
        
        tmp =[]
        
        for (dirpath, dirnames, filenames) in os.walk(walk_dir):
            tmp.extend(filenames)
            #print(f)
            break
        for file in tmp:
            if 0<file.find(self.file_recognise_string):
                self.data_file_list.append(file)
                
    def data_picker(self, directory):
        '''data picker make instances of in_xls_model with xsl files'''

        for item in self.data_file_list:
            tmp = directory + '\\' +item
            self.meas_series.append(in_m.spreadsheet('W_02_S6_data_net.txt', tmp))
            
    def dir_checker(self):
        pass
        '''This fills meas_series list by in_xls_model objects'''
        
    def gauge_setter(self):
        pass
        '''This fills gauge_blocks_set list by not existing yet objects.
        This not existing objects need to be as in_xls_objects but they
        need to use {key:[val1,val2,val3]} construct.'''

    def meas_filter(self):
        '''filter data. No value na data.'''

        
        for item in self.meas_series:
            if type(item.ret_nv()['center_length_deviation'] ) == float:
                self.propper_meas.append(item)
    
    def meas_sorter(self):
        '''Sort data from every propper meas to list of gauge.'''
        
        for m in self.propper_meas:
            tmp_p = m.show_me()
            try:
                index = self.help_list.index(tmp_p)
                self.list_of_gauge[index].update(**m.nick_value)
                #print(m.nick_value)
                
                
            except ValueError:
                #append help and list
                self.help_list.append(tmp_p)
                self.list_of_gauge.append(g_b_m('W_02_S6_data_net.txt'))
                self.list_of_gauge[-1].update(**m.nick_value)
    def min_max_date(self):
        '''returns min and max date of measurement'''

        lod = []
        for gb in self.list_of_gauge:
            lod.append(gb.date_show())
        self.d_min_max = (min(lod),max(lod))
        return self.d_min_max
    
    def min_max_temp(self):
        '''returns min and max temperature of gauge block at measurements'''

        mn = [5000]
        mx = [0]
        for gb in self.list_of_gauge:
            tmp1, tmp2 =gb.t_gauge_show()
            mn.append(tmp1)
            mx.append(tmp2)
        self.min_max = (min(mn), max(mx))
        return (self.min_max)

    def data_show(self):
        '''returns data to summary'''

        ret_list = []
        for meas in self.list_of_gauge:
            #print('show_me: ', meas.show_me())
            ret_list.append(meas.show_me())

        return ret_list

    def num_pick(self):
        '''check case number in all xls the same'''

        cn = ''
        for m in self.meas_series:
            tmp = m.ret_case_number()
            #print('tmp = %s, cn =  %s' %(tmp,cn))
            if cn == '': cn = tmp
            elif cn != tmp:
                print('błąd numeru sprawy')
                cn = '0000'
        self.case_number = cn
        return self.case_number
    
    
if __name__ == '__main__':
    b=set_cal_model(sys.argv[0]+ '\\data', 'set_calibration_model_config.txt')
    #print(b.data_show())
    print(b.d_min_max)
    #print(b.list_of_gauge)
    #print(b.min_max)
    #print(b.data_show())
    #print(b.propper_meas[0])
    #print(type(b.propper_meas[0]))
    #print(b.num_pick())
    #print(type(b.meas_series[0].ret_nom_len()))
    #print(b.__dict__)
    #b.meas_sorter()
    #print(b.help_list)
    #print(len(b.propper_meas))
    #print(b.list_of_gauge)


    '''for meas in b.meas_series:
        print(meas.ret_nv()['nom_len'], meas.ret_nv()['gauge_serial_number'],
              type(meas.ret_nv()['center_length_de']))
    for meas in b.propper_meas:
        print(meas.ret_nv()['nom_len'], meas.ret_nv()['gauge_serial_number'],
              type(meas.ret_nv()['center_length_de']))
'''



#b = in_m.spreadsheet('W_02_S6_data_net.txt', \
#                     'W_02_S6_L.DM_02.03.2017 500mmA 12.03.2019.xls' )

