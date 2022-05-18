import hashlib
import json

from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transaction = []

        # Создание блока генезиса
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Создание нового блока в блокчейне

        :param proof: <int> Доказательства проведённой работы
        :param previous_hash: (Опционально) хеш предыдущего блока
        :return: <dict> Новый блок
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transaction,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # Перезагрузка текущего списка транзакций
        self.current_transaction = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Направляет новую транзакцию в следующий блок

        :param sender: <str> Адрес отправителя
        :param recipient: <str> Адрес получателя
        :param amount: <int> Сумма
        :return: <int> Индекс блока, который будет хранить транзакцию
        """

        self.current_transaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        """
        Проверка алгоритма:
        - Поиск числа p` такого, что hash(pp`) содержит 4 заглавных нуля, где p - предыдущий
        - p является предыдущим доказательством, а p` - новым

        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def hash(block):
        """
        Создаёт хеш SHA-256 блока

        :param block: <dict> Блок
        :return: <str>
        """
        # Мы должны убедиться в том, что словарь упорядочен, иначе у нас будут непоследовательные хеши
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Подтверждение доказательства: содержит ли hash(last_proof, proof) 4 заглавных нуля

        :param last_proof: <int> Предыдущее доказательство
        :param proof: <int> Текущее доказательство
        :return: <bool> True, если верно, False, если нет.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @property
    def last_block(self):
        return self.chain[-1]