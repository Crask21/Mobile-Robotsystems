import sys
#import Turtlebot.Turtlebot_Python.moveClass as moveClass
from Protocol.DataLink.protocol_class import protocolClass
from Protocol.Physical.DTMF_overclass import DTMF
import time

def main():
    baudrate = 50
    sync = 30

    robot=DTMF(baudrate,sync)
    
    #moveObj = moveClass.bot()
    
    move = [[0,100],[90,100]]
    #[[20,10],[-10,30],["Dees large Nuts"]]
    pack = protocolClass(baudrate,sync,move,'output.txt')
    pack.DataLinkDown()
    pack.print()
    
    #print(pack.data_list)

    #hej=[7,7,7,7,7,7,7,7,7,7,7,15,15,15]

    robot.send.send_package(pack.data_list)
    #robot.send.send_package(pack.data_list)
    
    #moveObj.move(ang, dist)
    #moveObj.stop()

if __name__ == "__main__":
    main()