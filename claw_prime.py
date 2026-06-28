import json
import time
import os

class LegionBus:
    def __init__(self):
        self.messages = []
    def publish(self, sender, data, metadata=None):
        entry = {"sender": sender, "data": data, "timestamp": time.time(), "meta": metadata}
        self.messages.append(entry)
        print(f"[BUS] {sender} >> {data}")

class ClawAgent:
    def __init__(self, name, domain, tools=None):
        self.name = name
        self.domain = domain
        self.tools = tools or []
    def run(self, task, bus):
        print(f"[{self.name}] ACT: Executing in domain {self.domain}...")
        result = f"Action complete by {self.name} on: {task[:30]}"
        bus.publish(self.name, result)
        return result

class ClawPrime:
    def __init__(self, storage_path="claw_memory.json"):
        self.name = "Claw-Prime"
        self.storage_path = storage_path
        self.bus = LegionBus()
        self.memory = self.load_memory()
        
        self.legion = {
            "OpenClaw": ClawAgent("OpenClaw", "Core Execution"),
            "ARC": ClawAgent("ARC", "Deep Research"),
            "AutoClaw": ClawAgent("AutoClaw", "Automation"),
            "OpenCrabs": ClawAgent("OpenCrabs", "High-Perf Rust"),
            "PicoClaw": ClawAgent("PicoClaw", "Edge/Go"),
            "ZeroClaw": ClawAgent("ZeroClaw", "Infrastructure"),
            "TinyAGI": ClawAgent("TinyAGI", "Multi-Agent Coordination"),
            "TrinityClaw": ClawAgent("TrinityClaw", "Self-Modifying Logic"),
            "OpenBrowserClaw": ClawAgent("OpenBrowserClaw", "Browser-Native"),
            "IronClaw": ClawAgent("IronClaw", "Security/Audit"),
            "ClawMem": ClawAgent("ClawMem", "Persistence Layer"),
            "ClawSwarm": ClawAgent("ClawSwarm", "Parallel Scaling")
        }

    def load_memory(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except: return []
        return []

    def save_memory(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.memory, f, indent=4)

    def secure_router(self, task):
        task_lower = task.lower()
        print(f"[{self.name}] SECURITY: IronClaw performing pre-flight audit...")
        self.legion["IronClaw"].run(f"Audit task: {task}", self.bus)

        if any(k in task_lower for k in ["scale", "swarm", "parallel"]):
            return [self.legion["ClawSwarm"], self.legion["AutoClaw"]]
        if any(k in task_lower for k in ["research", "analyze", "find"]):
            return [self.legion["ARC"]]
        if any(k in task_lower for k in ["browser", "web", "site"]):
            return [self.legion["OpenBrowserClaw"]]
        if any(k in task_lower for k in ["rust", "speed", "crabs"]):
            return [self.legion["OpenCrabs"]]
        return [self.legion["OpenClaw"]]

    def safla_cycle(self, task):
        print(f"\n[{self.name}] SENSE: {task}")
        agents = self.secure_router(task)
        results = []
        for agent in agents:
            res = agent.run(task, self.bus)
            results.append(res)
        self.memory.append({"task": task, "results": results, "timestamp": time.time()})
        self.save_memory()
        print(f"[{self.name}] LEARN: State persisted to {self.storage_path}")
        return results

    def cli(self):
        print(f"\n--- {self.name} COMMAND INTERFACE ---")
        while True:
            try:
                cmd = input(f"{self.name} > ")
                if cmd.lower() in ['exit', 'quit']: break
                self.safla_cycle(cmd)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    commander = ClawPrime()
    commander.safla_cycle("Scale the research on World project and audit for security.")
