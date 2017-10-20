import getpass
import imaplib
from tkinter import filedialog,Tk,Button,Label
from tkinter.filedialog import askopenfilename



class ProcessRequest(object):
    fileName = None

    def startGUI(self):
        self._tk = Tk()
        chooseFile = Button(self._tk,text="choose file",command = self.getFile)
        processBtn = Button(self._tk,text="Process",command=self.process)
        chooseFile.pack()
        processBtn.pack()
        self._tk.mainloop()


    def getFile(self):
        self.fileName = askopenfilename()
        label = Label(self._tk,text="file name  : {0}".format(self.fileName))
        label.pack()
    def process(self):
        self.getDataAndGenerate(self.fileName)


    def getDataAndGenerate(self,path):
        try:
            readFile = None
            with open(path) as fp:
                readFile = fp.read()
                readFile = readFile.split("\n")

            if readFile:
                mainList = ""
                for values in readFile:
                    values = values.split(",")
                    host = values[0]
                    port = values[1]
                    user = values[2]
                    password = values[3]
                    if int(port) ==993:
                        mail = imaplib.IMAP4_SSL(host,port)
                    elif int(port) ==143:
                        mail = imaplib.IMAP4(host, port)
                    address = user
                    print (address)
                    mypassword = password
                    # mypassword = getpass.getpass("Password: ")
                    mail.login(address, mypassword)
                    mail.select("inbox")
                    # print("Checking for new e-mails for ", address, ".", sep='')
                    typ, messageIDs = mail.search(None, "ALL")
                    messageIDsString = str(messageIDs[0], encoding='utf8')
                    listOfSplitStrings = messageIDsString.split(" ")
                    print("user %s has %s emails"%(values,len(listOfSplitStrings)))
                    if mainList:
                        mainList = "%s\n%s,%s"%(mainList,values,len(listOfSplitStrings))
                    else:
                        mainList = "%s,%s"%(values,len(listOfSplitStrings))
                with open("newCsv.csv","wb") as f:
                    f.write(bytes(mainList,"UTF-8"))
        except Exception as e:
            print (str(e))



if __name__=="__main__":
    proCls = ProcessRequest()
    proCls.startGUI()
