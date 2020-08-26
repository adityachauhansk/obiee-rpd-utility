
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import requests
import json

window = Tk()
selected = IntVar()

#logo=PhotoImage(file="name.gif") 
    
# titlebar and window settings 
window.title("OBI 12C RPD Utility")
window.geometry('650x500')
window.configure(background='white')

# logo and placement
Label(window, image=logo, bg='white').grid(row=0,column=0)
Label(window, bg='white' ).grid(row=1,column=0)
Label(window, text="   OBI 12C RPD UPLOAD AND DOWNLOAD UTILITY", bg='WHITE', font=('Helvetica', 16, 'bold') ).grid(row=2,column=0)
Label(window, bg='white' ).grid(row=3,column=0)
# radio buttons for upload/download
Label(window, text="Select RPD Operation", bg='white', font=('Helvetica', 12, 'bold') ).grid(row=4,column=0)
rad1=Radiobutton(window,text='RPD UPLOAD', bg='white', font=('Helvetica', 12), value=1, variable=selected)
rad2=Radiobutton(window,text='RPD DOWNLOAD', bg='white',font=('Helvetica', 12), value=2, variable=selected)
rad1.grid(row=5, column=0)
rad2.grid(row=6, column=0)

Label(window, bg='white' ).grid(row=7,column=0)
Label(window, text="Enter OBI Credentials", bg='white', font=('Helvetica', 12, 'bold') ).grid(row=8,column=0)

# text box and entry for target host
Label(window, text="Target Hostname", bg='WHITE',font=('Helvetica', 12) ).grid(row=9,column=0)
hostEntry= Entry(window, width=20, bg='WHITE')
hostEntry.grid(row=9, column=1, sticky=W)

# text box and entry for username and password
Label(window, text="OBI Username", bg='WHITE',font=('Helvetica', 12) ).grid(row=10,column=0)
userEntry= Entry(window, width=20, bg='WHITE')
userEntry.grid(row=10, column=1, sticky=W)

Label(window, text="OBI Password", bg='WHITE',font=('Helvetica', 12) ).grid(row=11,column=0)
passEntry= Entry(window, width=20, show="*", bg='WHITE')
passEntry.grid(row=11, column=1, sticky=W)

# text box and entry for rpd password
Label(window, text="RPD Password", bg='WHITE',font=('Helvetica', 12) ).grid(row=12,column=0)
rpdEntry= Entry(window, width=20, show="*", bg='WHITE')
rpdEntry.grid(row=12, column=1, sticky=W)

# on click function

def clicked():
    rpdFunction=selected.get()
    hostName=hostEntry.get()
    userName=userEntry.get()
    userPass=passEntry.get()
    rpdPass=rpdEntry.get()
    #print(rpdFunction,hostName,userName,userPass,rpdPass)
    
    if rpdFunction ==2:
        #print('Download RPD')
        #messagebox.showinfo("OBI RPD Utility","RPD Download in Progress")

        # replace xxxx.xxx:0000 with appropriate domain and port
        urlDown = "http://" + hostName + ".xxxx.xxx:0000/bi-lcm/v1/si/ssi/rpd/downloadrpd"
        messagebox.showinfo("OBI RPD Utility","Please note that the utility may become unresponsive during download, click OK to continue")
        rpdFilename = filedialog.asksaveasfilename(title = "Select FILE NAME FOR DOWNLOAD", defaultextension=".rpd", confirmoverwrite=False, 
                                                   filetypes = (("RPD files","*.rpd"),("all files","*.*")))
        if not rpdFilename:
            messagebox.showinfo("OBI RPD Utility","File name was not given, download process cancelled!")
            return
        req = requests.post(urlDown, data = {'target-password':rpdPass}, auth=(userName, userPass))
        #req.raise_for_status()
        open(rpdFilename, 'wb').write(req.content)
        messagebox.showinfo("OBI RPD Utility","RPD Download Completed Successfully")
        return
    else: 
        #print('Upload RPD')

        # replace xxxx.xxx:0000 with appropriate domain and port

        urlUp = "http://" + hostName + ".xxxx.xxx:0000/bi-lcm/v1/si/ssi/rpd/uploadrpd"
        messagebox.showinfo("OBI RPD Utility","Please note that the utility may become unresponsive during upload, click OK to continue")
        uprpdFilename = filedialog.askopenfilename(title = "Select RPD File FOR UPLOAD", 
                                                 filetypes = (("RPD files","*.rpd"),("all files","*.*")))
        if not uprpdFilename:
            messagebox.showinfo("OBI RPD Utility","No file was not selected, upload process cancelled!")
            return
        files = {'file': open(uprpdFilename, 'rb')}
        values = {'type':'application/vnd.oracle.rpd', 'rpd-password':rpdPass }
        response = requests.post(urlUp, files=files, data=values, auth=(userName, userPass))
        if not response.text:
            messagebox.showinfo("OBI RPD Utility", 'There was an error processing your request, please check your credentials')
        json_data = json.loads(response.text)
        rpdMssg = json_data['properties']['entry'][1]['value']['value']
        #print(json_date)
        messagebox.showinfo("OBI RPD Utility", rpdMssg)
        return
        

# submit button and action
Button(window, text='Submit', width=13, font=('Helvetica', 12), command=clicked).grid(row=13,column=1)

window.mainloop()

