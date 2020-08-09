from time import sleep
import time, csv, random
import DAN


ServerURL = 'http://demo.iottalk.tw:9999'
Reg_addr = 'CD8677D52' + '181'

DAN.profile['dm_name']='rfidreader'
DAN.profile['df_list']=['rfidreader_distance_i', 'rfidreader_phase_i', 'rfidreader_rssi_i', 'rfidreader_filename_i', 'rfidreader_distance_o', 'rfidreader_phase_o', 'rfidreader_rssi_o', 'rfidreader_filename_o']
DAN.device_registration_with_retry(ServerURL, Reg_addr)


distance_list = []
rssi_list = []

distance_idx = 0
rssi_idx = 0
filename_pulled = False

while True:
    try:

        if filename_pulled == False:
            ODF_data = DAN.pull('rfidreader_filename_o')
            if ODF_data != None: 
                print('file')
                filename_pulled = True
                csvFileName = ODF_data[0]

                print("-----")
                print("File Name:")
                print(csvFileName)
                print("-----")


        ODF_data = DAN.pull('rfidreader_distance_o')   
        if ODF_data != None:
            rfid_distance = ODF_data[0]
            print("-----")
            print("distance:")
            print(rfid_distance)
            distance_list.append(rfid_distance)
            print("-----")
            distance_idx += 1
            print(distance_idx)

            if rfid_distance == [1,0,0,0,0,0]:
                break


    

    except Exception as e:
        print(e)
        sleep(1)

    sleep(0.002)
    
