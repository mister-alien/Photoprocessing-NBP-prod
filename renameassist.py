import os, shutil

#########################
# Tries to rename a file based on
# prefix and a number
#
# Max Added digits going to be 6 by default
# shouldnt need more than 3 or 4 in reality.



def renhelper(prefix, picnum, destname, max_digits):
    
    for x in range(0,max_digits):
        photop=prefix+str(picnum)+'.jpg';
        try:
            shutil.copy(photop,destname)   # Copy both tx and plate pic over to the destination
            err=None
            break
        except IOError, e:
            err= photop+" Error: "+str(e)+"\n"
        prefix=prefix+'0'
    return err
