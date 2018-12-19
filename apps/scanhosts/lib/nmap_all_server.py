import nmap
import telnetlib
import re,time


from scanhosts.lib import j_ssh_do



def mac_trans(mac):
    '''
    转化mac地址，将传递到mac进行数据格式的转换
    :param mac:
    :return:
    '''
    if mac:
        mac_lst = mac.split("\n")
        mac_res = [item.replace(":",'').replace("000000000000",'').replace("00000000",'') for item in mac_lst]
        mac_string = "_".join(mac_res)
        return mac_string
    else:
        return ""


def sn_trans(sn):
    '''
    转化SN序列号，将传递到SN号进行数据格式的转换
    :param mac:
    :return:
    '''
    if sn:
        sn_res = sn.replace(" ",'')
        return sn_res
    else:
        return ""


def getsysversion(version_list):
    '''
    提取系统版本
    :param version_list:
    :return:
    '''
    for version_data in version_list:
        v_data_lst = re.findall("vmware|centos|linux|ubuntu|redhat|\d{1,}\.\d{1,}",version_data,re.IGNORECASE)
        if v_data_lst:
            if len(v_data_lst) > 1:
                v_data = " ".join(v_data_lst)
                break
        else:
            v_data = ""
    return v_data




def machine_type_trans(mt):
    '''
    转化类型，将传递到类型进行数据格式的转换
    :param mac:
    :return:
    '''
    if mt:
        mt_res = mt.replace("\n",'')
        return mt_res
    else:
        return ""



class NmapScan(object):
    '''
    扫描类：扫描获取指定网段主机等对象信息
    '''

    def __init__(self,black_list=[]):
        self.black_list = black_list
        self.can_login_lst = {}
        self.not_login_lst = {}
        # self.can_key_login_lst = {}
        # self.key_not_login_lst = {}

    def nmap_allip(self,nmap_net):
        '''
        扫描网段中存活主机
        '''
        nm = nmap.PortScanner()
        nm.scan(hosts=nmap_net,arguments = ' -n -sP -PE')
        hostlist = nm.all_hosts()
        return hostlist

    def nmap_sship(self,ports,nmap_net):
        '''
        扫描主机指定ssh端口是否开通ssh端口
        :param ports:
        :param port_list:
        :param unkown_list:
        :param nmap_net:
        :return:
        '''
        ports = ports
        port_list = ports.split(',')
        # 创建端口扫描对象
        nm = nmap.PortScanner()
        ssh_info = {}
        unkown_list = []
        # 调用扫描方法，参数指定扫描主机hosts，nmap扫描命令行参数arguments
        nm.scan(hosts=nmap_net, arguments='-n -sP -PE')
        tcp_all_ip = nm.all_hosts()
        host_list = []
        for ip in tcp_all_ip:  # 遍历扫描主机
            if nm[ip]['status']['state'] == "up":
                 host_list.append(ip)
                 for port in port_list:
                     try:
                         tm = telnetlib.Telnet(host=ip,port=port,timeout=4)
                         tm_res = tm.read_until("\n",timeout=4)
                         if tm_res:
                             if re.search("ssh",tm_res.lower()):
                                 if ip not in self.black_list:
                                     ssh_info[ip]=port
                                     connet = "IP:%s Port:%s Server:%s"%(ip,port,tm_res.lower())
                             else:
                                 if ip not in unkown_list and ip not in ssh_info.keys():
                                    unkown_list.append(ip)
                         else:
                             if ip not in unkown_list and ip not in ssh_info.keys():
                                unkown_list.append(ip)
                     except EOFError as e:
                         if ip not in unkown_list and ip not in ssh_info.keys():
                            unkown_list.append(ip)
                         unkown_list.append(ip)
                     except Exception as e:
                         if ip not in unkown_list and ip not in ssh_info.keys():
                            unkown_list.append(ip)
        return ssh_info,host_list,list(set(unkown_list))

    def try_login(self,sship_list,password_list,syscmd_list):
        '''
        尝试ssh用户密码登录，获取机器基本信息
        :param sship_list:
        :param password_list:
        :param syscmd_list:
        :return:
        '''
        password_list = password_list
        syscmd_list = syscmd_list
        if isinstance(sship_list, dict):
            ssh_tuple_list = [(ip,port) for ip,port in sship_list.items()]
        elif isinstance(sship_list,list):
            ssh_tuple_list = sship_list
        for ip,port in ssh_tuple_list:
            system_info = ""
            for password in password_list:
                if ip not in self.can_login_lst.keys():
                    login_info = (ip,int(port),'root', password)
                    doobj = j_ssh_do(login_info)
                    res = doobj.pass_do(login_info,syscmd_list)
                    if res["status"] == "success":
                        if self.not_login_lst.has_key(ip):
                            self.not_login_lst.pop(ip)
                        sys_hostname = res["hostname"]
                        sys_mac = mac_trans(res["cat /sys/class/net/[^vtlsb]*/address||esxcfg-vmknic -l|awk '{print $8}'|grep ':'"])
                        sys_sn = sn_trans(res["dmidecode -s system-serial-number"])
                        system_info = getsysversion([res["cat /etc/issue"],res["cat /etc/redhat-release"]])
                        machine_type = machine_type_trans(res["dmidecode -s system-manufacturer"] + res["dmidecode -s system-product-name"])
                        self.can_login_lst[ip] = (port,password,'root',system_info,sys_hostname,sys_mac,sys_sn,machine_type)
                    elif res["status"] == "failed" and re.search(r"reading SSH protocol banner",res["res"]):
                        time.sleep(60)
                    else:
                        if ip not in self.not_login_lst.keys() and ip not in self.can_login_lst.keys():
                            self.not_login_lst[ip] = port
                        # print ip,port,password,traceback.print_exc()
        return self.can_login_lst,self.not_login_lst

