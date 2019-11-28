#########################################################
# Avro Schema Validator                                 #
# Performs all validation operations                    #
#                                                       #
# Authors : Ajinkya                                     #
# Last Modified : 11/30/2018                            #
#########################################################


import os #For Changing Directory
import json
import re
import ast
import requests
import logall


wxFlag = 0

global uri
global nFlag,sregistry
nFlag=0
sregistry = 0
uri=''
####################################
# Check for necessary libraries

try:
    import wx
    wxFlag = 1
except ImportError as e:
    logall.loginfo(str(e),'Package not imported')
    #print(e , 'Package not imported')
    os.system('pip install -U wxPython')

      

####################################
        
# Importing UI module
import vali_UI


####################################

# Main window of tool
class Myapp1 ( vali_UI.MyFrame1 ):
    global genSchema
    genSchema = ""
    
    #Intiating UI window
    def __init__(self, parent):
        vali_UI.MyFrame1.__init__(self,parent, title='Avro Schema Validator',pos=(200,200), size=(610,750))
        
    def startWindow(self,Schemagen):
        global genSchema
        if wxFlag ==1:
            genSchema = Schemagen
            app = wx.App(False)
            frame = Myapp1(None)
            frame.Show(True)
            app.MainLoop()
            del app
        else:
            logall.loginfo("Installing libraries, please restart tool again.")
            #print("Installing libraries, please restart tool again.")
            
    # Functionality for Restart button
    def onrestart(self,event):

        self.Close()
        app = wx.App(False)
        frame = Myapp1(None)
        frame.Show(True)
        app.MainLoop()
        del app
        
        
