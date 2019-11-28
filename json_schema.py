#########################################################
# Script for creating Avro schema from Json data        #
# Performs all validation operations                    #
#                                                       #
# Authors : Ajinkya                                     #
# Last Modified : 12/03/2018                            #
#########################################################

import sys
import re
import json
import ast
import six
from collections import defaultdict
import logall


#Setting necessary flags 
global strAvro,arrTab,countTab,fieldTab,dictinArr,missingKeys,recordnull,missingKeys_1,localflag,nullKeys,flag, list_temp, list_temp_2
recordnull = 0
localflag = 0
strAvro = ""
countTab = 1
fieldTab = 1
dictinArr = 0
missingKeys_1 = []
missingKeys = []
nullKeys = []
list_temp = []
list_temp_2 = []
flag = 0
arrTab = '\t'
# Function to extract keys inside a dictionary
def extractKeys(dict_in):
    # for key  in dict_in.items():
        # missingKeys.append(key)
    if isinstance(dict_in,dict):
        d = dict_in.keys()
    return list(dict_in.keys())
            
# Function to extract all keys inside an array of dictionaries, to make them nullable            
def extractNullkeys(array):    
    global nullKeys    
    for x in array:
        if isinstance(x,dict):
            for key,val in x.items():
                if isinstance(val,dict):
                    nullKeys = nullKeys + extractKeys(val)
                    
                    for inner_key,inner_val in val.items():
                        if isinstance(inner_val, list):
                            extractNullkeys(inner_val)
                            
                        if isinstance(inner_val,dict):
                            nullKeys = nullKeys + extractKeys(inner_val)
                            
                            
                if isinstance(val,list):
                    extractNullkeys(val)
    return nullKeys

# Function to create a schema out of an array    

def createArraySchema(doc,key):
    global list_temp,list_temp_2,missingKeys
    array_val = doc[key][0]
    arr_type = type(array_val)
    if arr_type is type({"f":"f"}):
        return createSchema(array_val)
    elif arr_type is type(1) and key not in list_temp and key not in list_temp_2 :
        return "int"
    elif arr_type is type(1.1) or key in list_temp or key in list_temp_2:
        if key not in list_temp and key not in list_temp_2:
            list_temp.append(doc)
        return "float"
    elif arr_type is type(True):
        return "boolean"
    elif arr_type is type('abc') or arr_type is type(u'abc')  :
        return "string"
# def createArraySchema(doc,key):
    # global flag, list_temp
    # array_val = doc[key]
    # arr_type = type(array_val[0])
    # if arr_type is type({"f":"f"}):
        # schema,missingKeys_f = createSchema_fromlist(array_val)
        
        # return schema
    # elif arr_type is type(9) and doc not in list_temp:
        # return "int"
    # elif arr_type is type(9.5) or doc in list_temp :
        # if doc not in list_temp:
            # list_temp.append(doc)
        # return "float"
    # elif arr_type is type(True):
        # return "boolean"
    # elif arr_type is type("abc") or arr_type is type(u'abc') :
        # return "string"

# Function to create a schema out of an array of dictionaries and find inner level missing keys
def missingKeys_list(doc,key):
    array_val = doc[key]
    arr_type = type(array_val[0])
    
    if arr_type is type({"f":"f"}):
        global missingKeys,missingKeys_1,nullKeys
        missingKeys_1 = []
        dicttem1 = {}
        data = []
        final_missing = []
        for element in array_val:
            data.append(str(element).replace("\\","").replace("u'","'").replace("'",'~`~').replace('"',"'").replace('~`~','"').replace(" ","").replace(":FALSE,",':false,').replace(":False,",':false,').replace(":TRUE,",':true,').replace(":True,",':true,'))
        
        if(len(array_val)>1):
            for x in data:
                try:
                    test_1 = json.loads(x)
                    dicttem1.update(test_1)
                
                except Exception as e:
                    logall.loginfo(str(e))
                    continue
            
            for x in data :
                try:
                    test_1 = json.loads(x)
                    tempKeys_1 = list(set(dicttem1.keys())-set(test_1.keys()))
                    if tempKeys_1 : 
                        missingKeys_1.append(tempKeys_1)
                except Exception as e :
                    logall.loginfo(str(e))
                    continue
                    
            for lst in missingKeys_1:
                final_missing = final_missing+ lst
            missingKeys_1 = list(set(final_missing))
        
        nullKeys = extractNullkeys(array_val)
        missingKeys = list(set().union(missingKeys,missingKeys_1,nullKeys))
        #missingKeys = map(str.replace(,''), missingKeys)
        missingKeys = [element.replace('-','_').replace('.','_') for element in missingKeys]
        # print (["xxx",missingKeys])
        
