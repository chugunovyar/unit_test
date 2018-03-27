from api.models import ZayavkiCreditOrg
import json
import random


class SendZayavkaToCreditOrg(object):
    """
         !!! Заглушка !!!
         Отправка заявки на рассмотрение в кредитную организацию.
    """
    def __init__(self, zayavka_id=None):
        """
            Получаем id заявки
            Инициализируем начальные переменные.
        :param zayavka_id:
        """
        self.zayavka_id = json.loads(zayavka_id)
        try:
            self.zayavka = ZayavkiCreditOrg.objects.get(
                **self.zayavka_id
            )
            # Проставляем статус что заявка отправлена.
            self.zayavka.status = 'SENDED'
            self.zayavka.save()

        except Exception as err:
            raise err

    # def query(self):
    #     """
    #         Предполагается что кредитная организация проставляет статус.
    #         На самом деле проставляем статус рандомно, выбирая его из списка статусов.
    #     :return:
    #     """
    #     r_choise = ['ACCEPT', 'AGREE', 'CANCELED', 'ISSUED']
    #     status = random.choice(r_choise)
    #     # Предполагаем что банк рассмотрел заявку и проставляем рандомно статус у заявки.
    #     self.zayavka.status = status
    #     self.zayavka.save()
    #     return True