
class WallEAgent:
    """A simple autonomous agent for the EVE signal mission."""

    def __init__(self, environment):
        self.env = environment
        self.observations = []
        self.best_position = list(environment.position)
        self.best_signal = -1.0
        self.reasoning_log = []

    def record_observation(self, observation):
        """Update the agent's belief using a local observation."""
        self.observations.append(observation)

        strength = observation["signal_strength"]

        if strength > self.best_signal:
            self.best_signal = strength
            self.best_position = list(observation["position"])

        self.reasoning_log.append({
            "time": self.env.time_elapsed,
            "position": list(self.env.position),
            "signal_strength": strength,
            "best_signal": self.best_signal,
            "estimated_eve_position": list(self.best_position),
        })

    def scan_current_location(self):
        """Scan and learn from the current location."""
        result = self.env.scan()

        if result["success"]:
            self.record_observation(result["observation"])

        return result

    def move_toward(self, target):
        """Take one valid step toward a target coordinate."""
        row, col = self.env.position
        target_row, target_col = target

        if row < target_row:
            direction = "down"
        elif row > target_row:
            direction = "up"
        elif col < target_col:
            direction = "right"
        elif col > target_col:
            direction = "left"
        else:
            return False

        result = self.env.move(direction)
        return result["success"]

    def run_mission(self):
        """Explore the grid using a simple diagonal search heuristic."""
        initial = self.env.observe()
        self.record_observation(initial)

        # Scan the starting cell if resources permit.
        if self.env.battery >= self.env.scan_battery_cost:
            self.scan_current_location()

        rows, cols = self.env.rows, self.env.cols

        # Follow diagonal checkpoints, adapting to observed signal.
        checkpoints = [
            [i, i]
            for i in range(min(rows, cols))
        ]

        for checkpoint in checkpoints:
            if self.env.is_at_eve():
                break

            if self.env.time_elapsed >= self.env.time_limit:
                break

            # Recharge when needed for a safe next step.
            while (
                self.env.battery < self.env.battery_per_move
                and self.env.time_elapsed < self.env.time_limit
            ):
                result = self.env.recharge()
                if not result["success"]:
                    break

            if self.env.battery < self.env.battery_per_move:
                break

            # Move one step at a time toward the checkpoint.
            while (
                self.env.position != checkpoint
                and self.env.time_elapsed < self.env.time_limit
            ):
                if self.env.battery < self.env.battery_per_move:
                    if self.env.battery < self.env.max_battery:
                        self.env.recharge()
                    else:
                        break

                if self.env.battery < self.env.battery_per_move:
                    break

                if not self.move_toward(checkpoint):
                    break

                if self.env.is_at_eve():
                    break

            if self.env.is_at_eve():
                break

            if self.env.time_elapsed >= self.env.time_limit:
                break

            # Scan only if enough battery remains.
            if self.env.battery >= self.env.scan_battery_cost:
                self.scan_current_location()
            elif self.env.battery < self.env.max_battery:
                self.env.recharge()

        return {
            "success": self.env.is_at_eve(),
            "final_status": self.env.mission_status(),
            "best_observed_position": self.best_position,
            "best_signal_strength": self.best_signal,
            "observations_count": len(self.observations),
            "reasoning_log": self.reasoning_log,
        }
