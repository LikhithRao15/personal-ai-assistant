from app.brain.llm import AIBrain


def main():
    print("=" * 60)
    print("NEXUS — Personal AI Assistant")
    print("=" * 60)
    print("Type 'exit' to quit.\n")

    brain = AIBrain()

    while True:

        try:
            user_input = input("You: ").strip()

            if user_input.lower() in {"exit", "quit"}:
                print("NEXUS: Goodbye.")
                break

            if not user_input:
                continue

            response = brain.ask(user_input)

            print(f"\nNEXUS: {response}\n")

        except KeyboardInterrupt:
            print("\nNEXUS: Goodbye.")
            break

        except Exception as error:
            print(f"\nERROR: {error}\n")


if __name__ == "__main__":
    main()