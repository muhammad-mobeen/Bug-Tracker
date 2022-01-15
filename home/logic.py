class Node:
  def __init__(self, id, priority):
    self.id = id
    self.priority = priority
    self.next = None

class LinkedList:
  def __init__(self):
    self.head = None
    self.tail = None

  def size(self):  #Returns number of nodes. Note: Counting starts from 1.
    temp = self.head
    i = 1
    while not (temp.next == None):
      temp = temp.next
      i += 1
    return i

  def show(self):  #Print whole Linked List along with it's index number
    temp = self.head
    i = 0
    print("")
    while True:  #Performs While-do functions
      if temp.next == None:
        print("node#{} ID:{} Priority:{}".format(i, temp.id, temp.priority))
        break
      else:
        print("node#{} ID:{} Priority:{}".format(i, temp.id, temp.priority))
        temp = temp.next
        i += 1
    print("")

  def push(self, id, priority):  #Pushes new nodes from Head side
    new_node = Node(id, priority)
    if self.head == None:
      self.head = new_node
      self.tail = new_node
    else:
      new_node.next = self.head
      self.head = new_node

  def append(self, id, priority):  #Appends new nodes from Tail side
    new_node = Node(id, priority)
    temp = self.head
    if self.head == None:
      self.head = new_node
      self.tail = new_node
    else:
      while(temp):
        if temp.next == None:
          temp.next = new_node
          self.tail = new_node
          break
        temp = temp.next
  
  def appendAfter(self, node, id, priority):  #Appends after a specific node/index number
    new_node = Node(id, priority)
    temp = self.head
    i = 0
    while True:
      if i == node:
        new_node.next = temp.next
        temp.next = new_node
        if new_node.next == None:
          self.tail = new_node
        break
      else:
        temp = temp.next
        i += 1

  #If an argument is passed then this functions pops out the specific position
  #Otherwise it removes the most recent node (tail node) by default
  def pop(self, position = None):
    if position is None:
      position = self.size()-1
    temp = self.head
    i = 0
    while True:
      if i+1 == position:
        temp.next = temp.next.next
        if temp.next is None:
          self.tail = temp
        break
      else:
        i += 1
        temp = temp.next

  def popLeft(self):  #Pops out the node from Head side
    self.head = self.head.next


class MergeSort:
  def __init__(self, llist):
    llist.head = self.mergeSort(llist.head)
    return None
  
  def getMiddle(self, head):
    if head is None:
      return head
    slow = head
    fast = head
    while fast.next is not None and fast.next.next is not None:
      slow = slow.next
      fast = fast.next.next
    return slow


  def sortedMerge(self, a, b):
    #Base Case
    if a is None:
      return b
    if b is None:
      return a

    result = None

    if a.priority <= b.priority:
      result = a
      result.next = self.sortedMerge(a.next, b)
    else:
      result = b
      result.next = self.sortedMerge(a, b.next)
    return result


  def mergeSort(self, h):
    if h is None or h.next is None:
      return h
    
    middle = self.getMiddle(h)
    nextomiddle = middle.next

    middle.next = None

    left = self.mergeSort(h)
    right = self.mergeSort(nextomiddle)

    sortedlist = self.sortedMerge(left, right)
    return sortedlist