# def createSchema_fromlist(array_val):
    
    # global missingKeys_1, missingKeys,nullKeys
    # missingKeys_1 = []
    # dicttem_1={}
    # data = []
    # final_missing =[]
    
    # def lengthsort(val):
        # return len(val)
    #array_val.sort(key=lengthsort)
    
    # for element in array_val:
        
        # data.append(str(element).replace("\\","").replace("u'","'").replace("'",'~`~').replace('"',"'").replace('~`~','"').replace(" ","").replace(":FALSE,",':false,').replace(":False,",':false,').replace(":TRUE,",':true,').replace(":True,",':true,'))
    
    # if (len(array_val)>1):
        # for x in data:
            # try:
                # test_1 = json.loads(x)
                # dicttem_1.update(test_1)

            # except Exception as e:
                #logall.loginfo(str(e))
                # print (str(e))
                # continue

        # for x in data:
            # try :
                # test_1 = json.loads(x)
                # tempKeys_1 = set(dicttem_1.keys()) - set(test_1.keys())
                # tempKeys_1 = list(tempKeys_1)
                # if tempKeys_1:
                    # missingKeys_1.append(tempKeys_1)
            # except Exception as e:
                # print (str(e))
                # continue
            
        # for lst in missingKeys_1:
            # final_missing = final_missing + lst
        # missingKeys_1 = list(set(final_missing))
        
        # doc = str(dicttem_1)
        
        # doc = doc.replace(" ","")
        # doc = doc.replace("':u'",'":"')
        # doc = doc.replace("',u'",'","')
        # doc = doc.replace("':u\"",'":"')
        # doc = doc.replace('", u\'','","')
        # doc = doc.replace("u'",'"')
        # doc = doc.replace("':",'":')
        # doc = doc.replace("'],",'"],')
        # doc = doc.replace("'},",'"},')
        # doc = doc.replace("']",'"]')
        # doc = doc.replace("'}",'"}')
        
        # doc = re.sub(r"\dL","",doc)
        # doc = doc.replace("\\","")
        
        # doc = doc.replace(":FALSE,",':false,')
        # doc = doc.replace(":False,",':false,')
        # doc = doc.replace(":TRUE,",':true,')
        # doc = doc.replace(":True,",':true,')
        
        
    # else :
        # return createSchema(array_val)
    # doc = json.loads(doc)
         
    # nullKeys = extractNullkeys(array_val)     # call this function to extract all keys inside a nested dictioanry level to be made as nulls   
    # missingKeys = list(set().union(missingKeys,missingKeys_1,nullKeys))
    # return createSchema(doc),missingKeys_1

# Function to create a schema for data
def createSchema(doc):
    ## create object schema
    global list_temp_2,list_temp
    schema = {}
    
    ## loop through keys
    for key in doc:
        ## get key type
        key_type = type(doc[key])
        ## change key from unicode to string
        key = str(key)

        ## Check which type this is
        if key_type is int and key not in list_temp and key not in list_temp_2:
            schema[key] = "int"
            
        elif key_type is float or key in list_temp or key in list_temp_2:
            if key in list_temp and key not in list_temp_2:
                list_temp.append(key)
            schema[key] = "float"
            
        elif key_type is bool:
            schema[key] = "boolean"
        elif isinstance(doc[key], six.string_types):
            schema[key] = "string"
        elif key_type is list:
            ## create array and add to current schema
            schema[key] = [createArraySchema(doc,key)]
            missingList = [missingKeys_list(doc,key)]
        elif key_type is dict:
            ## create object and add to current schema
            schema[key] = createSchema(doc[key])
        else:
            logall.loginfo("unknown type: "+str(key_type))
    return schema            ## return finished schema
    
