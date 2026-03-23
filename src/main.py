import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

#--------------------------------------------------DeleteTab_Functions--------------------------------------------------

def Delete_Words():
    delete_words = []
    for entry in (DeleteWords_Entry1, DeleteWords_Entry2, DeleteWords_Entry3):
        words = entry.get().strip()
        if words != "":
            delete_words.append(words)
    return delete_words

def Special_Symbols():
    special_symbols = []
    for symbols, boolean_variable in DeleteTab_SpecialSymbols_State.items():
        if boolean_variable.get() == True:
            special_symbols.append(symbols)
    return special_symbols

def Numbers():
    numbers = []
    for nums, boolean_variable in DeleteTab_Numbers_State.items():
        if boolean_variable.get() == True:
            numbers.append(nums)
    return numbers

def DeleteTab_SelectButton():
    DeleteTab_CurrentListbox.delete(0, tk.END)
    DeleteTab_RealPath.clear()
    if DeleteTab_Mode_Radiobutton.get() == 1:
        path = filedialog.askdirectory()
        if path == "":
            return
        for p in os.listdir(path):
            FullPath = os.path.join(path, p)
            if os.path.isfile(FullPath):
                DeleteTab_RealPath.append(FullPath)
                DeleteTab_CurrentListbox.insert(tk.END, p)
    elif DeleteTab_Mode_Radiobutton.get() == 2:
        files = filedialog.askopenfilenames()
        if files == ():
            return
        for f in files:
            DeleteTab_RealPath.append(f)
            DeleteTab_CurrentListbox.insert(tk.END, os.path.basename(f))
    else:
        messagebox.showerror("Error", "Please select a Mode")
        return
    DeleteTab_UpdatePreview()

def DeleteTab_UpdatePreview():
    DeleteTab_PreviewListbox.delete(0, tk.END)
    delete_words = Delete_Words()
    special_symbols = Special_Symbols()
    numbers = Numbers()
    for path in DeleteTab_RealPath:
        old_name = os.path.basename(path)
        new_name = Generate_New_Name(old_name, delete_words, special_symbols, numbers)
        DeleteTab_PreviewListbox.insert(tk.END, f"{new_name}")

def Generate_New_Name(old_name, delete_words, special_symbols, numbers):
    name, extension = os.path.splitext(old_name)
    for words in delete_words:
        if words.isalnum():
            name = name.replace(words, "")
    for symbol in special_symbols:
        name = name.replace(symbol, "")
    for nums in numbers:
        name = name.replace(nums, "")
    name = " ".join(name.split())
    return name + extension

def DeleteTab_StartButton():
    if DeleteTab_RealPath == []:
        messagebox.showerror("Error", "No Files Selected")
        return
    confirm = messagebox.askyesno("Confirm", "Start Batch Renaming?")
    if confirm:
        DeleteTab_BatchRename()

def DeleteTab_BatchRename():
    delete_words = Delete_Words()
    special_symbols = Special_Symbols()
    numbers = Numbers()
    for path in DeleteTab_RealPath:
        directory = os.path.dirname(path)
        old_name = os.path.basename(path)
        new_name = Generate_New_Name(old_name, delete_words, special_symbols, numbers)
        old_full_path = path
        new_full_path = os.path.join(directory, new_name)
        if old_full_path != new_full_path:
            os.rename(old_full_path, new_full_path)
    messagebox.showinfo("Completed", "Batch Renaming Finished")

#--------------------------------------------------AddTab_Functions--------------------------------------------------

def AddTab_SelectButton():
    AddTab_CurrentListbox.delete(0, tk.END)
    AddTab_RealPath.clear()
    if AddTab_Mode_Radiobutton.get() == 1:
        path = filedialog.askdirectory()
        if path == "":
            return
        for p in os.listdir(path):
            FullPath = os.path.join(path, p)
            if os.path.isfile(FullPath):
                AddTab_RealPath.append(FullPath)
                AddTab_CurrentListbox.insert(tk.END, p)
    elif AddTab_Mode_Radiobutton.get() == 2:
        files = filedialog.askopenfilenames()
        if files == ():
            return
        for f in files:
            AddTab_RealPath.append(f)
            AddTab_CurrentListbox.insert(tk.END, os.path.basename(f))
    else:
        messagebox.showerror("Error", "Please select a Mode")
        return
    AddTab_UpdatePreview()

def AddTab_UpdatePreview():
    AddTab_PreviewListbox.delete(0, tk.END)
    words = AddWords_Entry.get().strip()
    position = AddTab_AddWordsOptions_Radiobutton.get()
    space = AddTab_AddWordsOptions_Checkbutton.get()
    for path in AddTab_RealPath:
        old_name = os.path.basename(path)
        name, extension = os.path.splitext(old_name)
        if space == True:
            space_text = " "
        else:
            space_text = ""
        if words != "":
            if position == 1:
                new_name = words + space_text + name + extension
            else:
                new_name = name + space_text + words + extension
        else:
            new_name = old_name
        AddTab_PreviewListbox.insert(tk.END, new_name)

