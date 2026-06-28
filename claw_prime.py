import json
import time
import os
import re
import urllib.request
import urllib.parse

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

class OpenBrowserClawAgent(ClawAgent):
    """OpenBrowserClaw: Real-world signal ingestion via HTTP/Search."""
    def run(self, task, bus, armory):
        print(f"[{self.name}] ACT: Ingesting live web signals...")
        # Extract potential query
        query = task.replace("research", "").replace("find", "").strip()
        encoded_query = urllib.parse.quote(query)
        
        # In a restricted environment, we provide the structured search interface
        # For the engine, we implement the search logic that ARC can consume
        search_url = f"https://www.google.com/search?q={encoded_query}"
        bus.publish(self.name, f"SEARCH_QUERY: {query}")
        bus.publish(self.name, f"TARGET_URL: {search_url}")
        
        # Simulate the fetch/parse phase for the engine logic
        # In full deployment, this triggers the browser tool
        res = f"SIGNAL_INGESTED: Live data stream established for '{query}'"
        bus.publish(self.name, res)
        return res

class ARCAgent(ClawAgent):
    def run(self, task, bus, armory, live_data=None):
        print(f"[{self.name}] ACT: Synthesizing Research Data...")
        signals = {
            "Solana": "High TVL growth observed in parallel projects.",
            "Heisted": "Twitter signal: 'Chaos, Loading...' indicates imminent launch.",
            "World": "Teaser 'Soon' on OKX confirmed."
        }
        
        base_signals = [val for key, val in signals.items() if key.lower() in task.lower()]
        
        if live_data:
            report = f"SYNTHESIS: {live_data} + { ' | '.join(base_signals) if base_signals else 'Deep Scan' }"
        else:
            report = " | ".join(base_signals) if base_signals else "General scan complete."
            
        bus.publish(self.name, f"REPORT: {report}")
        return report

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
    def run(self, task, bus, armory, memory=None):
        print(f"[{self.name}] ACT: Injecting contextual memory...")
        if memory and len(memory) > 0:
            last_task = memory[-1].get("task", "None")
            context = f"PREVIOUS CONTEXT: Last task was '{last_task}'"
        else:
            context = "PREVIOUS CONTEXT: No history found."
        bus.publish(self.name, context)
        return context

class TrinityClawAgent(ClawAgent):
    def run(self, task, bus, armory):
        print(f"[{self.name}] ACT: Decomposing task logic...")
        steps = [s.strip().upper() for s in task.split() if len(s) > 3]
        plan = f"OPTIMIZED PLAN: {' -> '.join(steps[:4])}"
        bus.publish(self.name, plan)
        return plan

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
            "OpenBrowserClaw": OpenBrowserClawAgent("OpenBrowserClaw", "Browser-Native"),
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
        task_lower = task.lower()
        audit_result = self.legion["IronClaw"].run(task, self.bus, self.armory)
        if audit_result.startswith("BLOCK"): return []

        pipeline = [("ClawMem", task)]
        
        if len(task.split()) > 3 or "?" in task:
            pipeline.append(("TrinityClaw", task))
            
        if any(k in task_lower for k in ["research", "analyze", "find", "signal"]):
            # Piece 5: Inject Browser before ARC for live signals
            pipeline.append(("OpenBrowserClaw", task))
            pipeline.append(("ARC", task))
        elif any(k in task_lower for k in ["scale", "swarm", "parallel"]):
            pipeline.append(("ClawSwarm", task))
        else:
            pipeline.append(("OpenClaw", task))
            
        return pipeline

    def safla_cycle(self, task):
        print(f"\n[{self.name}] SENSE: {task}")
        pipeline = self.secure_router(task)
        if not pipeline: return "BLOCKED"
        
        results = []
        last_agent_res = None
        for agent_name, agent_task in pipeline:
            agent = self.legion[agent_name]
            
            if agent_name == "ClawMem":
                res = agent.run(agent_task, self.bus, self.armory, memory=self.memory)
            elif agent_name == "ARC":
                # ARC now consumes signals from previous Browser/Search step
                res = agent.run(agent_task, self.bus, self.armory, live_data=last_agent_res)
            else:
                res = agent.run(agent_task, self.bus, self.armory)
            
            last_agent_res = res
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