# Function to print a schema for array inside the data
def array(abc):
    global strAvro,arrTab,countTab,dictinArr, missingKeys,recordnull,localflag
    # print missingKeys
    for x in abc:
        
        if(type(x) == dict): 
            for key , val in x.items() :
                #print ["all_kay",key]            
                if isinstance(val,dict):
                    
                    temp = "{'"+key+"':"+str(val)+"}"
                    temp = ast.literal_eval(temp)
                    if(dictinArr == 1):
                        arrTabNumber = countTab + 1
                    else:
                        arrTabNumber = 1
                    strAvro = flatten_new(temp,arrTabNumber)
                    if recordnull == 1:
                        strAvro = strAvro[:-1]+'\n    ]\n    }]    },'
                        recordnull = 0
                    else:
                        strAvro = strAvro[:-1]+'\n    ]\n    }    },'
                    
                elif isinstance (val,list):
                    val = ''.join(val)
                    if key in missingKeys:
                        #print ("key elif-if",key)
                        strAvro = strAvro+'\n'+arrTab+'    '+'{'+'\n'+arrTab+'    '+'"name":"'+key+'",\n'+arrTab+'    '+'"type": ['+'\n'+arrTab+'        '+'{'+'"type":"array",'+'\n'+arrTab+'        '+'"items":{'+'\n'+arrTab+'        '+'"name":"'+key+'_details",'+'\n'+arrTab+'        '+'"type":"'+val+'"'+'\n'+arrTab+'        '+'}'+'\n'+arrTab+'        '+'},'+'\n'+arrTab+'        '+'"null"'+arrTab+'    '+'\n'+arrTab+'        '+']},'
                        
                    else:
                        #print ("key elif-else",key)
                        strAvro = strAvro+'\n'+arrTab+'    '+'{'+'\n'+arrTab+'    '+'"name":"'+key+'",\n'+arrTab+'    '+'"type": {'+'"type":"array",'+'\n'+arrTab+'        '+'"items":{'+'\n'+arrTab+'        '+'"name":"'+key+'_details",'+'\n'+arrTab+'        '+'"type":"'+val+'"'+'\n'+arrTab+'        '+'}'+'\n'+arrTab+'        '+arrTab+'    '+'\n'+arrTab+'        '+'}},'
                        #strAvro = strAvro+'\n'+arrTab+'    '+'{'+'\n'+arrTab+'    '+'"name":"'+key+'",\n'+arrTab+'    '+'"type":"'+val+'"\n'+arrTab+'    '+'},'

                else:
                    #print (['missing',missingKeys])
                    if key in missingKeys:
                        #print ("key else-if",key)
                        strAvro = strAvro+'\n'+arrTab+'    '+'{'+'\n'+arrTab+'    '+'"name":"'+key+'",\n'+arrTab+'    '+'"type":["'+val+'","null"]\n'+arrTab+'    '+'},'
                    else:
                        #print ("key else-else",key)
                        strAvro = strAvro+'\n'+arrTab+'    '+'{'+'\n'+arrTab+'    '+'"name":"'+key+'",\n'+arrTab+'    '+'"type":"'+val+'"\n'+arrTab+'    '+'},'


        elif(type(x)== list):
            array(x)
    return strAvro

