#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: XHao
from torch import nn
from torch import Tensor

class ViTorchNet(nn.Module):
    def __init__(self):
        super(ViTorchNet, self).__init__()
        self.layers = nn.Sequential(
			nn.Conv2d(1, 96, kernel_size=(11, 11), stride=(4, 4)),
			nn.ReLU(),
			nn.MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=False),
			nn.Conv2d(96, 256, kernel_size=(5, 5), stride=(1, 1), padding=(2, 2)),
			nn.ReLU(),
			nn.MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=False),
			nn.Conv2d(256, 384, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)),
			nn.ReLU(),
			nn.Conv2d(384, 384, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)),
			nn.ReLU(),
			nn.Conv2d(384, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)),
			nn.ReLU(),
			nn.MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=False),
			FlattenLayer(),
			nn.Linear(in_features=6400, out_features=4096, bias=True),
			nn.ReLU(),
			nn.Dropout(p=0.5, inplace=False),
			nn.Linear(in_features=4096, out_features=4096, bias=True),
			nn.ReLU(),
			nn.Dropout(p=0.5, inplace=False),
			nn.Linear(in_features=4096, out_features=10, bias=True),
		)
    def forward(self,x: Tensor) -> Tensor:
        return self.layers(x)
        
class FlattenLayer(nn.Module):
    def __init__(self):
        super(FlattenLayer, self).__init__()

    def forward(self, x):
        return x.view(x.shape[0], -1)