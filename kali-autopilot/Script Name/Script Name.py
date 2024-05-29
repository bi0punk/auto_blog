#!/usr/bin/env python3
#Kali Autopilot Generated
#----------------
import cherrypy, os, paramiko, pexpect, re, sarge, string, subprocess, sys, threading, time, re
import netifaces as ni
from random import choice, Random, randint, seed
from functools import wraps
temple = False
fmutex = './mutex.txt'
ftrace = './trace.txt'
iffy = [True]*50
users = {'offsec': 'offsec'}
api_port = 80
ssl_cert = "./Script Name.cert"
ssl_priv_key = "./kali-autopilot.key"
loop = False
delay_all = False
debug = False
trace = False
reset_mutex_on_start = True

#************************************
# Shell main routines               *
#************************************
class Shell:
    meterpreter_prompt = 'meterpreter.* > '
    powershell_prompt = 'PS .+> '
    @classmethod
    def spawn(cls, command, cwd=None, env_mods=None):
        pexpect_object = pexpect_spawn(command, cwd, env_mods)
        return cls(pexpect_object, shell_received=False, prompt=None)
    @classmethod
    def spawn_and_receive(cls, command, prompt, timeout=-1, cwd=None, env_mods=None):
        s = cls.spawn(command, cwd, env_mods)
        s.receive(prompt, timeout=timeout)
        return s
    def __init__(self, pexpect_object, shell_received, prompt):
        self.pexpect_object = pexpect_object
        self.shell_received = shell_received
        self.prompt = prompt
    def send_line(self, line=''):
        print('<' + line + '>', end='')
        self.pexpect_object.sendline(line)
    def expect(self, pattern, timeout=-1):
        try:
            return self.pexpect_object.expect(pattern, timeout=timeout)
        except pexpect.TIMEOUT as e:
            if self.shell_received:
                raise e
            else:
                raise FailedToGetShell from None
    def receive(self, prompt, timeout=-1):
        self.expect(prompt, timeout=timeout)
        self.mark_received(prompt)
    def mark_received(self, prompt):
        self.shell_received = True
        self.prompt = prompt
    def send_command(self, command, expect=None, new_prompt=None, timeout=-1):
        self.send_line(command)
        if new_prompt:
            self.prompt = new_prompt
        self.expect(expect or self.prompt, timeout=timeout)
        return self.output
    @property
    def output(self):
        return self.pexpect_object.before
    def interact(self):
        print('[+] Interacting...')
        self.pexpect_object.logfile_read = None  # Disable logging because it bugs out with interact()
        self.pexpect_object.sendline()
        self.pexpect_object.interact()
    def ctrl_c(self):
        self.pexpect_object.sendcontrol('c')
        self.expect(self.prompt)
    def terminate(self):
        self.pexpect_object.terminate(force=True)
def pexpect_spawn(command, cwd=None, env_mods=None):
    _print_command(command)
    if env_mods:
        env = os.environ.copy()
        env.update(env_mods)
    else:
        env = None
    p = pexpect.spawn(command, cwd=cwd, encoding='utf-8', env=env, timeout=60)
    p.logfile_read = sys.stdout
    p.ignorecase = True
    return p
def exec_command(command, timeout=None, with_exit_status=False, cwd=None, log=True):
    if log:
        _print_command(command)
        logfile = sys.stdout
    else:
        logfile = None
    return pexpect.run(command, withexitstatus=with_exit_status, cwd=cwd, encoding='utf-8', logfile=logfile, timeout=timeout)
def async_exec_command(command, **kwargs):
    t = threading.Thread(target=exec_command, args=(command,), kwargs=kwargs, daemon=True)
    t.start()
def exec_command_with_bash(command, timeout=-1, with_exit_status=False, log=True):
    if log:
        _print_command(command)
        logfile = sys.stdout
    else:
        logfile = None
    p = pexpect.spawn('/bin/bash', ['-c', command], encoding='utf-8', logfile=logfile)
    p.expect(pexpect.EOF, timeout)
    output = p.before
    if with_exit_status:
        p.close()
        return output, p.exitstatus
    else:
        return output
def async_exec_command_with_bash(command, **kwargs):
    t = threading.Thread(target=exec_command_with_bash, args=(command,), kwargs=kwargs, daemon=True)
    t.start()
def _print_command(command):
    combined_whitespace = re.sub(r' +', ' ', command).strip()
    print('[*] Running command:', combined_whitespace)

#************************************
# Lab Challenge Addressing       *
#************************************
def check_deployment():
    global x_subnet
    try:
        ni.ifaddresses('eth0')
        ip=ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    except:
        return False
    ip_array=ip.split('.')
    x_subnet=ip_array[2]
    if x_subnet=='50':
        if not temple:
            return False
    return True
def setup_ip(addr):
    addr_array=addr.split('.')
    addr_array[2]=x_subnet
    final_addr=".".join(addr_array)
    return final_addr

