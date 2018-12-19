#!/usr/bin/env python
# -*- coding:utf-8 -*-
#########################################################################
# File Name: nmap_all_server.py
# Program function:自动探测所有服务器，发现端口扫描、探测。
# Author:Jeson
# mail:iaskjob@163.com
# Created Time: 四  6/16 11:13:39 2016
# pip install paramiko python-nmap
#========================================================================

import paramiko
import traceback




import logging
logger = logging.getLogger("django")


class J_ssh_do(object):
    def __init__(self,info=""):
        self.whitelist = ""
        self.result = {"info":info}

    def pass_do(self,login_info,cmd_list=""):
        '''
        用户密码方式登录
        :param login_info:登录的信息，如：('192.168.6.11', 22, 'root', '123')
        :param cmd_list:登录机器后，需要执行的命令
        :return:
        '''
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(login_info[0],login_info[1],login_info[2],login_info[3],timeout=3)
            self.result["status"] = "success"
            for cmd in cmd_list:
                stdin,stdout,stderr = ssh.exec_command(cmd,timeout=10)
                std_res = stdout.read()
                self.result[cmd] = std_res
        except Exception as e :
            self.result["status"] = "failed"
            self.result["res"] = str(e)
        return self.result