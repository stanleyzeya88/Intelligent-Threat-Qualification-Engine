import pandas as pd
import numpy as np

class InputGate:
    def __init__(self):
        self.required_cols = [
            'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
            'serror_rate', 'rerror_rate', 'duration', 'count'
        ]

    def validate(self, telemetry_dict: dict) -> tuple[bool, str]:
        missing = [c for c in self.required_cols if c not in telemetry_dict]
        if missing:
            return False, f"Missing required fields: {missing}"

        numeric_fields = ['src_bytes', 'dst_bytes', 'serror_rate',
                          'rerror_rate', 'duration', 'count']
        for field in numeric_fields:
            try:
                float(telemetry_dict[field])
            except (ValueError, TypeError):
                return False, f"Field '{field}' must be numeric. Got: {telemetry_dict[field]}"
        return True, "Valid telemetry"
