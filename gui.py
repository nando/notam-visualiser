import os
import os.path

import wx
import wx.richtext

import process


class NotamProcessor(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='NOTAM Processor')

        self.richTextCtrlSource = wx.richtext.RichTextCtrl(self, wx.ID_ANY, 'Paste HTML source here...')

        self.buttonOK = wx.Button(self, wx.ID_OK)
        buttonCancel = wx.Button(self, wx.ID_CANCEL)
        buttonHelp = wx.Button(self, wx.ID_HELP)

        subBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxSizer = wx.BoxSizer(wx.VERTICAL)

        subBoxSizer.Add(buttonCancel)
        subBoxSizer.Add(buttonHelp)
        subBoxSizer.Add(self.buttonOK)

        boxSizer.Add(self.richTextCtrlSource, 1, wx.EXPAND)
        boxSizer.Add(subBoxSizer, 0, wx.ALIGN_RIGHT)

        self.SetSizer(boxSizer)

        self.Bind(wx.richtext.EVT_RICHTEXT_CONTENT_INSERTED, self.OnPaste, self.richTextCtrlSource)
        self.Bind(wx.richtext.EVT_RICHTEXT_CONTENT_DELETED, self.OnPaste, self.richTextCtrlSource)

        self.Bind(wx.EVT_BUTTON, self.OnOK, self.buttonOK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, buttonCancel)
        self.Bind(wx.EVT_BUTTON, self.OnHelp, buttonHelp)

        self.buttonOK.Disable()
        self.Maximize()
        self.Show()


    def OnPaste(self, event):
        if process.validate(self.richTextCtrlSource.GetValue()):
            self.buttonOK.Enable()
        else:
            self.buttonOK.Disable()


    def OnCancel(self, event):
        self.Destroy()


    def OnHelp(self, event):
        stringMessage = 'Copy and paste the entire HTML source of the web page containing the NOTAMs onto the text field.\n\nThis program only works with Mozilla Firefox.'

        messageDialog = wx.MessageDialog(self, stringMessage, 'Help', wx.OK | wx.ICON_INFORMATION)

        messageDialog.ShowModal()
        messageDialog.Destroy()


    def OnOK(self, event):
        singleChoiceList = process.extract(self.richTextCtrlSource.GetValue())

        if singleChoiceList:
            singleChoiceDialog = wx.SingleChoiceDialog(self, 'Select a NOTAM to process:', 'NOTAM Selection', singleChoiceList)

            if os.name == 'posix':
                singleChoiceDialog.Maximize()

            if singleChoiceDialog.ShowModal() == wx.ID_OK:
                self.informationList = [singleChoiceDialog.GetStringSelection()]
                singleChoiceDialog.Destroy()

                informationDialog = InformationDialog(self.informationList)

        else:
            stringMessage = 'ERROR: Cannot read source. An incorrectly formatted NOTAM is detected.'

            messageDialog = wx.MessageDialog(self, stringMessage, 'Error', wx.OK | wx.ICON_EXCLAMATION)

            messageDialog.ShowModal()
            messageDialog.Destroy()


