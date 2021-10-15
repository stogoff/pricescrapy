import os
import time


def status():
    in_path = '/tmp/uploads'
    files = []
    for r, d, f in os.walk(in_path):
        for filename in f:
            if '.txt' in filename:
                files.append(filename)
    if not files:
        return "Файлы пока не загружены"
    files.sort()
    txt = files[-1]
    out_path = 'static/'
    files = []
    for r, d, f in os.walk(out_path):
        for filename in f:
            if '.csv' in filename:
                files.append(filename)
    if not files:
        return f'Файл {txt} ожидает обработки'
    files.sort()
    csv = files[-1]
    print(csv)
    timestamp = int(csv[-14:-4])
    xlsx = csv[:-3] + 'xlsx'
    print(xlsx)
    link = '/static/result{}.xlsx'.format(timestamp)
    xlink = '/static/result_p{}.xlsx'.format(timestamp)
    if os.path.isfile(os.path.join(out_path, xlsx)):

        status = f'Файл обработан. Результаты доступны  <a href="{link}">здесь</a> и <a href="{xlink}">здесь</a>'
    else:
        t = int(time.time() - timestamp)
        status = f'Файл {txt} обрабатывается {t} c. По окончании результаты будут доступны  <a href="{link}">здесь</a> и <a href="{xlink}">здесь</a>'
    print(status)
    return status
