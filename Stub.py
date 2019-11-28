#########################################################
# Main script of Avro schema designer(generation sectn) #
# Imports all relevant codes and executes accordingly   #
#                                                       #
# Authors : Ajinkya                                     #
# Last Modified : 11/30/2018                            #
#########################################################

import os
import subprocess
import sys
import json
import pandas as pd
import wx
import numpy as np
#User defined imports
import logall
import UI
import json_schema
import checkDotHyphen as cdh
import checkDataType as cdt
#import vali_stub

#Defining classes for major features of brick

#Class for manual creation of schemas
class record(UI.Record):
    global countAddrecord,name,submitted,startOutput,nestedspace,fieldSpace,fieldtype,firstnested,bracketsAdded
    submitted = 0
    def __init__(self,parent): 
        global countAddrecord,submitted,nestedAddrecord,nestedspace,fieldSpace,fieldtype,firstnested,bracketsAdded
        UI.Record.__init__(self,parent)  
        countAddrecord = 0
        submitted = 0
        bracketsAdded = 0
        nestedAddrecord = 0
        firstnested = 1
        nestedspace = '    '
        fieldSpace = '    '
        fieldtype = '    '
    
    #Appends the user inputs to schema and asks for a new field to be added to schema
    def addrecord( self, event ):
        global countAddrecord,name,subname,bracketsAdded,firstnested
        name = self.textbox_main.GetValue()
        subname = self.textBox_name.GetValue()
        nameField = self.textBox_nameField.GetValue()
        data_type = self.dropdown_data_type.GetValue()
        default = self.textBox_default.GetValue()
        desc = self.textBox_desc.GetValue()
        closingbrackets = firstnested - 1
        endbrackets = ''
        if(closingbrackets > 0):
                    temnested = 1
                    firstnested = 1
                    closebracketscheck = 0
                    for i in range(closingbrackets):
                        if(closebracketscheck == 0):
                            closebrackets = self.textBox_screen_second.GetValue()
                            closebrackets = closebrackets.split('\n')
                            closebrackets = closebrackets[-1]
                        tab = (len(closebrackets) - len(closebrackets.strip()))/2
                        if(closebracketscheck == 0):
                            tab = tab+2
                        else:
                            tab = tab+1
                        sqbracket = '    '
                        curlbracket = '    '
                        curlbracket2 = '    '
                        sqspace = sqbracket * int(tab +(temnested))
                        curlspace = curlbracket * int(tab)
                        curlspace2 = curlbracket2*int(tab - temnested)
                        intermediate = endbrackets + '\n'+sqspace+']'
                        endbrackets = endbrackets + '\n'+sqspace+']'+'\n'+curlspace+'}'+'\n'+curlspace2+'}'
                        
                        closebrackets = intermediate
                        closebracketscheck = closebracketscheck + 1
                        
                    textbox_value = self.textBox_screen_second.GetValue()
                    textbox_value = textbox_value[:-1]+endbrackets+','
                    self.textBox_screen_second.SetValue(textbox_value)
                    bracketsAdded = 1
                    
                    
        if(name!="" and nameField != "" and data_type != ""):
                    
                    if(countAddrecord==0):
                        countAddrecord+=1
                        self.textBox_screen_second.AppendText('\n        {\n            "name"    :    "'+name+'",\n'+'            "type" : { \n                "type": "record",\n                "name": "' + subname+'",\n                "fields": [')
                    '''
                    if(self.checkBox_Null.GetValue()):
                        data_type = '"'+data_type+'","null"'
                        final='\n                    {\n                    "name": "'+nameField+'",\n                    "type": ['+data_type+']\n                    },'
                    else:
                        final = '\n                    {\n                    "name": "'+nameField+'",\n                    "type": "'+data_type+'"\n                    },'
                    '''
                    if(default == "" and desc ==""):
                        if(self.checkBox_Null.GetValue()):

                            data_type = '"'+data_type+'","null"'
                            final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    ['+data_type+']'+'\n                    },'

                        else:

                            final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    "'+data_type+'"'+'\n                    },'

                    elif(default == "" or desc ==""):
                        if(default == ""):
                            if(self.checkBox_Null.GetValue()):
                                data_type = '"'+data_type+'","null"'
                                final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    ['+data_type+'],'+'\n                    "doc"    :    "'+desc+'"\n                    },'
                            else:
                                final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    "'+data_type+'",'+'\n                    "doc"    :    "'+desc+'"\n                    },'
                        
                        if(desc == ""):
                            if(data_type == 'int' or data_type == 'float' or data_type == 'double' or data_type == 'long'):
                                if(self.checkBox_Null.GetValue()):
                                    data_type = '"'+data_type+'","null"'
                                    final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    ['+data_type+'],'+'\n                    "default"    :    '+default+'\n                    },'
                                else:
                                    final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    "'+data_type+'",'+'\n                    "default"    :    '+default+'\n                    },'
                            else:
                                if(self.checkBox_Null.GetValue()):
                                    data_type = '"'+data_type+'","null"'
                                    final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    ['+data_type+'],'+'\n                    "default"    :    "'+default+'"\n                    },'
                                else:
                                    final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    "'+data_type+'",'+'\n                    "default"    :    "'+default+'"\n                    },'
                    else:
                        if(self.checkBox_Null.GetValue()):
                            data_type = '"'+data_type+'","null"'
                            final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    ['+data_type+'],'+'\n            "default"    :    "'+default+'",'+'\n            "doc"    :    "'+desc+'"\n        },'
                        else:
                            final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    "'+data_type+'",'+'\n                    "default"    :    "'+default+'",'+'\n                    "doc"    :    "'+desc+'"\n                    },'            
                    
                    self.textBox_screen_second.SetInsertionPointEnd()
                    self.textBox_screen_second.WriteText(final)
                    self.textBox_name.SetEditable(0)
                    self.textbox_main.SetEditable(0)
                    self.textBox_nameField.SetValue("")

                    self.button_submit_schema.Enable()
                    self.nested.Enable()
        
        else:
                    dlg = wx.MessageDialog(self, "The fields Name,Sub-Record Name,FieldName and Data Type cannot be blank",'Error', wx.OK | wx.CANCEL | wx.ICON_ERROR)
                    val = dlg.ShowModal()
                    dlg.Show()
    
    #Adding one-level of nested records to schema during manual input
    def nestedfun(self,event):
        global nestedAddrecord,nestedspace,fieldSpace,fieldtype,firstnested
        showDialog = firstnested - 1
        if(showDialog > 0):
                    dlg = wx.MessageDialog(self, 'This will add a new nested Record! \n- Click OK to add new Nested Record \n- Click Cancel to add more fields in the existing record','Alert', wx.OK | wx.CANCEL |wx.ICON_INFORMATION)
                    dlg.Show()
                    if(dlg.ShowModal() == wx.ID_OK):
                        self.nestedField.Enable()
                        nestedAddrecord = 0
                        tabs = 0
                        nestedspace = '    '
                        fieldSpace = '    '
                        fieldtype = '    '

                        if (nestedAddrecord == 0):
                            self.textBox_name.SetEditable(1)
                            self.textbox_main.SetEditable(1)
                            self.textBox_name.SetValue("")
                            self.textbox_main.SetValue("")
                            self.textBox_nameField.SetValue("")
                            tempOutput = self.textBox_screen_second.GetValue()
                            tempOutput =  tempOutput.split('\n')
                            tempOutput = tempOutput[-1]

                        indent =  len(tempOutput)

                        tabs = (len(tempOutput) - len(tempOutput.strip()))/2

                        tabs = tabs + 2
                        
                        
                        
                        nestedspace = nestedspace*int((tabs+firstnested))
                        fieldSpace = fieldSpace*int((tabs + (firstnested+1)))
                        fieldtype = fieldtype*int((tabs+(firstnested+2)))
                    
                    else:
                        dlg.Destroy()
    
        else:
                    self.nestedField.Enable()
                    nestedAddrecord = 0
                    tabs = 0
                    nestedspace = '    '
                    fieldSpace = '    '
                    fieldtype = '    '

                    if (nestedAddrecord == 0):
                        self.textBox_name.SetEditable(1)
                        self.textbox_main.SetEditable(1)
                        self.textBox_name.SetValue("")
                        self.textbox_main.SetValue("")
                        self.textBox_nameField.SetValue("")
                        tempOutput = self.textBox_screen_second.GetValue()
                        tempOutput =  tempOutput.split('\n')
                        tempOutput = tempOutput[-1]

                    indent =  len(tempOutput)

                    tabs = (len(tempOutput) - len(tempOutput.strip()))/2

                    tabs = tabs + 2
                        
                        
                    nestedspace = nestedspace*int((tabs+firstnested))
                    fieldSpace = fieldSpace*int((tabs + (firstnested+1)))
                    fieldtype = fieldtype*int((tabs+(firstnested+2)))
    
    #Appending field to schema and asking for further input - used while adding nested fields
    def addnestedField(self , event):
        global nestedspace,fieldSpace,fieldtype,nestedAddrecord,firstnested
        name = self.textbox_main.GetValue()
        subname = self.textBox_name.GetValue()
        nameField = self.textBox_nameField.GetValue()
        data_type = self.dropdown_data_type.GetValue()
        default = self.textBox_default.GetValue()
        desc = self.textBox_desc.GetValue()
        
        if(name != '' and subname != '' and nameField != '' and data_type != ''):
                    if(nestedAddrecord == 0):
                        self.textBox_screen_second.AppendText('\n'+nestedspace+'{ "name":"'+name+'",\n'+nestedspace+'  "type":{'+'\n'+fieldSpace+'"type":"record",'+'\n'+fieldSpace+'"name": "'+subname+'",\n'+fieldSpace+'"fields": [')
                        nestedAddrecord = nestedAddrecord + 1
                        firstnested = firstnested + 1
                    '''
                    if(self.checkBox_Null.GetValue()):
                        data_type = '"'+data_type+'","null"'
                        self.textBox_screen_second.AppendText('\n'+fieldSpace+'{'+'\n'+fieldtype+'"name": "'+nameField+'",\n'+fieldtype+'"type": ['+data_type+']'+'\n'+fieldSpace+'},')
                    
                    else:
                        self.textBox_screen_second.AppendText('\n'+fieldSpace+'{'+'\n'+fieldtype+'"name": "'+nameField+'",\n'+fieldtype+'"type": "'+data_type+'"'+'\n'+fieldSpace+'},')
                    '''
                    if(default == "" and desc ==""):
                        if(self.checkBox_Null.GetValue()):

                            data_type = '"'+data_type+'","null"'
                            final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    ['+data_type+']'+'\n                    },'

                        else:

                            final='\n                {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    "'+data_type+'"'+'\n                    },'

                    elif(default == "" or desc ==""):
                        if(default == ""):
                            if(self.checkBox_Null.GetValue()):
                                data_type = '"'+data_type+'","null"'
                                final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    ['+data_type+'],'+'\n                    "doc"    :    "'+desc+'"\n                    },'
                            else:
                                final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    "'+data_type+'",'+'\n                    "doc"    :    "'+desc+'"\n                    },'
                        
                        if(desc == ""):
                            if(data_type == 'int' or data_type == 'float' or data_type == 'double' or data_type == 'long'):
                                if(self.checkBox_Null.GetValue()):
                                    data_type = '"'+data_type+'","null"'
                                    final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                     "type"    :    ['+data_type+'],'+'\n                    "default"    :    '+default+'\n                    },'
                                else:
                                    final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    "'+data_type+'",'+'\n                    "default"    :    '+default+'\n                    },'
                            else:
                                if(self.checkBox_Null.GetValue()):
                                    data_type = '"'+data_type+'","null"'
                                    final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    ['+data_type+'],'+'\n                    "default"    :    "'+default+'"\n                    },'
                                else:
                                    final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    "'+data_type+'",'+'\n                    "default"    :    "'+default+'"\n                    },'
                    else:
                        if(self.checkBox_Null.GetValue()):
                            data_type = '"'+data_type+'","null"'
                            final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    ['+data_type+'],'+'\n                    "default"    :    "'+default+'",'+'\n                     "doc"    :    "'+desc+'"\n                    },'
                        else:
                            final='\n                    {\n                    "name"    :    "'+name+'",'+'\n                    "type"    :    "'+data_type+'",'+'\n                    "default"    :    "'+default+'",'+'\n                     "doc"    :    "'+desc+'"\n                    },'            
                    
                    self.textBox_nameField.SetValue("")
                    self.textbox_main.SetEditable(0)
                    self.textBox_name.SetEditable(0)
        
        else:
                    dlg = wx.MessageDialog(self, "The fields Name,Sub-Record Name,FieldName and Data Type cannot be blank",'Error', wx.OK | wx.CANCEL | wx.ICON_ERROR)
                    val = dlg.ShowModal()
                    dlg.Show()        
    
    #Changes the 'editable' property of main window allowing user to manually edit schemas    
    def edit(self,event):
        if(self.checkBox_Edit.GetValue()):
                    self.textBox_screen_second.SetEditable(1)
                    self.textBox_screen_second.SetInsertionPointEnd()
        else : 
                    self.textBox_screen_second.SetInsertionPointEnd()
                    self.textBox_screen_second.SetEditable(0)

    
    #Checks for all nestings and appends closing brackets accordingly and saves the file on disk
    def submit(self,event):
        global bracketsAdded,name,countAddrecord,submitted

        if (bracketsAdded != 1):

                    bracketsAdded = 0
                    dlg = wx.MessageDialog(self, "Record submitted successfully!! \nClick 'Submit Sub-Record' to get the output in Visualization panel of the Main Window ",'Alert', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
                    val = dlg.ShowModal()

                    submitted = 1
                    countAddrecord = 0
                    final = self.textBox_screen_second.GetValue()
                    final = final[:-1] +'\n                ]\n                }\n        },'
                    QA(None).writeRecord(final)
                    self.textBox_screen_second.SetValue(final)
                    self.button_add.Disable()
                    self.Close()
                    
        else:

                    temnested = 1
                    closebracketscheck = 0
                    closing = firstnested - 1
                    if(closing > 0):

                        endbrackets = ''
                        for i in range(closing):
                            if(closebracketscheck == 0):
                                closebrackets = self.textBox_screen_second.GetValue()
                                closebrackets = closebrackets.split('\n')
                                closebrackets = closebrackets[-1]
                            
                        
                            tab = (len(closebrackets) - len(closebrackets.strip()))/2
                            if(closebracketscheck == 0):
                                tab = tab+2
                            else:
                                tab = tab+1
                            sqbracket = '    '
                            curlbracket = '    '
                            curlbracket2 = '    '
                            sqspace = sqbracket * int(tab +(temnested))
                            curlspace = curlbracket * int(tab)
                            curlspace2 = curlbracket2*int((tab - temnested))
                            intermediate = endbrackets + '\n'+sqspace+']'
                            endbrackets = endbrackets + '\n'+sqspace+']'+'\n'+curlspace+'}'+'\n'+curlspace2+'}'
                            closebrackets = intermediate
                            closebracketscheck = closebracketscheck + 1
                        
                        textbox_value = self.textBox_screen_second.GetValue()
                        textbox_value = textbox_value[:-1]+endbrackets+','

                        self.textBox_screen_second.SetValue(textbox_value)

                    dlg = wx.MessageDialog(self, "Record submitted successfully!! \nClick 'Submit Sub-Record' to get the output in Visualization panel of the Main Window ",'Alert', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
                    val = dlg.ShowModal()
                    submitted = 1
                    countAddrecord = 0
                    final = self.textBox_screen_second.GetValue()
                    final = final[:-1] +'\n                ]\n                }\n        },'
                    QA(None).writeRecord(final)
                    self.textBox_screen_second.SetValue(final)
                    self.button_add.Disable()
                    self.Close()
    
    #Check for progress and throw warnings at exit    
    def OnCloseWindow(self, event):

        if(submitted !=1):
                    if wx.MessageBox("The file has not been saved... Continue closing?",
                                 "Please confirm",
                                 wx.ICON_QUESTION | wx.YES_NO) != wx.YES:

                        event.Veto()
                        return

        self.Destroy()
    

#Class for automated creation of schemas from input data - csv, json ,avro
    
SelectionList = []
class QA(UI.MyFrame1):
    global count,schema_name,flag,appendstring,submitFlag
    submitFlag = 0
    count = 0
    appendstring = ""

    def __init__(self,parent): 
        UI.MyFrame1.__init__(self,parent)  
    
    def OnSelect(self,event):
        item = event.GetSelection()

        
    def addRecord( self , event):
        global count,schema_name
        namespace = self.textBox_namespace.GetValue()
        type = self.textBox_type.GetValue()
        schema_name = self.textBox_schema_name.GetValue()

        if(count == 0):
                    if(type!="" and schema_name != "" ):
                        count = count+1

                        self.button_submitRecord.Enable()
                        self.button_addRecord.Disable()
                        self.button_add.Disable()
                        self.button_import.Disable()
                        self.button_json.Disable()
                        #self.button_avro.Disable()
                        self.textBox_screen.AppendText('{\n    "namespace"    :    "'+namespace+'",\n    "type"    :    "'+type+'",\n    "name"    :    "'+schema_name+'",\n    "fields"    :[')

                        app = wx.App(False) 
                        frame = record(None) 
                        frame.Show(True) 

                        app.MainLoop()
                        
                    else:
                        dlg = wx.MessageDialog(self, "The fields Type and Schema Name cannot be blank",'Error', wx.OK | wx.CANCEL | wx.ICON_ERROR)
                        val = dlg.ShowModal()
                        dlg.Show()
        if(count != 0):
                    self.button_submitRecord.Enable()
                    self.button_addRecord.Disable()
                    self.button_add.Disable()
                    self.button_import.Disable()
                    self.button_json.Disable()
                    #self.button_avro.Disable()
                    app = wx.App(False) 
                    frame = record(None) 
                    frame.Show(True) 

                    app.MainLoop()
        
    
    
    def writeRecord(self,record):
        global appendstring,submitFlag
        submitFlag +=1 
        appendstring = record
        
        
    def addfield( self, event ):
        global schema_name,count,submitFlag
    
        namespace = self.textBox_namespace.GetValue()
        type = self.textBox_type.GetValue()
        schema_name = self.textBox_schema_name.GetValue()
        name = self.textBox_name.GetValue()
        data_type = self.dropdown_data_type.GetValue()
        default = self.textBox_default.GetValue()
        desc = self.textBox_desc.GetValue()
        
        if(type!="" and schema_name != ""):          
                    if(name!="" and data_type != ""):
                        if(count==0):
                            self.textBox_screen.AppendText('{\n    "namespace"    :    "'+namespace+'",\n    "type"    :    "'+type+'",\n    "name"    :    "'+schema_name+'",\n    "fields"    :[')
                        
                        if(default == "" and desc ==""):
                            if(self.checkBox_Null.GetValue()):

                                data_type = '"'+data_type+'","null"'
                                final='\n        {\n            "name"    :    "'+name+'",'+'\n            "type"    :    ['+data_type+']'+'\n        },'

                            else:

                                final='\n        {\n            "name"    :    "'+name+'",'+'\n            "type"    :    "'+data_type+'"'+'\n        },'

                        elif(default == "" or desc ==""):
                            if(default == ""):
                                if(self.checkBox_Null.GetValue()):
                                    data_type = '"'+data_type+'","null"'
                                    final='\n        {\n            "name"    :    "'+name+'",'+'\n            "type"    :    ['+data_type+'],'+'\n            "doc"    :    "'+desc+'"\n        },'
                                else:
                                    final='\n        {\n            "name"    :    "'+name+'",'+'\n            "type"    :    "'+data_type+'",'+'\n            "doc"    :    "'+desc+'"\n        },'
                            
                            if(desc == ""):
                                if(data_type == 'int' or data_type == 'float' or data_type == 'double' or data_type == 'long'):
                                    if(self.checkBox_Null.GetValue()):
                                        data_type = '"'+data_type+'","null"'
                                        final='\n        {\n            "name"    :    "'+name+'",'+'\n            "type"    :    ['+data_type+'],'+'\n            "default"    :    '+default+'\n        },'
                                    else:
                                        final='\n        {\n            "name"    :    "'+name+'",'+'\n            "type"    :    "'+data_type+'",'+'\n            "default"    :    '+default+'\n        },'
                                else:
                                    if(self.checkBox_Null.GetValue()):
                                        data_type = '"'+data_type+'","null"'
                                        final='\n        {\n            "name"    :    "'+name+'",'+'\n            "type"    :    ['+data_type+'],'+'\n            "default"    :    "'+default+'"\n        },'
                                    else:
                                        final='\n        {\n            "name"    :    "'+name+'",'+'\n            "type"    :    "'+data_type+'",'+'\n            "default"    :    "'+default+'"\n        },'
                        else:
                            if(self.checkBox_Null.GetValue()):
                                data_type = '"'+data_type+'","null"'
                                final='\n        {\n            "name"    :    "'+name+'",'+'\n            "type"    :    ['+data_type+'],'+'\n            "default"    :    "'+default+'",'+'\n            "doc"    :    "'+desc+'"\n        },'
                            else:
                                final='\n        {\n            "name"    :    "'+name+'",'+'\n            "type"    :    "'+data_type+'",'+'\n            "default"    :    "'+default+'",'+'\n            "doc"    :    "'+desc+'"\n        },'
                    
                        
                        
                        if(submitFlag == 0):
                            self.button_submit_schema.Enable()
                            self.button_import.Disable()
                            self.button_json.Disable()
                            #self.button_avro.Disable()
                            self.textBox_screen.SetInsertionPointEnd()
                            self.textBox_screen.WriteText(final)
                            self.textBox_name.SetValue("")
                            self.dropdown_data_type.SetValue("null")
                            self.textBox_default.SetValue("")
                            self.textBox_desc.SetValue("")
                            self.textBox_namespace.SetEditable(0)
                            self.textBox_schema_name.SetEditable(0)
                            count+=1
                        if(submitFlag != 0):
                            self.button_submit_schema.Enable()
                            self.button_import.Disable()
                            self.button_json.Disable()
                            #self.button_avro.Disable()
                            screenFinal = self.textBox_screen.GetValue()
                            screenFinal = screenFinal + final
                            self.textBox_screen.SetInsertionPointEnd()
                            self.textBox_screen.SetValue(screenFinal)
                            self.textBox_name.SetValue("")
                            self.dropdown_data_type.SetValue("null")
                            self.textBox_default.SetValue("")
                            self.textBox_desc.SetValue("")
                            self.textBox_namespace.SetEditable(0)
                            self.textBox_schema_name.SetEditable(0)
                            count+=1
                        
                    else:
                        dlg = wx.MessageDialog(self, "The fields Name and Data type cannot be blank",'Error', wx.OK | wx.CANCEL | wx.ICON_ERROR)
                        val = dlg.ShowModal()
                        dlg.Show()
        else:
                    dlg = wx.MessageDialog(self, "The fields Type, Schema Name cannot be blank",'Error', wx.OK | wx.CANCEL | wx.ICON_ERROR)
                    val = dlg.ShowModal()
                    dlg.Show()
        
    
    
    
    def submitRecord(self,event):
        global appendstring
        name = self.textBox_name.GetValue()

        self.textBox_name.SetValue("")
        if(appendstring == ""):
                    dlg = wx.MessageDialog(self, 'Record did not save successfully','Error', wx.OK | wx.CANCEL | wx.ICON_ERROR)
                    val = dlg.ShowModal()
                    dlg.Show()
                    self.button_submitRecord.Disable()
                    self.button_addRecord.Enable()
                    self.button_add.Enable()
        else:
                    final = self.textBox_screen.GetValue()
                    final = final+appendstring
                    appendstring = ''
                    self.textBox_screen.SetValue(final)
                    self.button_addRecord.Enable()
                    self.button_submitRecord.Disable()
                    self.button_submit_schema.Enable()
                    self.button_add.Enable()
                    
    def submit(self,event):
        global schema_name,appendstring
        final = self.textBox_screen.GetValue()
        if(final == ""):
                    self.button_submit_schema.Disable()
                    dlg = wx.MessageDialog(self, 'Error : No Input','Error', wx.OK | wx.CANCEL | wx.ICON_ERROR)
                    val = dlg.ShowModal()
                    dlg.Show()
        else:

                    final = final[:-1] +'\n    ]\n}'
                    self.textBox_screen.SetValue(final)
                    final_obj= open(schema_name+"_schema.avsc","w")
                    final_obj.write(final)
                    final_obj.close()
                    dlg = wx.MessageDialog(self, 'Schema submitted successfully!! \nClick OK to open the Avro schema in File Explorer.','Avro Schema Designer', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
                    val = dlg.ShowModal()
                    if(val == wx.ID_OK):
                        fileName = schema_name+"_schema.avsc"
                        fileName = '\\'+fileName

                        path = os.getcwd()
                        finalpath =  '"'+path+fileName+'"'

                        subprocess.Popen('explorer /select,"'+finalpath+'"')

                    self.button_submit_schema.Disable()
                    self.button_add.Disable()
                    self.button_addRecord.Disable()
                    self.button_submitRecord.Disable()
                    self.button_import.Disable()
                    self.button_json.Disable()
                    #self.button_avro.Disable()
                    self.button_restart.Enable()
    def openDialog(self,event):
        global flag
        self.textBox_name.SetValue("")
        self.textBox_default.SetValue("")
        self.textBox_desc.SetValue("")
        self.textBox_namespace.SetValue("")
        self.textBox_type.SetValue("")
        self.textBox_schema_name.SetValue("")
        self.textBox_name.SetEditable(0)
        self.textBox_default.SetEditable(0)
        self.textBox_desc.SetEditable(0)
        self.textBox_namespace.SetEditable(0)
        #self.textBox_type.SetEditable(0)
        self.textBox_schema_name.SetEditable(0)
        
        openFileDialog = wx.FileDialog(self, 'Open a file', '', '','Schema files (*.avsc)|*.avsc', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        
        if(openFileDialog.ShowModal() == wx.ID_CANCEL):
                    return
        pathname = openFileDialog.GetPath()
        with open(pathname, 'r') as content_file:
                    content = content_file.read()
        self.textBox_screen.SetValue(content)
        self.button_add.Disable()
        self.button_submit_schema.Disable()
        self.button_restart.Enable()
        self.button_import.Disable()
        self.button_json.Disable()
        #self.button_avro.Disable()
        flag = 1
        
    def exit(self, e):
        self.Close()
    
    def edit(self,e):
        if(self.checkBox_Edit.GetValue()):
                    self.textBox_screen.SetEditable(1)
                    self.textBox_screen.SetInsertionPointEnd()
        else : 
                    self.textBox_screen.SetInsertionPointEnd()
                    self.textBox_screen.SetEditable(0)
                    
    def saveDialog( self, event ):
        screenText = self.textBox_screen.GetValue()
        if(screenText != ""):
                    with wx.FileDialog(self, "Save schema file", wildcard="Schema files (*.avsc)|*.avsc", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                        if fileDialog.ShowModal() == wx.ID_CANCEL:
                            return     # the user changed their mind
                        pathname = fileDialog.GetPath()
                    
                        with open(pathname, 'wb') as file:
                            final = self.textBox_screen.GetValue()
                            final = final[:-1] +'\n    ]\n}'
                            self.textBox_screen.SetValue(final)
                            final = self.textBox_screen.GetValue()
                            file.write(final)
                            file.close()
        
        else:
                    dlg = wx.MessageDialog(self, "The file is empty",'Error', wx.OK | wx.CANCEL | wx.ICON_ERROR)
                    val = dlg.ShowModal()
                    dlg.Show()
    
    def import_from_excel(self,event):
        namespace = self.textBox_namespace.GetValue()
        type = self.textBox_type.GetValue()
        schema_name = self.textBox_schema_name.GetValue()
        
        if(type!="" and schema_name != ""):
                    self.button_restart.Enable()
                    openFileDialog = wx.FileDialog(self, 'Open a file', '', '','CSV files (*.csv)|*.csv', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
                    if(openFileDialog.ShowModal() == wx.ID_CANCEL):
                        return
                    pathname = openFileDialog.GetPath()
                    
                    df = pd.read_csv(pathname)
                    
                    colTypes = df.columns.to_series().groupby(df.dtypes).groups
                    
                    boolcol = []
                    strcol = []
                    intcol = []
                    floatcol = []
                    doublecol = []
                    longcol = []
                    for i in colTypes:
                        if(i == np.int64):
                            intcol.append(colTypes[i])
                        elif(i == np.int32):
                            intcol.append(colTypes[i])
                        elif( i == object):
                            strcol.append(colTypes[i])
                        elif(i == bool):
                            boolcol.append(colTypes[i])
                        elif(i == float):
                            floatcol.append(colTypes[i])
                        elif(i == np.double):
                            doublecol.append(colTypes[i])
                        #elif(i == np.long):
                        #    longcol.append(colTypes[i])
                        else:
                                            continue
                    booleantype = [item for sublist in boolcol for item in sublist]
                    strtype = [item for sublist in strcol for item in sublist]
                    inttype = [item for sublist in intcol for item in sublist]
                    floattype = [item for sublist in floatcol for item in sublist]
                    doubletype = [item for sublist in doublecol for item in sublist]
                    #longtype = [item for sublist in longcol for item in sublist]
                    
                    self.textBox_screen.AppendText('{\n    "namespace"    :    "'+namespace+'",\n    "type"    :    "'+type+'",\n    "name"    :    "'+schema_name+'",\n    "fields"    :[')
                    
                    for i in strtype : 
                        self.textBox_screen.AppendText('\n        {\n            "name"    :    "'+i+'",'+'\n            "type"    :    "string"'+'\n        },')
                    
                    for i in inttype : 
                        self.textBox_screen.AppendText('\n        {\n            "name"    :    "'+i+'",'+'\n            "type"    :    "int"'+'\n        },')
                    
                    for i in floattype :
                        self.textBox_screen.AppendText('\n        {\n            "name"    :    "'+i+'",'+'\n            "type"    :    "float"'+'\n        },')
                    
                    for i in booleantype :
                        self.textBox_screen.AppendText('\n        {\n            "name"    :    "'+i+'",'+'\n            "type"    :    "boolean"'+'\n        },')
                        
                    for i in doubletype :
                        self.textBox_screen.AppendText('\n        {\n            "name"    :    "'+i+'",'+'\n            "type"    :    "double"'+'\n        },')
                    
                    #for i in longtype :
                    #    self.textBox_screen.AppendText('\n        {\n            "name"    :    "'+i+'",'+'\n            "type"    :    "long"'+'\n        },')
                    
                    final = self.textBox_screen.GetValue()
                    final = final[:-1] +'\n    ]\n}'
                    self.textBox_screen.SetValue(final)
                    final_obj= open(schema_name+"_schema.avsc","w")
                    final_obj.write(final)
                    final_obj.close()
                    self.button_submit_schema.Disable()
                    self.button_add.Disable()
                    self.button_addRecord.Disable()
                    self.button_submitRecord.Disable()
                    self.button_import.Disable()
                    self.button_json.Disable()
                    #self.button_avro.Disable()
                    self.button_restart.Enable()
                    dlg = wx.MessageDialog(self, "Schema saved successfully in the installation/working directory.\nClick OK to open the Avro schema in File Explorer.",'Avro Schema Designer', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
                    val = dlg.ShowModal()
                    dlg.Show()
                    if(val == wx.ID_OK):
                        fileName = schema_name+"_schema.avsc"
                        fileName = '\\'+fileName

                        path = os.getcwd()
                        finalpath =  '"'+path+fileName+'"'

                        subprocess.Popen('explorer /select,"'+finalpath+'"')
        
        else :
                    dlg = wx.MessageDialog(self, "The fields Type and Schema Name cannot be blank",'Error', wx.OK | wx.CANCEL | wx.ICON_ERROR)
                    val = dlg.ShowModal()
                    dlg.Show()
                    
    def import_from_json(self,event):
        namespace = self.textBox_namespace.GetValue()
        type = self.textBox_type.GetValue()
        schema_name = self.textBox_schema_name.GetValue()
        
        if(type!="" and schema_name != ""):
                    status = 0
                    try:
                        openFileDialog = wx.FileDialog(self, 'Open a file', '', '','json files (*.json)|*.json', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
                        if(openFileDialog.ShowModal() == wx.ID_CANCEL):
                            return
                        pathname = openFileDialog.GetPath()
                        file = open(pathname,'r')
                        data = file.read()
                        jsonSuccess = -1
                        try:
                            jsonData = json.loads(data)
                            jsonSuccess = 1
                        except Exception as e:
                            jsonSuccess = 0
                            logall.loginfo(str(e))
                            dlg = wx.MessageDialog(self, "The Json file is incorrect, please select the correct file",'Error', wx.OK | wx.CANCEL | wx.ICON_ERROR)
                            val = dlg.ShowModal()
                            dlg.Show()
                        file.close()
                        # dotHyphenFlag = 1
                        if (jsonSuccess ==1):
                            dotHyphenFlag = cdh.checkDotHyphenDict(jsonData)
                            
                            if dotHyphenFlag==1:
                                dlg = wx.MessageDialog(self, "Warning ! The input JSON file contains some non-permitted characters ('.','-' etc.). The generated schema may or may not function as expected.\nThe brick will attempt to replace all such characters with empty characters.\nClick OK to continue.",'Avro Schema Designer', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
                                val = dlg.ShowModal()
                                dlg.Show()
                                if(val == wx.ID_OK):
                                    temp = json_schema.generateAvroSchema(pathname)
                                    status = 1
                            else:
                                temp = json_schema.generateAvroSchema(pathname)
                                status = 1
                            
                            dataTypeCheck = cdt.compareList(jsonData)
                            
                            if dataTypeCheck[0]==True:
                                dlg = wx.MessageDialog(self, "Warning ! The input JSON file contains fields having changing datatypes. This is the message recieved from datatype check : \n "+dataTypeCheck[1]+"\nThe generated schema may be incorrect.\nClick OK to continue.",'Avro Schema Designer', wx.OK | wx.CANCEL | wx.ICON_ERROR)
                                val = dlg.ShowModal()
                                dlg.Show()
                                if(val == wx.ID_OK):
                                    temp = json_schema.generateAvroSchema(pathname)
                                    status = 1
                            elif dataTypeCheck[0]==False:
                                dlg = wx.MessageDialog(self, "Information: The input JSON file may contain fields having changing datatypes. This is the message recieved from datatype check : \n "+dataTypeCheck[1]+"\nClick OK to continue.",'Avro Schema Designer', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
                                val = dlg.ShowModal()
                                dlg.Show()
                                if(val == wx.ID_OK):
                                    temp = json_schema.generateAvroSchema(pathname)
                                    status = 1
                        
                    except Exception as e:
                        logall.loginfo(str(e))
                        #print (e)
                        dlg = wx.MessageDialog(self, "The Json file is incorrect, please select the correct file",'Error', wx.OK | wx.CANCEL | wx.ICON_ERROR)
                        val = dlg.ShowModal()
                        dlg.Show()
                    if(status == 1):
                        self.textBox_screen.AppendText('{\n    "namespace"    :    "'+namespace+'",\n    "type"    :    "'+type+'",\n    "name"    :    "'+schema_name+'",\n    "fields"    :[')
                        final = self.textBox_screen.GetValue()
                        final = final + temp
                        final = final[:-1] +'\n    ]\n}'
                        
                        self.textBox_screen.SetValue(final)
                        final_obj= open(schema_name+"_schema.avsc","w")
                        final_obj.write(final)
                        final_obj.close()
                        self.button_submit_schema.Disable()
                        self.button_add.Disable()
                        self.button_addRecord.Disable()
                        self.button_submitRecord.Disable()
                        self.button_import.Disable()
                        self.button_json.Disable()
                        #self.button_avro.Disable()
                        self.button_restart.Enable()
                        dlg = wx.MessageDialog(self, "Schema saved successfully in the installation/working directory.\nClick OK to open the Avro schema in File Explorer.",'Avro Schema Designer', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
                        val = dlg.ShowModal()
                        dlg.Show()
                        if(val == wx.ID_OK):
                                            fileName = schema_name+"_schema.avsc"
                                            fileName = '\\'+fileName
                                            path = os.getcwd()
                                            finalpath =  '"'+path+fileName+'"'
                                            subprocess.Popen('explorer /select,"'+finalpath+'"')
        
        else :
                    dlg = wx.MessageDialog(self, "The fields Type and Schema Name cannot be blank",'Error', wx.OK | wx.CANCEL | wx.ICON_ERROR)
                    val = dlg.ShowModal()
                    dlg.Show()
    
    def import_from_avro(self,event):
        namespace = self.textBox_namespace.GetValue()
        type = self.textBox_type.GetValue()
        schema_name = self.textBox_schema_name.GetValue()
        
        if(type!="" and schema_name != ""):
                    status = 0
                    try:
                        openFileDialog = wx.FileDialog(self, 'Open a file', '', '','avro files (*.avro)|*.avro', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
                        if(openFileDialog.ShowModal() == wx.ID_CANCEL):
                            return
                        pathname = openFileDialog.GetPath()

                        temp = json_schema.generateAvroSchema(pathname)
                        
                        status = 1
                        
                    except Exception as e:
                        dlg = wx.MessageDialog(self, "The Json file is incorrect, please select the correct file",'Error', wx.OK | wx.CANCEL | wx.ICON_ERROR)
                        val = dlg.ShowModal()
                        dlg.Show()
                    if(status == 1):
                        self.textBox_screen.AppendText('{\n    "namespace"    :    "'+namespace+'",\n    "type"    :    "'+type+'",\n    "name"    :    "'+schema_name+'",\n    "fields"    :[')
                        final = self.textBox_screen.GetValue()
                        final = final + temp
                        final = final[:-1] +'\n    ]\n}'
                        
                        self.textBox_screen.SetValue(final)
                        final_obj= open(schema_name+"_schema.avsc","w")
                        final_obj.write(final)
                        final_obj.close()
                        self.button_submit_schema.Disable()
                        self.button_add.Disable()
                        self.button_addRecord.Disable()
                        self.button_submitRecord.Disable()
                        self.button_import.Disable()
                        self.button_json.Disable()
                        #self.button_avro.Disable()
                        self.button_restart.Enable()
                        dlg = wx.MessageDialog(self, "Schema saved successfully in the installation/working directory.\nClick OK to open the Avro schema in File Explorer.",'Avro Schema Designer', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
                        val = dlg.ShowModal()
                        dlg.Show()
                        if(val == wx.ID_OK):
                                            fileName = schema_name+"_schema.avsc"
                                            fileName = '\\'+fileName
                                            path = os.getcwd()
                                            finalpath =  '"'+path+fileName+'"'
                                            subprocess.Popen('explorer /select,"'+finalpath+'"')
        
        else :
                    dlg = wx.MessageDialog(self, "The fields Type and Schema Name cannot be blank",'Error', wx.OK | wx.CANCEL | wx.ICON_ERROR)
                    val = dlg.ShowModal()
                    dlg.Show()
    
    #Kills the main instance and creates a new one    
    def restart( self,event):

        self.Close()
        global count,appendstring
        count = 0
        appendstring = ''
        app = wx.App(False) 

        frame = QA(None) 
        frame.Show(True) 

        app.MainLoop()

        del app
    
    def help( self,event):
        app = wx.App(False)  
        frame = UI.MyHelp()  
        frame.Show(True)  
        app.MainLoop()
    
    def validator(self,event):
        createdSchema = self.textBox_screen.GetValue()
        import vali_stub
        vali_stub.Myapp1(None).startWindow(createdSchema)
        #vali_stub.Myapp1(None).generatorOutput(createdSchema)
        #print(createdSchema)


app = wx.App(False) 
frame = QA(None) 
frame.Show(True) 
app.MainLoop()

del app   
