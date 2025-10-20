import pandas as pd
import numpy as np
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.styles.borders import Border, Side
from openpyxl.utils import get_column_letter
from IPython.display import display

# Запрос даты у пользователя
date_str = input("Введите дату в формате DD.MM.YYYY: ")
date_obj = datetime.strptime(date_str, "%d.%m.%Y")
short_date = date_obj.strftime("%d.%m.%Y")

# Чтение файлов Excel
df = pd.read_excel(f'Трафик {short_date}.xlsx')
df_mag = pd.read_excel('Данные для расчета трафика.xlsx', sheet_name='Магазины')

# Обработка данных из Excel
df = df.iloc[14:]
df = df.dropna(axis=1, how='all')
df = df.reset_index(drop=True)
df = df.drop([1,2,3,8,11,12])
df = df.T
df.columns = df.iloc[0]
df = df.reset_index(drop=True)
df = df.drop([0])
df = df.rename(columns={'Тип показателя':"Магазины"})

# Удаляем лишние/закрытые магазины
StopList = ['РЦ "Победа" Ритейл', 
           'РЦ «Родина» ИНЕТ', 
           'РЦ «Родина» РИТЕЙЛ',
           '0005 Казань, Победа, ул. Закиева д.1',
           '0006 Нижнекамск, Якорь ул. Корабельная 44',
           '0008 Уфа, МИР просп. Октября, д. 4. кор. 1',
           '0010 Октябрьский, Верба, Ленина, д. 59/1',
           '0022 Ульяновск, ТЦ Самолет, просп.Ульяновский, д.1',
           '0023 Белебей, ТЦ Эссен, ул. им. Морозова, д.9',
           '0025 Ульяновск, ТЦ Пушкаревское, Московское ш,91',
           '0029 Челябинск, ТРК Горки, Артиллерийская, 136',
           '0033 Казань, ТРК Мега, пр-т. Победы, 141',
           '0035 Екатеринбург, ТЦ Радуга Парк, Репина, 94',
           '0044 Ижевск, ТЦ Аврора Парк, Удмуртская, 304',
           '0045 Ульяновск, КОРНЕР Аквамолл, Московское ш. 108',
           '0047 Москва, ТРЦ Павелецкая Плаза, Павелецкая, д.3',
           '0053 Казань, ТЦ Парк Хаус, Пр. Ямашева 46/33',
           '0054 Уфа, ТРЦ Планета, Энтузиастов, д. 20',
           '0072 Н.Новгород, ТРЦ Океанис, пр. Гагарина, 35',
           '0073 Москва, ТРЦ Щелковский, Щелковское шоссе, 75',
           '0080 Ярославль, ТРЦ Аура, Победы, 41',
           '0081 Пермь, ТРЦ Эспланада, Петропавловская, 73а',
           '0082 МО Химки, КОРНЕР ТЦ Лига, Ленинградское ш, 5',
           '0083 Москва, КОРНЕР МТК ЕвроПарк, Рублевское ш, 62',
           '0089 Новосибирск, КОРНЕР Аура, Военная, 5',
           '0102 Казань, КОРНЕР МЕГА, пр-т. Победы, 141',
           '0103 Уфа, КОРНЕР МЕГА, Рубежная, 174',
           '0104 Омск, КОРНЕР МЕГА, Бульвар Архитекторов, 35',
           '0105 Ростов-На Дону, КОРНЕР МЕГА, Аксайский, 23',
           '0107 МО Химки, КОРНЕР МЕГА, микрорайон ИКЕА, 2',
           '0106 Н. Новгород, КОРНЕР МЕГА, а/д Волга, Федяково',
           '0108 Москва, КОРНЕР МЕГА ТС, Калужское шоссе 21км',
           '0114 Новокузнецк, КОРНЕР ТРЦ Планета, ул.Доз, 10а']

# Заменяем пустые значения на 0 
df = df.fillna(0)

# Удаляем магазины из стоп-листа
indexMag = df[(df['Магазины'].isin(StopList))].index
df.drop(indexMag, inplace=True)

# Генерируем возрастающие значения от 1 до количества строк
number = range(1, len(df) + 1)

# Добавляем новый столбец '№ п/п' в начало датафрейма
df.insert(0, '№ п/п', list(number))

# Проверяем корректность выгрузки данных в 1С по магазинам.
list_mag = df['Магазины'].values.tolist()
df_mag['Result'] = np.where(df_mag['Магазины'].isin(list_mag), 'Данные есть', 'Н/Д')
df_mag_check = df_mag[df_mag['Result'] == 'Н/Д']  # Исправлено: создаем новый DataFrame

# Сохраняем отчеты в Excel
df.to_excel(f"Отчет за день за_{short_date}.xlsx", sheet_name=f'Отчет за день за_{short_date}', index=False)
df_mag_check.to_excel(f"Отчет по магазинам за_{short_date}.xlsx", index=False)  # Исправлено: используем правильный DataFrame

