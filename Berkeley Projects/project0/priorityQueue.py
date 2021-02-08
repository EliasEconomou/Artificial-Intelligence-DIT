######################################################################################################
#########################    project0 - Ilias Oikonomou - 1115201200133    ###########################
import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = [] # pq implemented by heap
        self.count = 0 # counter of items in pq


###### helpful class functions ######
    
    #Searches the "items sublist" of the heap and finds current item if exists
    def is_duplicate(self,item):
        if item in (x for items in self.heap for x in items):
            return True
        return None

    #Finds and returns position of current item in heap
    def find_position(self,item):
        position=-1
        for x in self.heap:
            position +=1
            if x[1]==item:
                return position
        return None


##### exercise's class funtions #####
    
    #Inserts item with priority=priority in pq
    def push(self, item, priority):             
        if self.is_duplicate(item): #if 'is_duplicate==True' skip pushing the item and just return
            print("item %s already in pq - skipped" % item)
            return
        heapq.heappush(self.heap,[priority,item])   #push item with it's priority value in heap
        print("item %s - %d pushed in pq" % (item,priority)) 
        self.count += 1
        return
        
    #pops item with smallest priority in pq
    def pop(self):     
        if self.count == 0: #if list is empty return an observation
            return "trying to pop from empty pq"
        popped = heapq.heappop(self.heap)[1] #pop the item and decrease count by one
        self.count -= 1
        return popped

    #checks weather pq is empty
    def isEmpty(self):
        return self.count == 0

    #updates the priority of an item
    def update(self,item,priority):
        if self.is_duplicate(item): #if item is in heap
            position = self.find_position(item) #item's position
            if self.heap[position][0] > priority:   #if item has greater priority in heap,
                self.heap[position][0] = priority   #update
                print("updated the priority of %s to %d" % (item,self.heap[position][0]))
                heapq.heapify(self.heap)    #keep heap's property
            return
        else:   #if item not in heap push it
            self.push(item,priority)
            return

##### sort function #####

#sorts a list of integers using the PriorityQueue class
def PQSort(int_list):
    pqtemp = PriorityQueue()
    for integer in int_list:    #push all integers of the list to pqtemp
        pqtemp.push(integer,0)  #priority not needed
    x=0
    while pqtemp.isEmpty() == False:
        int_list[x] = pqtemp.pop()  #pop every integer and store in the right position
        x+=1                        #of the list, then return the list
    return int_list




##### test class functions #####

p = PriorityQueue()

print("pq is empty -> %s" %(p.isEmpty()))

p.push("task2",2)
p.push("task2",7)
p.push("task1",3)
p.push("task4",6)

print("pq is empty -> %s" %(p.isEmpty()))

p.update("task4",1)

print(p.pop())
print(p.pop())
print(p.pop())
print()
##### test PQsort #####

list_of_integers = [4, 5, 2, 6, 1, 3, 15, 11]
print(list_of_integers)
PQSort(list_of_integers)
print(list_of_integers)


######################################################################################################