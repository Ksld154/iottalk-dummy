import os
import csv
import random
import threading
from time import sleep
from datetime import datetime

import DAN


ServerURL = 'http://demo.iottalk.tw:9999'
Reg_addr = 'CD8677D52' + '181'

DAN.profile['dm_name'] = 'rfidreader'
DAN.profile['df_list'] = ['rfidreader_distance_i', 'rfidreader_phase_i', 'rfidreader_rssi_i', 'rfidreader_filename_i', 'rfidreader_distance_o', 'rfidreader_phase_o', 'rfidreader_rssi_o', 'rfidreader_filename_o']  # noqa
DAN.profile['d_name'] = str(random.randint(100, 999)) + "_puller_"+ DAN.profile['dm_name']  # noqa
DAN.device_registration_with_retry(ServerURL, Reg_addr)


def prettyPrint(title, item):
    print("-----")
    print(title)
    print(item)
    print("-----")


def iottalkPuller():
    data_list = []
    idx = 0

    filename_pulled = False
    csvFileName = ''

    while True:
        try:
            if not filename_pulled:
                ODF_data = DAN.pull('rfidreader_filename_o')
                if ODF_data is not None:
                    print('file')
                    filename_pulled = True
                    csvFileName = ODF_data[0][0]

                    print("-----")
                    print("File Name:")
                    print(csvFileName)
                    print("-----")
                    if csvFileName == "N/A":
                        break

            if 'distance' in csvFileName:
                ODF_data = DAN.pull('rfidreader_distance_o')
                if ODF_data is not None:
                    rfid_distance = ODF_data[0]

                    # prettyPrint('distance:', rfid_distance)
                    data_list.append(rfid_distance)
                    idx += 1
                    # print(idx)
                    print("[distance] ", idx, ": ", ODF_data[0])

                    if rfid_distance == [0, 0, 0, 0, 0, 0]:
                        break

            elif 'rssi' in csvFileName:
                ODF_data = DAN.pull('rfidreader_rssi_o')
                if ODF_data is not None:
                    rfid_rssi = ODF_data[0]

                    # prettyPrint('RSSI: ', rfid_rssi)
                    data_list.append(rfid_rssi)
                    idx += 1
                    # print(idx)
                    print("[rssi] ", idx, ": ", ODF_data[0])

                    if rfid_rssi == [0, 0, 0, 0, 0, 0]:
                        break

            elif 'phase' in csvFileName:
                ODF_data = DAN.pull('rfidreader_phase_o')
                if ODF_data is not None:
                    rfid_phase = ODF_data[0]

                    # prettyPrint('phase: ', rfid_phase)
                    data_list.append(rfid_phase)
                    idx += 1
                    # print(idx)
                    print("[phase] ", idx, ": ", ODF_data[0])

                    if rfid_phase == [0, 0, 0, 0, 0, 0]:
                        break

        except Exception as e:
            print(e)
            sleep(1)

        sleep(0.002)

    if csvFileName == '' or len(data_list) == 0:
        return False, False
    else:
        return csvFileName, data_list


def csvBuilder(output_folder, filename, data_list):
    filename = os.path.join(output_folder, filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for item in data_list:
            entry_len = item[0]
            writer.writerow(item[1:entry_len+1])


if __name__ == "__main__":
    # build output folder
    current_time = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    output_folder = os.path.join(os.getcwd(), current_time)
    os.mkdir(output_folder)
    print(output_folder)

    t_list = []

    while True:
        csvFileName, data_list = iottalkPuller()
        if not csvFileName:
            print("error!")
            break

        # output csv file
        new_thread = threading.Thread(target=csvBuilder, args=(output_folder, csvFileName, data_list))  # noqa
        new_thread.start()
        t_list.append(new_thread)
        print(csvFileName)

    for t in t_list:
        t.join()