#****************************************
# Paramiko SSH Routines                 *
#****************************************
def paramiko_pmopen(dhost,dport,duser,dpwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=dhost,port=dport,username=duser,password=dpwd,allow_agent=True,timeout=10)
        return ssh
    except:
        print('Failed to connect')
def paramiko_pxopen(phost,puser,dhost,dport,duser,dpwd):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        psock=paramiko.ProxyCommand('ssh -o VisualHostKey=no -W'+dhost+':'+str(dport)+' '+puser+'@'+phost)
        ssh.connect(hostname=dhost,port=dport,username=duser,password=dpwd,allow_agent=True,timeout=10,sock=psock)
        return ssh
    except:
        print('Failed to connect to '+dhost+':'+str(dport))
def paramiko_pcmd(sshc,cmd):
    try:
        stdin,stdout,stderr = sshc.exec_command(cmd) 
        response=stdout.read().decode()
        return(response)
    except:
        return('Command '+cmd+' failed')

#****************************************
# Mutex functions                       *
#****************************************
class SetMutex:
    @cherrypy.expose
    def index(self):
        return "<h2>Kali Autopilot mutex interface</h2><br><br><h3>Example usage:</h3>https://127.0.0.1/set<br>https://127.0.0.1/set?mutex=-3<br>https://127.0.0.1/set?mutex=3<br>https://127.0.0.1/check"
    @cherrypy.expose
    def check(self):
        with open(fmutex,'r') as f:
            mutex=f.read()
            f.close()
        r=''
        with open(ftrace,'r') as t:
            for line in t:
               r=r+line+'<br>'
            t.close()
        if int(mutex)<0:
            r = r + '<br>Attack is running Stages 0' + mutex + ' of 1<br>'
        else:
            r = r + 'Attack is at Stage ' + mutex + ' of 1<br>'
        return r

    @cherrypy.expose
    def set(self,mutex=''):
        try:
            int(mutex)
            with open(fmutex,'w') as f:
                f.write(mutex)
                f.close()
        except:
            if mutex:
                return "mutex<b><i> " + mutex + "</i></b> is invalid<br>mutex must be an integer, e.g. <i>/set?mutex=1</i>"
            else:
                with open(fmutex,'r') as f:
                    mutex=f.read()
                    f.close()
                return 'Attack is at Stage '+ mutex +' of 1'

        if mutex == '0':
            return 'Attack reset'
        else:
            return 'Attack Stage ' + mutex + ' of 1 initiated'

def web_api():
    conf = {
       '/': {
            'tools.auth_digest.on': True,
            'tools.auth_digest.realm': 'localhost',
            'tools.auth_digest.get_ha1': cherrypy.lib.auth_digest.get_ha1_dict_plain(users),
            'tools.auth_digest.key': get_session_key(),
            'tools.auth_digest.accept_charset': 'UTF-8',
       }
    }

    if os.path.isfile(ssl_cert) and os.path.isfile(ssl_priv_key):
        cherrypy.server.ssl_module = 'builtin'
        cherrypy.server.ssl_certificate = ssl_cert
        cherrypy.server.ssl_private_key = ssl_priv_key
    cherrypy.config.update({'server.socket_host':'0.0.0.0','server.socket_port':api_port})
    cherrypy.quickstart(SetMutex(),'/',conf)

def get_session_key():
    rand = Random()
    characters = string.ascii_letters + string.digits + string.punctuation
    session_key = ''.join(rand.choice(characters) for i in range(16))
    return session_key

def tracer(stage,action,refer,prompt,cmd):
    if trace:
        with open(ftrace,'a') as t:
            s = action + ' ' + refer
            t.write(stage + ': ' + s.ljust(10,'_') + cmd +'\n')
            t.close()
    if debug:
        print('Debug:> ' + action + ' ' + refer + ' ' + prompt + ' ' + cmd)
    return

#****************************************
# Attack Script                         *
#****************************************
def attack():
    seed(1)
    delay_min = 5
    delay_max = 20

    if reset_mutex_on_start:
        f = open(fmutex,'w')
        f.write('0')
        f.close()
        index = 0

    open(ftrace,'w').close
    while True:

#****************************************
# Attack Terminates                     *
#****************************************
        tracer('Attack Complete','','','','')
        if loop and not index > 0:
            open(ftrace,'w').close
            tracer('-','RESTART','','','')
            continue
        else:
            while index != 0:
                time.sleep(5)
                f = open(fmutex,'r')
                index = int(f.read())
                f.close()
            open(ftrace,'w').close
            tracer('-','RESET','','','')
            continue

if 'api_port' in globals() and int(api_port) > 0:
    thread=threading.Thread(target=attack)
    thread.daemon = True
    thread.start()

    web_api()
else:
    if __name__ == '__main__':
        attack()

# Script complete
