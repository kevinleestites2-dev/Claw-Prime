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
        # Placeholder for actual module integration
        result = f"Action complete by {self.name} on: {task[:30]}"
        bus.publish(self.name, result)
        return result

class ClawPrime:
    def __init__(self, storage_path="claw_memory.json"):
        self.name = "Claw-Prime"
        self.storage_path = storage_path
        self.bus = LegionBus()
        self.memory = self.load_memory()
        
        # Instantiate ALL 12 Legion pieces
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
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return []

    def save_memory(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.memory, f, indent=4)

    def secure_router(self, task):
        """Enhanced Router: Pre-flight security check and multi-agent routing."""
        task_lower = task.lower()
        
        # 1. Pre-flight: IronClaw Audit
        print(f"[{self.name}] SECURITY: IronClaw performing pre-flight audit...")
        self.legion["IronClaw"].run(f"Audit task: {task}", self.bus)

        # 2. Parallel Dispatch/Swarm logic
        if "scale" in task_lower or "mass" in task_lower:
            return [self.legion["ClawSwarm"], self.legion["AutoClaw"]]
        
        # 3. Domain Routing
        if any(k in task_lower for k in ["research", "analyze"]):
            return [self.legion["ARC"]]
        if any(k in task_lower for k in ["browser", "web"]):
            return [self.legion["OpenBrowserClaw"]]
        if any(k in task_lower for k in ["rust", "speed"]):
            return [self.legion["OpenCrabs"]]
            
        return [self.legion["OpenClaw"]]

    def safla_cycle(self, task):
        print(f"\n[{self.name}] SENSE: {task}")
        
        # ACT: Secure Routing
        agents = self.secure_router(task)
        results = []
        for agent in agents:
            res = agent.run(task, self.bus)
            results.append(res)
            
        # FEEDBACK & LEARN
        self.memory.append({"task": task, "results": results, "timestamp": time.time()})
        self.save_memory()
        print(f"[{self.name}] LEARN: State persisted to {self.storage_path}")
        
        return results

    def cli(self):
        """Live Command Interface"""
        print(f"\n--- {self.name} COMMAND INTERFACE ---")
        while True:
            try:
                cmd = input(f"{self.name} > ")
                if cmd.lower() in ['exit', 'quit']: break
                self.safla_cycle(cmd)
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    commander = ClawPrime()
    # To start live: commander.cli()
    commander.safla_cycle("Scale the research on World project and audit for security.")
