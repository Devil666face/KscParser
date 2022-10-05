# #!/usr/bin/python -tt
# -*- coding: utf-8 -*-
from gettext import find
import csv
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
        self.result_list = list()
        # self.group_dict = dict()

    def find_cert(self):
        """Find klserver.cer"""
        print(KscParser.find_cert.__doc__)
        return (next(Path("C:\\","ProgramData","KasperskyLab").rglob("klserver.cer")))

    # def EnumerateGroups(self, oGroups, nLevel):
    #     for oGroup in oGroups:
    #         self.group_dict[oGroup['id']] = oGroup['name']
    #         if 'groups' in oGroup:
    #             groups = oGroup['groups']
    #             self.EnumerateGroups(groups, nLevel + 1)

    def find_hosts_by_query(self, query):
        self.fields_to_select =  ["KLHST_WKS_DN","KLHST_WKS_LAST_UPDATE","KLHST_INSTANCEID","KLHST_WKS_WINHOSTNAME","KLHST_WKS_WINDOMAIN","KLHST_WKS_FQDN"]
        strAccessor = KlAkOAPI.HostGroup.KlAkHostGroup(self.server).FindHosts(query, self.fields_to_select, [], {'KLGRP_FIND_FROM_CUR_VS_ONLY': False}, lMaxLifeTime = 60 * 60).OutPar('strAccessor')
        oChunkAccessor = KlAkOAPI.ChunkAccessor.KlAkChunkAccessor (self.server)    
        nCount = oChunkAccessor.GetItemsCount(strAccessor).RetVal()

        # oHostGroup = KlAkHostGroup(self.server)
        # nRootGroupID = oHostGroup.GroupIdGroups().RetVal()
        # oSubgroups = oHostGroup.GetSubgroups(nRootGroupID, 0).RetVal()
        # if oSubgroups == None or len(oSubgroups) == 0:
        #     print('Root group is empty')
        # else:
        #     self.EnumerateGroups(oSubgroups, 0)

        nStep = 100
        for nStart in range(0, nCount, nStep):
            oChunk = oChunkAccessor.GetItemsChunk(strAccessor, nStart, nStep)
            oHosts = oChunk.OutPar('pChunk')['KLCSP_ITERATOR_ARRAY']
            for oObj in oHosts:
                self.result_list.append([self.get_field(oObj, field) for field in self.fields_to_select])

        return self.result_list

    def get_field(self, oObj, field_name):
        # if field_name == 'KLHST_WKS_GROUPID':
        #     return self.group_dict.get(oObj['KLHST_WKS_GROUPID'],'No group')
        try:
            return oObj[field_name]
        except:
            return "-"

    def save_in_csv(self, table_name, data):
        with open(f'{table_name}.csv','w',encoding='cp1251',newline='') as file:
            writer = csv.writer(file,delimiter=';')
            for row in data:
                writer.writerow(row)

    
# def get_ksc_server(username:str, password:str, server_port):
#     server_address = socket.getfqdn()
#     server_url = f'https://{server_address}:{server_port}'
#     path_to_SSL_verify_cert = 'C:\\ProgramData\\KasperskyLab\\adminkit\\1093\\cert\\klserver.cer'
#     server = KlAkAdmServer.Create(server_url, username, password, verify = path_to_SSL_verify_cert) 
#     return server
    
# def FindHostsByQueryString(server, strQueryString):
#     strAccessor = KlAkOAPI.HostGroup.KlAkHostGroup(server).FindHosts(strQueryString, ["KLHST_WKS_HOSTNAME", "KLHST_WKS_DN"], [], {'KLGRP_FIND_FROM_CUR_VS_ONLY': True}, lMaxLifeTime = 60 * 60).OutPar('strAccessor')
#     # nStart = 0
#     # nStep = 100
#     oChunkAccessor = KlAkOAPI.ChunkAccessor.KlAkChunkAccessor (server)    
#     nCount = oChunkAccessor.GetItemsCount(strAccessor).RetVal()
#     print("Found hosts for query string:", nCount)
#     oResult = KlAkOAPI.Params.KlAkArray([])
#     nStep = 100
#     for nStart in range(0, nCount, nStep):
#     # while nStart < nCount:
#         oChunk = oChunkAccessor.GetItemsChunk(strAccessor, nStart, nStep)
#         oHosts = oChunk.OutPar('pChunk')['KLCSP_ITERATOR_ARRAY']
#         for oObj in oHosts:
#             print("Found host: " + oObj["KLHST_WKS_DN"]);
#             oResult.Add(oObj.GetValue("KLHST_WKS_HOSTNAME"))
#     #     nStart += nStep   
#     return oResult

def main():
    # server = KlAkAdmServer.Create("https://ksc.example.com:13299", "username", "password", verify = False)
    # server = get_ksc_server(username='kladmin', password='ghjcdtfub65D', server_port=13299)
    # host_name_list = FindHostsByQueryString(server, "")
    # print(len(host_name_list))
    server = KscParser(username='', password='', server_port=13299, find_cert=False)
    hosts = server.find_hosts_by_query("")
    print(len(hosts))
    server.save_in_csv(table_name='host',data=hosts)
    


if __name__=='__main__':
    main()
