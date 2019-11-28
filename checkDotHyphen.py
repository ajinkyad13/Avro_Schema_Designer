#########################################################
# Checks for non-permitted characters in field names    #
#                                                       #
# Authors : Ajinkya                                     #
# Last Modified : 12/27/2018                            #
#########################################################

import json
import six

global dotHyphenFlag
dotHyphenFlag = 0

''' This module is used to pass the control as per the structure of the schema'''
def checkDotHyphenList(jsonList):
    for ele in jsonList:
        if (type(ele) is list):
            checkDotHyphenList(ele)
        elif (type(ele) is dict):
            checkDotHyphenDict(ele)
        elif isinstance(ele,six.string_types):
            continue
        else:
            continue 

    
'''This module is used to check for dots or hyphens in all keys'''
def checkDotHyphenDict(jsonDict):
    global dotHyphenFlag
    for key,val in jsonDict.items():
        if (type(val) is list):
            if(('-' in key) or ('.' in key)):
                dotHyphenFlag = 1
                break
            else:
                checkDotHyphenList(val)
        elif (type(val) is dict):
            if(('-' in key) or ('.' in key)):
                dotHyphenFlag = 1
                break
            else:
                checkDotHyphenDict(val)
        else:
            if(('-' in key) or ('.' in key)):
                dotHyphenFlag = 1
                break
            else:
                continue
    return dotHyphenFlag