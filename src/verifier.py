import re

class SlotVerifier:
    def __init__(self):
        self.critical_slots = ['serror_rate', 'rerror_rate', 'src_bytes', 'dst_bytes']

    def verify(self, telemetry: dict, generated_brief: str) -> dict:
        results = {}
        for slot in self.critical_slots:
            expected_val = telemetry.get(slot)
            if expected_val is None:
                continue
            if 'rate' in slot:
                expected_str = f"{float(expected_val):.2f}"
            else:
                expected_str = str(int(float(expected_val)))
            pattern = r'\b' + re.escape(expected_str) + r'\b'
            if re.search(pattern, generated_brief):
                results[slot] = {"status": "PASS", "expected": expected_str}
            else:
                results[slot] = {"status": "FAIL", "expected": expected_str}
        return results
