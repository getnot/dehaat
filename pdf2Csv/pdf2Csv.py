import tabula
import time
import sys


# from tabula import read_pdf



def convert(file):
    ''' function to convert pdf file to csv 
        input => full qualified file name
    '''
    
    milliseconds = int(round(time.time() * 1000))

    fileInputPath=file
    fileTempPath="./"+"temp_"+str(milliseconds)+".csv"
    fileOutputPath="BalSheet_"+str(milliseconds)+".csv"


    tabula.convert_into(fileInputPath, fileTempPath )
    # output = read_pdf("/kaggle/input/balance-sheet/BalSheet.pdf",stream=True)

    return fileOutputPath



if __name__ == "__main__":
    output=convert(sys.argv[1])
    print(output)