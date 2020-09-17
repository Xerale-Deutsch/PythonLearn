import os
import shutil
import argparse


def clean_up(folder):
    """
    1、将不同扩展名、相同文件名的文件整理到一个文件夹内
    2、将相同扩展名、不同文件名的文件整理到一个文件夹内
    """
    seps = os.path.sep
    file_list = {}
    files = os.listdir(folder)
    oprate_list = []
    file_name_dict = {}
    file_ext_dict = {}
    cache = []
    for file in files:
        filex = "{0}{1}{2}".format(folder, seps, file)
        if os.path.isfile(filex):
            file_name = os.path.splitext(file)[0]
            file_ext = os.path.splitext(file)[-1]
            if '.' in file:
                item = (file_name, file_ext)
            else:
                item = (file, 'others')
            oprate_list.append(item)
            if file_name_dict.get(item[0]):
                file_name_dict[item[0]] += 1
            else:
                file_name_dict[item[0]] = 1

    for name, value in file_name_dict.items():
        if value > 1:
            if not os.path.exists("{0}{1}{2}".format(folder, seps, name)):
                os.mkdir("{0}{1}{2}".format(folder, seps, name))
            for item in oprate_list:
                if item[0] == name:
                    cache.append((item[0], item[1]))

    oprate_list = list(set(oprate_list).difference(set(cache)))

    for file in cache:
        src = "{0}{1}{2}{3}".format(folder, seps, file[0], file[1])

        if os.path.isfile(src):
            dst = "{0}{1}{2}".format(folder, seps, file[0])
            shutil.move(src=src, dst=dst)
            if file_list.get(file[0]):
                file_list[file[0]] += 1
            else:
                file_list[file[0]] = 1

    cache = []

    for item in oprate_list:
        if file_ext_dict.get(item[1]):
            file_ext_dict[item[1]] += 1
        else:
            file_ext_dict[item[1]] = 1

    for ext, value in file_ext_dict.items():
        if value > 1:
            if ext == 'others':
                dir_name = 'others'
            else:
                dir_name = ext.replace('.', "")
            dir_name = "{0}{1}{2}".format(folder, seps, dir_name)
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            for item in oprate_list:
                if item[1] == ext:
                    cache.append((item[0], item[1]))

    oprate_list = list(set(oprate_list).difference(set(cache)))

    for file in cache:
        if file[1] == 'others':
            ext_name = ''
        else:
            ext_name = file[1]
        src = "{0}{1}{2}{3}".format(folder, seps, file[0], ext_name)
        if os.path.isfile(src):
            if ext_name == 'othres':
                dst = "{0}{1}{2}".format(folder, seps, "others")
            else:
                dst = "{0}{1}{2}".format(folder, seps, file[1].replace(".", ""))
            shutil.move(src=src, dst=dst)
            if file_list.get(file[1].replace(".", "")):
                file_list[file[1].replace(".", "")] += 1
            else:
                file_list[file[1].replace(".", "")] = 1

    for file in oprate_list:
        if file[1] == "others":
            dir_name = "others"
            src = "{0}{1}{2}".format(folder, seps, file[0])
        else:
            src = "{0}{1}{2}{3}".format(folder, seps, file[0], file[1])
            dir_name = file[1].replace(".", "")

        dir_name = "{0}{1}{2}".format(folder, seps, dir_name)

        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        shutil.move(src=src, dst=dir_name)

        if file_list.get(file[1]):
            file_list[file[1].replace(".", "")] += 1
        else:
            file_list[file[1].replace(".", "")] = 1
    sort_list = sorted(file_list.items(), key=lambda e: e[1], reverse=True)
    file_list = {}
    for item in sort_list:
        file_list[item[0]] = item[1]

    return file_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('floder')
    args = parser.parse_args()

    floders = args.floder
    clean_res = clean_up(floders)
    print("整理完毕！")
    print(clean_res)
