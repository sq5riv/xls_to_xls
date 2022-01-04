import xls_cell_model
import xlrd
import os
import datetime as dt

class spreadsheet(object):
    u'''It  takes information about interesting spreadsheet fields.
    Every field is represented as xls_cell_model object and takes data  
    from indicated xls file'''

    def __init__(self, form_nick_file_name, xls_digg_file):
        """Init takes file with interesting cells in form and make cells
        objects, and digg data from xls_file"""

        #list od cells object
        self.cell_list = []
        self.nick_value = {}
        self.xls_digg_file = xls_digg_file
        try:
            form_nick_file = open(form_nick_file_name)
            lst = form_nick_file.readlines()
            form_nick_file.close()    
        except IOError:
            
            print("Brak pliku z danymi formularza, znajdź plik formularza \
i uruchom program jeszcze raz")
            input('')
            exit()
        #lst is list of lines from nick_name_file.
        for item in lst:
            item = item[:-1]
            data = item.split(', ')
            tmp_dict = {'coords':data[0],'nick_name':data[1]}
            self.cell_list.append(xls_cell_model.cell_obj(**tmp_dict))
        #data file grilling.
        try:
            xls = xlrd.open_workbook(self.xls_digg_file)
            sht = xls.sheet_by_index(0)
               
        except IOError:
            
            print("Brak pliku z danymi formularza, znajdź plik formularza \
                      i uruchom program jeszcze raz")
            input('')
            exit()
        for item in self.cell_list:
            #print(item)
            x, y = item.hook_coords()
            item.update_data(sht.cell_value(x, y))
            #print(item)
        self.up_dict()

        # checking for data set complet and print informationa about not complete data.

        self.data_check()

    def __repr__(self):
        return str(self.nick_value)
    
    def ret_nv(self):
        '''-> serial number of gauge block'''

        return self.nick_value

    def ret_data(self):
        return(self.cell_list)

    def ret_date(self):
        '''returns date of measurement in datetime.date format'''

        o = (di['measurement_date'].split('.'))
        o = [int(i) for i in o]
        return date(o[-1],o[-2],o[0])

    def ret_nom_len(self):
        return(self.nick_value['nom_len'])
    
    def up_dict(self):
        '''brings most interesting data from cell objects to nick_value dict'''

        for cell in self.cell_list:
            self.nick_value.update({cell.nick_name : cell.value})
            
    def data_check(self):
        '''prints info about of complete data.'''

        for key, item in self.nick_value.items():
            if item == "":
                print('in file %s item %s has no value' %(self.xls_digg_file, key))

    def show_me(self):
        '''shows nominal length and serial number of gauge'''

        return (self.nick_value['nom_len'],self.nick_value['gauge_serial_number'])

    def ret_case_number(self):
        '''return case number'''

        return self.nick_value['case_number']

    def ret_nom_len(self):
        '''return nominal lengrh of gauge'''

        return self.nick_value['nom_len']
if __name__ == '__main__':
    sp = spreadsheet('W_02_S6_data_net.txt', \
                     'W_02_S6_L.DM_02.03.2017 500mmA 12.03.2019.xls' )
    #print(sp.cell_list)
    print(sp)
    #print(sp.ret_nom_len())
    #print(sp.__dict__)
    #print(sp.show_me())
