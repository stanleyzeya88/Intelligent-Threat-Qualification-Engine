from input_gate import InputGate
from classifier import ThreatClassifier
from brief_writer import BriefWriter
from verifier import SlotVerifier


class ITQEAgent:
    def __init__(self, classifier, brief_writer):
        self.gate = InputGate()
        self.classifier = classifier
        self.writer = brief_writer
        self.verifier = SlotVerifier()

    def execute(self, telemetry: dict) -> dict:
        state = {"status": "INIT", "iterations": 0, "trace": [],
                 "telemetry": telemetry, "classification": None,
                 "brief": None, "verification": None}

        # 1. Input Gate
        valid, reason = self.gate.validate(telemetry)
        if not valid:
            state["status"] = "REFUSED"
            state["trace"].append(f"Input Gate: REJECTED ({reason})")
            return state
        state["trace"].append("Input Gate: PASS")

        # 2. P3 Classify
        state["iterations"] += 1
        classification = self.classifier.predict(telemetry)
        state["classification"] = classification
        state["trace"].append(
            f"Classifier: {classification['prediction']} "
            f"(Conf: {classification['confidence']:.4f})"
        )

        # If BENIGN, terminate (regardless of confidence)
        if classification['prediction'] == 'BENIGN':
            state["status"] = "BENIGN"
            state["trace"].append("Traffic is benign. No brief drafted.")
            return state

        # If ATTACK but low confidence, route to human
        if classification['confidence'] < 0.60:
            state["status"] = "CANNOT_VERIFY"
            state["trace"].append("Low-confidence attack. Routing to human.")
            return state

        # 3. P5 Draft
        state["iterations"] += 1
        brief = self.writer.generate_brief(telemetry)
        state["brief"] = brief
        state["trace"].append(f"Brief Writer: Drafted {len(brief)} chars.")

        # 4. P7 Verify
        state["iterations"] += 1
        verification = self.verifier.verify(telemetry, brief)
        state["verification"] = verification
        failed = [k for k, v in verification.items() if v['status'] == 'FAIL']

        # 5. Re-check Gate
        if failed:
            state["trace"].append(
                f"Verifier: Slot Drift on {failed}. Regenerating once.")
            state["iterations"] += 1
            brief_retry = self.writer.generate_brief(telemetry)
            verification_retry = self.verifier.verify(telemetry, brief_retry)
            failed_retry = [k for k, v in verification_retry.items()
                            if v['status'] == 'FAIL']
            if failed_retry:
                state["status"] = "CANNOT_VERIFY"
                state["trace"].append(
                    f"Verifier: Persistent drift on {failed_retry}. Routing to human.")
                state["verification"] = verification_retry
                return state
            else:
                state["brief"] = brief_retry
                state["verification"] = verification_retry
                state["trace"].append("Verifier: Retry successful. All slots verified.")

        state["status"] = "ADVISORY_BRIEF"
        state["trace"].append("Success: Brief verified and ready for human review.")
        return state
