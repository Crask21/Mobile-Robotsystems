
from Turtlebot.moveClass import moveClass
from Protocol.DataLink.protocol_class import protocolClass
from Protocol.Physical.DTMF_overclass import DTMF


def main():
    pack= [0, 1, 10, 11, 12, 1, 8, 10, 9, 4, 7, 0, 1, 0, 1, 10, 11, 12, 2, 7, 6, 9, 14, 5, 0, 1, 0, 1, 10, 11, 12, 3, 4, 4, 
6, 5, 6, 5, 7, 10, 2, 0, 6, 14, 7, 5, 7, 4, 7, 3, 0, 0, 1]
    #print(len(pack))
    global robot
    robot=DTMF(20,10)
    
    moveObj = moveClass()
    data = robot.listen.startListen()
    robot.send.compare(pack, robot.listen.outputList)
    data_prot = protocolClass(baud=20,moves=data)
    data_prot.DataLinkUp()  
    data_prot.print()
    for i in range(len(data_prot.data_list)-1):
        moveObj.move(data_prot.data_list[i][0],data_prot.data_list[i][1])
    moveObj.stop()

if __name__ == "__main__":
    main()