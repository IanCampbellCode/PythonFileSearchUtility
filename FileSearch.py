import mmap
import multiprocessing
import os
import Queue

def search_file(key,in_queue, out_queue):
   while not in_queue.empty():
      current = in_queue.get()
      
      with open(current) as f:
         if os.stat(current).st_size != 0:
            s = mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
            if s.find(key) != -1:
               out_queue.put(current)
               f.flush()
               f.close()

def main(): 
   manager = multiprocessing.Manager()

   directories = Queue.Queue()
   files = manager.Queue()
   target_files = manager.Queue()
   counter = 0
	
   pool = multiprocessing.Pool()
   
   
   directories.put(raw_input("Enter root directory:\n"))
   key = raw_input("Enter search term:\n")
	
   while not directories.empty():
      root = directories.get()
      for x in os.listdir(root):
         seekpath = os.path.join(root,x)
         if os.path.isfile(seekpath):
            files.put(seekpath)
            counter = counter+1
         elif os.path.isdir(seekpath):
            directories.put(seekpath)
   
	
   print("Reading " + str(counter) + " files\n")
   
   pool.apply_async(search_file, (key,files,target_files,))
   
   pool.close()
   pool.join()
   
   
   
   if target_files.empty():
      print("no results found\n")
   else:
      while not target_files.empty():
         print target_files.get()
		
   raw_input("end\n")
   
if __name__ == "__main__":
   main()