
inputList = [[927,1445],[764,1358],[1482,855]];

output = []

for i in range(len(inputList)):
    if(inputList[i][0]>inputList[i][1]):
        temp = inputList[i][0];
        inputList[i][0] = inputList[i][1];
        inputList[i][1] = temp;

for i in range(len(inputList)):
    input1 = inputList[i][0];
    input2 = inputList[i][1];

    if((input1>=650) and (input1<=730)):
        if((input2>=1150) and (input2<=1250)):
            output.append(0);
        elif((input2>=1280) and (input2<=1380)):
            output.append(1);
        elif((input2>=1420) and (input2<=1520)):
            output.append(2);
        elif((input2>=1580) and (input2<=1680)):
            output.append(3);
    elif((input1>=745) and (input1<=810)):
        if((input2>=1150) and (input2<=1250)):
            output.append(4);
        elif((input2>=1280) and (input2<=1380)):
            output.append(5);
        elif((input2>=1420) and (input2<=1520)):
            output.append(6);
        elif((input2>=1580) and (input2<=1680)):
            output.append(7);
    elif((input1>=820) and (input1<=890)):
        if((input2>=1150) and (input2<=1250)):
            output.append(8);
        elif((input2>=1280) and (input2<=1380)):
            output.append(9);
        elif((input2>=1420) and (input2<=1520)):
            output.append('A');
        elif((input2>=1580) and (input2<=1680)):
            output.append('B');
    elif((input1>=900) and (input1<=980)):
        if((input2>=1150) and (input2<=1250)):
            output.append('C');
        elif((input2>=1280) and (input2<=1380)):
            output.append('D');
        elif((input2>=1420) and (input2<=1520)):
            output.append('E');
        elif((input2>=1580) and (input2<=1680)):
            output.append('F');

print(output);