# Функция на вычисление суммы по столбцу
def sum_col(ws, col, col_top=2, col_start=1, tight=False):
    col_len = ws.max_row
    if tight:
        # Находим последнюю непустую строку
        for row in range(ws.max_row, 0, -1):
            if ws[f'{col}{row}'].value is not None:
                col_len = row
                break
    ws[f'{col}{col_start}'] = f'=SUM({col}{col_top}:{col}{col_len})'

# Функция на вычисление среднего по столбцу
def avg_col(ws, col, col_top=2, col_start=1, tight=False):
    col_len = ws.max_row
    if tight:
        # Находим последнюю непустую строку
        for row in range(ws.max_row, 0, -1):
            if ws[f'{col}{row}'].value is not None:
                col_len = row
                break
    ws[f'{col}{col_start}'] = f'=AVERAGE({col}{col_top}:{col}{col_len})'

# Специальная функция на вычисление среднего по столбцу Е
def avg_col_f(ws, col1, col_top1=2, col2='D', col_top2=2):
    col_len = ws.max_row
    
    cells1 = []
    for row in range(col_top1, col_len + 1):
        cell_value = ws[f'{col1}{row}'].value
        if cell_value is not None:
            try:
                cells1.append(float(cell_value))
            except (ValueError, TypeError):
                continue
    
    cells2 = []
    for row in range(col_top2, col_len + 1):
        cell_value = ws[f'{col2}{row}'].value
        if cell_value is not None:
            try:
                cells2.append(float(cell_value))
            except (ValueError, TypeError):
                continue
    
    if cells2 and sum(cells2) != 0:
        result = sum(cells1) / sum(cells2)
        ws['F1'] = result
    else:
        ws['F1'] = 0

# Загружаем нужный файл эксель в работу
wb = load_workbook(f"Отчет за день за_{short_date}.xlsx")

# Загружаем нужный лист эксель в работу
ws = wb[f'Отчет за день за_{short_date}']

# Добавляем пустую строку сверху
ws.insert_rows(1)

# Проводим нужные вычисления
sum_col(ws, 'C', col_top=3, col_start=1)
sum_col(ws, 'D', col_top=3, col_start=1, tight=True)
avg_col(ws, 'E', col_top=3, col_start=1, tight=True)
avg_col_f(ws, 'C', col_top1=3, col2='D', col_top2=3)
sum_col(ws, 'G', col_top=3, col_start=1, tight=True)
sum_col(ws, 'H', col_top=3, col_start=1, tight=True)

# Форматируем шрифт у 2-х первых строчек
for row in ws.iter_rows(min_col=1, max_col=8, max_row=2):
    for cell in row:
        cell.font = Font(bold=True, size=11)

# Форматируем фон ячеек у 1-й строчки
for row in ws.iter_rows(min_col=1, max_col=8, max_row=1):
    for cell in row:
        cell.fill = PatternFill(start_color="FFE4C4", end_color="FFE4C4", fill_type="solid")

# Форматируем фон ячеек у 2-й строчки
for row in ws.iter_rows(min_col=1, max_col=8, min_row=2, max_row=2):
    for cell in row:
        cell.fill = PatternFill(start_color="BCEE68", end_color="BCEE68", fill_type="solid")

# Форматируем границы ячеек для всех ячеек
for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=8):
    for cell in row:
        cell.border = Border(left=Side(style='thin'), 
                            right=Side(style='thin'), 
                            top=Side(style='thin'), 
                            bottom=Side(style='thin'))

# Автоматическая установка ширины столбцов
for column in ws.columns:
    max_length = 0
    column_letter = get_column_letter(column[0].column)
    for cell in column:
        try:
            if cell.value is not None and len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except:
            pass
    adjusted_width = min(max_length + 2, 50)  # Ограничиваем максимальную ширину
    ws.column_dimensions[column_letter].width = adjusted_width

# Форматируем формат чисел в 1-й строчке
ws['C1'].number_format = '# ##0'
ws['D1'].number_format = '# ##0'
ws['E1'].number_format = '# ##0.00'
ws['F1'].number_format = '0.000'
ws['G1'].number_format = '# ##0'
ws['H1'].number_format = '# ##0'

# Определяем колонки для форматирования
columns_to_format = ['A', 'C', 'D', 'E', 'F', 'G', 'H'] 

# Проходим по заданным ячейкам
for col in columns_to_format: 
    for row in range(1, ws.max_row + 1):
        cell = ws[f'{col}{row}']
        cell.alignment = Alignment(horizontal='center', vertical='center')
        
# Устанавливаем фильтр на первую строку
ws.auto_filter.ref = f"A2:H{ws.max_row}"

# Сохраняем результаты изменений в файле эксель
wb.save(f'Отчет за день за_{short_date}.xlsx')

display(df)
df.info()