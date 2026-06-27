import torch


class TorchAdapter:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"PyTorch Engine initialized on {self.device}")

    def process_signal(self, data):
        return torch.tensor(data) * 1.0
