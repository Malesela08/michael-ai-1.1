import subprocess


def push_to_phone(title, message):
    # This calls the Android API directly
    subprocess.run(
        [
            "termux-notification",
            "--title",
            title,
            "--content",
            message,
            "--priority",
            "high",
        ]
    )


if __name__ == "__main__":
    print("Sending test notification...")
    push_to_phone("Michael AI", "Direct connection established!")
