import json
import sys


def clean_vs_code_stream(raw_data):
    # Strip unnecessary VS Code metadata and artifacts
    # This keeps only the actionable code for the AI
    clean_data = raw_data.strip()
    return clean_data


if __name__ == "__main__":
    try:
        raw_input = sys.stdin.read()
        print(clean_vs_code_stream(raw_input))
    except Exception as e:
        print(f"Error processing stream: {e}", file=sys.stderr)
