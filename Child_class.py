"""Родительский класс для валюты фунт стерлингов GBR"""

from Currency_data_source import cache_file, web_site
from Money import Money


class GBR(Money):
    """Класс, описывающий валюту - фунт стерлингов GBR"""

    def gbr_to_usd(self):
        """Метод, выполняющий конвертацию GBR в USD по курсу ЦБ РФ
        или по последнему сохраненному курсу при отсутствии интернета (см. file.json)
        """

        cur = cache_file(web_site)["Valute"]["GBR"]["Value"]
        nom = cache_file(web_site)['Valute']['GBR']['Nominal']
        return Money(self.current_balance / cur * nom, 'USD')


if __name__ == '__main__':
    Wallet_4 = GBR(1000, 'GBR')
    Wallet_5 = Wallet_4.gbr_to_usd()
    print(Wallet_4)
    # print(Wallet_5)
