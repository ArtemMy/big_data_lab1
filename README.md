# Первая лабораторная по большим данным
Реализованы алгоритмы Apriori и FP-Growth

## Запуск:

* ./apriori.py filename min_support min_conf
* ./fp_growth.py filename min_support min_conf

## Запуск проверки юнит тестов и результатов алгоритмов:

* ./test.py

## Сравнение времени работы алгоритмов:

Apriori - красным и FP-Growth -синим

Зависимость времени (в секундах) от размера входных данных (строк):
![Alt text](https://cloud.githubusercontent.com/assets/8218840/26249805/fb54e73a-3cb8-11e7-8330-f4296c6b6d58.png)

Зависимость времени (в секундах) от величины минимальной допустимой поддержки:
![Alt text](https://cloud.githubusercontent.com/assets/8218840/26249804/fb455b94-3cb8-11e7-9460-0fdcff2c6359.png)
