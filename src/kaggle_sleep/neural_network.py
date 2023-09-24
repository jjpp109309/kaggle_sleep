import os
import torch

import pandas as pd

from torch.utils.data import Dataset
from torchvision.io import read_image


class TimeSeriesImageDataset(Dataset):

    def __init__(self, annotations_path: str,  img_dir: str):
        self.labels = pd.read_csv(annotations_path)
        self.img_dir = img_dir

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):

        image_id, label = self.labels.iloc[idx]

        anglez_img_path = os.path.join(self.img_dir, f'{image_id}_anglez.jpg')
        enmo_img_path = os.path.join(self.img_dir, f'{image_id}_enmo.jpg')

        anglez_image = read_image(anglez_img_path)
        enmo_image = read_image(enmo_img_path)

        image = torch.cat((anglez_image, enmo_image))

        return image, label
