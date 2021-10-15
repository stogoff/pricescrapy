import os
import time
import psutil


def status():
    running = False
    for pid in psutil.pids():
        process = psutil.Process(pid)
        if 'python' in process.name():
            if 'run_all.py' in process.cmdline()[1]:
                running = True
    in_path = '/tmp/uploads'
    xfiles = []
    xtimestamp = 0
    for r, d, f in os.walk(in_path):
        for filename in f:
            if '.xls' in filename:
                xfiles.append(filename)
    if len(xfiles) > 0:
        xfiles.sort()
        inxls = xfiles[-1]
        xtimestamp = int(inxls[2:12])
    files = []
    for r, d, f in os.walk(in_path):
        for filename in f:
            if '.txt' in filename:
                files.append(filename)
    if not files:
        return "Ожидание"
    files.sort()
    txt = files[-1]
    ttimestamp = int(txt[2:12])
    if xtimestamp > ttimestamp:
        txt = inxls
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
    if timestamp < ttimestamp:
        return f'Файл {txt} ожидает обработки'
    elif timestamp < xtimestamp:
        return f'Файл {inxls} ожидает обработки'
    xlsx = csv[:-3] + 'xlsx'
    print(xlsx)
    link = '/static/result{}.xlsx'.format(timestamp)
    xlink = '/static/result_p{}.xlsx'.format(timestamp)
    if os.path.isfile(os.path.join(out_path, xlsx)):
        size_csv = os.path.getsize(os.path.join(out_path, csv))
        if size_csv < 10:
            status = f'Произошла ошибка обработки файла {txt}. Обратитесь к разработчику'
        else:
            status = f'Файл обработан. Результаты доступны  <a href="{link}">здесь</a> и <a href="{xlink}">здесь</a>'
    else:
        if running:
            t = int(time.time() - timestamp)
            status = f'Файл {txt} обрабатывается {t} c. По окончании результаты будут доступны  <a href="{link}">здесь</a> и <a href="{xlink}">здесь</a>'
        else:
            status = f'Произошла ошибка обработки файла {txt}. Обратитесь к разработчику'
    print(status)
    return status


if __name__ == "__main__":
    status()
