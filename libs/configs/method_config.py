A2NetBCD_CFG = {
    'backbone_cfg': {
        'backbone_name': 'mobilenetv2',
        'output_stride': 32
    },
    'head_cfg': {
        'channel': 64,
        'dilation_sizes': [7, 5, 3, 1],
    },
    'optimizer_cfg': {
        'lr': 5e-4,
        'max_iter': 20000,
        'eva_per_iter': 2000,
        'power': 0.9,
        'min_lr': 0.0,
        'warm_up_iter': 1500,
        'warm_up_ratio': 1e-6,
        'lr_factor': 1.0,
    },
}

TFIGR_CFG = {
    'backbone_cfg': {
        'backbone_name': 'resnet18d',
        'output_stride': 32
    },
    'head_cfg': {
        'channel': 64,
        'num_grbs': 2,
    },
    'optimizer_cfg': {
        'lr': 5e-4,
        'max_iter': 20000,
        'eva_per_iter': 2000,
        'power': 0.9,
        'min_lr': 0.0,
        'warm_up_iter': 1500,
        'warm_up_ratio': 1e-6,
        'lr_factor': 1.0,
    },
}

ARCDNetBCD_CFG = {
    'backbone_cfg': {
        'backbone_name': 'resnet18d',
        'output_stride': 32
    },
    'head_cfg': {
        'channel': 64
    },
    'optimizer_cfg': {
        'lr': 5e-4,
        'max_iter': 20000,
        'eva_per_iter': 2000,
        'power': 0.9,
        'min_lr': 0.0,
        'warm_up_iter': 1500,
        'warm_up_ratio': 1e-6,
        'lr_factor': 1.0,
    },
}

ChangeStarUperNet_CFG = {
    'backbone_cfg': {
        'backbone_name': 'resnet18d',
        'output_stride': 32
    },
    'head_cfg': {
        'channel': 256,
        'inner_channel': 16,
    },
    'optimizer_cfg': {
        'lr': 5e-4,
        'max_iter': 20000,
        'eva_per_iter': 2000,
        'power': 0.9,
        'min_lr': 0.0,
        'warm_up_iter': 1500,
        'warm_up_ratio': 1e-6,
        'lr_factor': 1.0,
    },
}

A2Net_CFG = {
    'backbone_cfg': {
        'backbone_name': 'mobilenetv2',
        'output_stride': 32
    },
    'head_cfg': {
        'channel': 64,
    },
    'optimizer_cfg': {
        'lr': 5e-4,
        'max_iter': 20000,
        'eva_per_iter': 2000,
        'power': 0.9,
        'min_lr': 0.0,
        'warm_up_iter': 1500,
        'warm_up_ratio': 1e-6,
        'lr_factor': 1.0,
    },
}

A2NetMVIT_CFG = {
    'backbone_cfg': {
        'backbone_name': 'mobilevitv2',
        'output_stride': 32
    },
    'head_cfg': {
        'channel': 64,
    },
    'optimizer_cfg': {
        'lr': 5e-4,
        'max_iter': 20000,
        'eva_per_iter': 2000,
        'power': 0.9,
        'min_lr': 0.0,
        'warm_up_iter': 1500,
        'warm_up_ratio': 1e-6,
        'lr_factor': 1.0,
    },
}

A2Net34_CFG = {
    'backbone_cfg': {
        'backbone_name': 'resnet34d',
        'output_stride': 32
    },
    'head_cfg': {
        'channel': 128,
    },
    'optimizer_cfg': {
        'lr': 5e-4,
        'max_iter': 20000,
        'eva_per_iter': 2000,
        'power': 0.9,
        'min_lr': 0.0,
        'warm_up_iter': 1500,
        'warm_up_ratio': 1e-6,
        'lr_factor': 1.0,
    },
}

BISRNET_CFG = {
    'backbone_cfg': {
        'backbone_name': 'resnet34d',
        'output_stride': 8
    },
    'head_cfg': {
        'is_bisrnet': True,
        'de_channel_c5': 128,
    },
    'optimizer_cfg': {
        'lr': 5e-4,
        'max_iter': 20000,
        'eva_per_iter': 2000,
        'power': 0.9,
        'min_lr': 0.0,
        'warm_up_iter': 1500,
        'warm_up_ratio': 1e-6,
        'lr_factor': 1.0,
    },
}

SSCDL_CFG = {
    'backbone_cfg': {
        'backbone_name': 'resnet34d',
        'output_stride': 8
    },
    'head_cfg': {
        'is_bisrnet': False,
        'de_channel_c5': 128,
    },
    'optimizer_cfg': {
        'lr': 5e-4,
        'max_iter': 20000,
        'eva_per_iter': 2000,
        'power': 0.9,
        'min_lr': 0.0,
        'warm_up_iter': 1500,
        'warm_up_ratio': 1e-6,
        'lr_factor': 1.0,
    },
}

SCANNET_CFG = {
    'backbone_cfg': {
        'backbone_name': 'resnet34d',
        'output_stride': 8
    },
    'head_cfg': {
        'is_scannet': True,
        'image_size': [512, 512],
        'de_channel_c2': 64,
        'de_channel_c5': 128,
    },
    'optimizer_cfg': {
        'lr': 5e-4,
        'max_iter': 20000,
        'eva_per_iter': 2000,
        'power': 0.9,
        'min_lr': 0.0,
        'warm_up_iter': 1500,
        'warm_up_ratio': 1e-6,
        'lr_factor': 1.0,
    },
}

TED_CFG = {
    'backbone_cfg': {
        'backbone_name': 'resnet34d',
        'output_stride': 8
    },
    'head_cfg': {
        'is_scannet': True,
        'image_size': [512, 512],
        'de_channel_c2': 64,
        'de_channel_c5': 128,
    },
    'optimizer_cfg': {
        'lr': 5e-4,
        'max_iter': 20000,
        'eva_per_iter': 2000,
        'power': 0.9,
        'min_lr': 0.0,
        'warm_up_iter': 1500,
        'warm_up_ratio': 1e-6,
        'lr_factor': 1.0,
    },
}

CHANGEOS_CFG = {
    'backbone_cfg': {
        'backbone_name': 'resnet18d',
        'output_stride': 32
    },
    'head_cfg': {
        'decoder_channel': 64,
    },
    'optimizer_cfg': {
        'lr': 5e-4,
        'max_iter': 20000,
        'eva_per_iter': 2000,
        'power': 0.9,
        'min_lr': 0.0,
        'warm_up_iter': 1500,
        'warm_up_ratio': 1e-6,
        'lr_factor': 1.0,
    },
}

CHANGEOSGRM_CFG = {
    'backbone_cfg': {
        'backbone_name': 'resnet18d',
        'output_stride': 32
    },
    'head_cfg': {
        'decoder_channel': 64,
        'num_grbs': 2,
    },
    'optimizer_cfg': {
        'lr': 5e-4,
        'max_iter': 20000,
        'eva_per_iter': 2000,
        'power': 0.9,
        'min_lr': 0.0,
        'warm_up_iter': 1500,
        'warm_up_ratio': 1e-6,
        'lr_factor': 1.0,
    },
}

ARCDNet_CFG = {
    'backbone_cfg': {
        'backbone_name': 'resnet18d',
        'output_stride': 32
    },
    'head_cfg': {
        'channel': 64,
    },
    'optimizer_cfg': {
        'lr': 5e-4,
        'max_iter': 20000,
        'eva_per_iter': 2000,
        'power': 0.9,
        'min_lr': 0.0,
        'warm_up_iter': 1500,
        'warm_up_ratio': 1e-6,
        'lr_factor': 1.0,
    },
}
