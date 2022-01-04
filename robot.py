import sys
from out_xls_model import out

"""parser = argparse.ArgumentParser()
parser.add_argument('kat', help = '''Upuść katalog z wnikami z Mańki, żeby
                    otrzymać plik z zestawieniem wyników''')
parser.add_argument('du')
args = parser.parse_args()
print (args.kat)
print(args.du)
"""
#sys.argv[1:]=['2020OUMJasło150']
print (sys.argv[1:])
kat = ' '.join(sys.argv[1:])
try:
    b = out('W_03_S6.ini', kat)
except KeyError:
    print('error')
print('''Proszę przejrzeć zapisy, czy wszystko jest.
      Plik wynikowy znajduje się w katalogu z pomiarami''')
input('')
