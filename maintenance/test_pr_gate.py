import unittest

import pr_gate


def run(id_, name, status="completed"):
    return {"id": id_, "name": name, "status": status}


class GateTests(unittest.TestCase):
    def test_docs_only_needs_nothing_and_passes(self):
        needs, notes = pr_gate.required(["HANDOVER.md", "AGENTS.md"], "claude/docs")
        self.assertEqual((needs, notes), ([], []))
        self.assertEqual(pr_gate.evaluate(needs, [], {})[0], "pass")

    def test_infrastructure_and_generated_api_requirements(self):
        self.assertEqual(pr_gate.required(["maintenance/update.py"], "claude/x")[0], [pr_gate.MAINTENANCE])
        self.assertEqual(pr_gate.required([".github/workflows/x.yml"], "claude/x")[0], [pr_gate.MAINTENANCE])
        needs, _ = pr_gate.required(["APIs/a.com/1/openapi.yaml", "maintenance/sources.json"], "codex/official-update-a--g2")
        self.assertEqual(needs, [pr_gate.MAINTENANCE, pr_gate.DRAFT])
        needs, notes = pr_gate.required(["APIs/a.com/1/openapi.yaml"], "claude/manual")
        self.assertEqual(needs, [])
        self.assertIn("human review", notes[0])

    def test_skipped_missing_running_and_failed_jobs_do_not_pass(self):
        needs = [pr_gate.DRAFT]
        name = pr_gate.DRAFT[0]
        self.assertEqual(pr_gate.evaluate(needs, [], {})[0], "pending")
        self.assertEqual(pr_gate.evaluate(needs, [run(1, name, "in_progress")], {})[0], "pending")
        for conclusion in ("skipped", "failure", "cancelled"):
            jobs = {1: [{"name": "validate", "conclusion": conclusion}]}
            self.assertEqual(pr_gate.evaluate(needs, [run(1, name)], jobs)[0], "fail", conclusion)
        self.assertEqual(pr_gate.evaluate(needs, [run(1, name)], {1: []})[0], "fail")

    def test_latest_run_decides_and_success_passes(self):
        needs = [pr_gate.MAINTENANCE]
        name = pr_gate.MAINTENANCE[0]
        jobs = {1: [{"name": "tests", "conclusion": "failure"}], 2: [{"name": "tests", "conclusion": "success"}]}
        self.assertEqual(pr_gate.evaluate(needs, [run(1, name), run(2, name)], jobs)[0], "pass")
        jobs = {1: [{"name": "tests", "conclusion": "success"}], 2: [{"name": "tests", "conclusion": "failure"}]}
        self.assertEqual(pr_gate.evaluate(needs, [run(1, name), run(2, name)], jobs)[0], "fail")


if __name__ == "__main__":
    unittest.main()
