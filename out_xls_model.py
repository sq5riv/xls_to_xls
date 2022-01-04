import configparser
import xlsxwriter
import xls_imp as ip
import sys
import os
import set_calibration_model as scm
import ast
import datetime

sys.argv[0] = 'C:\\Users\\mkalenik\\OneDrive - Główny Urząd Miar\\AAAktualne\\2820 - 120 Płytki Mańka OUM Bydgoszcz\\2019 OUM Bydgoszcz ceramika'

class out(object):
    '''makes xlsx file'''
    
    def __init__(self, inif, kat):
        '''makes xlsx file'''

        #opens ini file
        self.outxls = configparser.ConfigParser()
        self.outxls.read(inif)
        #initiales xslx
        path = kat.split('\\')
        path.append(self.outxls['Name']['wb'])
        self.workbook = xlsxwriter.Workbook('\\'.join(path))
        self.worksheet = self.workbook.add_worksheet(self.outxls['Name']['ws'])
        

        foot = '&C'+self.outxls['Name']['foo']
        self.worksheet.set_footer(foot)
        self.worksheet.print_area(self.outxls['Name']['printing_area'])
        ori = self.outxls['Name']['orient']
        getattr(self.worksheet, ori)()
        lm = self.outxls['Name']['margin_left']
        rm = self.outxls['Name']['margin_right']
        self.worksheet.set_margins(left = lm, right = rm)
        self.merge()
        self.cells_format = [] #init format cells matrix
        self.workbook.add_format()
        self.const(self.cells_format, 80, 80, 'add_format')
        self.format_update('Color', 'set_bg_color', 'str')
        self.format_update('Bold', 'set_bold', 'str')
        self.format_update('Borders','set_border', 'int')
        self.format_update('Center','set_align','str')
        self.format_update('Bold_line','set_right','int')
        self.format_update('Bold_line2','set_bottom','int')
        self.format_update('Form','set_num_format','str')
        self.format_update('Num', 'set_num_format','str')
        self.format_update('Warp','set_text_wrap','str')
        self.format_update('Font','set_font_name','str')
        #print(self.cells_format)
        self.cell_dict = ast.literal_eval(self.outxls['Name']['cell_dict'])

        #initialize fields from data.
        self.cells_data = [] 
        self.const(self.cells_data, 80, 80, '')
        self.data_filer() #fills cells_data by data from .ini file
        self.formula_filler() #update cells_data by formulas
        self.gauge_filler(kat) #fills gauge data
        
        
        for i in range(80):
            for j in range(80):
                
                self.worksheet.write(i,j,self.cells_data[i][j],self.cells_format[i][j])
                
        

        # set column width
        for key, w in self.outxls['Column_width'].items():
            key2 = key.upper()
            x = int(ip.col_to_num(key2))
            w = int(w)
            self.worksheet.set_column(x,x,w,'')
        #set row hight
        for key, w in self.outxls['Row_hight'].items():
            key = int(key)
            w = int(w)
            #print(type(key), type(w))
            self.worksheet.set_row(key,w)           

       
        
        self.workbook.close()
        
    def const(self, field, a,b,app):
        '''makes matrix in field'''


        for i in range(a):
            field.append([])
            for j in range(b):
                if app == '':
                    field[i].append(app)
                elif app == 'add_format':
                    field[i].append(self.workbook.add_format())
                    
    def data_filer(self):
        '''fiils data information in cells'''

        data_list = []
        for key, data in self.outxls['Data'].items():
            a,b = ip.to_num(key.swapcase())
            try:
                data=float(data)
            except ValueError:
                pass
            to_l =(a,b,data)
            #print(to_l)
            data_list.append(to_l)

        for a,b,c in data_list:
            self.cells_data[a][b] = c

            
    def format_update(self, conf, command, bn):
       '''updates formatting data for all cells'''

       format_list = []
       for key,data in self.outxls[conf].items():
            if bn =='int': data = int(data)
            if key.find('_') != -1:
                t, p = key.swapcase().split('_')
                for x, y in ip.range_to_num(t, p):
                    getattr(self.cells_format[x][y], command)(data)
            if key.find('_') == -1:
                x,y = ip.to_num(key.swapcase())
                getattr(self.cells_format[x][y],command)(data)

 


    def merge(self):
        '''merge cells given in ini file'''

        for key, data in self.outxls['Merge'].items():
            a, b = key.swapcase().split('_')
            x1, y1 = ip.to_num(a)
            x2, y2 = ip.to_num(b)
            self.worksheet.merge_range(x1,y1,x2,y2, '')

            
    def formula_filler(self):
        '''updates self.cells_data. Adds formulas with change range'''

        formula_list = []
        zero_key = ''
        for key, form in self.outxls['Formula'].items():
             
            if key.find('_') != -1:
                t, p = key.swapcase().split('_')
                for x, y in ip.range_to_num(t,p):
                    if zero_key == '': zero_key = x+1
                    new_form = str(x+1).join(form.split(str(zero_key)))
                    self.cells_data[x][y] = new_form
                    
                    
            if key.find('_') == -1:
                x,y = ip.to_num(key.swapcase())
                self.worksheet.write_formula(x,y,form, self.cells_format[x][y])

    def gauge_filler(self, kat):
        '''fills cells_data with gauge block data'''

        
        gauge_num = 0
        data_dict = self.cell_dict
        mod = scm.set_cal_model(kat, 'set_calibration_model_config.txt')
        data = mod.data_show()
        if len(data) != 0:
            for gau in data:
                net_dict = self.line_ch(gauge_num)
                lp_x, lp_y = ip.to_num(net_dict['LP'])
                self.cells_data[lp_x][lp_y] = gauge_num+1
                ln_x, ln_y = ip.to_num(net_dict['LN'])
                self.cells_data[ln_x][ln_y]=gau['LN']
                lsn_x, lsn_y = ip.to_num(net_dict['SN'])
                self.cells_data[lsn_x][lsn_y]=gau['SN']
                
                # pętla dopisuje komórki z dwóch słownków po nazwach.
                liter = 0
                for m in gau['res']:
                    r_x,r_y = ip.to_num(net_dict['res'][liter])
                    self.cells_data[r_x][r_y] = m
                    s_x,s_y = ip.to_num(net_dict['side'][liter])
                    self.cells_data[s_x][s_y] = gau['side'][liter]
                    liter += 1
                
                gauge_num += 1
            n_x,n_y = ip.to_num(net_dict['Zg'])
            self.cells_data[n_x][n_y] = mod.num_pick()
            tmin_x,tmin_y = ip.to_num(net_dict['T_min'])
            tmax_x,tmax_y = ip.to_num(net_dict['T_max'])
            t_min, t_max = mod.min_max_temp()
            self.cells_data[tmin_x][tmin_y] = t_min
            self.cells_data[tmax_x][tmax_y] = t_max
            dmin,dmax = mod.min_max_date()
            #print(dmin,dmax)
            dmin_x,dmin_y = ip.to_num(net_dict['D_min'])
            dmax_x,dmax_y = ip.to_num(net_dict['D_max'])
            self.cells_data[dmin_x][dmin_y] = dmin.isoformat()
            self.cells_data[dmax_x][dmax_y] = dmax.isoformat()
        

    def line_ch(self, ln):
        '''changes line number'''

        wd = self.cell_dict
        ret_wd = {}
        for key, val in wd.items():
            if type(val) == str:
                di = val[-2:]
                if di == '13':
                    ret_wd.update({key: val[:-2]+str(int(di) + ln)})
                if di != '13':
                    ret_wd.update({key:val})
            if type(val) == list:
                lst = []
                for v in val:
                    di = v[-2:]
                    
                    lst.append(str(v[:-2]+str(int(di)+ln)))
                    
                ret_wd.update({key: lst})
                
        return ret_wd
            
if __name__ =='__main__':

    b = out('W_03_S6.ini', sys.argv[0])
    #print(b.line_ch(2))
    #print(b.outxls['Data'])
    #for key, data in b.outxls['Data'].items():
    #   print(ip.to_num(key.swapcase()), data)
'''
    print(b.outxls.sections())
    for sec in b.outxls.sections():
        print(b.outxls[sec])
        for key, item in b.outxls[sec].items():
            print(key.swapcase(), item)
'''
