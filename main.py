from abc import ABC, abstractmethod


class AnimalInterface:

    @abstractmethod
    def sound(self):
        pass

    @abstractmethod
    def feed(self):
        pass

    @abstractmethod
    def swim(self):
        pass


class Cat(Animal):

    def sound(self):
        pass

    def feed(self):
        pass

    def swim(self):
        print('swim')


class Dog(Animal):

    def sound(self):
        print('Hoof')

    def bite(self):
        print('Bite')


cat_1, cat_2 = Cat(), Cat()
dog_1, dog_2 = Dog(), Dog()

print(calc(2, 56))
