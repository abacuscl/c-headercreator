import tkinter as tk
from tkinter import *
from tkinter import StringVar, filedialog, scrolledtext, messagebox
from pathlib import Path


CRT_ENABLED_TEXT = "Enabled: _CRT_SECURE_NO_WARNINGS"
CRT_DISABLED_TEXT = "Disabled: _CRT_SECURE_NO_WARNINGS"
CRT_TEXT = "#define _CRT_SECURE_NO_WARNINGS\n"
DEFAULT_TITLE = "Header Creator - No C File Opened"
SELECTED_FILE_TITLE = "Header Creator - "
HEADER_TOP = "#ifndef header_h\n#define header_h\n\n"
HEADER_BOTTOM = "\n#endif"
rootWindow = tk.Tk()
cFilePath = ""
savePath = ""
importsToWrite = ""
functionsToWrite = ""
crtEnabled = False
crtButtonText = StringVar()


#Main Function
#Updated: 12/7/21
def main():
    rootWindow.mainloop()


#Opens a filedialog to select a C file to open.
#C file is obtained as a pathlib Path.
#Updated: 12/7/21
def findCFile():
    global cFilePath
    
    cFilePath = Path(filedialog.askopenfilename(initialdir = "/",
                                                title = "Select the C File",
                                                filetypes = (("C files", "*.c*"), 
                                                             ("All files", "*.*"))))
    if not ".c" in cFilePath.name:
        messagebox.showerror("Error", 
                             "Invalid File Selection (Not .c File)")
    else:
        rootWindow.title(SELECTED_FILE_TITLE + str(cFilePath)) 
        readCFile() 


#Saves valid lines of code into a string.
#Import and function lines are separated and recombined later.
#Parameter: line (str), the line to check.
#Updated: 12/7/21
def formatLines(line):
    global importsToWrite
    global functionsToWrite
    
    #Save imports
    if "#" in line:
        importsToWrite += line
    
    #Save functions
    elif "(" and ")" in line and not ";" in line:
        
        #Formats the semicolon at the end of the line
        if not "\n" in line:
            functionsToWrite += (line + ";")
        else:
            functionsToWrite += line.replace("\n", ";\n")


#Opens the C file and saves valid lines using formatLines()
#Updated: 12/7/21
def readCFile():
    global cFilePath
    global editsTextbox
    global importsToWrite
    global functionsToWrite
    importsToWrite = ""
    functionsToWrite = ""
    
    try:
        with open(cFilePath) as f:
            lines = f.readlines()
        f.close()
        
        for _ in range(0, len(lines)):
            formatLines(lines[_])
    except Exception as _:
        messagebox.showerror("Error", 
                             "Unable to Read C File: " + str(_))
    
    editsTextbox.delete("1.0", END)
    editsTextbox.insert(INSERT, 
                        importsToWrite + "\n" + functionsToWrite)
    

#Writes the contents of the editsTextbox to the header.h file.
#Opens a filedialog to find the save path.
#Appends _CRT_SECURE_NO_WARNINGS to the top of the file if the option is enabled.
#Updated: 12/7/21
def writeToFile():
    global savePath
    
    savePath = filedialog.askdirectory(initialdir = cFilePath,
                                       title = "Select Directory to Save to")
    savePath = Path(savePath + "/header.h")
    
    try:
        f = open(savePath, 'w')
        
        if crtEnabled == True:
            f.write(CRT_TEXT
                    + HEADER_TOP 
                    + editsTextbox.get("1.0", END)
                    + HEADER_BOTTOM)
        else:
            f.write(HEADER_TOP 
                    + editsTextbox.get("1.0", END) 
                    + HEADER_BOTTOM)
        
        f.close()
        messagebox.showinfo("Success", 
                            "Successfully Generated Header File")
    except Exception as _:
        messagebox.showerror("Error", 
                             "Error Writing to Header File: " + str(_))

