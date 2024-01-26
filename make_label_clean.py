import os
import pandas as pd
fannotation = []
frecording = []
lst = os.listdir('/data1/ar/data_process/ecg_data/csv')
lst.sort()
print(len(lst))
DS1 = [101, 106, 108, 109, 112, 114, 115, 116, 118, 119, 122, 124, 201, 203, 205, 207, 208, 209, 215, 220, 223, 230]
DS2 = [100, 103, 105, 111, 113, 117, 121, 123, 200, 202, 210, 212, 213, 214, 219, 221, 222, 228, 231, 232, 233, 234]
MITBIH_classes = ['N', 'L', 'R', 'e', 'j', 'A', 'a', 'J', 'S', 'V', 'E', 'F']  # , 'P', '/', 'f', 'u']
AAMI_classes = []
AAMI_classes.append(['N', 'L', 'R'])  # N label-0
AAMI_classes.append(['A', 'a', 'J', 'S', 'e', 'j'])  # SVEB label-1
AAMI_classes.append(['V', 'E'])  # VEB label-2
AAMI_classes.append(['F'])  # F label-3
# AAMI_classes.append(['P', '/', 'f', 'u'])              # Q drop


def clean_label_csv(datalist,AAMI_classes,root_dic):
    clean_list = []
    file_names = []
    for data in datalist:
        data_csv = pd.read_csv(os.path.join(root_dic,str(data)+'.csv'))
        labels_list = data_csv['labels'].tolist()
        file_name = data_csv['file_name'].tolist()
        for i in range(len(labels_list)):
            for j in range(len(AAMI_classes)):
                if labels_list[i] in AAMI_classes[j]:
                    clean_list.append(j)
                    file_names.append(file_name[i])
                    break
    dataset_frame = {'file_name': file_names, 'labels': clean_list}
    test_dataset_frame = pd.DataFrame(dataset_frame)
    #csv_path = '/data1/ar/data_process/DS1.csv'
    csv_path = '/data1/ar/data_process/DS2.csv'

    test_dataset_frame.to_csv(csv_path, index=False)
    print(f'DataFrame saved to {csv_path}')

#clean_label_csv(DS1, AAMI_classes, '/data1/ar/data_process/ecg_data/csv')
clean_label_csv(DS2,AAMI_classes,'/data1/ar/data_process/ecg_data/csv')








# label_dic = {}
#
# file_csv = pd.read_csv('/data1/ar/data_process/DS1.csv')
# labels_list = file_csv['labels'].tolist()
# for i in range(len(labels_list)):
#     label_dic[labels_list[i]] = label_dic.get(labels_list[i],0)+1
# print(label_dic)