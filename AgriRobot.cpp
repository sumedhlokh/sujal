#include "AgriRobot.h"
#include <sstream>

AgriRobot::AgriRobot() : Robot(0, 0), battery(100), status("READY") {
    char initialField[5][5] = {
        {'H','H','H','H','H'},
        {'H','H','W','H','H'},
        {'H','H','H','D','H'},
        {'H','H','H','H','H'},
        {'H','W','H','H','H'}
    };

    for (int i = 0; i < 5; i++)
        for (int j = 0; j < 5; j++)
            field[i][j] = initialField[i][j];
}

void AgriRobot::move(char direction) {
    int oldX = x, oldY = y;
    int nx = x, ny = y;

    if (direction == 'U') nx--;
    else if (direction == 'D') nx++;
    else if (direction == 'L') ny--;
    else if (direction == 'R') ny++;

    if (nx < 0 || nx >= 5 || ny < 0 || ny >= 5) {
        status = "Cannot move outside field";
        return;
    }

    if (battery <= 0) {
        status = "Battery empty";
        return;
    }

    x = nx;
    y = ny;
    battery -= 2;
    status = "MOVING";

    undoStack.push({"MOVE", oldX, oldY, x, y});
}

std::string AgriRobot::inspect() {
    status = "INSPECTING";
    battery = battery > 0 ? battery - 1 : 0;

    char cell = field[x][y];

    if (cell == 'H')
        return "Crop Status: HEALTHY";
    if (cell == 'W')
        return "Crop Status: WEED DETECTED";
    if (cell == 'D')
        return "Crop Status: POSSIBLE DISEASE";

    return "Crop Status: UNKNOWN";
}

void AgriRobot::addMission(const std::string& mission) {
    missionQueue.push(mission);
    status = "MISSION ADDED";
}

std::string AgriRobot::executeNextMission() {
    if (missionQueue.empty())
        return "Mission queue is empty.";

    std::string mission = missionQueue.front();
    missionQueue.pop();

    if (mission == "Inspect")
        return inspect();

    if (mission == "Move Right") {
        move('R');
        return "Robot moved right.";
    }

    if (mission == "Move Left") {
        move('L');
        return "Robot moved left.";
    }

    if (mission == "Move Up") {
        move('U');
        return "Robot moved up.";
    }

    if (mission == "Move Down") {
        move('D');
        return "Robot moved down.";
    }

    if (mission == "Spray")
        return "Spraying simulation completed after farmer approval.";

    if (mission == "Return")
        return "Return-to-start mission completed.";

    return "Unknown mission.";
}

std::string AgriRobot::undoLastMove() {
    if (undoStack.empty())
        return "Nothing to undo.";

    Command last = undoStack.top();
    undoStack.pop();

    x = last.oldX;
    y = last.oldY;
    battery = battery < 98 ? battery + 2 : 100;
    status = "UNDO COMPLETED";

    return "Last movement undone.";
}

std::string AgriRobot::getStatus() const {
    return status;
}

int AgriRobot::getBattery() const {
    return battery;
}

char AgriRobot::getCell(int row, int col) const {
    return field[row][col];
}