def AddTab_StartButton():
    if AddTab_RealPath == []:
        messagebox.showerror("Error", "No Files Selected")
        return
    confirm = messagebox.askyesno("Confirm", "Start Batch Renaming?")
    if confirm:
        AddTab_BatchRename()

def AddTab_BatchRename():
    words = AddWords_Entry.get().strip()
    position = AddTab_AddWordsOptions_Radiobutton.get()
    space = AddTab_AddWordsOptions_Checkbutton.get()
    for path in AddTab_RealPath:
        directory = os.path.dirname(path)
        old_name = os.path.basename(path)
        name, extension = os.path.splitext(old_name)
        if space == True:
            space_text = " "
        else:
            space_text = ""
        if position == 1:
            new_name = words + space_text + name + extension
        else:
            new_name = name + space_text + words + extension
        new_path = os.path.join(directory, new_name)
        if path != new_path:
            os.rename(path, new_path)
    messagebox.showinfo("Completed", "Batch Renaming Finished")

#--------------------------------------------------Global_Initializations--------------------------------------------------

# Root
root = tk.Tk()
root.title("Python-Batch-Rename-Tool")
root.geometry("760x540")

# Notebook
Notebook = ttk.Notebook(root)
Notebook.grid(row=0, column=0, sticky="nsew")

DeleteTab = ttk.Frame(Notebook)
Notebook.add(DeleteTab, text=" Delete ")

AddTab = ttk.Frame(Notebook)
Notebook.add(AddTab, text=" Add ")

# Tk Variables
DeleteTab_Mode_Radiobutton = tk.IntVar()
AddTab_Mode_Radiobutton = tk.IntVar()
AddTab_AddWordsOptions_Radiobutton = tk.IntVar()
AddTab_AddWordsOptions_Checkbutton = tk.BooleanVar()

# Global Variables
DeleteTab_RealPath = []
AddTab_RealPath = []
DeleteTab_SpecialSymbols = ["(", ")", "[", "]", "{", "}", "!", "@", "#", "$", "%", "^", "&", "-", "_", "=", "+", ",", ".", ";", "'", "~"]
DeleteTab_SpecialSymbols_State = {}
DeleteTab_Numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
DeleteTab_Numbers_State = {}

#--------------------------------------------------DeleteTab--------------------------------------------------

# CurrentFrame
DeleteTab_CurrentFrame = tk.LabelFrame(DeleteTab, text=" Current Select: ")
DeleteTab_CurrentFrame.grid(row=0, column=0, sticky="nsew")

DeleteTab_CurrentListbox = tk.Listbox(DeleteTab_CurrentFrame, width=50, height=25)
DeleteTab_CurrentListbox.grid()

# PreviewFrame
DeleteTab_PreviewFrame = tk.LabelFrame(DeleteTab, text = " Preview ")
DeleteTab_PreviewFrame.grid(row=0, column=1, sticky="nsew")

DeleteTab_PreviewListbox = tk.Listbox(DeleteTab_PreviewFrame, width=50, height=25)
DeleteTab_PreviewListbox.grid()

# ModeFrame
DeleteTab_ModeFrame = tk.LabelFrame(DeleteTab)
DeleteTab_ModeFrame.grid(row=0, column=2, pady=10, sticky="nsew")

tk.Radiobutton(DeleteTab_ModeFrame, text="Select a Single Folder", variable=DeleteTab_Mode_Radiobutton, value=1).grid()
tk.Radiobutton(DeleteTab_ModeFrame, text="Select Multiple Files", variable=DeleteTab_Mode_Radiobutton, value=2).grid()

tk.Button(DeleteTab_ModeFrame, text="Select", command=DeleteTab_SelectButton).grid()
tk.Button(DeleteTab_ModeFrame, text="Start", command=DeleteTab_StartButton).grid()

# DeleteWordsFrame
DeleteWordsFrame = tk.LabelFrame(DeleteTab, text=" Delete Words ")
DeleteWordsFrame.grid(row=1, column=0, sticky="nsew")

tk.Label(DeleteWordsFrame, text="Words 1:").grid(row=0, column=0)

DeleteWords_Entry1 = tk.Entry(DeleteWordsFrame)
DeleteWords_Entry1.grid(row=0, column=1)

tk.Label(DeleteWordsFrame, text="Words 2:").grid(row=1, column=0)

