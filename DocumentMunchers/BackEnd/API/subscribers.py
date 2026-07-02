from __future__ import annotations
from datetime import datetime
import time


class Node:
    def __init__(self, data:tuple[str,float]):
        self.data = data
        self.child:Node = None
    def get_child(self):
        return self.child
    def set_child(self, node:Node):
        self.child = node
    def get_data(self):
        return self.data

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, d1:str, d2:float):
        node = Node((d1,d2))
        if self.is_empty():
            self.head = node
            self.tail = node
        else:
            self.tail.set_child(node)
            self.tail = node
    def pop(self) -> tuple[str, float]:
        if self.is_empty():
            raise Exception("Queue empty!")

        val = self.head.get_data()

        if self.head.get_child() == None:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.get_child()
        return val

    def is_empty(self):
        return self.head == None


class BasicSubscriber:
    def __init__(self):
        self.update_queue = Queue()
    def update(self, update_message:str):
        self.update_queue.append(update_message, time.time())
    def get_oldest_update(self, with_timestamp=True):
        if self.update_queue.is_empty():
            raise Exception("No Messages!")
        
        msg, t = self.update_queue.pop()
        if(with_timestamp):
            return f"{datetime.fromtimestamp(round(t))} - {msg}"
        else:
            return msg
    def has_update(self):
        return not self.update_queue.is_empty()

    
    