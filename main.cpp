#include "AgriRobot.h"
#include <iostream>

int main() {
    AgriRobot robot;

    std::cout << "AGRIBOT C++ ENGINE\n";
    std::cout << "Position: (" << robot.getX() << "," << robot.getY() << ")\n";

    robot.addMission("Move Right");
    robot.addMission("Move Right");
    robot.addMission("Inspect");

    while (true) {
        std::string result = robot.executeNextMission();
        std::cout << result << "\n";

        if (result == "Mission queue is empty.")
            break;
    }

    std::cout << "Position: (" << robot.getX() << "," << robot.getY() << ")\n";
    std::cout << "Battery: " << robot.getBattery() << "%\n";

    return 0;
}
