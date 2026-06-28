import json
import time
import os
import re
import urllib.request
import urllib.parse
import concurrent.futures

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
    def run(self, task, bus, armory):
        print(f"[{self.name}] ACT: Fetching live web signals...")
        query = task.replace("research", "").replace("find", "").strip()
        try:
            url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1"
            headers = {'User-Agent': 'Claw-Prime/1.0'}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                signal = data.get("AbstractText") or data.get("Definition") or f"No direct summary for {query}."
                res = f"LIVE_SIGNAL: {signal[:100]}..."
                bus.publish(self.name, res)
                return res
        except Exception as e:
            err = f"SIGNAL_ERROR: {str(e)}"
            bus.publish(self.name, err)
            return err

class ClawSwarmAgent(ClawAgent):
    """ClawSwarm: Parallel execution of tasks using ThreadPoolExecutor."""
    def run(self, task, bus, armory, sub_tasks=None):
        print(f"[{self.name}] ACT: Fanning out swarm execution...")
        if not sub_tasks:
            # Default fan-out: break comma-separated task or duplicate for broad search
            sub_tasks = [t.strip() for t in task.split(',') if t.strip()]
            if len(sub_tasks) == 1: sub_tasks = [f"{task} primary", f"{task} secondary"]

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(sub_tasks)) as executor:
            # Map sub_tasks to browser fetches for parallel research
            browser = OpenBrowserClawAgent("OpenBrowserClaw", "Browser")
            future_to_task = {executor.submit(browser.run, t, bus, armory): t for t in sub_tasks}
            
            for future in concurrent.futures.as_completed(future_to_task):
                t = future_to_task[future]
                try:
                    res = future.result()
                    results.append(res)
                except Exception as e:
                    results.append(f"Swarm Error on {t}: {str(e)}")
        
        report = f"SWARM_COMPLETE: Processed {len(results)} signals in parallel."
        bus.publish(self.name, report)
        return " | ".join(results)

class ARCAgent(ClawAgent):
    def run(self, task, bus, armory, live_data=None):
        print(f"[{self.name}] ACT: Synthesizing Research Data...")
        if live_data:
            report = f"SYNTHESIS: {live_data}"
        else:
            report = "No live signals provided for synthesis."
        bus.publish(self.name, f"REPORT: {report}")
        return report

class IronClawAgent(ClawAgent):
    def run(self, task, bus, armory):
        print(f"[{self.name}] ACT: Executing Zero-Trust Audit...")
        blacklist = [(r"rm\s+-rf", "Mass deletion"), (r"format\s+", "Drive format")]
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
        context = f"PREVIOUS CONTEXT: {memory[-1]['task'] if memory else 'None'}"
        bus.publish(self.name, context)
        return context

class TrinityClawAgent(ClawAgent):
    def run(self, task, bus, armory):
        print(f"[{self.name}] ACT: Decomposing task logic...")
        steps = [s.strip().upper() for s in task.split() if len(s) > 3]
        plan = f"PLAN: {' -> '.join(steps[:3])}"
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
            "OpenClaw": ClawAgent("OpenClaw", "Core"),
            "ARC": ARCAgent("ARC", "Deep Research"),
            "AutoClaw": ClawAgent("AutoClaw", "Automation"),
            "OpenCrabs": ClawAgent("OpenCrabs", "Rust"),
            "PicoClaw": ClawAgent("PicoClaw", "Edge"),
            "ZeroClaw": ClawAgent("ZeroClaw", "Infrastructure"),
            "TinyAGI": ClawAgent("TinyAGI", "Coordination"),
            "TrinityClaw": TrinityClawAgent("TrinityClaw", "Refinement"),
            "OpenBrowserClaw": OpenBrowserClawAgent("OpenBrowserClaw", "Browser"),
            "IronClaw": IronClawAgent("IronClaw", "Security"),
            "ClawMem": ClawMemAgent("ClawMem", "Persistence"),
            "ClawSwarm": ClawSwarmAgent("ClawSwarm", "Scaling")
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
        if self.legion["IronClaw"].run(task, self.bus, self.armory).startswith("BLOCK"): return []

        pipeline = [("ClawMem", task)]
        if len(task.split()) > 3: pipeline.append(("TrinityClaw", task))
            
        if any(k in task_lower for k in ["swarm", "scale", "parallel"]):
            pipeline.append(("ClawSwarm", task))
            pipeline.append(("ARC", task))
        elif any(k in task_lower for k in ["research", "analyze", "find"]):
            pipeline.append(("OpenBrowserClaw", task))
            pipeline.append(("ARC", task))
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
