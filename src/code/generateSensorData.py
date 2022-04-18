# -*- coding: utf-8 -*-
'''
模拟传感器数据
Created on 2022-04-18   12:04:21
@author: TA
'''
import os
import random

dirname = os.path.dirname(__file__)
temperature_file = os.path.join(dirname, 'temperature.csv')
humidity_file = os.path.join(dirname, 'humidity.csv')

def generate_temperature_data():
    with open(temperature_file, 'w') as f:
        for i in range(1000):
            temperature = random.randint(20, 30)
            f.write('{},{}\n'.format(i, temperature))
            
def generate_humidity_data():
    with open(humidity_file, 'w') as f:
        for i in range(1000):
            humidity = random.randint(60, 80)
            f.write('{},{}\n'.format(i, humidity))
            

if __name__ == '__main__':
    generate_temperature_data()
    generate_humidity_data()
    
