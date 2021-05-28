import json
import re
import binascii
'''
"{0:#0{1}x}".format(42,6)
'0x002a'
{   # Format identifier
0:  # first parameter
#   # use "0x" prefix
0   # fill with zeroes
{1} # to a length of n characters (including 0x), defined by the second parameter
x   # hexadecimal number, using lowercase letters for a-f
}   # End of format identifier
"{0:0{1}x}".format(address, 4)
'''

def ConvertToHex(conf_data):

    temp = conf_data["hardware_rev"]
    temp = int(temp, 10)
    temp = "{0:0{1}x}".format(temp, 2)
    conf_data["hardware_rev"] = temp

    temp = conf_data["hardware_type"]
    temp = int(temp, 10)
    temp = "{0:0{1}x}".format(temp, 2)
    conf_data["hardware_type"] = temp

    #temp = conf_data["firmware_version"].encode("utf-8").hex()
    #conf_data["firmware_version"] = temp.upper()

    temp = conf_data["serial_number"]
    temp = int(temp, 10)
    temp = "{0:0{1}x}".format(temp, 8)
    temp = re.findall(r'.{2}', temp)
    temp.reverse()
    temp = "".join(temp)
    conf_data["serial_number"] = temp

    temp = conf_data["identifier_number"]
    temp = int(temp, 10)
    temp = "{0:0{1}x}".format(temp, 8)
    temp = re.findall(r'.{2}', temp)
    temp.reverse()
    temp = "".join(temp)
    conf_data["identifier_number"] = temp

    temp = conf_data["name_dcu"].encode("utf-8").hex()
    conf_data["name_dcu"] = temp.upper()

    temp = conf_data["cmd_password_dcu"].encode("utf-8").hex()
    conf_data["cmd_password_dcu"] = temp.upper()

    temp = conf_data["cmd_login_dcu"].encode("utf-8").hex()
    conf_data["cmd_login_dcu"] = temp.upper()

    temp = int(conf_data["dns_enable"], 10)
    temp = "{0:0{1}x}".format(temp, 2)
    conf_data["dns_enable"] = temp.upper()

    temp = int(conf_data["dhcp_enable"], 10)
    temp = "{0:0{1}x}".format(temp, 2)
    conf_data["dhcp_enable"] = temp.upper()

    temp = conf_data["mac_address"].split(":")
    str_temp = ""
    for item in temp:
        item = int(item, 16)
        str_temp = str_temp + "{0:0{1}x}".format(item, 2)
    conf_data["mac_address"] = str_temp.upper()

    temp = conf_data["ip_source"].split(".")
    str_temp = ""
    for item in temp:
        item = int(item, 10)
        str_temp = str_temp + "{0:0{1}x}".format(item, 2)
    conf_data["ip_source"] = str_temp.upper()

    temp = conf_data["mask"].split(".")
    str_temp = ""
    for item in temp:
        item = int(item, 10)
        str_temp = str_temp + "{0:0{1}x}".format(item, 2)
    conf_data["mask"] = str_temp.upper()

    temp = conf_data["ip_gateway"].split(".")
    str_temp = ""
    for item in temp:
        item = int(item, 10)
        str_temp = str_temp + "{0:0{1}x}".format(item, 2)
    conf_data["ip_gateway"] = str_temp.upper()

    temp = conf_data["ip_dds_first"].split(".")
    str_temp = ""
    for item in temp:
        item = int(item, 10)
        str_temp = str_temp + "{0:0{1}x}".format(item, 2)
    conf_data["ip_dds_first"] = str_temp.upper()

    temp = conf_data["ip_dds_second"].split(".")
    str_temp = ""
    for item in temp:
        item = int(item, 10)
        str_temp = str_temp + "{0:0{1}x}".format(item, 2)
    conf_data["ip_dds_second"] = str_temp.upper()

    temp = conf_data["ip_dns"].split(".")
    str_temp = ""
    for item in temp:
        item = int(item, 10)
        str_temp = str_temp + "{0:0{1}x}".format(item, 2)
    conf_data["ip_dns"] = str_temp.upper()

    temp = conf_data["url_dds_first"].encode("utf-8").hex()
    conf_data["url_dds_first"] = temp.upper()

    temp = conf_data["url_dds_second"].encode("utf-8").hex()
    conf_data["url_dds_second"] = temp.upper()

    temp = conf_data["identifier_scu_number"]
    temp = int(temp, 10)
    temp = "{0:0{1}x}".format(temp, 8)
    temp = re.findall(r'.{2}', temp)
    temp.reverse()
    temp = "".join(temp)
    conf_data["identifier_scu_number"] = temp

    temp = conf_data["numbers_slave"]
    temp = int(temp, 10)
    temp = "{0:0{1}x}".format(temp, 2)
    conf_data["numbers_slave"] = temp

    return conf_data

