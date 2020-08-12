import os
import csv
import time
import random

import DAN


ServerURL = 'http://demo.iottalk.tw:9999'  # with non-secure connection
Reg_addr = 'CD1234D49' + '100'

DAN.profile['dm_name'] = 'rfidreader'
DAN.profile['df_list'] = ['rfidreader_distance_i', 'rfidreader_phase_i', 'rfidreader_rssi_i', 'rfidreader_filename_i', 'rfidreader_distance_o', 'rfidreader_phase_o', 'rfidreader_rssi_o', 'rfidreader_filename_o']  # noqa
DAN.profile['d_name'] = str(random.randint(100, 999)) + '_pusher_' + DAN.profile['dm_name']  # noqa
DAN.device_registration_with_retry(ServerURL, Reg_addr)

CsvFileRoot = os.path.join(os.getcwd(), 'GC/reader_data/ML_realdata/gc_dis_ang_ori/')  # noqa


def csvFileScanner():
    global CsvFileRoot
    files = os.listdir(CsvFileRoot)
    csvFiles = []

    for f in files:
        if f.endswith('.csv'):
            csvFiles.append(f)

    return csvFiles


def pushSingleRow(featureName, idx, total_rows, data_entry):
    pass


def iottalkPusher(csvFile):
    global CsvFileRoot

    # CsvFilePath = 'distance_circle_0_50_0_1_1.csv'
    csvData = open(CsvFileRoot+csvFile, newline='')
    data_rows = list(csv.reader(csvData))
    total_rows = len(data_rows)

    idx = 0
    csvData.close()

    filename_pushed = False
    while True:
        try:

            if not filename_pushed:
                push_res = DAN.push('rfidreader_filename_i', [csvFile])
                if push_res:
                    print(csvFile)
                    filename_pushed = True
                continue

            if 'distance' in csvFile:
                if idx == total_rows:
                    DAN.push('rfidreader_distance_i', [1, 0, 0, 0, 0, 0])
                    break

                push_result = True
                data_entry = data_rows[idx]
                print(idx)
                print(data_entry)
                push_result = push_result and DAN.push('rfidreader_distance_i', [len(data_entry), data_entry[0] if len(data_entry) >= 1 else 0,  data_entry[1] if len(data_entry) >= 2 else 0,  data_entry[2] if len(data_entry) >= 3 else 0,  data_entry[3] if len(data_entry) >= 4 else 0,  data_entry[4] if len(data_entry) >= 5 else 0])  # noqa
                if idx < total_rows and push_result is not None:
                    idx += 1

            elif 'rssi' in csvFile:
                if idx == total_rows:
                    DAN.push('rfidreader_rssi_i', [1, 0, 0, 0, 0, 0])
                    break

                push_result = True
                data_entry = data_rows[idx]
                print(idx)
                print(data_entry)
                push_result = push_result and DAN.push('rfidreader_rssi_i', [len(data_entry), data_entry[0] if len(data_entry) >= 1 else 0,  data_entry[1] if len(data_entry) >= 2 else 0,  data_entry[2] if len(data_entry) >= 3 else 0,  data_entry[3] if len(data_entry) >= 4 else 0,  data_entry[4] if len(data_entry) >= 5 else 0])  # noqa
                if idx < total_rows and push_result is not None:
                    idx += 1

            elif 'phase' in csvFile:
                if idx == total_rows:
                    DAN.push('rfidreader_phase_i', [1, 0, 0, 0, 0, 0])
                    break

                push_result = True
                data_entry = data_rows[idx]
                print(idx)
                print(data_entry)
                push_result = push_result and DAN.push('rfidreader_phase_i', [len(data_entry), data_entry[0] if len(data_entry) >= 1 else 0,  data_entry[1] if len(data_entry) >= 2 else 0,  data_entry[2] if len(data_entry) >= 3 else 0,  data_entry[3] if len(data_entry) >= 4 else 0,  data_entry[4] if len(data_entry) >= 5 else 0])  # noqa
                if idx < total_rows and push_result is not None:
                    idx += 1

        except Exception as e:
            print(e)
            if str(e).find('mac_addr not found:') != -1:
                print('Reg_addr is not found. Try to re-register...')
                DAN.device_registration_with_retry(ServerURL, Reg_addr)
            else:
                print('Connection failed due to unknow reasons.')
                time.sleep(1)

        time.sleep(0.5)


if __name__ == "__main__":
    # csvFiles = csvFileScanner()

    # for f in csvFiles:
    #     iottalkPusher(f)

    # iottalkPusher('distance_circle_0_50_0_1_1.csv')
    # iottalkPusher('rssi_circle_0_50_0_1_1.csv')
    iottalkPusher('distance_circle_0_50_0_3_1.csv')
