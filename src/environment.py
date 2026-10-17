
import json
import math


class Environment:
    """Grid-world simulation for the WALL-E and EVE mission."""

    def __init__(self, config_path):
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

        self.rows, self.cols = self.config["grid_size"]
        self.position = list(self.config["start_position"])
        self.battery = self.config["initial_battery"]
        self.max_battery = self.config["max_battery"]
        self.time_limit = self.config["time_limit"]
        self.time_elapsed = 0
        self.battery_per_move = self.config["battery_per_move"]
        self.scan_battery_cost = self.config["scan_battery_cost"]
        self.recharge_amount = self.config["recharge_amount"]

        self.eve_position = tuple(
            self.config["hidden_eve_position"]
        )

        self.clues = {
            tuple(item["position"]): item["strength"]
            for item in self.config["signal_clues"]
        }

        self.action_log = []

    def log_action(self, action, details):
        """Record an action for later reporting."""
        entry = {
            "time": self.time_elapsed,
            "position": list(self.position),
            "action": action,
            "battery": self.battery,
            "details": details,
        }
        self.action_log.append(entry)
        return entry

    def is_valid_position(self, position):
        """Check whether a position is inside the grid."""
        row, col = position
        return 0 <= row < self.rows and 0 <= col < self.cols

    def move(self, direction):
        """Move one cell in one of four directions."""
        moves = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
        }

        if direction not in moves:
            return {"success": False, "reason": "Invalid direction"}

        if self.time_elapsed >= self.time_limit:
            return {"success": False, "reason": "Time limit reached"}

        if self.battery < self.battery_per_move:
            return {"success": False, "reason": "Insufficient battery"}

        dr, dc = moves[direction]
        target = [
            self.position[0] + dr,
            self.position[1] + dc,
        ]

        if not self.is_valid_position(target):
            return {"success": False, "reason": "Grid boundary reached"}

        self.position = target
        self.battery -= self.battery_per_move
        self.time_elapsed += 1

        return {
            "success": True,
            "observation": self.observe(),
            "log": self.log_action("move", direction),
        }

    def observe(self):
        """Return observations available at the current cell."""
        position = tuple(self.position)

        # The agent receives a clue, not EVE's hidden coordinates.
        clue_strength = self.clues.get(position, 0.0)

        distance = math.dist(self.position, self.eve_position)

        return {
            "position": list(self.position),
            "signal_strength": clue_strength,
            "signal_detected": clue_strength > 0,
            "distance_band": (
                "near" if distance <= 1
                else "medium" if distance <= 3
                else "far"
            ),
            "time_elapsed": self.time_elapsed,
            "battery": self.battery,
        }

    def scan(self):
        """Spend energy to collect a local signal observation."""
        if self.time_elapsed >= self.time_limit:
            return {"success": False, "reason": "Time limit reached"}

        if self.battery < self.scan_battery_cost:
            return {"success": False, "reason": "Insufficient battery"}

        self.battery -= self.scan_battery_cost
        self.time_elapsed += 1

        observation = self.observe()
        entry = self.log_action("scan", observation)

        return {
            "success": True,
            "observation": observation,
            "log": entry,
        }

    def recharge(self):
        """Recharge WALL-E's battery at its current position."""
        if self.time_elapsed >= self.time_limit:
            return {"success": False, "reason": "Time limit reached"}

        if self.battery >= self.max_battery:
            return {"success": False, "reason": "Battery already full"}

        self.battery = min(
            self.max_battery,
            self.battery + self.recharge_amount,
        )
        self.time_elapsed += 1

        return {
            "success": True,
            "log": self.log_action("recharge", "Battery restored"),
        }

    def is_at_eve(self):
        """Check mission success when WALL-E reaches EVE."""
        return tuple(self.position) == self.eve_position

    def mission_status(self):
        """Return a concise summary of mission resources."""
        return {
            "position": list(self.position),
            "battery": self.battery,
            "time_elapsed": self.time_elapsed,
            "time_remaining": max(
                0, self.time_limit - self.time_elapsed
            ),
            "mission_success": self.is_at_eve(),
        }
