class CruncherEngine:
    def __init__(self):
        self.name = "Cruncher Data Sanitization Engine"

    def sanitize(self, raw_data):
        print(f"Cruncher: Sanitizing input data...")
        return "cleaned_data"

cruncher = CruncherEngine()
print(f"Engine {cruncher.name} initialized.")