def ArrangeBytes(data):
    eeprom = ""
    # 0 page - reset and bootloader - reset off
    eeprom = eeprom + "AA00{:F<28}".format("")
    # 1 page - reserve for future
    eeprom = eeprom + "{:F<32}".format("")
    # 2 page - ip source
    eeprom = eeprom + "{:F<32}".format(data["ip_source"])
    # 3 page - ip dest - empty
    eeprom = eeprom + "{:F<32}".format("")
    # 4 page - ip gateway
    eeprom = eeprom + "{:F<32}".format(data["ip_gateway"])
    # 5 page - mask
    eeprom = eeprom + "{:F<32}".format(data["mask"])
    # 6 page - mac
    eeprom = eeprom + "{:F<32}".format(data["mac_address"])
    # 7 page - ip dns
    eeprom = eeprom + "{:F<32}".format(data["ip_dns"])
    # 8, 9 page - url - not used
    eeprom = eeprom + "{:F<64}".format("")
    # 10 page - login
    eeprom = eeprom + "{:0<32}".format(data["cmd_login_dcu"])
    # 11 page - password
    eeprom = eeprom + "{:0<32}".format(data["cmd_password_dcu"])
    # 12 page - name dcu
    eeprom = eeprom + "{:0<32}".format(data["name_dcu"])
    # 13 page - version
    eeprom = eeprom + "{:F<32}".format("")
    # 14 page - dns_dhcp enable
    eeprom = eeprom + "{:F<32}".format(data["dns_enable"] + data["dhcp_enable"])
    # 15 page - hardware type
    eeprom = eeprom + "{:F<32}".format(data["hardware_type"])
    # 16 page - hardware revision
    eeprom = eeprom + "{:F<32}".format(data["hardware_rev"])
    # 17 page - serial_number
    eeprom = eeprom + "{:F<32}".format(data["serial_number"])
    # 18 page - identifier
    eeprom = eeprom + "{:F<32}".format(data["identifier_number"])
    # 19 page - first dds ip destination
    eeprom = eeprom + "{:F<32}".format(data["ip_dds_first"])
    # 20 page - second dds ip destination
    eeprom = eeprom + "{:F<32}".format(data["ip_dds_second"])
    # 21, 22 page - first dds url
    eeprom = eeprom + "{:0<64}".format(data["url_dds_first"])
    # 23, 24 page - second dds url
    eeprom = eeprom + "{:0<64}".format(data["url_dds_second"])
    # 25 - scu id
    eeprom = eeprom + "{:F<32}".format(data["identifier_scu_number"])
    # 26 - numbers slave board
    eeprom = eeprom + "{:F<32}".format(data["numbers_slave"])

    eeprom = eeprom.upper()
    return eeprom

def AddingHead(data):
    data_list = re.findall(r'.{32}', data)
    end_data = []
    address = 0

    for part_data in data_list:
        one_row_hex = "10{0:0{1}x}00".format(address, 4) + part_data
        one_row = re.findall(r'.{2}', one_row_hex)
        sum = 0
        for byte_hex in one_row:
            sum = sum + int(byte_hex, 16)
        sum = sum%256
        crc = 256 - sum
        crc = crc % 256
        one_row_hex = ":" + one_row_hex + "{0:0{1}x}".format(crc, 2)
        address = address + 16
        end_data.append(one_row_hex.upper())

    return end_data

def main():
    conf_file = open("config_eeprom.json", "r")
    conf_data = json.load(conf_file)
    conf_file.close()

    name_file = conf_data["name_file"]

    conf_data = ConvertToHex(conf_data)
    eeprom_data = ArrangeBytes(conf_data)
    ready_eeprom = AddingHead(eeprom_data)

    out_file = open(name_file+".eep", "w")
    for row in ready_eeprom:
        out_file.write(row+"\n")

    out_file.write(":00000001FF")
    out_file.close()

    #temp = "{:0<64}".format(temp)

    print(conf_data)


if __name__ == "__main__":
    # execute only if run as a script
    main()