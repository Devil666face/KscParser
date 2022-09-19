# #!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import csv
from gettext import find
import pathlib
import socket
from sys import platform
import KlAkOAPI.AsyncActionStateChecker
import KlAkOAPI.Params
import KlAkOAPI.ChunkAccessor
from pathlib import Path
from KlAkOAPI.Params import KlAkArray
from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI.HostGroup import KlAkHostGroup
from KlAkOAPI.UaControl import KlAkUaControl
from KlAkOAPI.Updates import KlAkUpdates

class KscParser:
    def __init__(self, username:str, password:str, server_port, find_cert=False):
        server_address = socket.getfqdn()
        server_url = f'https://{server_address}:{server_port}'
        path_to_SSL_verify_cert = 'C:\\ProgramData\\KasperskyLab\\adminkit\\1093\\cert\\klserver.cer' if not find_cert else self.find_cert()
        self.server = KlAkAdmServer.Create(server_url, username, password, verify = path_to_SSL_verify_cert) 
        self.rusult_list = list()

    def find_cert(self):
        """Find klserver.cer"""
        print(KscParser.find_cert.__doc__)
        return (next(Path("C:\\","ProgramData","KasperskyLab").rglob("klserver.cer")))

    def get_updates(self):
        update_obj = KlAkUpdates(self.server)
        update_list = update_obj.GetUpdatesInfo([]).RetVal()
        
        for update in update_list:
            self.rusult_list.append([update.GetValue('FileName'),self.replacer(update.GetValue('Date').get('value')),update.GetValue('KLUPDSRV_BUNDLE_ID'),update.GetValue('KLUPDSRV_BUNDLE_TYPE_DESCR'),self.replacer(update.GetValue('KLUPDSRV_BUNDLE_DWL_DATE').get('value'))])
        return(self.rusult_list)

    def save_in_csv(self, data):
        with open('updates.csv','w',encoding='cp1251',newline='') as file:
            writer = csv.writer(file,delimiter=';')
            writer.writerow(['Имя файла обновлений','Дата обновления','Имя пакета','Описание пакета','Время загрузки пакета'])
            for row in data:
                writer.writerow(row)

    def replacer(self,string):
        return string.replace('T',' ').replace('Z',' ')
def main():
    server = KscParser(username='kladmin', password='ghjcdtfub65D', server_port=13299, find_cert=False)
    update_result_list = server.get_updates()
    server.save_in_csv(update_result_list)

if __name__=='__main__':
    main()