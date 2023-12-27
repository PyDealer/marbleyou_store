from django.core.mail import send_mail
import traceback
import logging
import os
from dotenv import load_dotenv

from .models import WorkPrice

load_dotenv()

logging.basicConfig(
        filename='service_log.log',
        level=logging.ERROR,
        encoding='utf-8',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

try:
    work_price_instance = WorkPrice.objects.get(id=1)
    CUT_PRICE = work_price_instance.cut
    EDGE_RICE = work_price_instance.edge
    AVERAGE_PRICE = work_price_instance.average
    HOB_PRICE = work_price_instance.hob
    SINK_PRICE = work_price_instance.sink
    TAP_PRICE = work_price_instance.tap
    DROPPER_PRICE = work_price_instance.dropper
except:
    CUT_PRICE = 700
    EDGE_RICE = 1300
    AVERAGE_PRICE = 13000
    HOB_PRICE = 4500
    SINK_PRICE = 4000
    TAP_PRICE = 1500
    DROPPER_PRICE = 900

SERVICE_EMAIL = os.getenv('SMTP')
ERROR_MESSAGE_FOR_USER = {
    'ERROR_CALCULATOR': 'Произошла ошибка в расчетах'}


class Calculator:
    def __init__(self, form_data):
        self.form_data = form_data
        self.length = self.form_data.cleaned_data['length']
        self.width = self.form_data.cleaned_data['width']
        self.thickness = self.form_data.cleaned_data['thickness']
        self.name = self.form_data.cleaned_data['name']
        self.email = self.form_data.cleaned_data['email']
        self.message = self.form_data.cleaned_data['message']
        self.hob = self.form_data.cleaned_data['hob']
        self.sink = self.form_data.cleaned_data['sink']
        self.tap = self.form_data.cleaned_data['tap']
        self.phone = self.form_data.cleaned_data['phone']
        self.category = self.form_data.cleaned_data['category']
        self.genus = self.form_data.cleaned_data['genus']
        self.url = ''
        self.title = ''
        self.calc_data = None

    def calculate_cut(self):
        '''Рассчет стоимости реза'''
        length = self.length*0.01 * 2
        width = self.width*0.01 * 2
        running_meter = length + width
        cost = running_meter * CUT_PRICE
        data = [round(running_meter, 1), int(cost)]
        return data

    def calculate_edge(self):
        '''Рассчет стоимости обработки кромки'''
        running_meter = self.length * 0.01
        cost = running_meter * EDGE_RICE
        data = [round(running_meter, 1), int(cost)]
        return data

    def calculate_array(self):
        '''Расчет площади материала'''
        array = (self.length * 0.01) * (self.width * 0.01)
        return round(array, 1)

    def add_data_to_db(self, field, attribute):
        '''Добавление дополнительных данных в бд'''
        setattr(self.calc_data, field, attribute)

    def response_processing(self, array, cut, edge):
        '''Формирование данных'''
        data = {}
        hob = 0
        sink = 0
        tap = 0
        dropper = 0
        cut_cost = cut[1]
        edge_cost = edge[1]
        cut_rm = cut[0]
        edge_rm = edge[0]
        material_cost = int(AVERAGE_PRICE*array)
        riser_array = self.length*0.01 * 0.13

        if str(self.category) == 'Плитка' or 'tile' in self.url:
            data['Площадь материала'] = [f'{array} м²', f'{material_cost/2} р.']
            if self.email or self.phone:
                self.sending_data(data)
            return data

        data['Площадь материала'] = [f'{array} м²', f'{material_cost} р.']
        self.add_data_to_db('array', array)
        if str(self.category) == 'Лестницы' or 'ladder' in self.url:
            cut_rm += self.length*0.01 * 2
            dropper = self.length * 0.01
            self.add_data_to_db('riser_array', riser_array)
            data['Площадь материала подступенка'] = [
                f'{riser_array} м²', f'{int(riser_array*AVERAGE_PRICE)} р.'
                ]
            self.add_data_to_db('dropper', dropper)
            data['Капельник'] = [
                f'{dropper} м/п', f'{int(dropper*DROPPER_PRICE)} р.']
        data['Рез камня'] = [f'{cut_rm} м/п', f'{cut_cost} р.']
        self.add_data_to_db('cut', cut_rm)
        data['Полировка кромки'] = [f'{edge_rm} м/п', f'{edge_cost} р.']
        self.add_data_to_db('edge', edge_rm)
        if self.hob:
            hob = HOB_PRICE
            data['Вырез под варочную панель'] = [1, f'{HOB_PRICE} р.']
            self.add_data_to_db('hob', True)
        if self.sink:
            sink = SINK_PRICE
            data['Вырез под раковину'] = [1, f'{SINK_PRICE} р.']
            self.add_data_to_db('sink', True)
        if self.tap:
            tap = TAP_PRICE
            data['Отверстие под кран'] = [1, f'{TAP_PRICE} р.']
            self.add_data_to_db('tap', True)
        final_price_production = cut_cost+edge_cost+hob+sink+tap+dropper
        final_price = final_price_production+material_cost
        data['Общая стоимость производства'] = [
            '', f'{int(final_price_production)} р.']
        self.add_data_to_db('final_price_production', final_price_production)
        data['Итоговая стоимость'] = ['', f'{int(final_price)} р.']
        self.add_data_to_db('final_price', final_price)
        if self.email or self.phone:
            try:
                self.sending_data(data)
            except Exception as e:
                error_traceback = traceback.format_exc()
                logger.exception(
                    f'Ошибка в функции send_mail: {e}\n\n{error_traceback}')
                send_mail(
                    subject=f'ERROR: {e}',
                    message=(
                        f'Ошибка при отправке сообщения: {e}\n\n{error_traceback}'),
                    from_email=SERVICE_EMAIL,
                    recipient_list=[SERVICE_EMAIL])
                return ERROR_MESSAGE_FOR_USER
        return data

    def sending_data(self, data):
        '''Отправка результатов расчета'''
        product = ''
        if self.title:
            product += f'{self.title}'
        elif self.category and self.genus:
            product += f'{self.category}. {self.genus}'
        elif self.category:
            product += f'{self.category}'
        elif self.genus:
            product += f'{self.genus}'
        else:
            product += 'Изделие из камня'
        self.add_data_to_db('product', product)
        message_data_for_company = f'''{product}
{self.length}x{self.width}x{self.thickness}
{self.name}
{self.email}
{self.phone}
{self.message}

'''
        message_data_for_user = f'''
Спасибо за проявленный интерес к нашей компании, в скором времени мы с вами свяжемся.

{product}
{self.length}x{self.width}x{self.thickness}
'''
        for key, values in data.items():
            count, cost = values
            message_data_for_company += f'{key} {count}: {cost}\n'
            message_data_for_user += f'{key} {count}: {cost}\n'
        self.add_data_to_db('general_info', message_data_for_company)
        self.calc_data.save()

        subject = f'Заявка от {self.email}. №{self.calc_data.id}'
        message = f'{message_data_for_company}'
        from_email = SERVICE_EMAIL
        recipient_list = [SERVICE_EMAIL]
        send_mail(subject, message, from_email, recipient_list)
        message_data_for_user += f'\nЗявка № {self.calc_data.id}'
        if self.email:
            send_mail(subject=f'Заявка на расчет. {product}.',
                      message=message_data_for_user,
                      from_email=from_email,
                      recipient_list=[f'{self.email}',])

    def main(self, url, form,  title=''):
        self.url = url
        self.title = title
        self.calc_data = form
        try:
            array = self.calculate_array()
            cut = self.calculate_cut()
            edge = self.calculate_edge()
            data = self.response_processing(array, cut, edge)
        except Exception as e:
            error_traceback = traceback.format_exc()
            logger.exception(
                f'{e}\n\n{error_traceback}')
            send_mail(
                subject=f'ERROR: {e}',
                message=(
                    f'Ошибка: {e}\n\n{error_traceback}'),
                from_email=SERVICE_EMAIL,
                recipient_list=[SERVICE_EMAIL])
            return ERROR_MESSAGE_FOR_USER
        return data


class Question:
    def __init__(self, form_data):
        self.form_data = form_data
        self.name = self.form_data.cleaned_data['name']
        self.email = self.form_data.cleaned_data['email']
        self.message = self.form_data.cleaned_data['message']

    def mail(self):
        send_mail(
            f'Вопрос от {self.email}',
            f'''{self.name}
{self.email}
{self.message}''',
            SERVICE_EMAIL,
            [SERVICE_EMAIL],
            fail_silently=False,
        )


class Order:
    def __init__(self, form_data, obj=None, url=''):
        self.form_data = form_data
        self.obj = obj
        self.url = url
        self.name = self.form_data.cleaned_data['name']
        self.email = self.form_data.cleaned_data['email']
        self.message = self.form_data.cleaned_data['message']
        self.composition = f'''{obj}
{url}'''

    def add_data_to_db(self, composition):
        self.form_data.instance.composition = composition
        self.form_data.instance.save()

    def send_email_to_company(self):
        send_mail(
            f'Заказ № {self.form_data.instance.id} от {self.email}',
            f'''{self.name}
{self.email}
{self.message}''',
            SERVICE_EMAIL,
            [SERVICE_EMAIL],
            fail_silently=False,
        )

    def send_email_to_user(self):
        message_data_for_user = f'''
Спасибо за заказ, в скором времени мы с вами свяжемся.

Заказ № {self.form_data.instance.id}
{self.composition}
'''
        send_mail(
            f'Заказ № {self.form_data.instance.id}',
            message_data_for_user,
            SERVICE_EMAIL,
            [self.email],
            fail_silently=False,
        )

    def main(self):
        try:
            self.add_data_to_db(self.composition)
        except Exception as e:
            error_traceback = traceback.format_exc()
            logger.exception(
                f'{e}\n\n{error_traceback}')
            send_mail(
                subject=f'ERROR: {e}',
                message=(
                    f'Ошибка: {e}\n\n{error_traceback}'),
                from_email=SERVICE_EMAIL,
                recipient_list=[SERVICE_EMAIL])
        self.send_email_to_company()
        self.send_email_to_user()
