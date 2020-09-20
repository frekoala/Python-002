from abc import ABCMeta, abstractmethod


class Animal(metaclass=ABCMeta):
    def __init__(self, animal_type, animal_shape, animal_character):
        self.animal_type = animal_type
        self.animal_shape = animal_shape
        self.animal_character = animal_character

    @property
    def is_feral_animal(self):
        animal_shape_weight = {'小': 1, '中等': 2, '大': 3}
        if animal_shape_weight[self.animal_shape] >= 2 and self.animal_type == '食肉' and self.animal_character == '凶猛':
            return True
        else:
            return False

    @abstractmethod
    def is_suitable_for_pets(self):
        pass


class Cat(Animal):
    _sound = '喵喵'

    def __init__(self, name, animal_type, animal_shape, animal_character):
        self.name = name
        super().__init__(animal_type, animal_shape, animal_character)

    @property
    def is_suitable_for_pets(self):
        if self.is_feral_animal:
            print("不适合作为宠物")
            return False
        else:
            print("适合作为宠物")
            return True


class Dog(Animal):
    _sound = '汪汪'

    def __init__(self, name, animal_type, animal_shape, animal_character):
        self.name = name
        super().__init__(animal_type, animal_shape, animal_character)

    @property
    def is_suitable_for_pets(self):
        if self.is_feral_animal:
            print("不适合作为宠物")
            return False
        else:
            print("适合作为宠物")
            return True


class Zoo(object):
    def __init__(self, name):
        self.name = name
        self.animal_dict = {}

    def add_animal(self, animal):
        if animal.__class__.__name__ in self.animal_dict.keys():
            print('该动物已存在')
        else:
            self.animal_dict[animal.__class__.__name__] = animal
            setattr(self, animal.__class__.__name__, animal)


if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    cat2 = Cat('大花猫 2', '食肉', '大', '凶猛')
    print(cat1.is_suitable_for_pets)
    print(cat2.is_suitable_for_pets)
    # 增加一只猫到动物园
    z.add_animal(cat1)
    z.add_animal(cat2)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')
    print(have_cat)
    print(cat1._sound)
    #动物类不能实例化
    # a = Animal('食肉', '小', '温顺')