# Function to flatten nested data
def flatten_new(d,tabNumber): # arguments are dictionary generated and number of tabs
    
    global strAvro,arrTab,countTab,fieldTab,dictinArr,recordnull

    for key in d:              # Iterating through dictionary with keys
        
        tab = '    '              
        generalTab = tab * tabNumber    #  For number of tabs needed
        if key in missingKeys:          ## TODO
            strAvro    = strAvro+'\n'+generalTab+'{'+'\n'+generalTab+'"name" :"'+key+'",'+'\n'+generalTab+'"type":[\n'+generalTab+'    "null",\n'+generalTab+'    {'+'\n'+generalTab+'   '+'    "name":"'+key+'_details",'+'\n'+generalTab+'   '+'    "type":"record",'+'\n'+generalTab+'   '+'    "fields":['
            recordnull = 1
        else:                           # Generates payload
            strAvro    = strAvro+'\n'+generalTab+'{'+'\n'+generalTab+'"name" :"'+key+'",'+'\n'+generalTab+'"type":{'+'\n'+generalTab+'   '+'"name":"'+key+'_details",'+'\n'+generalTab+'   '+'"type":"record",'+'\n'+generalTab+'   '+'"fields":['
        countTab = countTab + 1         # Increment number of tabs by 1 for next level
        fieldTab = fieldTab + 1
    for val in d.values():             #  Iterating through values of dictionary
        val = d[key]

        if isinstance(val, dict):      #  if the value is also a dictionary i.e. nested dictionary 
            for inner_key, inner_val in val.items():         #   Iterating through nested dictionary 
                if isinstance(inner_val, list):               # If value is a list
                    
                    listab = tab*countTab                         # tab * incremented number of tabs   
                    countTab = countTab +1                        # again increment for next level
                    arrTab = tab*countTab                         # tab * incremented number of tabs 
                    strAvro = strAvro+'\n'+listab+'{'+'\n'+arrTab+'"name":"'+inner_key+'",\n'+arrTab+'"type":{\n'+arrTab+'  '+'"type":"array",'+'\n'+arrTab+'  '+'"items":{'+'\n'+arrTab+'    '+'"name":"'+inner_key+'_details",\n'+arrTab+'    '+'"type":"record",'+'\n'+arrTab+'    '+'"fields":['
                    dictinArr = 1                                
                    strAvro = array(inner_val)                    # storing values into an array <WHY?>

                    strAvro = strAvro[:-1]+'\n    ]\n    }    }    },'    # Taking last element <WHY?>
                    
                elif isinstance(inner_val,dict):              # If value is a dictionary        
                    if(dictinArr == 1):                           # To check if this is a list inside a dictionary  
                        temp = "{'"+inner_key+"':"+str(inner_val)+"}"   # Create dictionary out of key-value pair
                        temp = ast.literal_eval(temp)                   # convert above to dict
                        dictnumber = tabNumber + 1                      # increment no. of tabs 
                        strAvro = flatten_new(temp,dictnumber)          # calling flatten_new recursively 
                        if(recordnull == 1):                            # To check if it exists in missing keys
                            strAvro = strAvro[:-1]+'\n    ]\n    } ]    },'   # 
                            recordnull = 0                              # <WHY?>
                        else:
                            strAvro = strAvro[:-1]+'\n    ]\n    }    },'     # Can't understand difference 
                    else:                                          # if not list in a dict
                        temp = "{'"+inner_key+"':"+str(inner_val)+"}"   # 
                        temp = ast.literal_eval(temp)                   # Creating dict.

                        dictnumber = tabNumber                          # #dict = #tab
                        strAvro = flatten_new(temp,dictnumber)          #
                        strAvro = strAvro[:-1]+'\n    ]\n    }    },'         #   <WHY?>
                
                else:                                           # In case of a string 
                    if(dictinArr == 1) :
                        if(inner_key in missingKeys):
                            dictTab = generalTab + '    '
                            strAvro = strAvro + ('\n'+dictTab+'{'+'\n'+dictTab+'"name" : "' +inner_key+'",\n'+dictTab+'"type" : ["'+inner_val+'","null"]\n'+dictTab+'},')
                        else:
                            dictTab = generalTab + '    '
                            strAvro = strAvro + ('\n'+dictTab+'{'+'\n'+dictTab+'"name" : "' +inner_key+'",\n'+dictTab+'"type" : "'+inner_val+'"\n'+dictTab+'},')
                    else:
                        if(inner_key in missingKeys):
                            valtab = tab*fieldTab
                            if recordnull ==1:
                                                                valtab=tab*(fieldTab+1)
                                                                strAvro = strAvro + ('\n'+tab+'{'+'\n'+valtab+'"name" : "' +inner_key+'",\n'+valtab+'"type" : ["'+inner_val+'","null"]\n'+tab+'},')
                            else:
                                                                strAvro = strAvro + ('\n'+tab+'{'+'\n'+valtab+'"name" : "' +inner_key+'",\n'+valtab+'"type" : ["'+inner_val+'","null"]\n'+tab+'},')
                        else:
                            valtab = tab*fieldTab
                            if recordnull ==1:
                                                                valtab=tab*(fieldTab+1)
                                                                strAvro = strAvro + ('\n'+tab+'    {'+'\n'+valtab+'"name" : "' +inner_key+'",\n'+valtab+'"type" : "'+inner_val+'"\n'+tab+'    },')
                            else:
                                                                strAvro = strAvro + ('\n'+tab+'    {'+'\n'+valtab+'"name" : "' +inner_key+'",\n'+valtab+'"type" : "'+inner_val+'"\n'+tab+'    },')

    return strAvro
            
        
