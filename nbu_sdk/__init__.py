import datetime

import requests


def get_date_from_format(date_str):
    date_patterns = ["%d-%m-%Y", "%d.%m.%Y", "%d/%m/%Y",
                     "%Y-%m-%d", "%Y%m%d", ]
    for pattern in date_patterns:
        try:
            return datetime.datetime.strptime(date_str, pattern).date()
        except Exception:
            pass
    return None


class NbuApi(object):
    BASE_URL = 'https://bank.gov.ua/NBU_BankInfo'
    HEADERS = {
        'User-Agent': 'python',
        'Content-Type': 'application/json;charset=utf8',
        'Accept': 'application/json',
    }

    def request_url(self, type_request, **arg):
        url = '{}/{}'.format(self.BASE_URL, type_request)
        arg['json'] = 'json'
        r = requests.get(url, params=arg, headers=self.HEADERS)
        if r.status_code in [200, 201]:
            if 'message' in r.json()[0]:
                raise Exception(
                    'Server respond error! Error {}'.format(
                        r.json()[0]['message']))
            return r.json()
        else:
            raise Exception(
                'Server respond error! Error {}'.format(r.status_code))

    def get_bank(self, mfo=None):
        param = {'type_request': '/get_data_branch', 'typ': 0}
        if mfo:
            if not isinstance(mfo, str):
                mfo = str(mfo)
            if len(mfo) == 6 and mfo.isdigit():
                param['glmfo'] = mfo
            raise Exception('"mfo" length must be 6 digit exactly')
        return self.request_url(**param)

    def get_exchange_rate(self, currency=None, date=None):
        param = {'type_request': '/v1/statdirectory/exchange', }
        if currency:
            if isinstance(currency, str) and len(
                    currency) == 3 and currency.isalpha():
                param['valcode'] = currency
            else:
                raise Exception('"currency" must be correct currency code')
        if date:
            if isinstance(date, str):
                date = get_date_from_format(date)
                if date:
                    param['date'] = date.strftime('%Y%m%d')
                else:
                    raise Exception(
                        '"date" must be type of date, datetime or date '
                        'compatible string')
            elif isinstance(date, datetime.datetime):
                param['date'] = date.strftime('%Y%m%d')
            elif isinstance(date, datetime.date):
                param['date'] = date.strftime('%Y%m%d')
            else:
                raise Exception(
                    '"date" must be type of date, datetime or date '
                    'compatible string')
        return self.request_url(**param)
