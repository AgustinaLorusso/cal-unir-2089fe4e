"""Genera unir.ics a partir de las filas extraídas del campus UNIR.

Formato de cada fila (separado por |):
id|titulo|asignatura|type|fechaInicio(ISO, UTC)|fechaFin(ISO, UTC)|isInstantEvent(0/1)

Uso: python3 tools/gen_ics.py eventos.txt unir.ics
"""
import re
import sys
import datetime as dt


def clean_subject(a):
    a = re.sub(r'^1C1Q ', '', a or '')
    a = re.sub(r' - PER \d+ - \w+ \d{4}$', '', a)
    a = re.sub(r'^PER \d+ \w+ \d{4} - ', '', a)
    return a.strip()


def short(a):
    return a.replace('Seminario los Conflictos y Crímenes Internacionales. La Ayuda Humanitaria en Tiempos de Guerra y Paz',
                     'Seminario Conflictos y Crímenes Internacionales')


def parse(s):
    return dt.datetime.fromisoformat(s.strip()).astimezone(dt.timezone.utc).replace(tzinfo=None)


def esc(t):
    return t.replace('\\', '\\\\').replace(',', '\\,').replace(';', '\\;').replace('\n', '\\n')


def fmt(d):
    return d.strftime('%Y%m%dT%H%M00Z')


def main(src, dst):
    now = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//UNIR sync//ES', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
           'X-WR-CALNAME:UNIR', 'X-WR-TIMEZONE:Europe/Madrid',
           'REFRESH-INTERVAL;VALUE=DURATION:PT12H', 'X-PUBLISHED-TTL:PT12H']
    seen = set()
    for line in open(src, encoding='utf-8'):
        line = line.strip()
        if not line:
            continue
        parts = line.split('|')
        if len(parts) != 7:
            print('fila ignorada:', line[:80], file=sys.stderr)
            continue
        id_, tit, asig, typ, st, en, inst = parts
        start, end = parse(st), parse(en)
        subj = short(clean_subject(asig))
        key = (tit, subj, start)
        if key in seen:
            continue
        seen.add(key)
        uid = f"{re.sub(r'[^A-Za-z0-9]', '-', id_)}-{start:%Y%m%d%H%M}@unir-sync"
        ev = ['BEGIN:VEVENT', f'UID:{uid}', f'DTSTAMP:{now}']
        if typ == 'Academico':
            d = start.date()
            ev += [f'DTSTART;VALUE=DATE:{d:%Y%m%d}', f'DTEND;VALUE=DATE:{d + dt.timedelta(days=1):%Y%m%d}',
                   f'SUMMARY:{esc(tit)}', 'TRANSP:TRANSPARENT']
        elif typ == 'Entregas':
            title = 'Entrega: ' + tit
            ev += [f'DTSTART:{fmt(start)}', f'DTEND:{fmt(start)}', f'SUMMARY:{esc(title)}',
                   f'DESCRIPTION:{esc(subj + " — fecha límite")}', 'TRANSP:TRANSPARENT',
                   'BEGIN:VALARM', 'ACTION:DISPLAY', f'DESCRIPTION:{esc(title)}', 'TRIGGER:-P1D', 'END:VALARM']
        else:
            if subj == 'Aula Cero':
                title = 'Aula de Información General (Aula Cero)'
            else:
                title = 'Clase: ' + short(tit)
            ev += [f'DTSTART:{fmt(start)}', f'DTEND:{fmt(end)}', f'SUMMARY:{esc(title)}',
                   'BEGIN:VALARM', 'ACTION:DISPLAY', f'DESCRIPTION:{esc(title)}', 'TRIGGER:-PT30M', 'END:VALARM']
        ev.append('END:VEVENT')
        out += ev
    out.append('END:VCALENDAR')
    with open(dst, 'w', encoding='utf-8', newline='') as f:
        f.write('\r\n'.join(out) + '\r\n')
    print(len(seen), 'eventos')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
