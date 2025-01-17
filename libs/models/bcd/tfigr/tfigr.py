import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvBnAct(nn.Module):
    def __init__(self, in_channel, out_channel,
                 kernel_size=1, stride=1, padding=0, dilation=1, groups=1, bias=True, act=True):
        super(ConvBnAct, self).__init__()
        if act:
            self.conv = nn.Sequential(
                nn.Conv2d(in_channel, out_channel, kernel_size=kernel_size, stride=stride, padding=padding,
                          dilation=dilation, groups=groups, bias=bias),
                nn.BatchNorm2d(out_channel),
                nn.ReLU(inplace=True)
            )
        else:
            self.conv = nn.Sequential(
                nn.Conv2d(in_channel, out_channel, kernel_size=kernel_size, stride=stride, padding=padding,
                          dilation=dilation, groups=groups, bias=bias),
                nn.BatchNorm2d(out_channel)
            )

    def forward(self, x):
        x = self.conv(x)
        return x


class ChannelAttention(nn.Module):
    def __init__(self, channel: int, reduction: int = 8):
        super(ChannelAttention, self).__init__()
        self.channel = channel
        self.reduction = reduction
        hid_channel = self.channel // self.reduction
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        self.mlp = nn.Sequential(
            nn.Conv2d(self.channel * 4, hid_channel, 1, bias=False),
            nn.ReLU(inplace=True),
            nn.Conv2d(hid_channel, self.channel * 4, 1, bias=False),
        )
        self.act = nn.Sigmoid()

    def forward(self, x):
        ca_max = self.mlp(self.max_pool(x))
        ca_avg = self.mlp(self.avg_pool(x))
        x = x * self.act(ca_max + ca_avg)

        return x


class GuideRefinementBlock(nn.Module):
    def __init__(self, channel: int):
        super(GuideRefinementBlock, self).__init__()
        self.channel = channel
        self.channel_attention = ChannelAttention(self.channel)
        self.fusion_conv = ConvBnAct(self.channel * 4, self.channel, kernel_size=3, stride=1, padding=1)
        self.pools_sizes = [0, 2, 4, 8]
        self.pool_convs = nn.ModuleList()
        self.refine_convs = nn.ModuleList()
        for pool_size in self.pools_sizes:
            pool_conv = nn.Sequential(
                nn.AvgPool2d(kernel_size=pool_size, stride=pool_size) if pool_size > 0 else nn.Identity(),
                nn.Conv2d(self.channel, self.channel, kernel_size=1)
            )
            refine_conv = ConvBnAct(self.channel, self.channel, kernel_size=3, stride=1, padding=1)
            self.pool_convs.append(pool_conv)
            self.refine_convs.append(refine_conv)

    def forward(self, inputs: list):
        inputs_up = inputs.copy()
        for i in range(len(inputs_up) - 1, 0, -1):
            inputs_up[i] = F.interpolate(inputs_up[i], inputs_up[0].size()[2:], mode='bilinear', align_corners=True)

        inputs_agg = self.channel_attention(torch.cat(inputs_up, dim=1))
        inputs_agg = self.fusion_conv(inputs_agg)
        outputs = []
        for idx, pool_conv in enumerate(self.pool_convs):
            x_pool = pool_conv(inputs_agg)
            x_output = self.refine_convs[idx](x_pool + inputs[idx])
            outputs.append(x_output)

        return outputs


