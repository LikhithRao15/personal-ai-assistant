class ConfirmationManager:

    def ask(self, command, classification, reason):

        print()
        print("=" * 60)
        print("⚠️  NEXUS ACTION REQUIRES CONFIRMATION")
        print("=" * 60)
        print()
        print(f"Command: {command}")
        print(f"Risk: {classification.upper()}")
        print(f"Reason: {reason}")
        print()

        answer = input("Allow this action? [y/N]: ").strip().lower()

        print()

        return answer in ("y", "yes")