from threading import *
from random import randint
from time import sleep
from queue import Queue


class Table:
    def __init__(self, number, guest=None):
        self.number = number
        self.guest = guest


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        for guest in guests:
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    print(f'{table.guest.name} сел(-а) за стол номер {table.number}')
                    break
            else:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        t = [True if i.guest is not None else False for i in self.tables]
        while not self.queue.empty() or True in t:
            t.clear()
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)===============\n'
                          f'Стол номер {table.number} свободен')
                    table.guest = None
                if not self.queue.empty() and table.guest is None:
                    table.guest = self.queue.get()
                    print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    table.guest.start()
                if table.guest is not None:
                    t.append(True)
                else:
                    t.append(False)


# Создание столов
tables_in_cafe = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
list_guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables_in_cafe)
# Приём гостей
cafe.guest_arrival(*list_guests)
cafe.discuss_guests()
