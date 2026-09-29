#ifndef AGRIROBOT_H
#define AGRIROBOT_H

#include "Robot.h"
#include <stack>
#include <queue>
#include <string>

struct Command {
    std::string action;
    int oldX, oldY;
    int newX, newY;
};

class AgriRobot : public Robot {
private:
    int battery;
    std::string status;
    char field[5][5];

    std::stack<Command> undoStack;
    std::queue<std::string> missionQueue;

public:
    AgriRobot();

    void move(char direction) override;
    std::string inspect() override;

    void addMission(const std::string& mission);
    std::string executeNextMission();
    std::string undoLastMove();

    std::string getStatus() const;
    int getBattery() const;
    char getCell(int row, int col) const;
};

#endif
