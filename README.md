# 捡球机器人控制系统设计

## 设计（论文）的目的、原理、路线：

目的：设计一个捡球机器人控制系统，实现待捡球的视觉识别与捡起，并将球运送至目标位置。

原理：自动控制原理、单片机技术原理、传感器技术

路线：本文以树莓派为主控芯片，通过摄像头采集球场的图像，利用待捡球的颜色特征和轮廓特征对球进行识别、定位和跟踪，在视觉导航下引导捡球小车向目标移动，通过耙轮机构完成捡球作业。

## 最终形态
演示视频：[Bilibili](https://www.bilibili.com/video/BV1vS4y1z7Se?share_source=copy_web)
![图片1](https://user-images.githubusercontent.com/65287961/171074607-12210ff4-e7b2-481e-93ed-71b21a3282db.png)
![IMG_1230(20220531-092220)](https://user-images.githubusercontent.com/65287961/171074713-aa86f96d-b0d2-4c7f-a414-c89c13aa2706.JPG)

