import json
import time

class LegionBus:
    def __init__(self):
        self.messages = []
    def publish(self, sender, data):
        self.messages.append({"sender": sender, "data": data, "timestamp": time.time()})
        print(f"[BUS] {sender}: {data}")

class ClawAgent:
    def __init__(self, name, capabilities):
        self.name = name
        self.capabilities = capabilities
    def run(self, task, bus):
        print(f"[{self.name}] ACT: Running domain logic for {task[:30]}...")
        result = f"Output from {self.name} for {task[:20]}"
        bus.publish(self.name, result)
        return result

class ClawPrime:
    def __init__(self):
        self.name = "Claw-Prime"
        self.bus = LegionBus()
        self.memory = []
        self.legion = {
            "ARC": ClawAgent("ARC", ["research", "analysis"]),
            "AutoClaw": ClawAgent("AutoClaw", ["execution", "automation"]),
            "IronClaw": ClawAgent("IronClaw", ["security", "audit"]),
            "ClawMem": ClawAgent("ClawMem", ["persistence", "recall"])
        }

    def router(self, task):
        # Dispatcher intelligence
        task_lower = task.lower()
        if any(kw in task_lower for kw in ["research", "find", "who", "what"]):
            return self.legion["ARC"]
        if any(kw in task_lower for kw in ["run", "do", "click", "build"]):
            return self.legion["AutoClaw"]
        return self.legion["AutoClaw"]

    def safla_cycle(self, task):
        """The core Sense-Act-Feedback-Learn-Act loop."""
        # 1. SENSE
        print(f"\n[{self.name}] SENSE: New Task -> {task}")
        self.bus.publish(self.name, f"Sense phase complete for {task[:20]}")
        
        # 2. ACT
        agent = self.router(task)
        print(f"[{self.name}] DISPATCH: Routing to {agent.name}")
        action_result = agent.run(task, self.bus)
        
        # 3. FEEDBACK
        print(f"[{self.name}] FEEDBACK: Observing result -> {action_result}")
        
        # 4. LEARN
        observation = {"task": task, "agent": agent.name, "result": action_result}
        self.memory.append(observation)
        print(f"[{self.name}] LEARN: Updating state with {agent.name} metrics.")
        
        # 5. ACT (Refinement)
        print(f"[{self.name}] REFINING: Preparing next stage of execution.")
        return action_result

    def autonomous_loop(self, task, depth=3):
        print(f"[{self.name}] STARTING AUTONOMOUS ENGINE (Depth: {depth})")
        current_objective = task
        for i in range(depth):
            print(f"\n--- LOOP {i+1} ---")
            result = self.safla_cycle(current_objective)
            current_objective = f"Refine and verify: {result}"
        print(f"[{self.name}] Objective Finalized.")

if __name__ == "__main__":
    commander = ClawPrime()
    commander.autonomous_loop("Execute the high-signal research on Solana project Heisted.")
