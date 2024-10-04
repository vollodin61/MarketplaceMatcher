# Marketplace Product Matcher

## Пример
| UUID                                   | Title                                                                                                          | Similar UUID                            | Similar Title                                                                                                           |
|----------------------------------------|----------------------------------------------------------------------------------------------------------------|-----------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| c3ca9af2-c271-4152-9993-1388ca3d1ef9 | Тыловой канал BEHRINGER Eurolive B210D, 1 колонка, чёрный                                                   | f5569616-9a93-4dfd-a15d-30be6ed6d4a3 | NordFolk ICE-5WP bl настенная влагозащищенная АС, 60 Вт, 5,25"/1", IP-54, 100V, черная (1шт)                       |
| c3ca9af2-c271-4152-9993-1388ca3d1ef9 | Тыловой канал BEHRINGER Eurolive B210D, 1 колонка, чёрный                                                   | a1a76393-e675-4897-a8ad-c712cf55e4ee | Центральный канал BEHRINGER Eurolive B110D, 1 колонка, черный                                                        |
| ff4df86b-9cc1-4590-87b8-b08221a51c1f | Смартфон Apple iPhone 15 Pro 1 ТБ, Dual: nano SIM + eSIM, серый титан                                        | 51cac817-e8ef-431e-95a3-3c88d826597a | Смартфон Samsung Galaxy S21 5G 8/128 ГБ RU, Dual: nano SIM + eSIM, Фиолетовый фантом                                |
| ff4df86b-9cc1-4590-87b8-b08221a51c1f | Смартфон Apple iPhone 15 Pro 1 ТБ, Dual: nano SIM + eSIM, серый титан                                        | 70a3be93-2605-49db-bc5e-97c981d77f43 | Умная колонка Apple HomePod mini (без часов), синий                                                                   |
| cc3977c2-cac3-4a62-860a-5b498e960123 | HISENSE Телевизор QLED Hisense 55" 55E7KQ черный 4K Ultra HD 60Hz DVB-T DVB-T2 DVB-C DVB-S DVB-S2 WiFi Smart TV | cc085e01-8b78-402b-b527-ca82c2e7a718 | Телевизор SKYLINE 40LST5971, SMART (Android), черный                                                                  |
| cc3977c2-cac3-4a62-860a-5b498e960123 | HISENSE Телевизор QLED Hisense 55" 55E7KQ черный 4K Ultra HD 60Hz DVB-T DVB-T2 DVB-C DVB-S DVB-S2 WiFi Smart TV | 9ce71bee-f619-495d-9533-75c7f4c5487f | 32" Телевизор TELEFUNKEN TF-LED32S71T2 2021 VA, черный                                                               |
| 96968f1a-2244-4f18-923a-d0253d664f98 | Смартфон Samsung Galaxy S21 FE 8/256 ГБ, Dual nano SIM, зеленый                                              | 78646164-0701-4f18-ba12-94508cc1d577 | Смартфон Apple iPhone 15 Pro 256 ГБ, Dual еSIM, черный титан                                                         |
| 96968f1a-2244-4f18-923a-d0253d664f98 | Смартфон Samsung Galaxy S21 FE 8/256 ГБ, Dual nano SIM, зеленый                                              | 48e7c015-deea-4beb-8af8-e0ada9a227c6 | Смартфон Apple iPhone 15 Pro 256 ГБ, Dual еSIM, синий титан                                                          |


## Запуск проекта

#### 1. Клонируйте репозиторий

```shell
git clone https://github.com/vollodin61/MarketplaceMatcher
```

#### 2. Создайте файл `.env`, используя пример `.env_temp`

```shell
mv .env_temp .env
```

#### 3. Запустите проект:
```shell
docker-compose up --build
```

#### 4. Наилучшие пожелания
- [X] Чтобы избежать ошибок elasticsearch, перед перезапуском делайте "docker compose down -v"

#### 5. Мелочи:
- [X] В поле barcode изменил тип на str, потому что слишком длинные числа туда попадают. 
- [X] Файл с примером был обрезан некорректно, без закрывающих тегов, исправил.

## Это было интересное задание, спасибо! Возьмите, меня на работу, пожалуйста)