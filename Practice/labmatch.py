import csv
import json

import country_converter as coco


def count(data):
    """
    实验楼楼赛的一道题，将csv中的数据按照需求进行统
    计，返回json数据，需求要统计大洲的数据，然后去学
    习country-converter包的使用，最后统计处要求的数
    据。（由于我当时审题不仔细，提交了好久都是失败，
    而实验楼这个提交，错误根本不提示，不像力扣一样，
    错了根本没个改错的方向，导致卡了好久。
    后来发现，原来是返回的数据结构问题。。。。。。
    到我提交时，都已经是第五个了，最后只能拿了个第五，
    在那里做的每道题，都是这个原因，早早写好，不知道
    哪里不符合要求，改的话只能一点一点调试...有的样例
    给了等于没给...总之就一句话好坑T_T）
    """

    cc = coco.CountryConverter()
    cc.OECDas('ISO3')
    key1_list = ["Confirmed", "Deaths", "Recovered", "Active"]
    key2_list = ["Africa", "Asia", "Oceania", "Europe", "America", "Others", "Total"]
    results = {}
    for key1 in key1_list:
        for key2 in key2_list:
            results.setdefault(key1, {})[key2] = 0
    data_list = []
    with open(data, 'r', encoding='utf-8') as incsv:
        item_list = csv.reader(incsv)
        for item in item_list:
            data_list.append(item)
    data_list.pop(0)
    for item in data_list:

        country = item[0]
        region = cc.convert(country, to='continent', not_found="Others")
        confirm_num = 0
        death_num = 0
        recover_num = 0
        active_num = 0
        if item[4] != "":
            confirm_num = int(float(item[4]))
        if item[5] != "":
            death_num = int(float(item[5]))
        if item[6] != "":
            recover_num = int(float(item[6]))
        if item[7] != "":
            active_num = int(float(item[7]))
        check = death_num + recover_num + active_num
        if confirm_num == check:
            results["Confirmed"][region] += confirm_num
            results["Confirmed"]["Total"] += confirm_num
            results["Deaths"][region] += death_num
            results["Deaths"]["Total"] += death_num
            results["Recovered"][region] += recover_num
            results["Recovered"]["Total"] += recover_num
            results["Active"][region] += active_num
            results["Active"]["Total"] += active_num
    results = json.dumps(results)
    print(type(results))

    return results


if __name__ == '__main__':
    file = './cases_country.csv'
    a = count(file)
    print(a)
