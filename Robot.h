#ifndef ROBOT_H
#define ROBOT_H

#include <string>

class Robot {
protected:
    int x, y;

public:
    Robot(int startX = 0, int startY = 0) : x(startX), y(startY) {}
    virtual ~Robot() {}

    virtual void move(char direction) = 0;
    virtual std::string inspect() = 0;

    int getX() const { return x; }
    int getY() const { return y; }
};

#endif
