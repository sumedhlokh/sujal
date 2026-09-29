# AgriBot – Agricultural Robot Mission & Crop Inspection Simulator

A basic BTech C++ mini-project with a Streamlit interface.

## Main concepts demonstrated

- Abstract class
- Inheritance
- Encapsulation
- Runtime polymorphism
- Stack for undo/history
- Queue for mission scheduling
- 2D array for virtual field
- Basic file/project organization
- Streamlit GUI

## How the simulation works

The crop field is a 5x5 virtual grid.

- H = Healthy crop
- W = Weed
- D = Possible disease
- Robot moves between cells
- Inspect checks the predefined condition of the current cell
- Undo restores the previous movement
- Missions are processed through a queue

There is intentionally no real AI, camera, GPS, or hardware in this version.

## Run the Streamlit app

Open a terminal in this project folder:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The browser will open the Streamlit application.

## Compile the C++ core

Using g++:

```bash
g++ cpp/main.cpp cpp/AgriRobot.cpp -o agribot
```

Run:

```bash
./agribot
```

On Windows:

```bash
agribot.exe
```

## Viva explanation

The project simulates an agricultural robot. `Robot` is an abstract base class. `AgriRobot` inherits from it and implements movement and inspection. Robot data such as battery and position is private, demonstrating encapsulation. A stack stores previous movement states for undo, while a queue stores missions that must be executed in order.

The crop inspection is intentionally simulated using a predefined virtual field. A real image-processing or AI model is a possible future extension.
