import sys
#import Turtlebot.Turtlebot_Python.moveClass as moveClass
from Protocol.DataLink.protocol_class import protocolClass
from Protocol.Physical.DTMF_overclass import DTMF
import time


def main():
    baudrate = 20
    sync = 30

    robot=DTMF(baudrate,sync,mono_robot=True)
    
    #moveObj = moveClass.bot()
    
    move = [[0,20],[90,15]]

    pack = protocolClass(move,robot,'output.txt')

    pack.DataLinkDown()
    #pack.print()
    #pack.DataLinkUp()
    print(pack.data_list)
    
    robot.send.send_package(pack.data_list)


    
    #moveObj.move(ang, dist)
    #moveObj.stop()

if __name__ == "__main__":
    main()