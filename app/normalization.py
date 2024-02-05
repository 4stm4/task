
class Normalizer:

    @staticmethod
    def _get_digit(text: str) -> int:
        text = text.lower()
        units = ['ноль', 'один', 'дв', 'тр', 'чет', 'пят', 'шест',
            'сем', 'восем', 'девят']
        tens = [
            'десят', 'двадцат', 'тридцат', 'сорок', 'пятьдесят',
            'шестьдесят', 'семяьдесят', 'восемьдесят', 'девяносто',
        ]
        if str(text).isdigit():
            return int(text)
        # определяем прописные десятки
        for index, ten in enumerate(tens):
            ten_pos = str(text).find(ten)
            if ten_pos < 0:
                continue
            digit = 10 + 10*index
            return digit
        # определяем прописные единицы
        for index, unit in enumerate(units):
            unit_pos = str(text).find(unit)
            if unit_pos < 0:
                continue
            if str(text).find('цат') > 3:
                digit = 10 + index
            else:
                digit = index
            return digit
        return 0

    @staticmethod
    def _get_period(text: str):
        text = text.lower()
        periods = {
            'год': 0,
            'лет': 0,
            'мес': 1,
            'нед': 2,
            'дн': 3,
            'сут': 3,
        }
        for period in periods.keys():
            period_pos = str(text).find(period)
            if period_pos < 0:
                continue
            return periods[period]
        return -1

    @staticmethod
    def _get_month(text: str) -> str:
        text = text.lower()
        months = [
            'янв', 'февр', 'март', 'апр', 'ма', 'июн',
            'июл', 'август', 'сентябр', 'октябр', 'ноябр', 'декабр',
        ]      
        for index, month in enumerate(months):
            period_pos = str(text).find(month)
            if period_pos < 0:
                continue
            if index < 10:
                return '0' + str(index + 1) 
            else:
                return str(index + 1)
        return ''

    def period(self, text: str) -> str:
        text = text.lower()
        output_list = [0, 0, 0, 0]
        digit = 0
        words = str(text).split()
        for word in words:
            if word == 'полгода' or word == 'полугода':
                output_list[1] += 6
                continue
            if digit > 0:
                period = self._get_period(word)
                if period >= 0:
                    output_list[period] += digit
                    digit = 0            
            digit += self._get_digit(word)
        return '_'.join([str(elem) for elem in output_list])

    def date(self, text: str) -> str:
        words = str(text).split()
        month = ''
        day = ''
        year = 0
        for word in words:
            if month == '':
                month = self._get_month(word)
            digit = self._get_digit(word)
            if digit < 1:
                continue
            if digit < 32:
                if digit < 10:
                    day = '0'+ str(digit)
                else:
                    day = str(digit)
            else:
                year = digit
        return str(day)+'.'+month+'.'+str(year)
