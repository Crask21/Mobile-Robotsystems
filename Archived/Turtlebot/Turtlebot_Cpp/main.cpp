#include <iostream>
#include <chrono>
#include <thread>
#include <csignal> // Catch sigterm (CTRL + C)
#include "mqtt/async_client.h"
#include "json.hpp"

using namespace std;
using json = nlohmann::json;

//const string ADDRESS { "tcp://192.168.0.6:1883" };
const string ADDRESS { "tcp://localhost:1883" };
const string TOPIC { "cmd_vel" };
const int QOS = 1;

// Declared globally as signal handler can't be part of the class..
mqtt::async_client* cli;
mqtt::topic* top;
mqtt::token_ptr tok;

// Handle CTRL + C and stop the robot
void signalHandler(int signum) {
    json stop_msg = {{"linear", {{"x", 0.0}, {"y", 0}, {"z", 0}}},
    {"angular", {{"x", 0}, {"y", 0}, {"z", 0.0}}}
    };
    cout << "CTRL + C pressed, exiting.." << endl;
    tok = top->publish(stop_msg.dump());
    tok->wait();
    exit(signum);
}


int main(int argc, char const *argv[])
{
    signal(SIGINT, signalHandler);
	cout << "Initializing for server '" << ADDRESS << "'..." << endl;
    mqtt::async_client cli(ADDRESS, "");
    mqtt::topic top(cli, TOPIC, QOS);

    try {  
        cout << "\nConnecting..." << endl;
        cli.connect()->wait();
        cout << "  ...OK" << endl;
    }
    catch (const mqtt::exception& exc) {
        cerr << exc << endl;
        return false;
    }
    float i = 0.0;
    json forward = {
        {"linear", {{"x", 0.0}, {"y", 0}, {"z", 0}}},
        {"angular", {{"x", 0}, {"y", 0}, {"z", 0}}}
    }; //x = 0.2 max speed
    json back = {
        {"linear", {{"x", -0.0}, {"y", 0}, {"z", 0}}},
        {"angular", {{"x", 0}, {"y", 0}, {"z", 0}}}
    };
    while (true) {
        forward = {
            {"linear", {{"x", i}, {"y", 0}, {"z", 0}}},
            {"angular", {{"x", 0}, {"y", 0}, {"z", 0}}}
        };
        back = {
            {"linear", {{"x", -i}, {"y", 0}, {"z", 0}}},
            {"angular", {{"x", 0}, {"y", 0}, {"z", 0}}}
        };
        tok = top.publish(forward.dump());
        tok->wait();
        this_thread::sleep_for(chrono::milliseconds(1000));
        tok = top.publish(back.dump());
        tok->wait();
        this_thread::sleep_for(chrono::milliseconds(1000));
        i+=0.01;
    }
    return 0;
}
