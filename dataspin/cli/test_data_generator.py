import datetime
import gzip
import json
import os
from random import randint
import shutil
from typing import List
import uuid
import click
from random import shuffle

app_ids = ['APPIOXDKXIESP', 'APPOWLSLSDWLD', 'APPSISEKIDESS']

event_names = ['login', 'logout', 'enter_splash', 'leave_splash', 'session']
platform = ['android', 'ios']


def generate_json_data(bp_timestamp):
    data_dict = {
        'app_id': app_ids[randint(0, len(app_ids)-1)],
        'event_name': event_names[randint(0, len(event_names)-1)],
        'event_id': str(uuid.uuid4()),
        'bp_timestamp': bp_timestamp,
        'platform': platform[randint(0, len(platform)-1)],
        'device': {
            'brand': '',
            'os_type': 'android',
            'os_version': '12'
        }
    }
    return json.dumps(data_dict)


def save_json_file(file_dir: str, file_name, data_list: List[str]):
    full_file_name = file_dir+'/'+file_name+'.gz'
    with gzip.open(full_file_name, 'wb') as f:
        f.write('\n'.join(data_list).encode('utf-8'))


def generate_test_data(file_dir='tmp/source', file_numbers=1, data_counts=1000, duplicate_data_count=1, data_format='jsonl', time_range=2, time_unit='day'):
    file_dir = file_dir.strip('/')
    if os.path.exists(file_dir):
        shutil.rmtree(file_dir)
    os.makedirs(file_dir)
    now = datetime.datetime.utcnow()
    duplicate_data_seq = set()
    for i in range(duplicate_data_count):
        seq = randint(0, data_counts-1)
        while seq in duplicate_data_seq:
            seq = randint(0, data_counts-1)
        duplicate_data_seq.add(seq)
    data_list = []
    for i in range(data_counts):
        if time_unit == 'day':
            start_time = now + datetime.timedelta(days=-time_range)
            target_bp_timestamp = start_time + \
                datetime.timedelta(seconds=randint(0, time_range*24*60*60-1))
        elif time_unit == 'hour':
            start_time = now + datetime.timedelta(hours=-time_range)
            target_bp_timestamp = start_time + \
                datetime.timedelta(seconds=randint(0, time_range*60*60-1))
        elif time_unit == 'minute':
            start_time = now + datetime.timedelta(minutes=-time_range)
            target_bp_timestamp = start_time + \
                datetime.timedelta(seconds=randint(0, time_range*60-1))
        json_data = generate_json_data(
            bp_timestamp=target_bp_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'))
        data_list.append(json_data)
        if i in duplicate_data_seq:
            data_list.append(json_data)
    shuffle(data_list)
    if file_numbers > len(data_list):
        for i in range(0, file_numbers):
            save_json_file(file_dir, file_name='test_%s.jsonl' %
                           i, data_list=data_list[i:i+1] if i < len(data_list) else [])
    else:
        step = int(len(data_list)/file_numbers)+1
        n = 0
        for i in range(0, len(data_list), step):
            save_json_file(file_dir, file_name='test_%s.jsonl' %
                           n, data_list=data_list[i:i+step])
            n = n + 1


@click.group(context_settings={'help_option_names': ['-h', '--help']})
def cli():
    pass


@cli.command()
@click.option('--execute_duration', '-ed', type=click.IntRange(min=10), default=60, help='execute duration,unit is second,default 60')
@click.option('--file_dir', '-fd', default='tmp/source', help='file dir')
@click.option('--file_numbers', '-fn', type=click.IntRange(min=1), default=1, help='file numbers')
@click.option('--data_counts', '-dc', type=click.IntRange(min=10), default=100000, help='data counts')
@click.option('--duplicate_data_count', '-dd', type=click.IntRange(min=0), default=1000, help='duplicate data counts')
@click.option('--data_format', '-df', type=click.Choice(['jsonl']), default='jsonl', help='data format')
@click.option('--time_range', '-tr', type=click.IntRange(min=1), default=2, help='time range')
@click.option('--time_unit', '-tu', type=click.Choice(['day', 'hour', 'minute']), default='minute', help='time unit')
def run(execute_duration, file_dir, file_numbers, data_counts, duplicate_data_count, data_format, time_range, time_unit):
    while True:
        generate_test_data(file_dir=file_dir.strip(), file_numbers=file_numbers, data_counts=data_counts,
                           duplicate_data_count=duplicate_data_count, data_format=data_format,
                           time_range=time_range, time_unit=time_unit)
