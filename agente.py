import platform
import psutil
import pwd, grp
import subprocess

# Librerias
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.behaviours.protocols import TimedBehaviour
from sys import argv


class ComportTemporal(TimedBehaviour):
    def __init__(self, agent, time):
        super(ComportTemporal, self).__init__(agent, time)

    def on_time(self):
        super(ComportTemporal, self).on_time()
        display_message(self.agent.aid.localname, self.get_os_info())

    def get_os_info(self):
        # Get Operation Sysrtem Information
        platform_name = platform.system()# e.g. Windows, Linux, Darwin
        platform_architecture = platform.architecture()# e.g. 64-bit
        platform_machine = platform.machine()# e.g. x86_64
        platform_host_name = platform.node()# Hostname
        platform_processor = platform.processor()# e.g. i386

        print('-----------------Atributos Server---------------------')
        print('Operation System Name:',platform_name)  
        print('Type Architecture:',platform_architecture)  
        print('Processor Architecture:',platform_machine)  
        print('Host Name:',platform_host_name)  
        print('Platform Processor',platform_processor)  
        print('')

        print('-----------------Listado de Procesos---------------------')
        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                processName = proc.name()
                processID = proc.pid
                print(processName , ' ::: ', processID)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        print('')

        listOfProcessNames = list()
        # Iterate over all running processes
        for proc in psutil.process_iter():
            # Get process detail as dictionary
            pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
            print("Process Dictionary")
            print(pInfoDict)
            # Append dict of process detail in list
            listOfProcessNames.append(pInfoDict)
        print('')

        print('-----------------Listado Usuarios---------------------')
        for p in pwd.getpwall():
            print(p[0], grp.getgrgid(p[3])[0])

        print('-----------------Listado Sesiones---------------------')
        #res = subprocess.check_output(["WMIC", "ComputerSystem", "GET", "UserName"], universal_newlines=True)
        res = subprocess.check_output('w', universal_newlines=True)
        #username = res.strip().rsplit("\n", 1)
        #print("Sessions:",username.rsplit("\\", 1))
        print(res)

        return "End OS Info"


class SmartAgent(Agent):

    def __init__(self, aid):
        super(SmartAgent, self).__init__(aid=aid, debug=False)
        #super(AgenteHelloWorld, self).__init__(aid=aid)
        #display_message(self.aid.localname, self.get_os_info())
        comp_temp = ComportTemporal(self, 60.0)
        self.behaviours.append(comp_temp)


if __name__ == '__main__':
    agents_per_process = 2
    c = 0
    agents = list()
    for i in range(agents_per_process):
        port = int(argv[1]) + c
        agent_name = 'smart_agent_{}@localhost:{}'.format(port, port)
        agente_hello = SmartAgent(AID(name=agent_name))
        agents.append(agente_hello)
        c += 1000

    start_loop(agents)

