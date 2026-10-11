# 江南小小探索家 · Little Explorers · Jiangnan

研学文创周边系列 · 个人概念项目（Personal Concept Project）

**入口：打开 `index.html`（纯静态，无需构建、无需联网）。**

本项目是一份面向「研学周边设计师」岗位投递的完整概念作品：从 IP 角色、视觉识别、6 件 SKU 到场景应用与主视觉，全部素材共用同一套比例、色谱与构图规则。
所有视觉素材均为**代码生成的 SVG**（手写 + Python 构建脚本），文字由 HTML / SVG 排版，不依赖任何图像生成模型，保证文字零错字、角色比例零漂移。

---

## 目录结构

```
index.html              作品集网页（8 个章节，单文件，内联 CSS）
exports/                微信可直接发送的 PNG（7 张）
assets/
  characters/           角色：三视图 / 道具动作（11 件）
  identity/             识别：Logo / 色板 / 字体 / 纹样 / 图标（6 件）
  products/             6 件 SKU 设计图（900×700 统一画布）
  mockups/              产品矩阵 / 场景图 / 礼盒（3 件）
  final/                主视觉 hero（1600×900）
docs/design-brief.md    设计简报（PHASE 1）
IMAGE_PROMPTS.md        如需照片级质感场景图的可复用 prompt（14 条）
scripts/                构建与截图脚本（Python 3，无第三方依赖）
```

## 视觉系统（5 色定案，不再改动）

| 角色 | 名称 | 色值 |
|---|---|---|
| 主色 | 墨蓝 INK | `#26364F` |
| 主色 | 河青 CANAL TEAL | `#2E7D77` |
| 主色 | 荷绿 LOTUS GREEN | `#79B473` |
| 强调 | 柿橘 PERSIMMON | `#E9793B` |
| 底色 | 宣米 RICE PAPER | `#F4ECDD` |

配比：底色 60% / 河青+荷绿 25% / 墨蓝 10% / 柿橘 5%。
字体：中文 PingFang SC，西文 Helvetica Neue，点缀 Georgia Italic（均为系统字体栈，零字体依赖）。

## 6 件 SKU

1. 研学帆布袋 Canvas Bag — 河青
2. 儿童 / 亲子水杯 Water Bottle — 荷绿
3. 研学笔记本 Notebook — 河青
4. 贴纸套装 Sticker Set — 多色均衡
5. 徽章 / 冰箱贴 Badge & Magnet — 柿橘
6. 研学 T-shirt / Cap — 墨蓝

## exports/ · 微信发送用 PNG

| 文件 | 内容 |
|---|---|
| `01-hero.png` | 主视觉（1600×900，左上留标题区） |
| `02-characters.png` | 角色系统总览（三视图 / 道具动作 / 表情 / 组合） |
| `03-identity.png` | 视觉识别全套（Logo / 色板 / 字体 / 纹样 / 图标） |
| `04-product-grid.png` | 6 件 SKU 产品矩阵 |
| `05-lifestyle.png` | 场景图（河岸步道观察时刻） |
| `06-gift-box.png` | 礼盒包装概念 |
| `07-skus.png` | 6 张 SKU 设计图总览 |

## 重新生成

```bash
python3 scripts/export_wechat.py          # 重新导出 exports/*.png
python3 scripts/build_giftbox.py          # 重建礼盒 mockup
python3 scripts/contact.py out.png 3 460 500 assets/products/*.svg   # 任意接触表
```

仓库自检：27 件 SVG 全部 XML 合法、无重复 id；`index.html` 内所有资源路径存在。

## 说明与免责

本项目为**个人概念项目**，无真实客户、无真实订单、未量产，仅作为岗位能力参考作品。
角色与 IP 均为原创，不仿任何现有 IP；仓库内不含任何图像模型生成的位图素材。
如需帆布袋上身、礼盒摄影等照片级质感场景图，可在 `IMAGE_PROMPTS.md` 中取用与本视觉系统一致的 prompt，由人工或图像模型后续生成。
