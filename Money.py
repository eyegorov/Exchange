from Currency_data_source import web_site, cache_file, currencies


class Money:
    """
    Класс Wallet описывает электронный кошелек для фиатных денег;
    Для класса реализован метод для операции сложения - добавление валют на текущий баланс кошелька, __add__();
    Для класса реализован метод для операции вычитания - уменьшает текущий баланс кошелька, __sub__();
    Для класса реализован метод для операции умножения - умножает текущий баланс кошелька на число, __mul__();
    Для класса реализован метод для операции деления - делит текущий баланс кошелька на число, __truediv__();
    Для класса реализован метод для операции сравнения "меньше"- сравнивает текущий баланс, __lt__();
    Для класса реализован метод для операции сравнения "меньше или равно"- сравнивает текущий баланс,__le__();
    Для класса реализован метод для операции сравнения "больше"- сравнивает текущий баланс, __gt__();
    Для класса реализован метод для операции сравнения "больше или равно"- сравнивает текущий баланс,__ge__()

    Для класса реализован метод конвертации RUB в USD  convert_to_usd()."""

    def __init__(self, current_balance: (int, float), initial_currency: str):
        self.current_balance = current_balance
        self.initial_currency = initial_currency
        self.current_date = None

    """
        Создание экземпляра класса Money
        :param self.current_balance: Параметр отражает текущий баланс кошелька
        :param initial_currency: Наименование исходной валюты в виде кода в соответствии со стандартом ISO 4217
        """

    def __str__(self):
        return f"{self.current_balance} {self.initial_currency}"

    def __repr__(self):
        return f" На Вашем {self.__class__.__name__} баланс ({self.current_balance}, {self.initial_currency} RUB)"

    def __add__(self, add_money_to_wallet: "Money"):

        """ Метод операции сложения - добавление валюты к текущему балансу кошелька"""
        if isinstance(add_money_to_wallet, Money):
            if self.initial_currency == add_money_to_wallet.initial_currency:
                return Money(self.current_balance + add_money_to_wallet.current_balance, self.initial_currency)
            else:
                raise ValueError(f"К сожалению, данная валюта пока не поддерживается вашим {self.__class__.__name__},"
                                 f" снять деньги только в {self.__class__.__name__} RUB")

    def __sub__(self, withdraw_money_to_wallet: "Money"):
        """ Метод операции вычитания - изменения баланса кошелька """
        if isinstance(withdraw_money_to_wallet, Money):
            if self.initial_currency == withdraw_money_to_wallet.initial_currency:
                return Money(self.current_balance - withdraw_money_to_wallet.current_balance, self.initial_currency)
            else:
                raise ValueError(f"К сожалению, данная валюта пока не поддерживается вашим {self.__class__.__name__},"
                                 f" вы можете добавить в {self.__class__.__name__} RUB")

    def __mul__(self, factor: int):
        """ Метод умножения на число """
        if isinstance(factor, (int, float)):
            return Money(self.current_balance * factor, self.initial_currency)

    def __truediv__(self, division: int):
        """ Метод деления на число"""
        if isinstance(division, (int, float)):
            return Money(self.current_balance // division, self.initial_currency)

    def __lt__(self, other: "Money"):
        if isinstance(other, Money):
            if self.self.initial_currency == other.initial_currency:
                return self.current_balance < other.current_balance
            else:
                raise TypeError("Неверная операция,проверьте вводимые данные")

    def __le__(self, other: "Money"):
        """ Метод сравнения "меньше или равно" """
        if isinstance(other, Money):
            if self.self.initial_currency == other.initial_currency:
                return self.current_balance <= other.current_balance
            else:
                raise TypeError("Неверная операция,проверьте вводимые данные")

    def __gt__(self, other: "Money"):
        """ Метод сравнения "больше" """
        if isinstance(other, Money):
            if self.self.initial_currency == other.initial_currency:
                return self.current_balance > other.current_balance
            else:
                raise TypeError("Неверная операция,проверьте вводимые данные")

    def __ge__(self, other: "Money"):
        """Метод сравнения "больше или равно" """
        if isinstance(other, Money):
            if self.self.initial_currency == other.initial_currency:
                return self.current_balance >= other.current_balance
            else:
                raise TypeError("Неверная операция,проверьте вводимые данные")

    def __eq__(self, other: "Money"):
        if isinstance(other, Money):
            if self.self.initial_currency == other.initial_currency:
                return self.current_balance == other.current_balance
            else:
                raise TypeError("Неверная операция,проверьте вводимые данные")

    @classmethod
    def convert_to_usd(cls, obj: "Money", exchange='USD'):
        """Метод класса, который конвертируем рубли в доллары США по текущему курсу ЦБ РФ
        или по последнему сохраненному курсу при отсутствии интернета (см. cache_file.json)"""

        convert = cache_file['Valute']['USD']['Value']

        return cls(obj.current_balance / convert, exchange)

    @classmethod
    def convert_to_valute(cls, obj: "Money", exchange: str):

        """ Метод класса, который конвертирует рубли, а также любую валюту из списка exchange.json в
        другую валюту из списка exchange.json по текущему курсу ЦБ РФ или по последнему сохраненному курсу
    при отсутствии интернета (см. file.json)"""

        if exchange != 'RUR' and exchange not in currencies().keys():
            raise TypeError
        # конвертируем рубли
        if obj.initial_currency == 'RUR':
            cur = cache_file(web_site)['Valute'][exchange]['Value']
            nom = cache_file(web_site)['Valute'][exchange]['Nominal']
            return cls(obj.current_balance / (cur / nom), exchange)
            # конвертируем валюту, отличную от рублей
        else:
            # конвертируем в рубли
            cur_rur = cache_file(web_site)['Valute'][obj.initial_currency]['Value']
            nom_rur = cache_file(web_site)['Valute'][obj.initial_currency]['Nominal']
            result_in_rur = cls(obj.current_balance / nom_rur * cur_rur, 'RUR')
            if exchange == 'RUR':
                return result_in_rur
            # конвертируем в валюту, отличную от рублей
            else:
                cur = cache_file(web_site)['Valute'][exchange]['Value']
                num = cache_file(web_site)['Valute'][exchange]['Nominal']
            return cls(result_in_rur.current_balance / (cur / num), exchange)


if __name__ == '__main__':
    Wallet_1 = Money(100000, 'RUR')
    Wallet_2 = Money(24455.22, 'RUR')
    Wallet_3 = Money(100, 'USD')
    print(Wallet_1, Wallet_2, Wallet_3)

    # Проверка работы магических методов

    print(Wallet_1 - Wallet_2)
    print(Wallet_1 / 25)

    print(Wallet_1, Money.convert_to_usd(Wallet_2))
    print(Wallet_1, Money.convert_to_valute(Wallet_1, 'CAD'))
    # print(Wallet_3, Money.convert_to_valute(Wallet_3, 'KGS'))