DeleteWords_Entry2 = tk.Entry(DeleteWordsFrame)
DeleteWords_Entry2.grid(row=1, column=1)

tk.Label(DeleteWordsFrame, text="Words 3:").grid(row=2, column=0)

DeleteWords_Entry3 = tk.Entry(DeleteWordsFrame)
DeleteWords_Entry3.grid(row=2, column=1)

DeleteWords_Entry1.bind("<KeyRelease>", lambda e: DeleteTab_UpdatePreview())
DeleteWords_Entry2.bind("<KeyRelease>", lambda e: DeleteTab_UpdatePreview())
DeleteWords_Entry3.bind("<KeyRelease>", lambda e: DeleteTab_UpdatePreview())

# SpecialSymbolsFrame
SpecialSymbolsFrame = tk.LabelFrame(DeleteTab, text=" Special Symbols ")
SpecialSymbolsFrame.grid(row=1, column=1, sticky="nsew")

for i, symbols in enumerate(DeleteTab_SpecialSymbols):
    DeleteTab_SpecialSymbols_Checkbutton = tk.BooleanVar()
    DeleteTab_SpecialSymbols_State[symbols] = DeleteTab_SpecialSymbols_Checkbutton
    tk.Checkbutton(SpecialSymbolsFrame, text=symbols, variable=DeleteTab_SpecialSymbols_Checkbutton, command=DeleteTab_UpdatePreview).grid(row=i//8, column=i%8)

# NumbersFrame
NumbersFrame = tk.LabelFrame(DeleteTab, text=" Numbers ")
NumbersFrame.grid(row=1, column=2, sticky="nsew")

for i, numbers in enumerate(DeleteTab_Numbers):
    DeleteTab_Numbers_Checkbutton = tk.BooleanVar()
    DeleteTab_Numbers_State[numbers] = DeleteTab_Numbers_Checkbutton
    tk.Checkbutton(NumbersFrame, text=numbers, variable=DeleteTab_Numbers_Checkbutton, command=DeleteTab_UpdatePreview).grid(row=i//4, column=i%4)

#--------------------------------------------------AddTab--------------------------------------------------

# CurrentFrame
AddTab_CurrentFrame = tk.LabelFrame(AddTab, text=" Current Select: ")
AddTab_CurrentFrame.grid(row=0, column=0, sticky="nsew")

AddTab_CurrentListbox= tk.Listbox(AddTab_CurrentFrame, width=50, height=25)
AddTab_CurrentListbox.grid()

# PreviewFrame
AddTab_PreviewFrame = tk.LabelFrame(AddTab, text = " Preview ")
AddTab_PreviewFrame.grid(row=0, column=1, sticky="nsew")

AddTab_PreviewListbox = tk.Listbox(AddTab_PreviewFrame, width=50, height=25)
AddTab_PreviewListbox.grid()

# ModeFrame
AddTab_ModeFrame = tk.LabelFrame(AddTab)
AddTab_ModeFrame.grid(row=0, column=2, pady=10, sticky="nsew")

tk.Radiobutton(AddTab_ModeFrame, text="Select a Single Folder", variable=AddTab_Mode_Radiobutton, value=1).grid()
tk.Radiobutton(AddTab_ModeFrame, text="Select Multiple Files", variable=AddTab_Mode_Radiobutton, value=2).grid()

tk.Button(AddTab_ModeFrame, text="Select", command=AddTab_SelectButton).grid()
tk.Button(AddTab_ModeFrame, text="Start", command=AddTab_StartButton).grid()

# AddWordsFrame
AddWordsFrame = tk.LabelFrame(AddTab, text=" Add Words ")
AddWordsFrame.grid(row=1, column=0, sticky="nsew")

tk.Label(AddWordsFrame, text="Words:").grid(row=0, column=0)

AddWords_Entry = tk.Entry(AddWordsFrame)
AddWords_Entry.grid(row=0, column=1)

AddWords_Entry.bind("<KeyRelease>", lambda e: AddTab_UpdatePreview())

# AddWordsOptionsFrame
AddWordsOptionsFrame = tk.LabelFrame(AddTab, text=" Add Words Options ")
AddWordsOptionsFrame.grid(row=1, column=1, sticky="nsew")

tk.Radiobutton(AddWordsOptionsFrame, text="Front", variable=AddTab_AddWordsOptions_Radiobutton, value=1, command=AddTab_UpdatePreview).grid()
tk.Radiobutton(AddWordsOptionsFrame, text="End", variable=AddTab_AddWordsOptions_Radiobutton, value=2, command=AddTab_UpdatePreview).grid()

tk.Checkbutton(AddWordsOptionsFrame, text="Add Space", variable=AddTab_AddWordsOptions_Checkbutton, command=AddTab_UpdatePreview).grid()
root.mainloop()