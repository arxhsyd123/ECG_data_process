import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import cv2
import sys
import os


#filename_csv = '/data1/ar/data_process/data/mitbih_database/100.csv'
#将其字符串变为‘100’
def change_name(name):
    parts = name.split('/')
    # 获取文件名部分
    filename_with_extension = parts[-1]

    # 使用字符串分割操作，按照 '.' 分割，获取文件名和扩展名
    filename, extension = filename_with_extension.split('.')

    return filename

def chage_name2(name):
    parts = name.split('/')
    result = parts[-1]
    return result

def draw_pictures(data_frame, raw_data,filename_csv):
    #生成图片的存放地址
    directory = '/data1/ar/data_process/ecg_data_demo'

    labels = []
    file_name = []

    #第一个和最后两个样本不要
    for i in range(1,len(data_frame['labels'])-1):
        fig = plt.figure(frameon=True)
        labels.append(data_frame['labels'][i])
        #plt.plot(raw_data[2][data_frame['sample_dot'][i]-50:data_frame['sample_dot'][i]+150])
        plt.plot(raw_data[2][data_frame['sample_dot'][i - 1] + 20:data_frame['sample_dot'][i + 1] - 20])
        plt.xticks([]), plt.yticks([])
        for spine in plt.gca().spines.values():
            spine.set_visible(False)
        filename = directory + '/' + change_name(filename_csv)+str(data_frame['sample_dot'][i]) + data_frame['labels'][i] + '.jpg'
        fig.savefig(filename)
        file_name.append(chage_name2(filename))

        im_gray = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        im_gray = cv2.resize(im_gray, (128, 128), interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite(filename, im_gray)
        plt.close()

    dataset_frame = {'file_name': file_name, 'labels': labels}
    dataset_frame = pd.DataFrame(dataset_frame)

    #dataset_frame保存为csv文件
    csv_filename = change_name(filename_csv)

    #csv存放地址
    csv_path = '/data1/ar/data_process/ecg_data_demo/csv'
    csv_path = os.path.join(csv_path, csv_filename+'.csv')
    dataset_frame.to_csv(csv_path, index=False)
    print(f'DataFrame saved to {csv_path}')


def slice_label_and_dot(annotations):
    labels = []
    sample_dot = []
    for i in range(len(annotations)):
        #label中有/的符号，在读取图片名称时，会报错
        if annotations[i][2] == '/':
            labels.append('P')
        else:
            labels.append(annotations[i][2])
        sample_dot.append(int(annotations[i][1]))
    return labels, sample_dot

if __name__=='__main__':
    fannotation = []
    frecording = []

    #mit-bih数据存放位置
    lst = os.listdir('/data1/ar/data_process/data/mitbih_database')
    lst.sort()
    for file in lst:
        if file.endswith(".csv"):
            frecording.append(file)
        else:
            fannotation.append(file)


    for i in range(len(frecording)):
        print(f"number{i}iter")
        filename_csv= '/data1/ar/data_process/data/mitbih_database' +'/'+ frecording[i]
        print(filename_csv)
        data_csv = pd.read_csv(filename_csv)
        data_csv.columns = list(range(len(data_csv.columns)))

        filename_annotation= '/data1/ar/data_process/data/mitbih_database' +'/'+ fannotation[i]
        print(filename_annotation)
        f = open(filename_annotation, 'r')
        next(f)  # skip first line!
        annotations = []
        for line in f:
            tmp_list = line.split()
            annotations.append(tmp_list)
        f.close


        labels, sample_dot = slice_label_and_dot(annotations)
        data_frame = {'sample_dot': sample_dot, 'labels': labels}
        data_frame = pd.DataFrame(data_frame)


        test_data_frame = draw_pictures(data_frame, data_csv,filename_csv)

    print("successful")




























