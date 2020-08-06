import time, random, requests, csv
import DAN

CsvFilePath = './GC/reader_data/ML_realdata/'

ServerURL = 'http://demo.iottalk.tw:9999'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = None #if None, Reg_addr = MAC address

DAN.profile['dm_name']='rfidreader'
DAN.profile['df_list']=['rfidreader_distance_i', 'rfidreader_phase_i', 'rfidreader_rssi_i', 'rfidreader_distance_o', 'rfidreader_phase_o', 'rfidreader_rssi_o']
#DAN.profile['d_name']= 'Assign a Device Name' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line

distance = open(CsvFilePath+'gc_dis_ang_ori/distance_circle_0_50_0_1_1.csv', newline='')
d_rows = list(csv.reader(distance))
d_cnter = 0
distance.close()

rssi = open(CsvFilePath+'gc_dis_ang_ori/rssi_circle_0_50_0_1_1.csv', newline='')
r_rows = list(csv.reader(rssi))
r_cnter = 0
rssi.close()

# phase = open(CsvFilePath+'gc_dis_ang_ori/rssi_circle_0_50_0_1_1.csv', newline='')
# p_rows = csv.reader(phase)
# phase.close()

while True:
    try:
        # IDF_data = random.uniform(1, 10)
        d_list = d_rows[d_cnter]
        DAN.push ('rfidreader_distance_i', [len(d_list), d_list[0] if len(d_list)>=1 else 0,  d_list[1] if len(d_list)>=2 else 0,  d_list[2] if len(d_list)>=3 else 0,  d_list[3] if len(d_list)>=4 else 0,  d_list[4] if len(d_list)>=5 else 0]) #Push data to an input device feature "Dummy_Sensor"
        r_list = r_rows[r_cnter]
        DAN.push ('rfidreader_rssi_i', [len(r_list), r_list[0] if len(r_list)>=1 else 0,  r_list[1] if len(r_list)>=2 else 0,  r_list[2] if len(r_list)>=3 else 0,  r_list[3] if len(r_list)>=4 else 0,  r_list[4] if len(r_list)>=5 else 0])

        if d_cnter < len(d_rows)-1:
            d_cnter+=1
        if r_cnter < len(r_rows)-1:
            r_cnter+=1
        #==================================

        ODF_data = DAN.pull('rfidreader_distance_o')#Pull data from an output device feature "Dummy_Control"
        if ODF_data != None:
            print("-----")
            print("d:")
            print(ODF_data[0])
            print("-----")

        ODF_data = DAN.pull('rfidreader_rssi_o')#Pull data from an output device feature "Dummy_Control"
        if ODF_data != None:
            print("-----")
            print("r:")
            print(ODF_data[0])
            print("-----")

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.002)

