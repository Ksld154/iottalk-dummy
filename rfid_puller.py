from time import sleep
import csv, os, random
import DAN
from datetime import datetime


ServerURL = 'http://demo.iottalk.tw:9999'
Reg_addr = 'CD8677D52' + '181'

DAN.profile['dm_name'] = 'rfidreader'
DAN.profile['df_list'] = ['rfidreader_distance_i', 'rfidreader_phase_i', 'rfidreader_rssi_i', 'rfidreader_filename_i', 'rfidreader_distance_o', 'rfidreader_phase_o', 'rfidreader_rssi_o', 'rfidreader_filename_o']
DAN.profile['d_name'] = str( random.randint(100,999 ) ) + "_puller_"+ DAN.profile['dm_name']
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

            if filename_pulled == False:
                ODF_data = DAN.pull('rfidreader_filename_o')
                if ODF_data != None: 
                    print('file')
                    filename_pulled = True
                    csvFileName = ODF_data[0][0]

                    print("-----")
                    print("File Name:")
                    print(csvFileName)
                    print("-----")

            if 'distance' in csvFileName:
                ODF_data = DAN.pull('rfidreader_distance_o')   
                if ODF_data != None:
                    rfid_distance = ODF_data[0]

                    prettyPrint('distance:', rfid_distance)
                    data_list.append(rfid_distance)
                    idx += 1
                    print(idx)

                    if rfid_distance == [1,0,0,0,0,0]:
                        break

            elif 'rssi' in csvFileName:
                ODF_data = DAN.pull('rfidreader_rssi_o')   
                if ODF_data != None:
                    rfid_rssi = ODF_data[0]
                    
                    prettyPrint('RSSI: ', rfid_rssi)
                    data_list.append(rfid_rssi)
                    idx += 1
                    print(idx)

                    if rfid_rssi == [1,0,0,0,0,0]:
                        break
            
            elif 'phase' in csvFileName:
                ODF_data = DAN.pull('rfidreader_phase_o')   
                if ODF_data != None:
                    rfid_phase = ODF_data[0]
                    
                    prettyPrint('phase: ', rfid_phase)
                    data_list.append(rfid_phase)
                    idx += 1
                    print(idx)

                    if rfid_phase == [1,0,0,0,0,0]:
                        break

        except Exception as e:
            print(e)
            sleep(1)

        sleep(0.002)
    
    if csvFileName == '' or len(data_list) == 0:
        return False, False
    else:
        return csvFileName, data_list


def csvBuilder(filename, data_list):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ')

        for item in data_list:
            entry_len = item[0]
            writer.writerow(item[1:entry_len+1])


if __name__ == "__main__":
    csvFileName, data_list = iottalkPuller()
    if csvFileName == False:
        print("error!")
        exit()


    # build output folder    
    current_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    output_folder = os.path.join(os.getcwd(), current_time)
    os.mkdir(output_folder)
    print(output_folder)


    # output csv file
    csvFileName = os.path.join(output_folder, csvFileName)
    csvBuilder(csvFileName, data_list)
    print(csvFileName)