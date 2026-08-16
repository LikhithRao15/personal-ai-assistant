def request_confirmation(
    tool_name: str,
    description: str
):

    print()
    print("=" * 60)
    print("⚠️  CONFIRMATION REQUIRED")
    print("=" * 60)
    print(f"Tool: {tool_name}")
    print(f"Action: {description}")
    print()

    answer = input("Allow this action? [y/N]: ").strip().lower()

    return answer == "y"