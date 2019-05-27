import os
import pandas as pd


def file_split(filename, file_num, header=True):
    # 根据是否有表头执行不同程序，默认是否表头的
    if header:
        # 获得每个文件需要有的行数
        chunksize = 400000  # 先初始化的chunksize是100W
        data1 = pd.read_csv(filename, chunksize=chunksize, sep=',', encoding='gbk')
        num = 0
        for chunk in data1:
            num += len(chunk)
        chunksize = round(num / file_num + 1)

        # 需要存的file
        head, tail = 'movie','01'
        data2 = pd.read_csv(filename, chunksize=chunksize, sep=',', encoding='gbk', low_memory=False)
        i = 0  # 定文件名
        for chunk in data2:
            chunk.to_csv('{0}_{1}{2}.csv'.format(head, i, tail), header=None, index=False)
            print('保存第{0}个数据'.format(i))
            i += 1
    else:
        # 获得每个文件需要有的行数
        chunksize = 400000  # 先初始化的chunksize是100W
        data1 = pd.read_csv(filename, chunksize=chunksize, header=None, sep=',', low_memory=False)
        num = 0
        for chunk in data1:
            num += len(chunk)
        chunksize = round(num / file_num + 1)

        # 需要存的file
        head, tail = 'movie','01'
        data2 = pd.read_csv(filename, chunksize=chunksize, header=None, sep=',', low_memory=False)
        i = 0  # 定文件名
        for chunk in data2:
            chunk.to_csv('{0}_{1}{2}.csv'.format(head, i, tail), header=None, index=False)
            print('保存第{0}个数据'.format(i))
            i += 1


if __name__ == '__main__':
    filename = 'movie_data.csv'
    file_split(filename, 6, header=False)