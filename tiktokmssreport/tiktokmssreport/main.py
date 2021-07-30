import os,requests,sys,threading,time
pathNameLength = len(os.path.basename(__file__))
pathModule = __file__[:-pathNameLength]
proxieslist = []
user = ''
request_done = False
times_ran = 0
request_sc = 0
run = True
threads = 3
CYAN = u'\u001b[35m'
RESET = u'\u001b[0m'
threadamount = 10
report_type = 0
object_id = 0
device_id = 0
'''user-type
----------------
----------------'''
reason = 0
def get_report_type():
    global reason,report_type
    print(f'''> ╔[{CYAN}1{RESET} = {CYAN}User{RESET}]
> ║[{CYAN}2{RESET} = {CYAN}All {RESET}user {CYAN}videos{RESET}]
> ║[{CYAN}3{RESET} = {CYAN}Singular{RESET} video]''')
    report_type = input(f'> ╚[{CYAN}Report {RESET}type]: ')
    if report_type == '1':
        reason = 3072
    elif report_type == '2':
        reason = 399
    elif report_type == '3':
        reason = 1002
    else:
        sys.exit(0)
def get_info():
    global threadamount,user,device_id
    user = input(f'> ╔[{CYAN}UserID{RESET}]: ')
    threadamount = input(f'> ║[{CYAN}Threads{RESET}({RESET}{CYAN}30{RESET} threads{CYAN} recommended{RESET})]: ')
    device_id = input(f'> ║[{CYAN}Device ID{RESET}]: ')
    input(f'> ╚[{CYAN}Press{RESET} enter{CYAN} to{RESET} start{RESET}]: ')
def get_info2():
    global threadamount,user,object_id,device_id
    user = input(f'> ╔[{CYAN}Owner ID:{RESET}]: ')
    object_id = input(f'> ║[{CYAN}Object ID:{RESET}]: ')
    device_id = input(f'> ║[{CYAN}Device ID{RESET}]: ')
    threadamount = input(f'> ║[{CYAN}Threads{RESET}({RESET}{CYAN}30{RESET} threads{CYAN} recommended{RESET})]: ')
    input(f'> ║[{CYAN}Press{RESET} enter{CYAN} to{RESET} start{RESET}]: ')
def check_proxies():
    global proxieslist
    print(f'> ║[{CYAN}Checking{RESET} proxies{CYAN}...]')
    proxy_file = open(file=pathModule+'proxies.txt',mode='r')
    proxieslist = []
    for line in proxy_file.readlines():
        newline_index = line.rfind('n')
        if newline_index!='1':
            newline = line[0:newline_index-1]
        else:
            newline = '0.0.0.0'
        proxieslist.append(newline)
    newproxylist = []
    for i in range(len(proxieslist)):
        proxy = {'https://':proxieslist[i]}
        try:
            r = requests.get('https://www.Google.com/',proxies=proxy)
            newproxylist.append(proxieslist[i])
            print(f'{RESET}> ║[{CYAN}{i+1}{RESET}/{CYAN}{len(proxieslist)}{RESET}...  {CYAN} Checked{RESET} proxy{CYAN} {proxieslist[i]}{RESET}]')
        except Exception:
            print(f'{RESET}> ║[{CYAN}failed{RESET} to{CYAN} ping{RESET} proxy{CYAN}...{RESET}]')
    proxieslist = newproxylist
def main(payload_type):
    if payload_type == 3:
        payload = {'owner_id': object_id,'object_id': user,'reason': reason,'report_type': 'video'}
        link = f'https://www.tiktok.com/node/report/reasons_put?aid=1988&app_name=tiktok_web&device_platform=web_pc&device_id={device_id}8&region=COM&priority_region=CH&os=windows&referer=&root_referer=&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=de-CH&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F92.0.4515.107+Safari%2F537.36&browser_online=true&verifyFp=verify_krqi2edh_KLaw82Cu_gXIG_4f4z_9Tpj_RFdA0IY1VqgI&app_language=de-DE&timezone_name=Europe%2FZurich&is_page_visible=true&focus_state=true&is_fullscreen=false&history_len=5&battery_info=1'
    else:
        payload ={'owner_id': user,'object_id': user,'reason': reason,'report_type': 'user'}
        link = f'https://www.tiktok.com/node/report/reasons_put?aid=1988&app_name=tiktok_web&device_platform=web_pc&device_id={device_id}&region=COM&priority_region=CH&os=windows&referer=&root_referer=&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=de-CH&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F92.0.4515.107+Safari%2F537.36&browser_online=true&verifyFp=verify_krjl931y_WYAl14JB_b1CI_4tNy_922U_ghJgWujl6ZzI&app_language=de-DE&timezone_name=Europe%2FZurich&is_page_visible=true&focus_state=true&is_fullscreen=false&history_len=3&battery_info=1'
    def singular_thread():
        global times_ran,request_done,request_sc
        while run:
            for i in range(len(proxieslist)):
                try:
                    r = requests.post(link,proxies={'https://':proxieslist[i]},data=payload)
                except Exception:
                    request_sc = 403
                if r.status_code == 200:
                    times_ran+=1
                request_done = True
                request_sc = r.status_code
    def print_stuff():
        global request_done,request_sc
        while run:
            if request_done:
                if request_sc == 200:
                    print(f'{RESET}> ║[{CYAN}+{RESET}] {CYAN}successfully {RESET}reported{CYAN}!{RESET} times {CYAN}reported{RESET}: {CYAN}{times_ran}{RESET}]')
                else:
                    print(f'{RESET}> ║[{CYAN}-{RESET}] {CYAN}timed {RESET}out]')
                request_done = False
    def make_threads():
        global run
        try:
            threads = []
            for i in range(int(threadamount)):
                t = threading.Thread(target=singular_thread)
                t.daemon = True
                t2 = threading.Thread(target=print_stuff)
                threads.append(t)
            for i in range(int(threadamount)):
                threads[i].start()
            t2.start()
            while True:
                time.sleep(100)
        except KeyboardInterrupt:
            run = False
    make_threads()
def what_to_do():
    get_report_type()
    if report_type == '3':
        get_info2()
    else:
        get_info()
    check_proxies()
    main(report_type)
if __name__ == '__main__':
    what_to_do()