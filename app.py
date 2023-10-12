import requests
import datetime
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get():
    now = datetime.datetime.now()
    year = request.args.get('year')
    if year is None:
        year = now.strftime('%Y')

    month = request.args.get('month')
    if month is None:
        month = now.strftime('%m')

    day = request.args.get('day')
    if day is None:
        day = now.strftime('%d')

    almanac = get_calendar(year, month)

    for a in almanac:
        if a['year'] == year and a['month'] == month and a['day'] == day:
            return date_format(a)
    return {'date': '%s-%s-%s' % (year, month, day)}


def get_calendar(year, month):
    ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) Chrome/65.0.3325.181'}
    res = requests.get(
        "https://opendata.baidu.com/data/inner?tn=reserved_all_res_tn&type=json&resource_id=52109&query=%s年%s月&apiType=yearMonthData" % (
        year, month), headers=ua)
    almanac = res.json()['Result'][0]['DisplayData']['resultData']['tplData']['data']['almanac']
    return almanac


def date_format(almanac):
    return {
        "animal": almanac.get("animal"),
        "avoid": almanac.get("avoid"),
        "cnDay": '周'+ almanac.get("cnDay"),
        "day": almanac.get("day"),
        "gzDate": almanac.get("gzDate"),
        "gzMonth": almanac.get("gzMonth"),
        "gzYear": almanac.get("gzYear"),
        "lDate": almanac.get("lDate"),
        "lMonth": almanac.get("lMonth"),
        "lunarYear": almanac.get("lunarYear"),
        "month": almanac.get("month"),
        "suit": almanac.get("suit"),
        "year": almanac.get("year"),
        "term": almanac.get("term"),
        "festivalList": almanac.get("festivalList"),
        "date": '%s-%s-%s' % (almanac.get("year"), almanac.get("month"), almanac.get("day"))
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
