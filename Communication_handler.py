from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class Caller:
    name: str

class CommunicationException(Exception):
    def __init__(self, message):
        super().__init__(message)

class CommsHandlerABC(ABC):
    @abstractmethod
    def connect(self, user1: Caller, user2: Caller) -> str:
        """Implement connect method"""

    @abstractmethod
    def hangup(self, user1: Caller, user2: Caller) -> str:
        """Implement hangup method"""

    @abstractmethod
    def clear_all(self) -> None:
        """Implement clear_all"""

class CommsHandler(CommsHandlerABC):
    def __init__(self):
        self.connected_users = set()

    def connect(self, user1: Caller, user2: Caller) -> str:
        if user1 == user2:
            raise CommunicationException(f"{user1.name} não pode se comunicar com {user2.name}")

        if (user1, user2) in self.connected_users or (user2, user1) in self.connected_users:
            raise CommunicationException("Conexão em uso. Por favor tente novamente mais tarde.")

        self.connected_users.add((user1, user2))
        return f"Conexão estabelecida entre {user1.name} e {user2.name}"

    def hangup(self, user1: Caller, user2: Caller) -> str:
        if user1 == user2:
            raise CommunicationException(f"{user1.name} não consegue hangup com {user2.name}")

        if (user1, user2) in self.connected_users:
            self.connected_users.remove((user1, user2))
            return f"{user1.name} e {user2.name} estão desconectados"
        elif (user2, user1) in self.connected_users:
            self.connected_users.remove((user2, user1))
            return f"{user1.name} e {user2.name} estão desconectados"
        else:
            raise CommunicationException(f"{user1.name} e {user2.name} não se encontram no canal de comunicação")

    def clear_all(self) -> None:
        self.connected_users.clear()

# Exemplo de uso
user1 = Caller("Camila")
user2 = Caller("Mateus")

handler = CommsHandler()

try:
    print(handler.connect(user1, user2))
except CommunicationException as e:
    print(f"Erro: {e}")

try:
    print(handler.hangup(user1, user2))
except CommunicationException as e:
    print(f"Erro: {e}")

handler.clear_all()
