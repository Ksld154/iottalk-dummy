import time, random, requests, csv
import DAN

ServerURL = 'http://demo.iottalk.tw:9999'      #with non-secure connection
Reg_addr = 'CD1234D49' + '100'

DAN.profile['dm_name']='rfidreader'
DAN.profile['df_list']=['rfidreader_distance_i', 'rfidreader_phase_i', 'rfidreader_rssi_i', 'rfidreader_filename_i', 'rfidreader_distance_o', 'rfidreader_phase_o', 'rfidreader_rssi_o', 'rfidreader_filename_o']
DAN.device_registration_with_retry(ServerURL, Reg_addr)


CsvFileRoot = './GC/reader_data/ML_realdata/'
CsvFilePath = 'gc_dis_ang_ori/distance_circle_0_50_0_1_1.csv'
distance = open(CsvFileRoot+CsvFilePath, newline='')
d_rows = list(csv.reader(distance))
d_cnter = 0
distance.close()

def parseCsvFileName(csvFile):
    pass

filename_pushed = False
while True:
    try:        
       
        if filename_pushed == False:
            push_res = DAN.push('rfidreader_filename_i', [CsvFilePath])
            if push_res == True:
                print(CsvFilePath)
                filename_pushed = True
                continue


        print(d_cnter)
        if d_cnter == len(d_rows)-1:
            d_list = d_rows[0]
            DAN.push('rfidreader_distance_i', [1, 0, 0, 0, 0, 0])
            break

        push_result = True
        d_list = d_rows[d_cnter]
        print(d_list)
        push_result = push_result and DAN.push('rfidreader_distance_i', [len(d_list), d_list[0] if len(d_list)>=1 else 0,  d_list[1] if len(d_list)>=2 else 0,  d_list[2] if len(d_list)>=3 else 0,  d_list[3] if len(d_list)>=4 else 0,  d_list[4] if len(d_list)>=5 else 0]) #Push data to an input device feature "Dummy_Sensor"         
        if d_cnter < len(d_rows)-1 and push_result != None:
            d_cnter+=1
       
        # r_list = r_rows[r_cnter]
        # push_result = push_result and DAN.push('rfidreader_rssi_i', [len(r_list), r_list[0] if len(r_list)>=1 else 0,  r_list[1] if len(r_list)>=2 else 0,  r_list[2] if len(r_list)>=3 else 0,  r_list[3] if len(r_list)>=4 else 0,  r_list[4] if len(r_list)>=5 else 0])
        # if r_cnter < len(r_rows)-1 and push_result != None:
        #     r_cnter+=1
       
       
        #==================================

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.2)

