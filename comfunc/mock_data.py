from faker import Faker
from datetime import datetime, timedelta

now = datetime.now()
now_data = now.date()
past_60_date = now_data - timedelta(60)
future_30_date = now_data + timedelta(30)

fake = Faker('zh_cn')

mock_datas = [
    {'key': '人名', 'value': 'fake.name()'},
    {'key': 'Email', 'value': 'fake.email()'},
    {'key': '电话', 'value': 'fake.phone_number()'},
    {'key': '地址', 'value': r'fake.address().replace("\n", ", ")'},
    {'key': '身份证', 'value': 'fake.ssn()'},
    {'key': '当前日期', 'value': 'now_data'},
    {'key': '当前时间', 'value': 'now'},
    {'key': '历史日期', 'value': 'fake.date_between_dates(date_start=past_60_date, date_end=now_data)'},
    {'key': '将来日期', 'value': 'fake.date_between_dates(date_start=now_data, date_end=future_30_date)'},
    {'key': '历史时间', 'value': 'fake.date_time_between(start_date="-60d", end_date="now")'},
    {'key': '将来时间', 'value': 'fake.date_time_between(start_date="now", end_date="+30d")'},
    {'key': '随机文本', 'value': 'fake.text(max_nb_chars=200)'}
]