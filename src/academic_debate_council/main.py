#!/usr/bin/env python
import sys
from dotenv import load_dotenv
from academic_debate_council.crew import AcademicDebateCouncilCrew

# Load environment variables
load_dotenv()

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'wellbeing_topic': 'sample_value'
    }
    AcademicDebateCouncilCrew().crew().kickoff(inputs=inputs)


def run_with_streaming(topic: str, callback_handler=None):
    """
    Run the crew with streaming support for Streamlit.
    
    Args:
        topic: The wellbeing topic to analyze
        callback_handler: Optional callback handler for streaming updates
    
    Returns:
        The crew execution result
    """
    inputs = {
        'wellbeing_topic': topic
    }
    
    crew = AcademicDebateCouncilCrew().crew()
    result = crew.kickoff(inputs=inputs)
    
    return result


def run_interactive():
    """
    Run the crew interactively with user input from command line.
    """
    print("=" * 60)
    print("Academic Debate Council - Interactive Mode")
    print("=" * 60)
    print()
    
    topic = input("Enter wellbeing topic to analyze: ").strip()
    
    if not topic:
        print("Error: Topic cannot be empty")
        return
    
    print(f"\n🚀 Starting analysis of: {topic}\n")
    print("This may take several minutes as 7 AI agents debate across 12 tasks...\n")
    
    inputs = {
        'wellbeing_topic': topic
    }
    
    result = AcademicDebateCouncilCrew().crew().kickoff(inputs=inputs)
    
    print("\n" + "=" * 60)
    print("✅ Analysis Complete!")
    print("=" * 60)
    
    return result


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'wellbeing_topic': 'sample_value'
    }
    try:
        AcademicDebateCouncilCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AcademicDebateCouncilCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'wellbeing_topic': 'sample_value'
    }
    try:
        AcademicDebateCouncilCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        print("\nCommands:")
        print("  run          - Run with sample topic")
        print("  interactive  - Run with interactive topic input")
        print("  train        - Train the crew")
        print("  replay       - Replay a specific task")
        print("  test         - Test the crew")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "interactive":
        run_interactive()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        print("\nAvailable commands: run, interactive, train, replay, test")
        sys.exit(1)
