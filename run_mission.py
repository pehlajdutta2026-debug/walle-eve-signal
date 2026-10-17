
import json
import os

from src.environment import Environment
from src.agent import WallEAgent


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    config_path = os.path.join(BASE_DIR, "configs", "mission.json")
    logs_dir = os.path.join(BASE_DIR, "logs")
    reports_dir = os.path.join(BASE_DIR, "reports")

    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    # Initialize and execute the mission.
    env = Environment(config_path)
    agent = WallEAgent(env)
    result = agent.run_mission()

    # Save the action and reasoning logs.
    log_data = {
        "mission_name": env.config["mission_name"],
        "actions": env.action_log,
        "reasoning": result["reasoning_log"],
    }

    log_path = os.path.join(logs_dir, "action_log.json")
    with open(log_path, "w", encoding="utf-8") as file:
        json.dump(log_data, file, indent=4)

    # Build a readable mission report.
    status = result["final_status"]
    outcome = "SUCCESS" if result["success"] else "INCOMPLETE"

    report = f"""# WALL-E and EVE's Signal — Mission Report

## Mission outcome

- **Status:** {outcome}
- **EVE found:** {result["success"]}
- **Final position:** {status["position"]}
- **Final battery:** {status["battery"]}
- **Time used:** {status["time_elapsed"]}
- **Time remaining:** {status["time_remaining"]}

## Agent's estimate

- **Best observed position:** {result["best_observed_position"]}
- **Best observed signal strength:** {result["best_signal_strength"]}
- **Observations collected:** {result["observations_count"]}
- **Actions recorded:** {len(env.action_log)}

## Recommended next step

"""

    if result["success"]:
        report += (
            "Mission complete. Review the action log and "
            "verify the agent's observations.\n"
        )
    else:
        report += (
            "Continue searching using the collected observations. "
            "Review battery use and the remaining mission time.\n"
        )

    report_path = os.path.join(reports_dir, "mission_report.md")
    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report)

    print(report)
    print(f"\nAction log saved to: {log_path}")
    print(f"Mission report saved to: {report_path}")


if __name__ == "__main__":
    main()
