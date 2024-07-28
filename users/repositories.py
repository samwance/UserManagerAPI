import os
from abc import ABC, abstractmethod
from .models import User


class BaseRepository(ABC):
    """
    Абстрактный базовый класс для репозитория пользователей.
    Определяет основные операции CRUD, которые должны быть реализованы в подклассах.
    """

    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def update(self, id, data):
        pass

    @abstractmethod
    def delete(self, id):
        pass


class ORMRepository(BaseRepository):
    """
    Реализация репозитория пользователей с использованием ORM.
    """

    def create(self, full_name):
        user = User.objects.create(full_name=full_name)
        return user

    def update(self, user_id, full_name):
        user = User.objects.get(id=user_id)
        user.full_name = full_name
        user.save()
        return user

    def get(self, user_id):
        return User.objects.get(id=user_id)

    def delete(self, user_id):
        user = User.objects.get(id=user_id)
        user.delete()

    def list(self):
        return User.objects.all()


class InMemoryRepository(BaseRepository):
    """
    Реализация репозитория пользователей с использованием хранения данных в памяти.
    """

    def __init__(self):
        self.users = {}
        self.counter = 0

    def create(self, full_name):
        user_id = self.counter
        self.users[user_id] = {"id": user_id, "full_name": full_name}
        self.counter += 1
        return self.users[user_id]

    def update(self, user_id, full_name):
        user_id = int(user_id)
        if user_id in self.users:
            self.users[user_id]["full_name"] = full_name
            return self.users[user_id]
        raise KeyError(f"User with id {user_id} not found")

    def get(self, user_id):
        user_id = int(user_id)
        if user_id in self.users:
            return self.users[user_id]
        raise KeyError(f"User with id {user_id} not found")

    def delete(self, user_id):
        user_id = int(user_id)
        if user_id in self.users:
            del self.users[user_id]
        else:
            raise KeyError(f"User with id {user_id} not found")

    def list(self):
        return list(self.users.values())


def get_repository():
    """
    Возвращает репозиторий в зависимости от переменной окружения REPOSITORY_TYPE.
    :return: Экземпляр репозитория (InMemoryRepository или ORMRepository).
    :raises ValueError: Если указано неизвестное значение переменной окружения REPOSITORY_TYPE.
    """
    if os.getenv("REPOSITORY_TYPE") == "memory":
        return InMemoryRepository()
    elif os.getenv("REPOSITORY_TYPE") == "orm":
        return ORMRepository()
    else:
        raise ValueError("Unknown repository type")