# Function to extract missing keys from json data    
def getSchema(file_name):
    '''
    Open file and pass the json document to createSchema
    '''
    global missingKeys,list_temp_2
    missingKeys = []
    file = open(file_name,'r')
    data = file.read()
    file.close()
    temp = data.strip()
    data = data.strip()
    data = data.replace('.','_').replace('-','_')
    data = data.split('\n')
    data = [x for x in data if x.strip() != ""]          
    dicttem1 = defaultdict(list)
    dicttem={}
    
    if (len(data)>1):
        for x in data:
            try:
                test = json.loads(x)
                for k,v in test.items():
                    if type(v) is type(1.1):
                        list_temp_2.append(k)
                        
                    
                dicttem.update(test)
            
                
            except Exception as e:
                logall.loginfo(str(e))
                continue
        for x in data:
                        try :
                                test = json.loads(x)
                                tempKeys = set(dicttem.keys()) - set(test.keys())
                                tempKeys = list(tempKeys)
                                if tempKeys:
                                        missingKeys = list(set().union(missingKeys,tempKeys))
                                        
                        except Exception as e:
                                logall.loginfo(str(e))
                            
                                continue
        
        doc = str(dicttem)
        doc = re.sub(r"\dL","",doc)
        
        doc = doc.replace("\\","")
        doc = doc.replace("u'","'")
        doc = doc.replace("'",'~`~')
        doc = doc.replace('"',"'")
        doc = doc.replace('~`~','"')
        doc = doc.replace(" ","")
        doc = doc.replace(":FALSE,",':false,')
        doc = doc.replace(":False,",':false,')
        doc = doc.replace(":TRUE,",':true,')
        doc = doc.replace(":True,",':true,')
        
    else :
        doc = str(temp)
        
    doc = json.loads(doc)
    
    
    
   
    return createSchema(doc)

    
# Main function to create a schema from input json    
def generateAvroSchema(file_name):
    global strAvro,countTab,fieldTab,recordnull
    avro =  json.dumps(getSchema(file_name))
    print(avro)# gets schema of the JSON and jumped for replacements
    avro = avro.replace("@", "_")#
    avro = avro.replace("-", "_")#     replaced special characters from JSON schema as per use cases 
    avro = avro.replace(".", "_")#
    avro = json.loads(avro)     #     Again loding JSON, becomes dictioanry 
    global finalAvro
    finalAvro = ""
    for key,val in avro.items():      #   Iterating thru the generated dictionary     
        if isinstance(val, dict):                   # If value is dictionary
            dicttemp = "{'"+key+"':"+str(val)+"}"   # Creating separate small dictionaries from individual key-value pairs
            dicttemp = ast.literal_eval(dicttemp)   # convert to dictionary from above string
            
            strAvro = ""
            countTab = 1 ## Count of tabs for each level , by default it'll be one 
            fieldTab = 1 ##TODO    
            intAvro = flatten_new(dicttemp , 1)     # TO LINE #215
            finalAvro = finalAvro + intAvro[:-1]+'\n    ]\n}    },'     
            
            
        elif isinstance(val,list):
            finalAvro = finalAvro+'\n'+'    '+'{'+'\n'+'        '+'"name":"'+key+'",\n'+'        '+'"type":{\n'+'        '+'  '+'"type":"array",'+'\n'+'        '+'  '+'"items":{'+'\n'+'        '+'    '+'"name":"'+key+'_details",\n'+'        '+'    '+'"type":"record",'+'\n'+'        '+'    '+'"fields":['
            strAvro = ""
            countTab = 1
            fieldTab = 1
            arrAvro = array(val)
            finalAvro = finalAvro + arrAvro[:-1]+'\n    ]\n    }    }    },'
            
        else:
            if key in missingKeys:
                finalAvro = finalAvro+('\n    '+'{'+'\n        '+'"name" : "' +key+'",\n        '+'"type" : ["'+val+'","null"]\n    '+'},')
            else:
                finalAvro = finalAvro+('\n    '+'{'+'\n        '+'"name" : "' +key+'",\n        '+'"type" : "'+val+'"\n    '+'},')
    return finalAvro
    
