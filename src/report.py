def print_agent_report(state):
    print("=" * 60)
    print(f"TRIAGE AGENT REPORT — STATUS: {state['status']}")
    print("=" * 60)
    print(f"Telemetry: {state['telemetry'].get('label', 'N/A')} / {state['telemetry'].get('service', 'N/A')}")
    print(f"Iterations: {state['iterations']}")
    print("-" * 60)
    print("Execution Trace:")
    for t in state['trace']:
        print(f"  -> {t}")
    print("-" * 60)
    if state['status'] == 'ADVISORY_BRIEF':
        print("Generated Brief (machine_draft — advisory only):")
        print(state['brief'])
        print("\nSlot Verification:")
        for k, v in state['verification'].items():
            print(f"  {k}: {v['status']} (expected: {v['expected']})")
    elif state['status'] == 'CANNOT_VERIFY':
        print("⚠️ CANNOT VERIFY: This event requires human review.")
        if state.get('brief'):
            print("\nRejected Draft:")
            print(state['brief'])
    elif state['status'] == 'REFUSED':
        print("❌ INPUT REFUSED: Malformed telemetry.")
    elif state['status'] == 'BENIGN':
        print("✅ BENIGN: No action required.")
    print("=" * 60 + "\n")
