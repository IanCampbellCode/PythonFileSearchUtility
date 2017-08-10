import os
import Queue
import mmap

directories = Queue.Queue()
files = Queue.Queue()
target_files = Queue.Queue()
counter = 0

#Todo change this to prompt
directories.put(os.getcwd())
directories.put(raw_input("Enter root directory:\n"))

#Todo prompt for search term
#key = "@PropertyEditorRegistration(targetType = Schema.class)"
key = '@PropertyEditorRegistration(targetType = String[].class)'
key = raw_input("Enter search term:\n")

print("")

while not directories.empty():
        root = directories.get()
        for x in os.listdir(root):
            seekpath = os.path.join(root,x)
            if seekpath is "StringListEditor.java":
                print seekpath
            if os.path.isfile(seekpath):
                files.put(seekpath)
                counter = counter+1
            elif os.path.isdir(seekpath):
                directories.put(seekpath)

print("Reading " + str(counter) + " files\n")

while not files.empty():
    #try:
        #ToDo scan each file for key word
        counter = counter - 1
        if counter % 1000 == 0:
            print counter
        current = files.get()
        with open(current) as f:
            if os.stat(current).st_size != 0:
                s = mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
                if s.find(key) != -1:
                    target_files.put(current)
            f.flush()
            f.close()
    #except:
     #   pass
if target_files.empty():
    print("no results found\n")
else:
    while not target_files.empty():
        print target_files.get()
    
raw_input("end\n")
