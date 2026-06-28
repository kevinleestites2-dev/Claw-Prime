import json
import time
import os
import re

class LegionBus:
    def __init__(self):
        self.messages = []
    def publish(self, sender, data, metadata=None):
        entry = {"sender": sender, "data": data, "timestamp": time.time(), "meta": metadata}
        self.messages.append(entry)
        print(f"[BUS] {sender} >> {data}")

class ArmoryLoader:
    def __init__(self):
        self.source = "https://github.com/VoltAgent/awesome-openclaw-skills"
    def load_skill(self, skill_name):
        print(f"[ARMORY] Indexing {skill_name}...")
        return True

class ClawAgent:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain
    def run(self, task, bus, armory):
        result = f"Action by {self.name}"
        bus.publish(self.name, result)
        return result

class ARCAgent(ClawAgent):
    def run(self, task, bus, armory):
        print(f"[{self.name}] ACT: Initiating High-Signal Discovery...")
        signals = {
            "Solana": "High TVL growth observed in parallel projects.",
            "Heisted": "Twitter signal: 'Chaos, Loading...' indicates imminent launch.",
            "World": "Teaser 'Soon' on OKX confirmed."
        }
        found_signals = [val for key, val in signals.items() if key.lower() in task.lower()]
        res = " | ".join(found_signals) if found_signals else "General broad-spectrum scan complete."
        bus.publish(self.name, f"REPORT: {res}")
        return res

class IronClawAgent(ClawAgent):
    def run(self, task, bus, armory):
        print(f"[{self.name}] ACT: Executing Zero-Trust Audit...")
        blacklist = [(r"rm\s+-rf", "Mass deletion"), (r"format\s+", "Drive format"), (r"chmod\s+777", "Insecure perms")]
        violations = [reason for pattern, reason in blacklist if re.search(pattern, task, re.I)]
        if violations:
            msg = f"BLOCK: {', '.join(violations)}"
            bus.publish(self.name, msg, {"status": "BLOCK"})
            return msg
        bus.publish(self.name, "Audit: CLEAN")
        return "PASS"

class ClawMemAgent(ClawAgent):
    """ClawMem: Vectorized memory retrieval and context injection."""
    def run(self, task, bus, armory):
        print(f"[{self.name}] ACT: Retrieving relevant context...")
        # In a real implementation, this would use embeddings/search.
        # For Piece 4, we leverage the existing safla history.
        return "Context: Legion active. Previous signals indexed."

class TrinityClawAgent(ClawAgent):
    """TrinityClaw: Self-Refinement and Task Decomposition."""
    def run(self, task, bus, armory):
        print(f"[{self.name}] ACT: Decomposing task into optimized steps...")
        steps = [f"Step {i+1}: Optimize {s.strip()}" for i, s in enumerate(task.split(',')) if s.strip()]
        res = " | ".join(steps)
        bus.publish(self.name, f"PLAN: {res}")
        return res

class ClawPrime:
    def __init__(self, storage_path="claw_memory.json"):
        self.name = "Claw-Prime"
        self.storage_path = storage_path
        self.bus = LegionBus()
        self.armory = ArmoryLoader()
        self.memory = self.load_memory()
        
        self.legion = {
            "OpenClaw": ClawAgent("OpenClaw", "Core Execution"),
            "ARC": ARCAgent("ARC", "Deep Research"),
            "AutoClaw": ClawAgent("AutoClaw", "Automation"),
            "OpenCrabs": ClawAgent("OpenCrabs", "High-Perf Rust"),
            "PicoClaw": ClawAgent("PicoClaw", "Edge/Go"),
            "ZeroClaw": ClawAgent("ZeroClaw", "Infrastructure"),
            "TinyAGI": ClawAgent("TinyAGI", "Multi-Agent Coordination"),
            "TrinityClaw": TrinityClawAgent("TrinityClaw", "Self-Modifying Logic"),
            "OpenBrowserClaw": ClawAgent("OpenBrowserClaw", "Browser-Native"),
            "IronClaw": IronClawAgent("IronClaw", "Security/Audit"),
            "ClawMem": ClawMemAgent("ClawMem", "Persistence Layer"),
            "ClawSwarm": ClawAgent("ClawSwarm", "Parallel Scaling")
        }

    def load_memory(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f: return json.load(f)
            except: return []
        return []

    def save_memory(self):
        with open(self.storage_path, 'w') as f: json.dump(self.memory, f, indent=4)

    def secure_router(self, task):
        audit_result = self.legion["IronClaw"].run(task, self.bus, self.armory)
        if audit_result.startswith("BLOCK"): return []

        pipeline = [self.legion["ClawMem"]] # Context injection first
        
        task_lower = task.lower()
        if any(k in task_lower for k in ["plan", "how to", "complex"]):
            pipeline.append(self.legion["TrinityClaw"])
        if any(k in task_lower for k in ["research", "analyze", "find"]):
            pipeline.append(self.legion["ARC"])
        
        if len(pipeline) == 1: pipeline.append(self.legion["OpenClaw"])
        return pipeline

    def safla_cycle(self, task):
        print(f"\n[{self.name}] SENSE: {task}")
        agents = self.secure_router(task)
        if not agents: return "BLOCKED"
        
        results = []
        for agent in agents:
            res = agent.run(task, self.bus, self.armory)
            results.append(res)
        
        self.memory.append({"task": task, "results": results, "timestamp": time.time()})
        self.save_memory()
        return results

    def cli(self):
        print(f"\n--- {self.name} COMMAND INTERFACE ---")
        while True:
            try:
                cmd = input(f"{self.name} > ")
                if cmd.lower() in ['exit', 'quit']: break
                if not cmd.strip(): continue
                self.safla_cycle(cmd)
            except (KeyboardInterrupt, EOFError): break

if __name__ == "__main__":
    commander = ClawPrime()
    commander.cli()
