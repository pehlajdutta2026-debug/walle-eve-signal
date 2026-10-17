
# WALL-E and EVE's Signal 🤖🌱

## Overview

**WALL-E and EVE's Signal** is a Python-based mission simulation in which WALL-E navigates an environment, scans for EVE's signal, manages battery power, and attempts to locate EVE within a limited amount of time.

The project demonstrates basic autonomous agent behavior, grid-based navigation, signal detection, battery management, and mission logging.

## 🎯 Mission Objectives

- Navigate a 5 × 5 grid environment.
- Detect and follow signal clues.
- Manage battery consumption while moving and scanning.
- Recharge when necessary.
- Locate EVE before the mission time limit.
- Record actions and generate a mission report.

## 🛠️ Technologies Used

- **Python 3**
- JSON for mission configuration and action logs
- Markdown for mission reporting
- Google Colab for development and execution
- GitHub for version control and project hosting

## 📁 Project Structure

```text
walle-eve-signal/
├── configs/
│   └── mission.json
├── src/
│   ├── environment.py
│   └── agent.py
├── logs/
│   └── action_log.json
├── reports/
│   └── mission_report.md
├── run_mission.py
└── README.md
```

The `tests/` folder may also be included if test files are available.

## ⚙️ Configuration

The mission settings are stored in `configs/mission.json`.

The current configuration includes:

- Grid size: 5 × 5
- Starting position: `[0, 0]`
- EVE's hidden position: `[4, 4]`
- Initial battery: 100
- Battery cost per move: 5
- Battery cost per scan: 8
- Mission time limit: 40 steps

These settings can be modified in the configuration file.

## ▶️ How to Run

### Option 1: Google Colab

1. Open your Google Colab notebook.
2. Run the cells that create the project files.
3. Execute `run_mission.py` from the project directory.

### Option 2: Run Locally

1. Install Python 3.
2. Download or clone this repository.
3. Open a terminal in the project directory.
4. Run:

```bash
python run_mission.py
```

No additional third-party packages are required by the current implementation, provided it uses only Python's standard library.

## 📊 Mission Results

The completed simulation produced the following results:

| Metric | Result |
|---|---|
| Mission status | SUCCESS |
| EVE found | Yes |
| Final position | `[4, 4]` |
| Final battery | 20 |
| Time used | 13 steps |
| Time remaining | 27 steps |
| Observations collected | 6 |
| Actions recorded | 13 |

## 📄 Generated Outputs

### Action Log

`logs/action_log.json`

Contains the recorded mission actions and associated information.

### Mission Report

`reports/mission_report.md`

Contains the mission outcome, final state, agent estimate, and summary statistics.

## 🧠 Key Concepts Demonstrated

- Grid-based movement
- Autonomous agent decision-making
- Signal scanning and observation
- Battery and time management
- JSON-based configuration
- Action logging and report generation

## 🚀 Future Improvements

- Implement a more adaptive path-planning algorithm.
- Add automated unit tests for movement, scanning, and recharging.
- Improve decision-making using signal observations.
- Add visualisation of WALL-E's route.
- Compare different agent strategies.

## 👤 Author

Add your name here.

## 📜 License

This project is available for educational and learning purposes. Add a specific open-source license if you intend to distribute it under one.
