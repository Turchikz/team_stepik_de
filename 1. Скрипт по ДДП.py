import pandas as pd
import numpy as np
from IPython.display import display

# Запрос даты для формирования отчета:
Date_report = input("Введите даты для составления отчета: ")

# Чтение файлов Excel
df_DDP = pd.read_excel('прайс DDP на 27.08.2025.xlsx') # Данные по DDP. Изменяем названия файла на требуемое при необходимости 
df_TV = pd.read_excel('ТВ+ВСТ.08-2025.xlsx') # Данные по Тв и встройке. Изменяем названия файла на требуемое при необходимости
df_br_lc = pd.read_excel('SKU_ERP_27.08.2025.xlsx') # Данные по бренду и ЖЦ. Изменяем названия файла на требуемое при необходимости

# Обработка данных из 1С "Прайс DDP"
df_DDP = df_DDP.dropna(axis=1, how='all')
df_DDP = df_DDP.dropna(axis=0, how='all')
df_DDP.columns.values[0] = 'Код'
df_DDP.columns.values[1] = 'Артикул'
df_DDP.columns.values[2] = 'Номенклатура'
df_DDP.columns.values[3] = 'DDP'
df_DDP = df_DDP.iloc[4:]
df_DDP = df_DDP.reset_index(drop=True)
df_DDP['Артикул'] = df_DDP['Артикул'].str.strip()

# Запрос обменного курса для 1 USD:
usd_prais = input("Введите курс 1 USD: ")

# Рассчитываем себестоимоть в рублях. Предварительно меняем типы данных у DDP и Курса валют.
df_DDP['Курс'] = usd_prais
df_DDP = df_DDP.astype({'DDP': 'float', 'Курс': 'float'})
df_DDP['Себестоимость, руб'] = df_DDP['DDP']*df_DDP['Курс']

# Объединяем с данными по ТВ и ВСТ от ком.отдела
df_DDP = df_DDP.merge(
    df_TV[['Артикул', 'ср.закуп']],
    on='Артикул',
    how='left'
)

# Заменяем нуловые значения на 0 и создаем итоговый столбец по себестоимости с учетом данных от ком.отдела
df_DDP['ср.закуп'] = df_DDP['ср.закуп'].fillna(0)
df_DDP['Себестоимость ИТОГ, руб'] = np.where(df_DDP['ср.закуп'] == 0, df_DDP['Себестоимость, руб'], df_DDP['ср.закуп'])

# Готовим справочные данные по ЖЦ и Бренду
df_spr = df_br_lc[['Артикул 1С', 'Рабочее наименование', 'ЖЦ', 'Активность']].copy()
df_spr = df_spr.drop_duplicates(subset=['Артикул 1С'])
df_spr.columns.values[0] = 'Артикул'
df_spr.columns.values[1] = 'Номенклатура'
df_spr.columns = df_spr.columns.str.strip()
df_spr['Бренд'] = np.where(df_spr['Номенклатура'].str.contains('Polaris', case=False) == True, 'Polaris', 'не_Polaris')
Articuls = ['10206793', 
            '10206372', 
            '10206830', 
            '10605594', 
            'ЦБ-00028534', 
            '10605772', 
            '10605773', 
            'ЦБ-00024691', 
            'ЦБ-00019604', 
            'ЦБ-00019863', 
            'ЦБ-00020053'] # Включаем в список товары Поларис, у которых некорректно отображается бренд в исх файле
df_spr['Бренд'] = np.where(df_spr['Артикул'].isin(Articuls) == True, 'Polaris', df_spr['Бренд'])

# Объединяем со справочными данными. Добавляем данные по ЖЦ и Бренду
df_DDP = df_DDP.merge(
    df_spr[['Артикул', 'ЖЦ', 'Активность', 'Бренд']],
    on='Артикул',
    how='left'
)

df_report = df_DDP[['Артикул', 'Номенклатура', 'DDP', 'Курс', 'Себестоимость ИТОГ, руб', 'ЖЦ', 'Активность', 'Бренд']].copy()

# Сохранение отчета в Excel
df_report.to_excel(f"DDP_на_{Date_report}.xlsx", sheet_name=f'DDP_{Date_report}', index=False) # Изменяем названия файла на требуемое при необходимости
df_spr.to_excel(f"СПР.ЖЦ+Бренд_{Date_report}.xlsx", sheet_name=f'ЖЦ+Бренд_{Date_report}', index=False) # Изменяем названия файла на требуемое при необходимости

#df_DDP
display(df_report)
df_report.info()