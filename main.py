from abc import ABC, abstractmethod


class Storage(ABC):
    """
    абстрактный класс
    """

    @abstractmethod
    def add(self, title:str, quantity: int):
        pass

    @abstractmethod
    def remove(self, title:str, quantity: int):
        pass

    @property
    @abstractmethod
    def free_space(self):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @property
    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):
    """
    Класс склад, в нем храняться товары которые отправляются в магазин
    """

    def __init__(self, _capacity=11):
        self._store = {}
        self._capacity = _capacity

    def add(self, title: str, quantity: int):
        if quantity <= self.free_space:
            self._store[title] = self._store.get(title, 0) + quantity
            print(f'Товар {title} добавлен в магазин.')
        else:
            print(f'Не хватает места по продукту.')

    def remove(self, title: str, quantity: int):
        if self._store.get(title, 0) > 0:
            self._store[title] = self._store.get(title, 0) - quantity
            if self._store[title] == 0:
                self._store.pop(title, 0)
            print(f'Курьер забрал {quantity} {title} со склада.')

    @property
    def free_space(self) -> int:
        count = sum(self.get_items().values())
        return self._capacity - count

    @property
    def get_unique_items_count(self) -> int:
        return len(self._store)

    def get_items(self) -> dict:
        return self._store


class Shop(Store):
    """
        Класс магазин в нем хранятся, товары поступающие из склада
    """

    def __init__(self, _limit=5, _capacity=20):
        super().__init__(_capacity)
        self._limit = _limit

    # Добавляем геттер чтобы можно было просмотреть Limit из вне класса, но не изменить..
    @property
    def limit(self) -> int:
        return self._limit

    def add(self, title: str, quantity: int):
        if self.limit > self.get_unique_items_count:
            super().add(title, quantity)
        else:
            print('В магазин слишком много наименований!')


class Request:
    """Класс отвещающий за разбор строки, то есть запроса из склада в магазин"""

    def __init__(self, str_):
        words = Request.get_str_(str_)
        self.from_ = words[4]
        self.to = words[6]
        self.amount = words[1]
        self.product = words[2]

    @staticmethod
    def get_str_(str_) -> str:
        return str_.split(' ')

    # Добавляем геттер чтобы можно было просмотреть amount из вне класса, и сеттер чтобы изменить..
    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value)

    @property
    def from_(self):
        return self._from_

    @from_.setter
    def from_(self, value):
        self._from_ = value

    @property
    def to(self):
        return self._to

    @to.setter
    def to(self, value):
        self._to = value

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, value):
        self._product = value

    def __repr__(self):
        return f'Доставить {self._amount} {self._product}, из {self.from_} в {self.to}!'


if __name__ == '__main__':
    st_ = Store()
    shop = Shop()
    st_.add(title='пельмени', quantity=9)
    st_.add(title='печенья', quantity=10)
    st_.add(title='пельмени1', quantity=10)
    st_.add(title='пельмени2', quantity=10)
    st_.add(title='пельмени3', quantity=10)
    st_.add(title='пельмени4', quantity=10)
    st_.add(title='пельмени5', quantity=10)
    shop.add(title='печенья1', quantity=1)
    shop.add(title='печенья2', quantity=1)
    shop.add(title='печенья3', quantity=11)
    shop.add(title='печенья4', quantity=10)
    req_ = Request('Доставить 3 пельмени из склад в магазин')
    if st_.get_items().get(req_.product, 0) < req_.amount:
        print('Не хватает на складе, попробуйте заказать меньше или другой продукт!')
    else:
        print('Нужное количество есть на складе!')
        st_.remove(title=req_.product, quantity=req_.amount)
        print(f'Курьер везет {req_.amount} {req_.product} со склад в магазин.')
        shop.add(title=req_.product, quantity=req_.amount)
    print('В складе хранится:')
    print(f'{st_.get_items()}')
    print('В магазине хранится:')
    print(f'{shop.get_items()}')