#Toggles the _CRT_SECURE_NO_WARNINGS button and text.
#Updated: 12/7/21
def toggleCRT():
    global crtEnabled
    
    if crtEnabled == True:
        crtEnabled = False
        crtButtonText.set(CRT_DISABLED_TEXT)
    else:
        crtEnabled = True
        crtButtonText.set(CRT_ENABLED_TEXT)


#tkinter UI Code
#Updated: 12/7/21

#Root window setup and configuration.
rootWindow.title(DEFAULT_TITLE)
rootWindow.geometry("800x450")
rootWindow.minsize(800, 450)
rootWindow.columnconfigure(0, weight = 1, minsize = 300)
rootWindow.columnconfigure(1, weight = 1, minsize = 300)
rootWindow.rowconfigure(0, weight = 1, minsize = 300)

#Button frame setup and configuration.
#buttonFrame is a slave to rootWindow.
buttonFrame = tk.Frame(master = rootWindow, 
                       borderwidth = 1)
buttonFrame.configure(background = "red4")
buttonFrame.grid(row = 0, 
                 column = 0, 
                 sticky = (N, S, E, W))

#Button that opens the file window to find a C file.
#Included in buttonFrame
getPathButton = tk.Button(buttonFrame, 
                          text = "Find C File", 
                          font = ("Helvetica", 20),
                          relief = FLAT, 
                          command = findCFile)
getPathButton.configure(background = "red4",
                        activebackground = "firebrick4", 
                        foreground = "white")
getPathButton.pack(expand = True, 
                   fill = BOTH)

#Button that refreshes the the contents of editsTextBox.
#Included in buttonFrame
refreshButton = tk.Button(buttonFrame, 
                          text = "Refresh File Contents", 
                          font = ("Helvetica", 20),
                          relief = FLAT, 
                          command = readCFile)
refreshButton.configure(background = "white",
                        activebackground = "grey91",
                        foreground = "black")
refreshButton.pack(expand = True, 
                   fill = BOTH)

#Button that exports the header.h file.
#Included in buttonFrame
exportButton = tk.Button(buttonFrame, 
                         text = "Export Header File",
                         font = ("Helvetica", 20),
                         relief = FLAT,
                         command = writeToFile)
exportButton.configure(background = "red4", 
                       activebackground = "firebrick4",
                       foreground = "white")
exportButton.pack(expand = True, 
                  fill = BOTH)

#Button that enables/disables _CRT_SECURE_NO_WARNINGS.
#Included in buttonFrame
crtButton = tk.Button(buttonFrame, 
                      textvariable = crtButtonText, 
                      font = ("Helvetica", 10),
                      relief = FLAT,
                      command = toggleCRT)
crtButton.configure(background = "white", 
                    activebackground = "grey91",
                    foreground = "black")
crtButtonText.set(CRT_DISABLED_TEXT)
crtButton.pack(expand = True, 
               fill = BOTH)

#Textbox frame setup and configuration.
#textboxFrame is a slave to rootWindow.
textboxFrame = tk.Frame(master = rootWindow, 
                        borderwidth = 1)
textboxFrame.configure(background = "red4")
textboxFrame.grid(row = 0, 
                  column = 1, 
                  sticky = (N, S, E,W))

#Scrollbar that scrolls editsTextbox along the x-axis.
#Included in textboxFrame
xScrollbar = Scrollbar(textboxFrame, 
                       orient = HORIZONTAL)
xScrollbar.pack(side = BOTTOM, 
                fill = X)

#Editable textbox that allows the user to alter the code before exporting.
#ScrolledText textbox, so it has a built-in y-axis scrollbar.
#Also contains the xview configuration for xScrollbar.
#Included in textboxFrame
editsTextbox = scrolledtext.ScrolledText(textboxFrame, 
                                         font = ("Helvetica", 10),
                                         wrap = NONE, 
                                         relief = FLAT, 
                                         xscrollcommand = xScrollbar.set)
editsTextbox.pack(fill = BOTH, 
                  expand = True)
xScrollbar.config(command = editsTextbox.xview)


#When this module is executed, run main()
if __name__ == "__main__":
    main()