class TemporalFeatureInteractionModule(nn.Module):
    def __init__(self, in_channel: int, out_channel: int, num_temporal: int = 2):
        super(TemporalFeatureInteractionModule, self).__init__()
        self.in_channel = in_channel
        self.out_channel = out_channel
        self.num_temporal = num_temporal
        self.sub_conv = ConvBnAct(self.in_channel, self.in_channel, kernel_size=3, stride=1, padding=1)
        self.enhance_convs = nn.ModuleList()
        for i in range(self.num_temporal):
            enhance_conv = ConvBnAct(self.in_channel, self.in_channel, kernel_size=3, stride=1, padding=1)
            self.enhance_convs.append(enhance_conv)

        self.cat_conv = ConvBnAct(self.in_channel * self.num_temporal, self.in_channel, kernel_size=3, stride=1,
                                  padding=1)
        self.channel_reduction_conv = ConvBnAct(self.in_channel, self.out_channel, kernel_size=1)

    def forward(self, temporal: list):
        sub_feature = self.sub_conv(torch.abs(temporal[0] - temporal[1]))
        enhance_temporal = temporal.copy()
        for idx, enhance_conv in enumerate(self.enhance_convs):
            enhance_temporal[idx] = enhance_conv(enhance_temporal[idx] * (1 + sub_feature))
        cat_feature = self.cat_conv(torch.cat(enhance_temporal, dim=1))
        out_feature = cat_feature + sub_feature
        out_feature = self.channel_reduction_conv(out_feature)

        return out_feature


class Decoder(nn.Module):
    def __init__(self, channel, num_bcd_class, num_features):
        super(Decoder, self).__init__()
        self.channel = channel
        self.num_bcd_class = num_bcd_class
        self.num_features = num_features
        self.sa_modules = nn.ModuleList()
        self.fusion_convs = nn.ModuleList()
        for i in range(0, self.num_features - 1):
            fusion_conv = ConvBnAct(self.channel, self.channel, kernel_size=3, stride=1, padding=1)
            self.fusion_convs.append(fusion_conv)

        self.cls = nn.Conv2d(self.channel, self.num_bcd_class, kernel_size=1)

    @staticmethod
    def up_add(a, b):
        out = F.interpolate(a, b.size()[2:], mode='bilinear', align_corners=True) + b
        return out

    def forward(self, inputs: list):
        reversed_inputs = inputs[::-1]
        for i in range(len(reversed_inputs) - 1):
            reversed_inputs[i + 1] = self.up_add(reversed_inputs[i], reversed_inputs[i + 1])
            reversed_inputs[i + 1] = self.fusion_convs[i](reversed_inputs[i + 1])

        mask = self.cls(reversed_inputs[-1])

        return mask


class TFIGR(nn.Module):
    def __init__(self,
                 context_encoder,
                 in_channels=None,
                 channel=64,
                 num_grbs=2,
                 num_bcd_class=2,
                 ):
        super(TFIGR, self).__init__()
        if in_channels is None:
            in_channels = [16, 24, 32, 96, 320]
        self.context_encoder = context_encoder
        self.in_channels = in_channels
        self.channel = channel
        self.num_grbs = num_grbs
        self.num_bcd_class = num_bcd_class
        self.temporal_difference_convs = nn.ModuleList()
        for in_channel in self.in_channels[1:]:
            td_conv = TemporalFeatureInteractionModule(in_channel, self.channel)
            self.temporal_difference_convs.append(td_conv)

        self.guide_refinement_blocks = nn.ModuleList(
            [GuideRefinementBlock(self.channel) for i in range(self.num_grbs)]
        )

        self.decoder = Decoder(self.channel, self.num_bcd_class, len(self.in_channels[1:]))

    def forward(self, x1, x2):
        x1_1, x1_2, x1_3, x1_4, x1_5 = self.context_encoder(x1)
        x2_1, x2_2, x2_3, x2_4, x2_5 = self.context_encoder(x2)
        x1_features = [x1_2, x1_3, x1_4, x1_5]
        x2_features = [x2_2, x2_3, x2_4, x2_5]

        td_features = []
        for idx, td_conv in enumerate(self.temporal_difference_convs):
            td_feature = td_conv([x1_features[idx], x2_features[idx]])
            td_features.append(td_feature)

        for idx, grb in enumerate(self.guide_refinement_blocks):
            td_features = grb(td_features)

        mask = self.decoder(td_features)
        mask = F.interpolate(mask, size=x1.size()[2:], mode='bilinear', align_corners=True)
        prediction = {
            'change_mask': [mask],
        }

        return prediction
