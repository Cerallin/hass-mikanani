## 蜜柑计划（Mikanani）的 homeassistant 集成

This is a hass integration for [Mikanani](https://mikanani.me).

### 功能

- 提供新番时间表传感器`sensor.bangumi_map`。

键是一个一位十进制数字，代表星期N或者是剧场版。0-6 代表从周日开始的一周，7 代表剧场版。

    0-6: 周日-周六
    7  : 剧场版

### 安装

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

打开HACS设置并添加本repo (https://github.com/Cerallin/hass-mikanani) 为一个自定义集成（分类要选**Integration**）

你也可以点击下方按钮一键安装：
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&repository=hass-mikanani&owner=Cerallin)

## 配置

在`config.yaml`里添加一行
```yaml
mikanani: true
```

之后重启HA。

（目前没什么配置，后续再添加一些选项）
