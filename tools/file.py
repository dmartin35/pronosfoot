"""
FILE TOOLS
"""

def read_file(filename):
    """
    opens and read a file from file system
    
    returns file content as data if ok
    returns None is error while reading file
    """
    try:
        fhnd = open(filename)
        data = fhnd.read()
        fhnd.close()
        return data
    except: 
        return None
    
def read_file_lines(filename):
    """
    opens and read file lines from file system
    
    returns file lines as list if ok
    returns None is error while reading file
    """
    try:
        fhnd = open(filename)
        lines = fhnd.readlines()
        fhnd.close()
        return lines
    except: 
        return None
    
def write_file_line(filename,line):
    """
    write a new line in the file filename
    """
    try:
        fhnd = open(filename,'a')
        fhnd.write(line)
        fhnd.write('\n')
        fhnd.close()
    except:
        pass