##        self.button_loadFile.Enable()
##        self.textBox_screen.SetValue("")
##        self.output_screen.SetValue("")
##        self.dropdown_topics.Disable()
##        self.textBox_topic.Disable()
##        self.dropdown_versions.Disable()
##        self.button_Delete.Disable()
##        self.button_DeleteAll.Disable()
##        self.button_pushSchema.Disable()

   
   
    # Functionality for Load Schema button
    def openDialog(self,event):
        global genSchema,uri
        loadValue = self.button_loadFile.GetValue()
        #self.button_loadFile.Disable()
        if (loadValue == "Local"):
            self.button_restart.Enable()
            self.dropdown_topics.Disable()
            self.textBox_topic.Disable()
            self.dropdown_versions.Disable()
            self.button_Delete.Disable()
            self.button_DeleteAll.Disable()
            self.button_pushSchema.Disable()
            self.output_screen.SetValue("")
            
            openFileDialog = wx.FileDialog(self, 'Load schema file', '', '','Schema files (*.avsc)|*.avsc', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if(openFileDialog.ShowModal() == wx.ID_CANCEL):
                return
            pathname = openFileDialog.GetPath()
            with open(pathname, 'r') as content_file:
                content = content_file.read()
            self.textBox_screen.SetValue(content)
            #self.button_loadFile.Disable()
        if(loadValue == "Schema Generator"):
            self.button_restart.Enable()
            self.dropdown_topics.Disable()
            self.textBox_topic.Disable()
            self.dropdown_versions.Disable()
            self.button_Delete.Disable()
            self.button_DeleteAll.Disable()
            self.button_pushSchema.Disable()
            self.output_screen.SetValue("")
            if (genSchema != ""):
                self.textBox_screen.SetValue(genSchema)
            else:
                dlg = wx.MessageDialog(self, "No input from Schema Generator",'Error', wx.OK | wx.ICON_ERROR)
                val = dlg.ShowModal()
                dlg.Show()
            
        
        if(loadValue == "Schema Registry"):
            global sregistry
            
            
            try:
                get_topics=requests.get(uri,timeout=5)
                self.dropdown_topics.Enable()
                self.dropdown_versions.Enable()
                self.button_Delete.Enable()
                self.button_DeleteAll.Enable()
                self.button_pushSchema.Enable()
                if(get_topics.status_code == 200):
                    sregistry = 1
                    try:
                        topic_encode=sorted(list(requests.get(uri,timeout=5).text.replace('"','').replace(']','').replace('[','').split(',')))
                        self.dropdown_topics.Clear()
                        self.dropdown_topics.Append("New subject")
                        for x in topic_encode:
                            self.dropdown_topics.Append(x)
                            
                    except requests.exceptions.Timeout as t:
                        dlg = wx.MessageDialog(self, "Timeout error, couldn't establish connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                        val = dlg.ShowModal()
                        dlg.Show()
                    except Exception as e:
                        dlg = wx.MessageDialog(self, "No connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                        val = dlg.ShowModal()
                        dlg.Show()
                        
            except requests.exceptions.Timeout as t:
                
                dlg = wx.MessageDialog(self, "Timeout error, couldn't establish connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                val = dlg.ShowModal()
                dlg.Show()
                        
            except Exception as e:
                
                dlg = wx.MessageDialog(self, "No connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                val = dlg.ShowModal()
                dlg.Show()
            

    global output
    output =" "
    
    #Functionality to load versions into the dropdown
    def loadVersion(self,event):
        input_Topic = self.dropdown_topics.GetValue()
        try:
            get_version= requests.get(uri+input_Topic+'/versions/',timeout=5).text
            if(input_Topic != "New subject"):
                if "error_code" in get_version:
                    dlg = wx.MessageDialog(self, "Schema doesn't exist",'Error', wx.OK  | wx.ICON_ERROR)
                    val = dlg.ShowModal()
                    dlg.Show()
                else:
                    self.dropdown_versions.Clear()
                    get_version = get_version.replace('[','')
                    get_version = get_version.replace(']','')
                    get_version = get_version.split(",")
                    for x in get_version:
                        self.dropdown_versions.Append(x)
            else:
                self.textBox_topic.SetValue("")
                self.textBox_topic.Enable()

        except requests.exceptions.Timeout as t:
                dlg = wx.MessageDialog(self, "Timeout error, couldn't establish connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                val = dlg.ShowModal()
                dlg.Show()
                
        except Exception as e:
            dlg = wx.MessageDialog(self, "No connection to Schema Registry",'Error', wx.OK  | wx.ICON_ERROR)
            val = dlg.ShowModal()
            dlg.Show()

    #Functionality to fetch the Schema from Schema Registry
    def fetchSchema(self,event):
        input_Topic = self.dropdown_topics.GetValue()
        input_Version = self.dropdown_versions.GetValue()
        try:
            version_value=requests.get(uri+input_Topic+'/versions/'+str(input_Version),timeout=5).text
            version_value = version_value.replace('\\','')
            version_value = version_value[version_value.find('{"type"'):]
            version_value = version_value[:-2]
            version_value = version_value.replace('{"type"','{\n"type"')
            version_value = version_value.replace('",','",\n')
            version_value = version_value.replace('"fields":[{','"fields":[{\n')
            version_value = version_value.replace(']}',']\n}')
            self.textBox_screen.SetValue(version_value)

        except requests.exceptions.Timeout as t:
                dlg = wx.MessageDialog(self, "Timeout error, couldn't establish connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                val = dlg.ShowModal()
                dlg.Show()
            
        except Exception as e:
            dlg = wx.MessageDialog(self, "No connection to Schema Registry",'Error', wx.OK  | wx.ICON_ERROR)
            val = dlg.ShowModal()
            dlg.Show()
        

    #Functionality to delete the Specific Version

    def delete(self,event):
        input_Topic = self.dropdown_topics.GetValue()                
        input_Version = self.dropdown_versions.GetValue()
        rest_location=uri+input_Topic
        
        if input_Topic != '' and input_Version !='':
            
            dlg = wx.MessageDialog(self, 'Specific version selected in the Version dropdown will get deleted !! \nClick OK to Continue !!','Alert', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
            val = dlg.ShowModal()
            if(val == wx.ID_OK):                    
                try:
                    delete_version=requests.delete(rest_location+'/versions/'+input_Version,timeout=5)
                    if delete_version.status_code ==200:
                        dlg = wx.MessageDialog(self, "Schema deleted successfully \n Message from server : "+delete_version.text,'Alert', wx.OK  | wx.ICON_INFORMATION)
                        val = dlg.ShowModal()
                        dlg.Show()
                        self.textBox_screen.SetValue("")
                        try:
                            get_version= requests.get(uri+input_Topic+'/versions/',timeout=5).text
                            if "error_code" in get_version:
                                dlg = wx.MessageDialog(self, "No schema exists in the subject"+input_Topic,'Alert', wx.OK | wx.ICON_INFORMATION)
                                val = dlg.ShowModal()
                                dlg.Show()
                            else:
                                self.dropdown_versions.Clear()
                                get_version = get_version.replace('[','')
                                get_version = get_version.replace(']','')
                                get_version = get_version.split(",")
                                for x in get_version:
                                    self.dropdown_versions.Append(x)

                        except requests.exceptions.Timeout as t:
                            dlg = wx.MessageDialog(self, "Timeout error, couldn't establish connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                            val = dlg.ShowModal()
                            dlg.Show()
                        except Exception as e:
                            dlg = wx.MessageDialog(self, "No connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                            val = dlg.ShowModal()
                            dlg.Show()
                    else:
                         dlg = wx.MessageDialog(self, "Couldn't delete the schema \n Message from server : "+delete_version.text,'Error', wx.OK | wx.ICON_ERROR)
                         val = dlg.ShowModal()
                         dlg.Show()
                         self.textBox_screen.SetValue("")

                except requests.exceptions.Timeout as t:
                    dlg = wx.MessageDialog(self, "Timeout error, couldn't establish connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                    val = dlg.ShowModal()
                    dlg.Show()
                         
                except Exception as e:
                    dlg = wx.MessageDialog(self, "No connection to Schema Registry",'Error', wx.OK  | wx.ICON_ERROR)
                    val = dlg.ShowModal()
                    dlg.Show()
        else:
            dlg = wx.MessageDialog(self, 'Please select a Subject name and Version to be deleted!','Error', wx.OK | wx.ICON_ERROR)
            val = dlg.ShowModal()
                
                        
    #Funtionality to delete the topic
    def deleteall(self,event):
        input_Topic = self.dropdown_topics.GetValue()
        rest_location=uri+input_Topic
        
        if input_Topic!= '':
            
            dlg = wx.MessageDialog(self, 'Deleting the subject !! \nClick OK to Continue !!','Alert', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
            val = dlg.ShowModal()
            if(val == wx.ID_OK):
                try:
                    delete_topic=requests.delete(rest_location,timeout=5)
                    if delete_topic.status_code ==200:
                        dlg = wx.MessageDialog(self, "Subject deleted successfully \n Message from server : "+delete_topic.text,'Alert', wx.OK  | wx.ICON_INFORMATION)
                        val = dlg.ShowModal()
                        dlg.Show()
                        self.textBox_screen.SetValue("")
                        try:
                            topic_encode=sorted(list(requests.get(uri,timeout=5).text.replace('"','').replace(']','').replace('[','').split(',')))
                            self.dropdown_topics.Clear()
                            self.dropdown_versions.Clear()
                            self.dropdown_topics.Append("New subject")
                            for x in topic_encode:
                                self.dropdown_topics.Append(x)

                        except requests.exceptions.Timeout as t:
                            dlg = wx.MessageDialog(self, "Timeout error, couldn't establish connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                            val = dlg.ShowModal()
                            dlg.Show()
                            
                        except Exception as e:
                            dlg = wx.MessageDialog(self, "No connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                            val = dlg.ShowModal()
                            dlg.Show()
                    else:
                        dlg = wx.MessageDialog(self, "Couldn't delete the subject"+delete_topic.text,'Error', wx.OK  | wx.ICON_ERROR)
                        val = dlg.ShowModal()
                        dlg.Show()
                        self.textBox_screen.SetValue("")

                except requests.exceptions.Timeout as t:
                    dlg = wx.MessageDialog(self, "Timeout error, couldn't establish connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                    val = dlg.ShowModal()
                    dlg.Show()
                        
                except Exception as e:
                        dlg = wx.MessageDialog(self, "No connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                        val = dlg.ShowModal()
                        dlg.Show()
        else:
            dlg = wx.MessageDialog(self, 'Please select a Subject name to be deleted!','Error', wx.OK | wx.ICON_ERROR)
            val = dlg.ShowModal()
            
    #Functionality to push Schema into Schema Registry
    def pushSchemaRegistry(self,event):

        global nFlag
        validate = self.textBox_screen.GetValue()
        if(validate != ""):
            if(nFlag==1 ):
                input_Topic = self.dropdown_topics.GetValue()
                if(input_Topic != "New subject"):
                    
                    dlg = wx.MessageDialog(self, "Current version will be pushed under the Subject :" +input_Topic+"\n Click Ok to Confirm",'Alert', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
                    val = dlg.ShowModal()
                    dlg.Show()
                    if(val == wx.ID_OK):
                        newVersion = self.textBox_screen.GetValue()
                        newVersion = newVersion.replace('"','\\"')
                        newVersion = '{"schema":"'+newVersion+'"}'
                        newVersion = newVersion.replace('\r','')
                        newVersion = newVersion.replace('\n','')
                        url_post_req=(uri+input_Topic+'/versions/')
                        headers={'Content-Type' : 'application/vnd.schemaregistry.v1+json'}
                        try :
                            file_post=requests.post(url_post_req,data=newVersion,headers=headers,timeout=5)
                            
                            if (file_post.status_code == 200):
                                self.button_pushSchema.Disable()
                                dlg = wx.MessageDialog(self, "Schema posted successfully \n Message from server : " + file_post.text,'Avro Schema Designer', wx.OK | wx.ICON_INFORMATION)
                                val = dlg.ShowModal()
                                dlg.Show()
                                self.textBox_screen.SetValue("")
                                try:
                                    get_version= requests.get(uri+input_Topic+'/versions/',timeout=5).text
                                    if "error_code" in get_version:
                                        dlg = wx.MessageDialog(self, "No schema exists in the subject"+input_Topic,'Alert', wx.OK | wx.ICON_INFORMATION)
                                        val = dlg.ShowModal()
                                        dlg.Show()
                                    else:
                                        self.dropdown_versions.Clear()
                                        get_version = get_version.replace('[','')
                                        get_version = get_version.replace(']','')
                                        get_version = get_version.split(",")
                                        for x in get_version:
                                            self.dropdown_versions.Append(x)
                                            
                                except requests.exceptions.Timeout as t:
                                    dlg = wx.MessageDialog(self, "Timeout error, couldn't establish connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                                    val = dlg.ShowModal()
                                    dlg.Show()

                                except Exception as e:
                                    dlg = wx.MessageDialog(self, "No connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                                    val = dlg.ShowModal()
                                    dlg.Show()
                
                            else:
                                self.button_pushSchema.Disable()
                                dlg = wx.MessageDialog(self, "Schema could not be published"+file_post.text,'Error', wx.OK  | wx.ICON_ERROR)
                                val = dlg.ShowModal()
                                dlg.Show()
                                self.textBox_screen.SetValue("")

                        except requests.exceptions.Timeout as t:
                            dlg = wx.MessageDialog(self, "Timeout error, couldn't establish connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                            val = dlg.ShowModal()
                            dlg.Show()
                
                        except Exception as e:
                            dlg = wx.MessageDialog(self, "No connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                            val = dlg.ShowModal()
                            dlg.Show()

                elif(input_Topic == "New subject"):
                    
                    subject = self.textBox_topic.GetValue()
                    if(subject != ""):
                        try:
                            dlg = wx.MessageDialog(self, "Creating a new subject :" +subject+"\n Click Ok to Confirm",'Alert', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
                            val = dlg.ShowModal()
                            dlg.Show()
                            if(val == wx.ID_OK):
                                newVersion = self.textBox_screen.GetValue()
                                newVersion = newVersion.replace('"','\\"')
                                newVersion = '{"schema":"'+newVersion+'"}'
                                newVersion = newVersion.replace('\r','')
                                newVersion = newVersion.replace('\n','')
                                newVersion = newVersion.replace('\t','')
                                newVersion = newVersion.replace(' ','')
                                                        
                                url_post_req=(uri+subject+'/versions/')
                                headers={'Content-Type' : 'application/vnd.schemaregistry.v1+json'}
                                file_post=requests.post(url_post_req,data=newVersion,headers=headers,timeout=5)
                                if (file_post.status_code == 200):
                                    self.button_pushSchema.Disable()
                                    self.textBox_topic.SetValue("Enter Subject Name")
                                    self.textBox_topic.Disable()
                                    dlg = wx.MessageDialog(self, "Schema posted successfully \n Message from server : " + file_post.text,'Avro Schema Designer', wx.OK  | wx.ICON_INFORMATION)
                                    val = dlg.ShowModal()
                                    dlg.Show()
                                    self.textBox_screen.SetValue("")
                                    try:
                                        topic_encode=sorted(list(requests.get(uri,timeout=5).text.replace('"','').replace(']','').replace('[','').split(',')))
                                        self.dropdown_topics.Clear()
                                        self.dropdown_topics.Append("New subject")
                                        for x in topic_encode:
                                            self.dropdown_topics.Append(x)

                                    except requests.exceptions.Timeout as t:
                                        dlg = wx.MessageDialog(self, "Timeout error, couldn't establish connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                                        val = dlg.ShowModal()
                                        dlg.Show()

                                    except Exception as e:
                                        dlg = wx.MessageDialog(self, "No connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                                        val = dlg.ShowModal()
                                        dlg.Show()
                
                                else:
                                    self.button_pushSchema.Disable()
                                    self.textBox_topic.Disable()
                                    dlg = wx.MessageDialog(self, "Schema could not be published"+file_post.text,'Error', wx.OK  | wx.ICON_ERROR)
                                    val = dlg.ShowModal()
                                    dlg.Show()
                                    self.textBox_screen.SetValue("")

                        except requests.exceptions.Timeout as t:
                            dlg = wx.MessageDialog(self, "Timeout error, couldn't establish connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                            val = dlg.ShowModal()
                            dlg.Show()
                                    
                        except Exception as e:
                            dlg = wx.MessageDialog(self, "No connection to Schema Registry",'Error', wx.OK | wx.ICON_ERROR)
                            val = dlg.ShowModal()
                            dlg.Show()

                    else:
                        dlg = wx.MessageDialog(self, "Subject Name can't be empty",'Error', wx.OK  | wx.ICON_ERROR)
                        val = dlg.ShowModal()
                        dlg.Show()

                else:
                    dlg = wx.MessageDialog(self, "Please specify Subject Name before pushing into Schema Registry",'Error', wx.OK  | wx.ICON_ERROR)
                    val = dlg.ShowModal()
                    dlg.Show()
                    
            else:
                dlg = wx.MessageDialog(self, "Validate the schema before pushing it into Schema Registry",'Alert', wx.OK  | wx.ICON_INFORMATION)
                val = dlg.ShowModal()
                dlg.Show()

        else:
            dlg = wx.MessageDialog(self, "Load the schema to verify and then push into Schema Regisrty",'Alert', wx.OK  | wx.ICON_INFORMATION)
            val = dlg.ShowModal()
            dlg.Show()

    # Functionality for Validate button
    def onValidate(self,event):
        global output
        output = "Performing formatting validation...\n"
        
        validateInput = self.textBox_screen.GetValue()
        sFlag=0
        
        try:
            parsedScript = json.loads(validateInput)
            sFlag=1
            output=output+"> No errors found while validating formatting rules in schema."
            self.output_screen.SetValue(output)  
       
            
        except Exception as e:
            logall.loginfo(str(e))
            #print (e)
            if validateInput=='':
                output=output+"> No input schema has been provided." ###+str(e)+"."
                self.output_screen.SetValue(output)
            else:
                self.validateForm(validateInput,e)
            
        if sFlag==1:
            self.validateSynt(validateInput)

       
    # Functionality for About button
    def openAbout(self,event):
        app = wx.App(False)
        frame = Myapp2(None)
        frame.Show(True)
        app.MainLoop()


    # Functionality for View Rules button
    def openRules(self,event):
        app=wx.App(False)
        frame = Myapp4(None)
        frame.Show(True)
        app.MainLoop()


    # Functionality for Save schema button
    def saveDialog(self):
        
        with wx.FileDialog(self, "Save schema to file", wildcard="Schema files (*.avsc)|*.avsc", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
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

    # Function for validating Formatting in input schema
    def validateForm(self,data,finalerror):
        data = data.replace('^','')
        data= data.replace('\n','^').replace('\r\t',' ').replace('\r',' ').replace('\t',' ')


        global opening_quotes_flag
        global closing_quotes_flag
        global opening_curly_flag
        global closing_curly_flag
        global opening_square_flag
        global closing_square_flag
        global comma_flag
        global alphanumeric_flag
        global colon_flag,new_line_flag

        global opened_flag 

        global brackets
        global status
        global second_last_char,index_counter

        global output

        opening_quotes_flag = 0
        closing_quotes_flag = 0
        opening_curly_flag = 1
        closing_curly_flag = 0
        opening_square_flag = 0
        closing_square_flag = 0
        comma_flag = 0
        alphanumeric_flag = 0
        colon_flag=0

        opened_flag = 0

        brackets=[]
        status=0
        second_last_char = ""
        new_line_flag = 0
        
        def validateSquareBrackets(dataSnippet):
            qoutes_flag = 0
            bracket_flag =0
            temp_comma_flag = 0
            dataSnippet = dataSnippet.replace('^','').replace(' ','')
            status = 0
            if dataSnippet[0] == '"':
                
                for e in dataSnippet: 
                    if qoutes_flag ==0 and e == '"':
                        qoutes_flag = 1
                    elif qoutes_flag ==1 and e == '"':    
                        temp_comma_flag = 1
                    elif temp_comma_flag == 1 and e == ',':
                        logall.loginfo("Correct")
                        #print("Correct")
                    elif temp_comma_flag == 1 and e == ':':
                        status = 1
                        break
                    elif temp_comma_flag == 1 and e == ']':
                        break
            return status

        def errors(last_char,x):
                global status,opened_flag,second_last_char,new_line_flag,output
                if (last_char == '^'):
                        last_char = second_last_char
                        new_line_flag = 1
                        output=output+"> Error at line no. "+str(line_no_counter-1)+", column "+str(last_line_end-2)
                else:
                        output=output+"> Error at line no. "+str(line_no_counter)+", column "+str(col_counter-2)

                if last_char == '{':
                        
                        output=output+"\n> Expecting '\"'\n"
                elif last_char == '}':
                        if x == ']':
                            output=output+"\n> Unexpected ']', please check for corresponding '['\n"
                        else:
                            output=output+"\n> Expecting ',' \n   OR\n   Expecting '}'\n   OR\n   Expecting ']'\n"
                elif last_char == '[':
                        output=output+"\n> Expecting '{'\n   OR\n   Expecting '\"'\n"
                elif last_char == ']':
                        output=output+"\n> Expecting '}' \n   OR\n   Expecting ','\n"    
                elif last_char == ',':
                        output=output+"\n> Expecting '{' \n   OR\n   Expecting '\"'\n"    
                elif last_char == '"':
                        if opened_flag == 1:
                                output=output+"\n> Expecting alphanumeric values\n"
                        else:
                                if (x == '"' and last_char == '"') and new_line_flag == 0:
                                        output=output+"\n> Expecting ':' \n   OR\n   Expecting ','\n"
                                elif x == '"' and last_char == '"' and new_line_flag == 1:
                                        output=output+"\n> Expecting ',' \n   OR\n   Expecting ':'\n"
                                elif x == '[' and last_char == '"':
                                        output = output+"\n> Expecting ':' \n"
                                else:
                                    
                                        if x == '}':
                                            
                                            output=output+"\n> Unexpected '}', please check for corresponding '{'\n"
                                        else:
                                            
                                            output=output+"\n> Expecting ',' \n   OR\n   Expecting '}'\n  OR\n   Expecting ']'\n"
                elif last_char == ':':
                        output=output+"\n> Expecting '\"'\n   OR\n   Expecting '['\n"    
                elif last_char.isalnum:
                        output=output+"\n> Expecting '\"'\n"    
                status = 1
                

        def closing_curly():
                global opening_quotes_flag,closing_quotes_flag,opening_curly_flag,closing_curly_flag,opening_square_flag,closing_square_flag,comma_flag,alphanumeric_flag,colon_flag,opened_flag, brackets,output
                test ="1"
                if(brackets[-1] == "{"):
                        if(closing_curly_flag == 1):
                                closing_curly_flag = comma_flag = closing_square_flag = 1
                                opening_quotes_flag = closing_quotes_flag = opening_curly_flag = opening_square_flag = alphanumeric_flag = colon_flag = 0
                                try:
                                        del brackets[-1]
                                except:
                                        test = "err"
                                return test

        def closing_square():
                global opening_quotes_flag,closing_quotes_flag,opening_curly_flag,closing_curly_flag,opening_square_flag,closing_square_flag,comma_flag,alphanumeric_flag,colon_flag,opened_flag, brackets,output
                
                if(brackets[-1] == "["):
                        if(closing_square_flag == 1):
                                closing_curly_flag = comma_flag = 1
                                opening_quotes_flag = closing_quotes_flag = opening_curly_flag = opening_square_flag = closing_square_flag = alphanumeric_flag = colon_flag = 0
                                del brackets[-1]
                                return "1"
                        
        def opening_square():
                global opening_quotes_flag,closing_quotes_flag,opening_curly_flag,closing_curly_flag,opening_square_flag,closing_square_flag,comma_flag,alphanumeric_flag,colon_flag,opened_flag, brackets,output
                
                if(opening_square_flag == 1):
                        brackets.append('[')
                        opening_curly_flag = opening_quotes_flag = 1
                        closing_quotes_flag = closing_curly_flag = opening_square_flag = closing_square_flag = comma_flag = alphanumeric_flag = colon_flag = 0
                        return "1"
                
        def comma():
                global opening_quotes_flag,closing_quotes_flag,opening_curly_flag,closing_curly_flag,opening_square_flag,closing_square_flag,comma_flag,alphanumeric_flag,colon_flag,opened_flag, brackets,output
                
                if(comma_flag == 1 and opened_flag == 0 and closing_quotes_flag == 0):
                        opening_quotes_flag = opening_curly_flag = 1
                        closing_quotes_flag = closing_curly_flag = opening_square_flag = closing_square_flag = comma_flag = alphanumeric_flag = colon_flag = opened_flag = 0
                        return "1"
                        
        def colon():
                global opening_quotes_flag,closing_quotes_flag,opening_curly_flag,closing_curly_flag,opening_square_flag,closing_square_flag,comma_flag,alphanumeric_flag,colon_flag,opened_flag, brackets,output
                if(closing_quotes_flag == 0 and opened_flag == 0 and colon_flag == 1):
                        opening_quotes_flag = opening_square_flag = opening_curly_flag = 1
                        closing_quotes_flag = closing_curly_flag = closing_square_flag = comma_flag = alphanumeric_flag = colon_flag = 0
                        return "1"
                
        def alphanumeric():
                global opening_quotes_flag,closing_quotes_flag,opening_curly_flag,closing_curly_flag,opening_square_flag,closing_square_flag,comma_flag,alphanumeric_flag,colon_flag,opened_flag, brackets,output
                if(alphanumeric_flag == 1 and opened_flag == 1):
                        closing_quotes_flag = 1
                        opening_quotes_flag = opening_curly_flag = closing_curly_flag = opening_square_flag = closing_square_flag = comma_flag = colon_flag = 0
                        return "1"
                
        def quotes():
                global opening_quotes_flag,closing_quotes_flag,opening_curly_flag,closing_curly_flag,opening_square_flag,closing_square_flag,comma_flag,alphanumeric_flag,colon_flag,opened_flag, brackets,output
                if(opened_flag == 0 and opening_quotes_flag== 1 and closing_quotes_flag==0 and alphanumeric_flag == 0):
                        opened_flag = alphanumeric_flag = 1
                        opening_quotes_flag = closing_quotes_flag = opening_curly_flag = closing_curly_flag = opening_square_flag = closing_square_flag = comma_flag = colon_flag = 0
                        return "1"
                        
                elif(opened_flag == 1 and closing_quotes_flag == 1 and alphanumeric_flag ==1 and opening_quotes_flag ==0):
                        comma_flag = colon_flag = closing_square_flag = closing_curly_flag = 1
                        opening_quotes_flag = closing_quotes_flag = opening_curly_flag = opening_square_flag = alphanumeric_flag = opened_flag =0
                        return "1"
                        
        def opening_curly():
                global opening_quotes_flag,closing_quotes_flag,opening_curly_flag,closing_curly_flag,opening_square_flag,closing_square_flag,comma_flag,alphanumeric_flag,colon_flag,opened_flag, brackets,output
                if(opening_curly_flag == 1):
                        brackets.append('{')
                        opening_quotes_flag = 1
                        closing_quotes_flag = opening_curly_flag = closing_curly_flag = opening_square_flag = closing_square_flag = comma_flag = alphanumeric_flag = colon_flag = 0
                        return "1"

        line_no_counter = 1
        col_counter = 1
        default_flag = 0
        last_char = ""
        last_line_end = 0
        qoutes_count = 0
        index_counter = 0
        d_flag=0
        temp = data.strip()
        if temp[0] != "{":
                output=output+"> Expecting '{' at the beginning\n"
                status =1
                #sys.exit()
        else:
            for x in data:
                    index_counter+=1
                    if status == 1:
                            break
                            
                    if x == " ":
                            col_counter += 1
                            continue
                            
                    if x == '^':
                            line_no_counter += 1
                            last_line_end = col_counter 
                            col_counter = 1
                            second_last_char = last_char
                    else:
                            if x == '{':
                                    out = opening_curly()
                                    if out != "1":
                                            errors(last_char,x)
                                            
                            elif x == '"':
                                    qoutes_count +=1
                                    if default_flag == 1:
                                            default_flag =0
                                    out = quotes()
                                    if out != "1":
                                            errors(last_char,x)
                                    
                            elif x.isalnum() or x == "_" or x == "." or x=="\\":
                                    if(default_flag == 1 and x.isdigit()):
                                            comma_flag = closing_curly_flag = 1
                                    elif (default_flag ==1 and x.isalpha() and d_flag ==0):
                                            
                                            i = index_counter-2
                                            def_check =''
                                            count = pos_def = 0
                                            while i>0:
                                                pos_def = data[i].find("\"")
                                                def_check=data[i]+def_check
                                                
                                                if pos_def!=-1:
                                                    count+=1    
                                                if count ==2:
                                                    def_check = def_check.replace(' ','')                                             
                                                    break
                                                i=i-1

                                            if x== "n":
                                                if data[index_counter-1:index_counter+3]== "null" and def_check == "\"default\":":
                                                    comma_flag = closing_curly_flag = 1
                                                    d_flag=1
                                                else:
                                                    errors(last_char,x)
                                            elif x == "t":
                                                if data[index_counter-1:index_counter+3]== "true" and def_check == "\"default\":":
                                                    comma_flag = closing_curly_flag = 1
                                                    d_flag=1
                                                else:
                                                    errors(last_char,x)
                                            elif x == "f":
                                                if data[index_counter-1:index_counter+4]== "false" and def_check == "\"default\":":
                                                    comma_flag = closing_curly_flag = 1
                                                    d_flag=1
                                                else:
                                                    errors(last_char,x)
                                            else:
                                                errors(last_char,x)
                                            
                                                    
##                                            if data[index_counter-11:index_counter-1]== "\"default\":":
##                                                comma_flag = closing_curly_flag = 1
##                                                d_flag=1
##                                            else:
##                                                errors(last_char,x)
                                    else:
                                        if d_flag!=1:
                                                                                       
                                            out = alphanumeric()
                                            if out != "1":
                                                    errors(last_char,x)
                                                    
                            elif x == ":":
                                    default_flag = 1
                                    out = colon()
                                    if out != "1":
                                            errors(last_char,x)
                                    
                            elif x == ",":
                                    if default_flag == 1:
                                            default_flag =0
                                    out = comma()
                                    if out != "1":
                                            errors(last_char,x)
                            
                            elif x == "[":
                                    out1 = validateSquareBrackets(data[index_counter:])
                                    if out1 == 1:
                                        status = 1
                                        output=output+("> Error at line no. "+str(line_no_counter)+" column " + str(col_counter)+"\n> Missing '{' bracket.")
                                        
                                        break
                                    out = opening_square()
                                    if out != "1":
                                            errors(last_char,x)
                                            
                            elif x == "]":
                                    out = closing_square()
                                    if out != "1":
                                            errors(last_char,x)
                                            
                            elif x == "}":
                                    if d_flag==1:
                                        d_flag=0
                                    out = closing_curly()
                                    if out != "1":
                                            errors(last_char,x)
                            else:
                                
                                errors(last_char,x)
                                status=1
                                
                    col_counter+=1
                    last_char = x
        if (status != 1):
                if brackets:
                        if brackets[-1] == '{':
                                output=output+"> Missing parenthesis '}' near end"
                        elif brackets[-1] == '[':
                                output=output+"> Missing parenthesis ']' near end"
                else: 
                        output=output+"\n> "+str(finalerror)+"."
        else:
                output=output+""
        self.output_screen.SetValue(output)

        
        
    # Function for validating syntax in input schema
    def validateSynt(self,data):
        global output, Rflag, typeCheck, kFlag, nFlag , vFlag
        output=output+"\n\nPerforming syntax validation..."
        key_space = ['namespace','type','name','fields','default','doc','values','items','symbols','aliases']
        type_space = ['int','long','float','double','string','record','array','null','boolean','enum','map','bytes']

        Flag1=0
        Flag2=0
        Rflag = 0
        typeCheck=0
        kFlag=0
        nFlag=0
        vFlag=0

        try:
            x = ast.literal_eval(data) #converting input schema into dict
            Flag1=1
        except Exception as a:
            
            try:
                out = json.loads(data)
                Flag2=1
            except Exception as e:
                msg = str(e)
                location = [int(s) for s in msg.split() if s.isdigit()]
                output=output+"\n> Error in line number ",location[0], " and position ",location[1]
                output=output+"\n> Invalid use of curly brackets, {} can be used to enclose a JSON object only."
                self.output_screen.SetValue(output)


        #get line number and position
        def getLinePos(item):
            global output
            lines = data.split('\n')
            for line in lines:

                if len(re.findall(re.escape(item),line))>0:
                    line_num=lines.index(line)+1
                    position = line.find(item)
                    output=output+"\n> Error in line number "+str(line_num)+ " and position "+str(position)
                    break


        #checkKeys function to validate Keys in key-value pairs

        def checkKeys(x):
            
            global Rflag,typeCheck,kFlag,output,nameFlag
            breakFlag=0
            nameFlag=0
            if kFlag!=1:
                
                if "type" not in x.keys():
                    
                    if Rflag==1:
                        try:
                            a= x['name']
                            nameFlag=1
                        except:
                            output=output+"\n> Missing name and type definition inside curly brackets."
                            kFlag=1
                        if nameFlag==1:
                            
                            lines = data.split('\n')
                            for line in lines:
                                line_num=lines.index(line)+1
                                position = line.find(a)
                                if position!=-1:
                                    
                                    output=output+"\n> Missing type defintion in schema at line number "+str(line_num)+" and position "+str(position + len(a)+1)
                                    typeCheck=1
                                    kFlag=1
                                    break
                    else:
                        output=output+"\n> Missing type definition in main outer loop."
                        typeCheck=1
                        kFlag=1


            if typeCheck!=1:
                
                for key,val in x.items():
                    if key not in key_space:

                        # case of preceding space or special characters
                        if re.findall('^[^a-zA-Z0-9]',key):
                            getLinePos(key)
                            output=output+"\n> Invalid key specified, special characters and space are not allowed."
                            kFlag=1
                            break
                                
                        # case of trailing space or special characters
                        elif re.findall('[^a-z0-9]$',key):
                            getLinePos(key)
                            output=output+"\n> Invalid key specified, special characters and space are not allowed."
                            kFlag=1
                            break

                        #other cases
                        else:
                            lines = data.split('\n')

                            for line in lines:
                                if len(re.findall('\\b'+key+'\\b',line))>0:
                                    line_num=lines.index(line)+1
                                    position = line.find(key)
                                    output=output+"\n> Error in line number "+str(line_num)+ " and position "+str(position)
                                    output=output+"\n> Invalid key specified, please recheck key definitions."
                                    kFlag=1
                                    break
                        break
                    

                                
                    if isinstance(val,list):
                        for element in val:
                            if isinstance(element,dict):
                                Rflag=1
                                checkKeys(element)
                        
                    if isinstance(val,dict):
                        Rflag=1
                        checkKeys(val)
                    
        #checkKeys function to validate Values in key-value pairs
        def checkValues(x):
            global kFlag,vFlag,output,nFlag,sregistry
            
            breakFlag=0
            lines = data.split('\n')
            
            for key,val in x.items():
                if key == "name":
                    #print(val)
                    m = re.findall('^[^A-Za-z_]',val)
                    if len(m)>0:
                        getLinePos(val)
                        output=output+"\n> Value for 'name'\n      (a) can only start with alphabets (lower/UPPER case) or underscore\n      (b) cannot start with numbers, space or other symbols"
                        vFlag=1
                        break
                    m = re.findall('[^A-Za-z0-9_]',val)
                    
                    if len(m)>0:
                        getLinePos(val)
                        output=output+"\n> Value for 'name'\n      (a) can contain alphanumerics (lower/UPPER case)\n      (b) can contain underscore\n      (c) cannot contain space or other symbols"
                        vFlag=1
                        break
                    if val == "":
                        output=output+"\n> Missing 'name' value"
                        vFlag=1
                        break

                    
                elif key=='namespace':
                    m = re.findall('^[^A-Za-z_]',val)
                    if len(m)>0:
                        getLinePos(val)
                        output=output+"\n> Value for 'namespace'\n      (a) can only start with alphabets (lower/UPPER case) or underscore\n      (b) cannot start with numbers, space or other symbols"
                        vFlag=1
                        break
                    m = re.findall('[^A-Za-z0-9._]',val)
                    if len(m)>0:
                        getLinePos(val)
                        output=output+"\n> Value for 'namespace' \n      (a) can contain alphanumerics (lower/UPPER case)\n      (b) can contain underscore or period\n      (c) cannot contain space or other symbols"
                        vFlag=1
                        break

                    if val == "":
                        output=output+"\n> Missing 'namespace' value"
                        vFlag=1
                        break
                elif key == 'type':

                    temp = str(val)
                    #print(temp)
                    #print('\n\n')

                    if val == "record":
                        if 'name' not in x.keys() or 'fields' not in x.keys():
                            
                            vFlag=1
                            test = '"'+str('type')+'":'+'"'+str(x['type'])+'"'
                            test_data = data.replace(' ','')
                            test_data = test_data.replace(test,'~')
                            
                            counter = 1
                            pos_counter  = 1
                            linenos=""
                            
                            for p in test_data:
                                    
                                    pos_counter+=1
                                    if p == '\n':
                                        counter += 1
                                        pos_counter =1
                                    elif p == '%':
                                        pos_counter +=1
                                    elif p == '~':
                                        linenos = linenos+str(counter)+","
                            output=output+"\n> Missing attribute in record. Please re-check nested schema loops for 'name' and 'fields' definitions at line numbers: "+str(linenos[:-1])
                            break
                            
                            
                    elif val == "array":
                        if 'items' not in x.keys():
                            vFlag=1
                            test = '"'+str('type')+'":'+'"'+str(x['type'])+'"'
                            test_data = data.replace(' ','')
                            test_data = test_data.replace(test,'~')
                        
                            counter = 1
                            pos_counter  = 1
                            linenos=""
                            
                            for p in test_data:
                                    
                                    pos_counter+=1
                                    if p == '\n':
                                        counter += 1
                                        pos_counter =1
                                    elif p == '%':
                                        pos_counter +=1
                                    elif p == '~':
                                        linenos = linenos+str(counter)+","
                            output=output+"\n> Missing attribute in array. Please re-check nested schema loops for 'items' definitions at line numbers: "+str(linenos[:-1])
                            break
                            
                            
                    elif val == "enum":
                        if 'name' not in x.keys() or 'type' not in x.keys() or 'symbols' not in x.keys():
                            vFlag=1
                            test = '"'+str('type')+'":'+'"'+str(x['type'])+'"'
                            test_data = data.replace(' ','')
                            test_data = test_data.replace(test,'~')
                        
                            counter = 1
                            pos_counter  = 1
                            linenos=""
                            
                            for p in test_data:
                                    
                                    pos_counter+=1
                                    if p == '\n':
                                        counter += 1
                                        pos_counter =1
                                    elif p == '%':
                                        pos_counter +=1
                                    elif p == '~':
                                        linenos = linenos+str(counter)+","
                            output=output+"\n> Missing attribute in enum. Please re-check nested schema loops for 'name', 'type' and 'symbols' definitions at line numbers: "+str(linenos[:-1])
                            break

                    elif val == "":
                        output=output+"\n> Missing 'type' value, please recheck type definitions."
                        vFlag=1
                        break
                      
                    elif temp[0]=='[':
                        #print(temp[0])
                        
                        if isinstance(val,list):
                            
                            #print(val)
                            for element in val:
                                if isinstance(element,dict):
                                    #print(element)
                                    checkValues(element)
                                    
                                elif len(val)==1:
                                    getLinePos(val[0])
                                    output=output+"\n> Single type element cannot be enclosed in square brackets, use [] only for multiple type values."
                                    vFlag=1
                                    break
                                elif element not in type_space:
                                    getLinePos(element)
                                    output=output+"\n> Unknown type specified, please recheck type definitions."
                                    vFlag=1
                                    break
                                    
                                elif isinstance(element,list):
                                    getLinePos(element[0])
                                    output=output+"\n> Type value cannot be a nested list."
                                    vFlag=1
                                    break
                                else:
                                    if element not in type_space:
                                        getLinePos(element)
                                        output=output+"\n> Unknown type specified, please recheck type definitions."
                                        vFlag=1
                                        break
                                    elif element == "":
                                        output=output+"\n> Missing type value, please recheck type definitions."
                                        vFlag=1
                                        break
        
                            if len(val)==0:
                                getLinePos(temp)
                                output=output+"\n> Missing type value, please recheck type definitions."
                                vFlag=1
                                break  
                            break
                        
                        elif len(re.findall('^[^a-z]',val))>0:
                            #print(val,'else')
                            getLinePos(val)
                            output=output+"\n> Invalid character in type value, please recheck type definitions."
                            vFlag=1
                            break
                            
                        
                    elif temp[0]=='{':
                        
                        if isinstance(val,dict):
                            #print(val)
                            #print('\n\n')
                            checkValues(val)
                        elif len(re.findall('^[^a-z]',val))>0:
                            getLinePos(val)
                            output=output+"\n> Invalid character in Type value, please recheck type definitions."
                            vFlag=1
                            break
    
                    elif val not in type_space:
                        getLinePos(val)
                        output=output+"\n> Unknown type specified, please recheck type definitions."
                        vFlag=1
                        break

                        
                elif key == "fields":
                    if isinstance(val,list):
                        for element in val:
                            if isinstance(element,dict):
                                checkValues(element)
                            else:
                                getLinePos(element)
                                output=output+"\n> Each field should be a JSON Object i.e. key-value pairs enclosed in {}"
                                vFlag=1
                                break
                        if len(val)==0:
                            output=output+"\n> Missing field value, please recheck field definitions."
                            vFlag=1    

                elif key == "default":
                    default_val = val
                    d_type = str(type(default_val))
                    d_type = d_type.split('\'')[1].split('\'')[0]
                    
                    if 'type' in x.keys():
                        type_val = x['type']
                        
                    if isinstance(type_val,list):
                        
                        for element in type_val:    
                            if element == 'string' and d_type == 'str':
                                type_check_flag=1
                                break
                            elif element == 'int' and d_type == 'int':
                                type_check_flag=1
                                break
                            elif element == 'float' and d_type == 'float':
                                type_check_flag=1
                                break
                            elif element == 'long' and d_type == 'long':
                                type_check_flag=1
                                break
                            elif element == 'boolean' and d_type == 'bool':
                                type_check_flag=1
                                break
                            elif element == 'null' and d_type == 'NoneType':
                                type_check_flag=1
                                break
                            else:
                                type_check_flag=0

                                
                        if type_check_flag!=1:
                            
                            output=output+"\n> Default value specified does not match with above mentioned type definition. Please recheck 'default' value definitions."
                            vFlag=1
                            
                            
                    else:
                        
                        if type_val == 'string' and d_type == 'str':
                            type_check_flag=1
                            break
                        elif type_val == 'int' and d_type == 'int':
                            type_check_flag=1
                            break
                        elif type_val == 'float' and d_type == 'float':
                            type_check_flag=1
                            break
                        elif type_val == 'long' and d_type == 'long':
                            type_check_flag=1
                            break
                        elif type_val == 'boolean' and d_type == 'bool':
                            type_check_flag=1
                            break
                        elif type_val == 'null' and d_type == 'NoneType':
                            type_check_flag=1
                            break
                        else:
                            type_check_flag=0
                            
                        if type_check_flag!=1:    
                            output=output+"\n> Default value specified does not match with above mentioned type definition. Please recheck 'default' value definitions."
                            vFlag=1    
                        

                        
        ### Executing the checkKeys and checkValues fucntions ###                    
        if Flag1==1:
            
            checkKeys(x)
            if kFlag!=1:
                checkValues(x)
                if vFlag!=1:
                    output=output+"\n> No errors found while validating syntax rules in schema."
                    nFlag=1
        elif Flag2==1:
            
            checkKeys(out)
            if kFlag!=1:
                checkValues(out)
                if vFlag!=1:
                    output=output+"\n> No errors found while validating syntax rules in schema."
                    nFlag=1
            

        self.output_screen.SetValue(output)
        
        if nFlag==1:
            output=output+"\n\n Validation complete. The input Avro schema is correct !!!"
            if(sregistry == 1):
                self.button_pushSchema.Enable()
            self.output_screen.SetValue(output)
            dlg = wx.MessageDialog(self, 'No error found in Schema Validation. Do you want to save the final schema?','Avro Schema Designer', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
            val = dlg.ShowModal()
            dlg.Show()
            if val == wx.ID_OK:
                self.saveDialog()



      
####################################
                
# About window of tool                
class Myapp2 ( vali_UI.aboutFrame1 ):

    #Intiating UI window
    def __init__(self, parent):
        vali_UI.aboutFrame1.__init__(self,parent, title='About Validator',pos=(200,200), size=(300,400))

    # Functionality for Help button
    def openHelp(self,event):
        app = wx.App(False)
        frame = Myapp3(None)
        frame.Show(True)
        app.MainLoop()

    # Functionality for Close button
    def onClose(self, event):
        self.Close()



####################################
        
# Help window of tool
class Myapp3 ( vali_UI.helpFrame1 ):

    #Intiating UI window
    def __init__(self, parent):
        vali_UI.helpFrame1.__init__(self,parent, title='Schema Validator Help',pos=(200,200), size=(520,500))
        
        
####################################
        
# View Rules window of tool
class Myapp4 ( vali_UI.ruleFrame1 ):

    #Intiating UI window
    def __init__(self, parent):
        vali_UI.ruleFrame1.__init__(self,parent, title='Schema Validation Rules',pos=(200,300), size=(500,500))



####################################
        
# Start the main window of application  
    

        



        

