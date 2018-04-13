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
