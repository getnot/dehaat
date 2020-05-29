import pandas
import tabula
import time
import sys
import os
from os import path

outputPath = os.getcwd()+"/ouput/"



def convert(file):
    ''' function to convert pdf file to csv 
        input => full qualified file name
    '''
    
    validateFile(file)
    createFolder(outputPath)
    
    milliseconds = int(round(time.time() * 1000))

    fileInputPath=file
    fileTempPath=outputPath+"temp_"+str(milliseconds)+".csv"
    fileOutputPath=outputPath+"BalSheet_"+str(milliseconds)+".csv"

    tabula.convert_into(fileInputPath, fileTempPath ,stream=True)

    output=pandas.read_csv(fileTempPath,header=None)
    arr=output[[2][0]].str.split(" ",n=1,expand=True)
    output[[2][0]]=arr[0]
    output[[3][0]]=arr[1]
    output.to_csv(fileOutputPath,index=False, header=False)
    return fileOutputPath

def validateFile(file):
    ''' function to validate input file details 
        [path,extension]
    '''
    if(path.exists(file) == False):
        raise fileNotFound
 
    if(file[-3:]!= "pdf"):
        raise incorrectFileExtension

def createFolder(path):
    '''fucntion to create output path'''
    if not os.path.exists(path):
        os.makedirs(path)


class Error(Exception):
    """Base class for other exceptions"""
    pass
class fileNotFound(Error):
    """Raised when file not found"""
    pass
class incorrectFileExtension(Error):
    """Raised when File with incorrect extension if provided in input"""
    pass


if __name__ == "__main__":
    output=convert(sys.argv[1])
    print(output)