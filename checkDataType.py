#########################################################
# Checks for consistency in datatypes of all fields     #
#                                                       #
# Authors : Ajinkya                                     #
# Last Modified : 12/27/2018                            #
#########################################################

import json
import six

global intList,floatList,booleanList,strList
intList = []
floatList = []
booleanList = []
strList = []

'''This module is used to check data type and asign key to rspective list'''
def checkDataType(key,val):
    global intList,floatList,booleanList,strList
    if(type(val) is int):
        intList.append(key)
    elif (type(val) is float):
        floatList.append(key)
    elif isinstance(val,six.string_types):
        strList.append(key)
    elif (type(val) is bool):
        booleanList.append(key)
    else:
        return

''' This module is used to iterate list and pass the control as per the structure of the schema'''
def iterList(jsonList):
    for ele in jsonList:
        if (type(ele) is list):
            iterList(ele)
        elif (type(ele) is dict):
            iterDict(ele)
        elif isinstance(ele,six.string_types):
            continue
        else:
            continue
    
''' This module is used to iterate dict and pass the control as per the structure of the schema'''
def iterDict(jsonDict):
    for key,val in jsonDict.items():
        if (type(val) is list):
            iterList(val)
        elif (type(val) is dict):
            iterDict(val)
        else:
            checkDataType(key,val)

'''This module executes the first function - iterDict and compares the final generated lists and raise flags as required'''
def compareList(jsonDict):
    global intList,floatList,booleanList,strList
    iterDict(jsonDict)
    
    intList = list(set(intList))
    floatList = list(set(floatList))
    booleanList = list(set(booleanList))
    strList = list(set(strList))
    
    # print ("ints")
    # print (intList)
    
    # print ("floats")
    # print (floatList)
    
    # print ("bools")
    # print (booleanList)
    
    # print ("strs")
    # print (strList)
    l = []
    def any_in(a,b):
        for i in a:
            if i in b:
                l.append(i)
        return list(set(l))
                
        
        
    #any_in = lambda a, b: any(i in b for i in a)
    if len(any_in(strList,intList))>0:
        return [True,"Error : "+','.join(any_in(strList,intList))+" are both String and Int"]
    elif len(any_in(strList,floatList))>0:
        return [True,"Error : "+','.join(any_in(strList,floatList))+" are both String and Float"]
    elif len(any_in(floatList,intList))>0:
        return [False,"Loss of precision !! : "+','.join(any_in(floatList,intList))+" are both Float and Int"]
    elif len(any_in(strList,booleanList))>0:
        return [True,"Error : "+','.join(any_in(strList,booleanList))+" are both String and Boolean"]
    elif len(any_in(intList,booleanList))>0:
        return [True,"Error : "+','.join(any_in(intList,booleanList))+" are both Int and Boolean"]
    elif len(any_in(floatList,booleanList))>0:
        return [True,"Error : "+','.join(any_in(floatList,booleanList))+" are both Float and Boolean"]
    else:
        return [False, "No discrepancies in datatypes"]