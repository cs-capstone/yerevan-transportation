class Queue:
    def __init__(self):
        self.__size = 0
        self.__data = []

    def __len__(self):
        return self.__size

    def enqueue(self, item):
        self.__data.append(item)
        self.__size += 1

    def dequeue(self):
        item = self.__data.pop(0)
        self.__size -= 1
        return item

    def first(self):
        return self.__data[0]

    def is_empty(self):
        return self.__size == 0
