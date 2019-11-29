#########################################################
# UI of N:1 Schema Designer   (validation section)      #
# Imports all wx libraries and creates GUI              #
#                                                       #
# Authors : Ajinkya                                     #
# Last Modified : 11/30/2018                            #
#########################################################

import wx
import wx.xrc
import wx.stc as stc
import wx.lib.scrolledpanel as scrolled
import json


############################
#  Setting up UI for Main Window of the tool
class MyFrame1 ( wx.Frame ):
    def __init__(self, parent, title, pos, size):
        
        wx.Frame.__init__(self,parent, title='N:1 Schema Designer 1.2.0',pos=(100,50), size=(620,775), style = wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)

        self.SetIcon(wx.Icon('Extras/logo.ico'))
               
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )

                
        # Define buttons on main window

        self.static_title = wx.StaticText(self, wx.ID_ANY, u"Enter Avro schema :",wx.DefaultPosition, wx.Size( 125,-1 ), 0)
        self.static_title.Wrap(-1)

        self.static_blank1 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString,wx.DefaultPosition, wx.Size( 233,-1 ), 0)
        self.static_blank1.Wrap( -1 )

        self.button_viewRules = wx.Button(self, wx.ID_ANY , u"View Rules" , wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
        self.button_about = wx.Button(self, wx.ID_ANY , u"About" , wx.DefaultPosition, wx.Size( 55,-1 ), 0 )
        

        self.button_restart = wx.Button(self, wx.ID_ANY , u"Restart" , wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.button_restart.Disable()

    # Add buttons to horizontal BoxSizer 
        hSizer1 = wx.BoxSizer( wx.HORIZONTAL )

        hSizer1.Add(self.static_title, 0 , wx.ALL| wx.TOP, 15)
        hSizer1.Add(self.static_blank1, 0 , wx.ALL,5)
        hSizer1.Add(self.button_about, 0 , wx.ALL,5)
        hSizer1.Add(self.button_viewRules, 0 , wx.ALL,5)
        hSizer1.Add(self.button_restart, 0 , wx.ALL,5)
        

        #Schema display text screen
        self.textBox_screen = stc.StyledTextCtrl(self,style=wx.TE_MULTILINE)        
        lines = self.textBox_screen.GetLineCount()
        width = self.textBox_screen.TextWidth(stc.STC_STYLE_LINENUMBER, "       "+str(lines))
        self.textBox_screen.SetMarginWidth(0, width)
        self.textBox_screen.SetFocus()
        


        #Define buttons below Schema display screen
        self.loadtype = wx.StaticText( self, wx.ID_ANY, u"Load from:", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
        self.loadtype.Wrap( -1 )
    #bSizer_data_type_1.Add( self.static_data_type, 0, wx.ALL, 5 )
        dropdown_loadSchemaChoices = [ u"Local", u"Schema Generator", u"Schema Registry"]
        self.button_loadFile = wx.ComboBox(self, -1, pos=wx.DefaultPosition, size=( 130,-1 ), choices=dropdown_loadSchemaChoices, style=wx.CB_READONLY)
        #self.button_loadFile = wx.Button(self, wx.ID_ANY , u"Load Schema",wx.DefaultPosition, wx.Size( 85,-1 ), 0 )
        
        #self.static_blank2 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString,wx.DefaultPosition, wx.Size( 315,-1 ), 0)
        #self.static_blank2.Wrap( -1 )

        fontDefault_id = wx.Font(8, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.static_title2 = wx.StaticText(self, wx.ID_ANY, u"",wx.DefaultPosition, wx.Size( 265,-1 ), 0)
        self.static_title2.Wrap(-1)
        self.static_title2.SetFont(fontDefault_id)
        
        self.button_valSynt = wx.Button(self, wx.ID_ANY , u"Validate Schema",wx.DefaultPosition, wx.Size( 100,-1 ), 0 )

        
    # Add buttons to horizontal BoxSizer 
        hSizer2 = wx.BoxSizer( wx.HORIZONTAL )
        hSizer2.Add(self.loadtype, 0 , wx.ALL,5)
        hSizer2.Add(self.button_loadFile, 0 , wx.ALL,5)
        hSizer2.Add(self.static_title2, 0 , wx.ALL,5)
        hSizer2.Add(self.button_valSynt, 0 , wx.ALL,5)

        dropdown_topicChoices = [ u"New subject"]
        
        #self.dropdown_topics = wx.ComboBox(panel, -1, "default value", (20, 20), (100, 20), dropdown_topicChoices, wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER)
        self.dropdown_topics = wx.ComboBox (self, -1,value = "Subject", pos=wx.DefaultPosition, size=( 120,-1 ), choices=dropdown_topicChoices, style=wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER)
        self.dropdown_topics.Disable()

        self.textBox_topic = wx.TextCtrl(self, wx.ID_ANY,"New subject name",style=wx.TE_LEFT )     
        self.textBox_topic.Disable()
        

        dropdown_versionChoices = [ u""]
        
        self.dropdown_versions = wx.ComboBox (self, -1,"Version", pos=wx.DefaultPosition, size=( 80,-1 ), choices=dropdown_versionChoices, style=wx.CB_DROPDOWN| wx.TE_PROCESS_ENTER)
        self.dropdown_versions.Disable()

        self.static_blank21 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString,wx.DefaultPosition, wx.Size( 75,-1 ), 0)
        self.static_blank21.Wrap( -1 )

        self.button_Delete = wx.Button(self, wx.ID_ANY , u"Delete",wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
        self.button_Delete.Disable()
        self.button_DeleteAll = wx.Button(self, wx.ID_ANY , u"Delete Subject",wx.DefaultPosition, wx.Size( 85,-1 ), 0 )
        self.button_DeleteAll.Disable()
        self.button_pushSchema = wx.Button(self, wx.ID_ANY , u"Push Schema",wx.DefaultPosition, wx.Size( 85,-1 ), 0 )
        self.button_pushSchema.Disable()


        hSizer21 = wx.BoxSizer( wx.HORIZONTAL )
        hSizer21.Add(self.dropdown_topics, 0 , wx.ALL| wx.TOP, 5)
        hSizer21.Add(self.dropdown_versions, 0 , wx.ALL| wx.TOP, 5)
        #hSizer21.Add(self.static_blank21, 0 , wx.ALL| wx.TOP, 5)
        hSizer21.Add(self.button_Delete, 0 , wx.ALL| wx.TOP, 5)
        hSizer21.Add(self.button_DeleteAll, 0 , wx.ALL| wx.TOP, 5)
        hSizer21.Add(self.textBox_topic, 0 , wx.ALL| wx.TOP, 5)
        hSizer21.Add(self.button_pushSchema, 0 , wx.ALL| wx.TOP, 5)   
        
    # Header for output display screen
        hSizer3 = wx.BoxSizer( wx.HORIZONTAL )
        self.static_outputTitle = wx.StaticText(self, wx.ID_ANY, u"Validation Report :",wx.DefaultPosition, wx.Size( 125,-1 ), 0)
        self.static_outputTitle.Wrap(-1)
        
        hSizer3.Add(self.static_outputTitle, 0 , wx.ALL| wx.TOP, 10)        

        #Output display text screen
        self.output_screen = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,style=wx.TE_MULTILINE|wx.TE_READONLY )     


        #Adding all elements to vertical BoxSizer bSizer1
        bSizer1.Add(hSizer1, 0, wx.ALL|wx.EXPAND)
        bSizer1.Add(self.textBox_screen, 3, wx.ALL|wx.EXPAND,10)
        bSizer1.Add(hSizer2, 0, wx.ALL|wx.EXPAND,5)
        bSizer1.Add(hSizer21, 0, wx.ALL|wx.EXPAND,5)
        bSizer1.Add(hSizer3, 0, wx.ALL|wx.EXPAND,5)
        bSizer1.Add(self.output_screen, 1, wx.ALL|wx.EXPAND,10)


        
        self.SetSizer(bSizer1)
        self.Layout()


        # Binding buttons to action events
        self.button_restart.Bind(wx.EVT_BUTTON,self.onrestart)
        self.button_Delete.Bind(wx.EVT_BUTTON,self.delete)
        self.button_DeleteAll.Bind(wx.EVT_BUTTON,self.deleteall)
        self.button_loadFile.Bind(wx.EVT_COMBOBOX,self.openDialog)
        self.dropdown_topics.Bind(wx.EVT_COMBOBOX,self.loadVersion)
        self.dropdown_versions.Bind(wx.EVT_COMBOBOX,self.fetchSchema)
        self.button_valSynt.Bind(wx.EVT_BUTTON,self.onValidate)
        self.button_about.Bind(wx.EVT_BUTTON,self.openAbout)
        self.button_viewRules.Bind(wx.EVT_BUTTON,self.openRules)
        self.button_pushSchema.Bind(wx.EVT_BUTTON,self.pushSchemaRegistry)
        

    def onrestart(self,event):
        event.Skip()
    def pushSchemaRegistry(self,event):
        event.Skip()
    def fetchSchema(self,event):
        event.Skip()
    def delete(self,event):
        event.Skip()
    def deleteall(self,event):
        event.Skip()
    def openDialog(self,event):
        event.Skip()
    def onValidate(self,event):
        event.Skip()
    def openAbout(self,event):
        event.Skip()
    def openRules(self,event):
        event.Skip()
    def loadVersion(self,event):
        event.Skip()
    


############################
#  Setting up UI for About Window of the tool
class aboutFrame1 ( wx.Frame ):
    
    def __init__(self, parent, title, pos, size):
        
        wx.Frame.__init__(self,parent, title='About',pos=(300,150), size=(300,400), style = wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)

        self.SetIcon(wx.Icon('Extras/logo.ico'))

        self.SetBackgroundColour('white')
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )  #1 vertical boxsizer
        
        str1 = "Avro Schema Validator"
        str2 = "Version 1.1\n\nAvro Schema validation tool with connection to Schema Registry developed on Python - 3.6\n\n"

        self.static_title = wx.StaticText(self, wx.ID_ANY, str1 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_desc = wx.StaticText(self, wx.ID_ANY, str2 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_desc.Wrap(280)
        
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.static_title.SetFont(font)
        self.static_title.SetForegroundColour((0,0,0))
        self.static_desc.SetForegroundColour((0,0,0))
        


        self.static_version = wx.StaticText(self, wx.ID_ANY, "\n\nRefer to 'Help' below for more details on the tool.\n\n",wx.DefaultPosition,wx.DefaultSize, style=wx.ALIGN_LEFT)
        self.static_version.SetForegroundColour((0,0,0))

        self.panel_2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

        

        #Define buttons 
        self.button_help = wx.Button(self, wx.ID_ANY , u"Help" , wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
        self.static_blank1 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString,wx.DefaultPosition, wx.Size( 80,-1 ), 0)
        self.static_blank1.Wrap( -1 )
        self.button_close = wx.Button(self, wx.ID_ANY , u"Close" , wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
        
        # Add buttons to horizontal BoxSizer
        hSizer1 = wx.BoxSizer( wx.HORIZONTAL )  
        hSizer1.Add(self.button_help, 0 , wx.ALL , 10)
        hSizer1.Add(self.static_blank1, 0 , wx.ALL , 10)
        hSizer1.Add(self.button_close, 0 , wx.ALL , 10)

        # Binding buttons to action events
        
        self.button_help.Bind(wx.EVT_BUTTON,self.openHelp)
        self.button_close.Bind(wx.EVT_BUTTON,self.onClose)

        #Adding all elements to vertical BoxSizer bSizer1
        bSizer1.Add(self.static_title, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_desc, 0 , wx.ALL , 10)
        bSizer1.Add(self.static_version, 0 , wx.ALL| wx.TOP , 10)
        bSizer1.Add(self.panel_2, 1, wx.ALL | wx.ALIGN_CENTER,5)
        bSizer1.Add(hSizer1, proportion=0, flag=wx.EXPAND|wx.ALL)        

        self.SetSizer(bSizer1)
        self.Layout()


############################
#  Setting up UI for Help Window of the tool
class helpFrame1 ( wx.Frame ):
    
    def __init__(self, parent, title, pos, size):
        wx.Frame.__init__(self,parent, title='Help',pos=(400,200), size=(520,500), style = wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)

        self.SetIcon(wx.Icon('Extras/logo.ico'))

        topPanel_h = scrolled.ScrolledPanel(self,-1, size=(480,480), pos=(0,28), style=wx.SIMPLE_BORDER)
        topPanel_h.SetupScrolling()

        self.SetBackgroundColour('white')

        fontHeading = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        fontSubheading = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        fontSubheading1 = wx.Font(11, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        fontSubheading2 = wx.Font(11, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
        fontDefault = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        fontDefault_h = wx.Font(11, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        fontDefault_i = wx.Font(10, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)

         
        self.static_title = wx.StaticText(topPanel_h, wx.ID_ANY, "Avro Schema Validator" , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_title.SetFont(fontHeading)
    

        help_content_1 = "Avro Schema Validator has the following features:\n\n* Coded in Python, using the wxpython GUI toolkit \n* Validates input Avro schemas (.avsc) based on general avro schema rules \n* The current version of the tool checks for formatting rules and syntax rules      (in that order)\n\n* Provision to upload schemas to Schema Registry after validation"
        self.static_content_1 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_1 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_1.SetFont(fontDefault)
        self.static_content_1.Wrap(440)

        disclaimer_content = "(Please see 'View Rules' for more details on rules being validated.)"
        self.static_disclaimer = wx.StaticText(topPanel_h, wx.ID_ANY, disclaimer_content , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_disclaimer.SetFont(fontDefault_i)
        self.static_disclaimer.Wrap(440)

        self.static_subtitle_1 = wx.StaticText(topPanel_h, wx.ID_ANY, "Navigating the tool" , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_subtitle_1.SetFont(fontSubheading)

        help_content_2 = " * The main window of the tool is divided into two parts: Schema Display panel \nand Validation Report panel"
        self.static_content_2 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_2 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_2.Wrap(500)
        self.static_content_2.SetFont(fontDefault)

        help_content_3 = " * The Schema Display panel enables user interaction such as add and edit an \ninput Avro schema (.avsc) file, and the Validation Report panel shows the output \nreport after validating the schema against the pre-defined rules"
        self.static_content_3 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_3 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_3.Wrap(500)
        self.static_content_3.SetFont(fontDefault)

        help_content_4 = " * There are four ways of giving input schema into the tool:\n    - Manual Input\n    The user can manually enter the Avro Schema by typing in the text window in        the Schema Display panel\n\n   - From local\n    The user can also load the Avro Schema from local file destination\n\n   - From Schema Generator\n    The user can load the schema that was just created using the Schema        Generator\n\n   - From Schema Registry\n    The user can also pull a schema that is present in the Schema Registry"
        self.static_content_4 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_4 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_4.Wrap(430)
        self.static_content_4.SetFont(fontDefault)

        help_content_5 = " * Line numbers have been provided on the left-hand side of the 'Schema Display' panel for ease of readability in case of a very long Schema input"
        self.static_content_5 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_5 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_5.Wrap(430)
        self.static_content_5.SetFont(fontDefault)

        help_content_6 = " * On loading the schema from file, the tool will automatically display the content from the Avro schema file onto the Schema Display panel. The user can also edit the schema before validation"
        self.static_content_6 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_6 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_6.Wrap(430)
        self.static_content_6.SetFont(fontDefault)

        help_content_7 = " * Click on the 'Validate Schema' button to validate the schema"
        self.static_content_7 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_7 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_7.Wrap(430)
        self.static_content_7.SetFont(fontDefault)

        help_content_8 = " * The tool takes the content on the 'Schema Display' panel as input for its Validate function  (refer below for more details) and checks against the pre-defined formatting and syntax checks"
        self.static_content_8 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_8 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_8.Wrap(430)
        self.static_content_8.SetFont(fontDefault)
        
        help_content_9 = " * The output of the validation is displayed in the Validation Report panel"
        self.static_content_9 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_9 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_9.Wrap(430)
        self.static_content_9.SetFont(fontDefault)

        help_content_10 = " * If the schema has no errors, the tool will automatically prompt the user to save the final schema. On clicking OK, the user can save the final schema at the desired file location"
        self.static_content_10 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_10 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_10.Wrap(420)
        self.static_content_10.SetFont(fontDefault)

        help_content_11 = " * There is also a provision to push the validated schema into the Schema Registry, by establishing a live real-time connection between the system and the Schema Registry"
        self.static_content_11 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_11 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_11.Wrap(430)
        self.static_content_11.SetFont(fontDefault)

        help_content_12 = " * Timeout functionality has been included that allows the system to attempt to connect to the Schema Registry for a time period of 5 seconds, after which a timeout error message pops up, indicating absence of connection to Schema Registry"
        self.static_content_12 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_12 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_12.Wrap(430)
        self.static_content_12.SetFont(fontDefault)

        self.static_subtitle_2 = wx.StaticText(topPanel_h, wx.ID_ANY, "  Schema Registry operations" , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_subtitle_2.SetFont(fontSubheading2)

        help_content_13 = "    a) Loading schema input from Schema Registry\n\n      * The 'Subject' dropdown lets the user to select the required schema from the list of Subjects in the Schema Registry, that requires validation\n\n      * The 'Version' dropdown lets you select the version of schema to be loaded"
        self.static_content_13 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_13 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_13.Wrap(430)
        self.static_content_13.SetFont(fontDefault)

        help_content_14 = "    b) Pushing to Schema Registry\n\n      * The 'Subject' dropdown lets the user to select the required Subject name to push the schema\n\n      * The user can also push the validated schema under a new Subject name by creating one. For this, select 'New Subject' in the dropdown list and type in the desired name in the adjacent text box\n\n      * For pushing the schema to Schema Registry, the tool automatically assigns it with corresponding version number (#1 if it is a New Subject)"
        self.static_content_14 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_14 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_14.Wrap(430)
        self.static_content_14.SetFont(fontDefault)

        help_content_15 = "    c) Deleting schema from Schema Registry\n\n      * In order to delete a particular version of a schema, select the corresponding Subject Name and Version and then click on 'Delete' button\n\n      * To delete the whole Subject (all the versions), select corresponding Subject Name and click on 'Delete Subject'"
        self.static_content_15 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_15 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_15.Wrap(430)
        self.static_content_15.SetFont(fontDefault)

        self.static_subtitle_3 = wx.StaticText(topPanel_h, wx.ID_ANY, "  Validate function" , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_subtitle_3.SetFont(fontSubheading2)

        help_content_16 = "      *  The tool first performs Formatting validation on the entire schema. If no errors are found in this stage, it proceeds on to perform Syntax validation.\n\n      *  In Syntax validation, the schema input is converted into python dictionary having key-value pairs.\n\n      *  The tool checks for syntax rules in the 'Keys' first and if no errors are found syntax rules for 'Values' are validated.\n\n      -  If error is found in any of the above-mentioned stages, the tool breaks from the validate function and displays error message in the Validation Report panel"
        self.static_content_16 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_16 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_16.Wrap(430)
        self.static_content_16.SetFont(fontDefault)

        self.static_subtitle_4 = wx.StaticText(topPanel_h, wx.ID_ANY, "  Other functionalities" , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_subtitle_4.SetFont(fontSubheading2)

        help_content_17 = " * The 'About' button on the main window provides a brief description of the tool functionality and the tool version. On clicking the 'Help' button in 'About' window, the user can see the whole functionality of the tool"
        self.static_content_17 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_17 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_17.Wrap(430)
        self.static_content_17.SetFont(fontDefault)

        help_content_18 = " * The 'View Rules' button on the main window gives an idea to the user on what rules are being checked in the backend by the Schema Validator"
        self.static_content_18 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_18 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_18.Wrap(430)
        self.static_content_18.SetFont(fontDefault)

        help_content_19 = " * The 'Restart' button facilitates clearing of the Schema Display panel, in order to load a new schema"
        self.static_content_19 = wx.StaticText(topPanel_h, wx.ID_ANY, help_content_19 , ( 125,-1 ),style=wx.ALIGN_LEFT)
        self.static_content_19.Wrap(430)
        self.static_content_19.SetFont(fontDefault)


        
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        #Adding all elements to vertical BoxSizer bSizer1
        bSizer1.Add(self.static_title, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_1, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_disclaimer, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_subtitle_1, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_2, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_3, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_4, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_5, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_6, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_7, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_8, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_9, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_10, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_11, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_12, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_subtitle_2, 0 , wx.ALL | wx.TOP , 5)
        bSizer1.Add(self.static_content_13, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_14, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_15, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_subtitle_3, 0 , wx.ALL | wx.TOP , 5)
        bSizer1.Add(self.static_content_16, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_subtitle_4, 0 , wx.ALL | wx.TOP , 5)
        bSizer1.Add(self.static_content_17, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_18, 0 , wx.ALL | wx.TOP , 10)
        bSizer1.Add(self.static_content_19, 0 , wx.ALL | wx.TOP , 10)
        
        topPanel_h.SetSizer(bSizer1)
        self.Layout()
        
    
############################
#  Setting up UI for View Rules Window of the tool
class ruleFrame1 ( wx.Frame):
    def __init__(self, parent, title, pos, size):
        wx.Frame.__init__(self,parent, title='Schema validation rules',pos=(400,200), size=(500,500), style = wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)

        self.SetIcon(wx.Icon('Extras/logo.ico'))

        topPanel = scrolled.ScrolledPanel(self,-1, size=(480,480), pos=(0,28))
        topPanel.SetupScrolling()
        
        self.SetBackgroundColour('white')

        fontHeading = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        fontSubheading = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        fontSubheading1 = wx.Font(11, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        fontDefault = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        
        
        
    #Define static texts to be displayed
        self.static_title = wx.StaticText(topPanel, wx.ID_ANY, u"\nRules for Avro Schema Validation" ,style=wx.ALIGN_LEFT)
        self.static_title.SetFont(fontHeading)
        
        self.static_desc = wx.StaticText(topPanel, wx.ID_ANY, u"The conditions specified below are checked by the tool for validating the Avro schema. The tool first checks for Formatting rules in the input schema and if no errors are found, it proceeds to check Syntax rules." ,style=wx.ALIGN_LEFT)
        self.static_desc.Wrap(440)

        self.static_subtitle1 = wx.StaticText(topPanel, wx.ID_ANY, u"Formatting rules" ,style=wx.ALIGN_LEFT)
        self.static_subtitle2 = wx.StaticText(topPanel, wx.ID_ANY, u"\nSchema Syntax rules" , style=wx.ALIGN_LEFT)
        
        self.static_subtitle1.SetFont(fontSubheading)
        self.static_subtitle2.SetFont(fontSubheading)

        self.static_fRule1 = wx.StaticText( topPanel, wx.ID_ANY, u"1. Data inside the schema should be in key/value pairs",style=wx.ALIGN_LEFT )
        self.static_fRule1.Wrap( 500 )
        self.static_fRule1.SetFont(fontDefault)
        
        self.static_fExample1 = wx.StaticText( topPanel, wx.ID_ANY, u'    Eg: key:value  ->   " namespace " : " alarms.avro" ',style=wx.ALIGN_LEFT)
        self.static_fExample1.Wrap( 500 )
        self.static_fExample1.SetFont(fontDefault)

        self.static_fRule2 = wx.StaticText( topPanel, wx.ID_ANY, u"2. Values in key-value pairs should be one of the following:\n    - string\n    - number\n    - object\n    - array\n    - boolean\n    - null\n    - Note: It cannot be a function, date or undefined" ,style=wx.ALIGN_LEFT)
        self.static_fRule2.Wrap( 500 )
        self.static_fRule2.SetFont(fontDefault)


        self.static_fRule3 = wx.StaticText( topPanel, wx.ID_ANY, u"3. Every key and value element should be enclosed in double quotes" ,style=wx.ALIGN_LEFT)
        self.static_fRule3.Wrap( 500 )
        self.static_fRule3.SetFont(fontDefault)
        
        self.static_fExample3 = wx.StaticText( topPanel, wx.ID_ANY, u'    Eg: "type", "record", "fields"' ,style=wx.ALIGN_LEFT)
        self.static_fExample3.Wrap(500)
        self.static_fExample3.SetFont(fontDefault)

        self.static_fRule4 = wx.StaticText( topPanel, wx.ID_ANY, u"4. Each element in the schema should be separated by comma",style=wx.ALIGN_LEFT )
        self.static_fRule4.Wrap(500)
        self.static_fRule4.SetFont(fontDefault)
        
        self.static_fExample4 = wx.StaticText( topPanel, wx.ID_ANY, u'    Eg: "namespace":"alarms. avro",\n    "type": "record",' ,style=wx.ALIGN_LEFT)
        self.static_fExample4.Wrap(500)
        self.static_fExample4.SetFont(fontDefault)

        self.static_fRule56 = wx.StaticText( topPanel, wx.ID_ANY, u"5. Objects in the schema should always be enclosed in curly braces\n\n6. Arrays in the schema should always be enclosed in square brackets" ,style=wx.ALIGN_LEFT)
        self.static_fRule56.Wrap( 500 )
        self.static_fRule56.SetFont(fontDefault)


        self.static_sRule1 = wx.StaticText( topPanel, wx.ID_ANY, u'1. The schema should start with specifying following elements:\n    - Name\n    - Namespace (optional)\n    - Type\n    - Fields',style=wx.ALIGN_LEFT )
        self.static_sRule1.Wrap( 500 )
        self.static_sRule1.SetFont(fontDefault)

        self.static_sRule2 = wx.StaticText( topPanel, wx.ID_ANY, u'2. Name element should\n    - Start with alphabets(lower or upper case) or underscore[A-Za-z_]\n    - Subsequently have only alphanumerics or underscore[A-Za-z0-9_]\n    - Cannot contain any symbol other than underscore',style=wx.ALIGN_LEFT )
        self.static_sRule2.Wrap( 500 )
        self.static_sRule2.SetFont(fontDefault)

        self.static_sRule3 = wx.StaticText( topPanel, wx.ID_ANY, u'3. Type element should have one of the following data-type values:\n    - null\n    - boolean\n    - int\n    - long\n    - float\n    - double\n    - string\n    - record\n    - enum\n    - array\n    - bytes',style=wx.ALIGN_LEFT )
        self.static_sRule3.Wrap( 500 )
        self.static_sRule3.SetFont(fontDefault)

        self.static_sRule4 = wx.StaticText( topPanel, wx.ID_ANY, u"4. Fields element should have the following attributes:\n    - 'name' specifying name of the column/field in schema\n    - 'type' specifying data-type of data in that field\n    - 'default' specifying default value for that field (optional)\n    - 'doc' describing the field for users (optional)",style=wx.ALIGN_LEFT )
        self.static_sRule4.Wrap( 500 )
        self.static_sRule4.SetFont(fontDefault)

        self.static_sRule5 = wx.StaticText( topPanel, wx.ID_ANY, u"5. Namespace should be\n    - Dot-separated sequence of names\n    - Start with alphabets (lower or upper case) or underscore[A-Za-z_]\n    - Subsequently have only alphanumerics or underscore [A-Za-z0-9_] \n    - Cannot contain any symbol other than underscore",style=wx.ALIGN_LEFT )
        self.static_sRule5.Wrap( 500 )
        self.static_sRule5.SetFont(fontDefault)

        self.static_subtitle21 = wx.StaticText(topPanel, wx.ID_ANY, u"\nData-type specific syntax rules" , style=wx.ALIGN_LEFT)
        self.static_subtitle21.SetFont(fontSubheading)
        self.static_sRule5.Wrap( 440 )

        self.static_sRule6 = wx.StaticText( topPanel, wx.ID_ANY, u'1. If datatype specified in type field is "record" (in case of nested schemas), it should contain following attributes:\n    - name\n    - fields\n    - namespace, aliases, doc (optional)',style=wx.ALIGN_LEFT )
        self.static_sRule6.Wrap( 440 )
        self.static_sRule6.SetFont(fontDefault)

        self.static_fExample6 = wx.StaticText( topPanel, wx.ID_ANY, u'    Eg: {\n          "type": "record",\n          "name": "LongList",\n          "aliases": ["LinkedLongs"],\n          "fields" : [\n           {"name": "value", "type": "long"},\n                   {"name": "next", "type": ["null", "LongList"]}\n           ]\n          }',style=wx.ALIGN_LEFT)
        self.static_fExample6.Wrap( 500 )
        self.static_fExample6.SetFont(fontDefault)

        self.static_sRule7 = wx.StaticText( topPanel, wx.ID_ANY, u'2. If datatype specified in type field is "enum", it should contain following attributes:\n    - name\n    - symbols',style=wx.ALIGN_LEFT )
        self.static_sRule7.Wrap( 420 )
        self.static_sRule7.SetFont(fontDefault)

        self.static_fExample7 = wx.StaticText( topPanel, wx.ID_ANY, u'    Eg: {\n         "type": "enum",\n          "name": "Suit",\n          "symbols" : ["SPADES", "HEARTS", "DIAMONDS", "CLUBS"]\n           }',style=wx.ALIGN_LEFT)
        self.static_fExample7.Wrap( 500 )
        self.static_fExample7.SetFont(fontDefault)

        self.static_sRule8 = wx.StaticText( topPanel, wx.ID_ANY, u'3. If datatype specified in type field is "array", it should contain following attributes:\n    - items',style=wx.ALIGN_LEFT )
        self.static_sRule8.Wrap( 420 )
        self.static_sRule8.SetFont(fontDefault)

        self.static_fExample8 = wx.StaticText( topPanel, wx.ID_ANY, u'    Eg: {"type": "array", "items": "string"}',style=wx.ALIGN_LEFT)
        self.static_fExample8.Wrap( 500 )
        self.static_fExample8.SetFont(fontDefault)

        self.static_sRule9 = wx.StaticText( topPanel, wx.ID_ANY, u'4. If datatype specified in type field is "map", it should contain following attributes:\n    - values',style=wx.ALIGN_LEFT )
        self.static_sRule9.Wrap( 420 )
        self.static_sRule9.SetFont(fontDefault)

        self.static_fExample9 = wx.StaticText( topPanel, wx.ID_ANY, u'    Eg: {"type": "map", "values": "long"}',style=wx.ALIGN_LEFT)
        self.static_fExample9.Wrap( 500 )
        self.static_fExample9.SetFont(fontDefault)

        

        #Adding all elements to vertical BoxSizer bSizer1
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL ) 

        bSizer1.Add(self.static_title, 0 , wx.ALL , 5)
        bSizer1.Add(self.static_desc, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_subtitle1, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_fRule1, 0 , wx.ALL , 5)
        bSizer1.Add(self.static_fExample1, 0 , wx.ALL , 5)
        bSizer1.Add(self.static_fRule2, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_fRule3, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_fExample3, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_fRule4, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_fExample4, 0 , wx.ALL , 5)
        bSizer1.Add(self.static_fRule56, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_subtitle2, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_sRule1, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_sRule2, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_sRule3, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_sRule4, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_sRule5, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_subtitle21, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_sRule6, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_fExample6, 0 , wx.ALL , 5)
        bSizer1.Add(self.static_sRule7, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_fExample7, 0 , wx.ALL , 5)
        bSizer1.Add(self.static_sRule8, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_fExample8, 0 , wx.ALL , 5)
        bSizer1.Add(self.static_sRule9, 0 , wx.ALL  , 5)
        bSizer1.Add(self.static_fExample9, 0 , wx.ALL , 5)

        topPanel.SetSizer(bSizer1)
        #self.Layout()        



################################