class InformationDialog(wx.Frame):

    def __init__(self, informationList):
        self.informationList = informationList

        wx.Frame.__init__(self, None, wx.ID_ANY, title='Document and Placemark Information')

        staticTextDocumentName = wx.StaticText(self, wx.ID_ANY, 'Document name:')
        staticTextDocumentDescription = wx.StaticText(self, wx.ID_ANY, 'Document description:')
        staticTextPlacemarkName = wx.StaticText(self, wx.ID_ANY, 'Placemark name:')
        staticTextPlacemarkDescription = wx.StaticText(self, wx.ID_ANY, 'Placemark description:')

        size = wx.Size(self.GetSize().GetWidth() - staticTextDocumentName.GetSize().GetWidth(), -1)

        self.textCtrlDocument = wx.TextCtrl(self, wx.ID_ANY, size=size)
        self.textCtrlPlacemark = wx.TextCtrl(self, wx.ID_ANY, size=size)
        self.textCtrlMultiDocument = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE)
        self.textCtrlMultiPlacemark = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE)

        buttonCancel = wx.Button(self, wx.ID_CANCEL)
        buttonHelp = wx.Button(self, wx.ID_HELP)
        buttonOK = wx.Button(self, wx.ID_OK)

        subBoxSizer0 = wx.BoxSizer(wx.HORIZONTAL)
        subBoxSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        subBoxSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        boxSizer = wx.BoxSizer(wx.VERTICAL)

        subBoxSizer0.Add(staticTextDocumentName)
        subBoxSizer0.Add(self.textCtrlDocument)

        subBoxSizer1.Add(staticTextPlacemarkName)
        subBoxSizer1.Add(self.textCtrlPlacemark)

        subBoxSizer2.Add(buttonCancel)
        subBoxSizer2.Add(buttonHelp)
        subBoxSizer2.Add(buttonOK)

        boxSizer.Add(subBoxSizer0)
        boxSizer.Add(staticTextDocumentDescription)
        boxSizer.Add(self.textCtrlMultiDocument, 1, wx.EXPAND)

        boxSizer.Add(subBoxSizer1)
        boxSizer.Add(staticTextPlacemarkDescription)
        boxSizer.Add(self.textCtrlMultiPlacemark, 1, wx.EXPAND)

        boxSizer.Add(subBoxSizer2, 0, wx.ALIGN_RIGHT)

        self.SetSizer(boxSizer)

        self.Bind(wx.EVT_BUTTON, self.OnCancel, buttonCancel)
        self.Bind(wx.EVT_BUTTON, self.OnHelp, buttonHelp)
        self.Bind(wx.EVT_BUTTON, self.OnOK, buttonOK)

        self.Center()
        self.Show()


    def OnCancel(self, event):
        self.Close()


    def OnHelp(self, event):
        stringMessage = 'Enter the Document and Placemark names and descriptions you want in the correct text fields.'

        messageDialog = wx.MessageDialog(self, stringMessage, 'Help', wx.OK | wx.ICON_INFORMATION)

        messageDialog.ShowModal()
        messageDialog.Destroy()


    def OnOK(self, event):
        self.informationList.append(self.textCtrlDocument.GetValue())
        self.informationList.append(self.textCtrlMultiDocument.GetValue())
        self.informationList.append(self.textCtrlPlacemark.GetValue())
        self.informationList.append(self.textCtrlMultiPlacemark.GetValue())

        saveFileDialog = wx.FileDialog(None, 'Save File Dialog', 'C:\\', 'unnamed', '*.kml', wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_CHANGE_DIR)

        if saveFileDialog.ShowModal() == wx.ID_OK:
            if os.name == 'posix':
                fullPath = process.name(saveFileDialog.GetPath(), saveFileDialog.GetWildcard())
            elif os.name == 'nt':
                fullPath = saveFileDialog.GetPath()

            saveFileDialog.Destroy()

            self.informationList.append(fullPath)
            process.generate(self.informationList)

            progressDialog = wx.ProgressDialog('Progress', 'Processing. Please wait...', 100, style=(wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_SMOOTH))

            for progress in range(100):
                progressDialog.Update(progress + 1)

            progressDialog.Destroy()

            confirmationDialog = ConfirmationDialog(fullPath)

        self.Destroy()


class ConfirmationDialog(wx.Dialog):

    def __init__(self, fullPath):
        self.fullPath = fullPath

        wx.Dialog.__init__(self, None, wx.ID_ANY, 'Confirmation')

        staticTextConfirmation = wx.StaticText(self, wx.ID_ANY, 'Processing finished.')

        self.checkBoxView = wx.CheckBox(self, wx.ID_ANY, 'View KML')
        self.checkBoxRun = wx.CheckBox(self, wx.ID_ANY, 'Run Google Earth')

        buttonHelp = wx.Button(self, wx.ID_HELP)
        buttonOK = wx.Button(self, wx.ID_OK)

        subBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxSizer = wx.BoxSizer(wx.VERTICAL)

        subBoxSizer.Add(buttonHelp)
        subBoxSizer.Add(buttonOK)

        boxSizer.Add(staticTextConfirmation, 0, wx.ALIGN_CENTER)
        boxSizer.Add(self.checkBoxView)
        boxSizer.Add(self.checkBoxRun)
        boxSizer.Add(subBoxSizer, 0, wx.ALIGN_RIGHT)

        self.SetSizer(boxSizer)
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.OnHelp, buttonHelp)
        self.Bind(wx.EVT_BUTTON, self.OnOK, buttonOK)

        self.Center()
        self.Show()


    def OnHelp(self, event):
        stringMessage = 'Tick the correct checkboxes to indicate whether you want to view the generated KML file and/or open it in Google Earth.\n\nFor Windows users: If you choose both options, then you must first close the KML view before the system can run Google Earth.'

        messageDialog = wx.MessageDialog(self, stringMessage, 'Help', wx.OK | wx.ICON_INFORMATION)

        messageDialog.ShowModal()


    def OnOK(self, event):
        if self.checkBoxView.GetValue():
            if os.name == 'posix':
                os.system('kate ' + self.fullPath)
            elif os.name == 'nt':
                os.system('notepad.exe ' + self.fullPath)

        if self.checkBoxRun.GetValue():
            if os.name == 'posix':
                os.system('googleearth ' + self.fullPath)
            elif os.name == 'nt':
                filePath = 'C:\\Program Files\\Google\\Google Earth\\client\\googleearth.exe'
                commandPath = 'C:\\"Program Files"\Google\\"Google Earth"\\client\googleearth.exe'

                if os.path.exists(filePath):
                    os.system(commandPath + ' ' + process.normalize(self.fullPath))
                else:
                    stringMessage = 'Google Earth installation not found (C:\Program Files\...).\n\nThe program will now close.'

                    messageDialog = wx.MessageDialog(None, stringMessage, 'Error', wx.ICON_EXCLAMATION)

                    messageDialog.ShowModal()
                    messageDialog.Destroy()

        self.Destroy()
