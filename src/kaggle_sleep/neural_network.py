from torch.utils.data import Dataset
from torchvision.io import read_image

class TimeSeriesImageDataset(Dataset):

    def __init__(self, img_dir: str):
        self.img_dir = img_dir


