"""
In-shop-clothes data-set for Pytorch
"""
import torch
import torch.utils.data as data
from PIL import Image

import os
from DataSet import transforms
from collections import defaultdict


def default_loader(path):
    return Image.open(path).convert('RGB')


class InShopClothes(data.Dataset):
    def __init__(self, root=None, label_txt=None,
                 transform=None, loader=default_loader):

        # Initialization data path and train(gallery or query) txt path

        if root is None:
            root = "/opt/intern/users/xunwang/DataSet/In_shop_clothes_retrieval/"
            label_txt = os.path.join(root, 'train.txt')

        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                         std=[0.229, 0.224, 0.225])
        if transform is None:
            transform = transforms.Compose([
                # transforms.CovertBGR(),
                transforms.Resize(256),
                transforms.RandomResizedCrop(scale=(0.16, 1), size=224),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                normalize,
            ])

        # read txt get image path and labels
        file = open(label_txt)
        images_anon = file.readlines()

        images = []
        labels = []

        for img_anon in images_anon:
            [img, label] = (img_anon.split('\t'))[:2]
            images.append(img)
            labels.append(int(label))

        classes = list(set(labels))

        # Generate Index Dictionary for every class
        Index = defaultdict(list)
        for i, label in enumerate(labels):
            Index[label].append(i)

        # Initialization Done
        self.root = root
        self.images = images
        self.labels = labels
        self.classes = classes
        self.transform = transform
        self.Index = Index
        self.loader = loader

    def __getitem__(self, index):
        fn, label = self.images[index], self.labels[index]
        img = self.loader(os.path.join(self.root, fn))
        if self.transform is not None:
            img = self.transform(img)
        return img, label

    def __len__(self):
        return len(self.images)


def testIn_Shop_Clothes():
    dataloader = InShopClothes(root="/Users/wangxun/DataSet/In_shop_clothes_retrieval/",
                           label_txt="/Users/wangxun/DataSet/In_shop_clothes_retrieval/train.txt")

    # print('dataloader.getName', dataloader.getName())
    print(dataloader.Index[3])

    img_loader = torch.utils.data.DataLoader(
        dataloader,
        batch_size=4, shuffle=True, num_workers=2)

    for index, batch in enumerate(img_loader):
        # print(img)
        print(batch)
        if index == 1:
            break
            # print('label', label)


if __name__ == "__main__":
    testIn_Shop_Clothes()