# IMAGE_PROMPTS.md

> **用途**：本仓库中的视觉素材当前全部由 **SVG 代码绘制**（矢量、可无限放大、可直接用于印刷排版）。
> 若需要**照片级实拍质感的产品效果图**，可使用下方 prompt 通过图像模型生成，
> 再替换 `assets/` 中对应文件即可。
>
> **通用规则（每条 prompt 均已内置）**
>
> 1. 画面中**不要出现任何文字 / 字母 / 数字 / logo 文字**——所有文案由 HTML/SVG 后期叠加。
> 2. 角色使用**统一 prompt 前缀**（见 §0），保证跨图一致性。
> 3. 统一光线：柔和自然光，左上 45° 主光，轻接触阴影，无强烈高反光。
> 4. 统一风格：modern flat illustration with subtle paper grain, no heavy outlines。
> 5. 禁止项：文字乱码、多余手指/肢体、变形五官、水印、真实品牌 logo、写实照片风格（除非该条明确要求 mockup）。
>
> **命名对应**：每条 prompt 对应一张目标图，文件名见 `assets/` 路径列。

---

## 0. 角色一致性前缀（Character Prefix，所有含角色的 prompt 都要拼接）

```
Two original flat-illustration child characters in a consistent style:
- BOY "Xiaozhou": 10 years old, short dark navy hair (#26364F) with one small tuft,
  oval face, simple dot-and-arc friendly face, small round blush, wearing an
  off-white raglan T-shirt with teal (#2E7D77) short sleeves, ink-navy shorts,
  white sneakers with teal soles, an orange (#E9793B) small field-research backpack.
- GIRL "Xiaohe": 10 years old, shoulder-length dark navy hair with two
  lotus-leaf-shaped green (#79B473) hair clips, same face construction as the boy,
  wearing a white blouse under a lotus-green pinafore dress, white sneakers with
  orange laces.
Same head-to-body ratio (about 1 : 2.9), same skin tone #F7DCC4, same eye style,
same lineless flat coloring with one darker shade for depth, no black outlines.
Style keywords: modern flat illustration, soft hand-drawn texture, gentle paper
grain, Jiangnan water-town palette, clean vector-like shapes, children's cultural
creative merchandise design, warm and fresh, premium stationery brand look.
```

**Negative (append everywhere)**：`text, letters, chinese characters, gibberish typography, watermark, logo, extra fingers, six fingers, deformed hands, blurry face, photorealistic, 3d render, heavy black outline, neon colors, cluttered background`

---

## 1. character_sheet — 角色设定表

- **文件**：`assets/characters/character-sheet.png`（当前为 SVG：`assets/characters/character-sheet.svg`）
- **Prompt**：
```
[Character Prefix]
Character design sheet, two full-body characters standing side by side on a pure
off-white (#F4ECDD) background, frontal neutral standing pose, arms relaxed, feet
evenly placed on an invisible baseline; large empty margin around them, symmetrical
composition, character turnaround grid feeling without any text or measurement lines.
View: straight-on eye-level, full body, generous negative space on all sides.
Lighting: soft diffused, left-top 45°, very light contact shadow under feet.
Flat vector illustration, subtle paper grain.
```

## 2. xiaozhou — 小舟 单人主图

- **文件**：`assets/characters/xiaozhou.png`（SVG：`assets/characters/xiaozhou-front.svg`）
- **Prompt**：
```
[Character Prefix]
Full-body portrait of the BOY character "Xiaozhou" alone, standing on off-white
background, confident friendly smile, one hand giving a small thumbs-up, the other
hand holding a folded paper map with abstract route lines (no text), orange backpack
visible over shoulders.
Composition: character centered slightly left, vertical portrait, head-to-toe with
20% empty space above the head.
View: front eye-level. Light: soft, left-top 45°, faint ground shadow.
```

## 3. xiaohe — 小荷 单人主图

- **文件**：`assets/characters/xiaohe.png`（SVG：`assets/characters/xiaohe-front.svg`）
- **Prompt**：
```
[Character Prefix]
Full-body portrait of the GIRL character "Xiaohe" alone, standing on off-white
background, curious tilted-head smile, holding a small cream-colored observation
notebook with a green leaf on the cover (no text), a big lotus leaf held like an
umbrella in her other hand.
Composition: character centered slightly right, vertical portrait, 20% empty space
above head. View: front eye-level. Light: soft, left-top 45°, faint ground shadow.
```

## 4. logo — 品牌标志

- **文件**：`assets/identity/logo.png`（SVG：`assets/identity/logo.svg`）
- **Prompt**：
```
Minimal abstract brand mark for a children's Jiangnan study-tour merchandise line:
a single continuous line forming a stone-arch bridge whose arch doubles as a
magnifying-glass circle, with a tiny water ripple below. Flat vector, two colors
only — canal teal #2E7D77 and ink navy #26364F — on off-white background.
Geometric, balanced, rounded terminals, no text, no letters, icon-only.
Square composition, centered, 25% padding.
```
> ⚠️ **推荐**：Logo 直接使用仓库中的 SVG（文字部分由 SVG 排版），图像模型仅用于灵感探索。

## 5. pattern — 底纹图案

- **文件**：`assets/identity/pattern.png`（SVG：`assets/identity/pattern.svg`）
- **Prompt**：
```
Seamless repeating pattern for stationery: small Jiangnan study-tour icons — arched
stone bridge, willow leaf, lotus pad, tiny fish, boat, magnifying glass, compass,
cloud — drawn as simple flat shapes, evenly spaced, alternating teal #2E7D77,
lotus green #79B473, persimmon #E9793B and ink navy #26364F on a warm off-white
#F4ECDD background. Uniform scale, 45° diagonal rhythm, no text, no outlines,
tileable edges, flat vector, subtle grain.
```

## 6. canvas_bag — SKU 01 研学帆布袋

- **文件**：`assets/products/sku01-canvas-bag.png`（SVG 同名 `.svg`）
- **Prompt**：
```
Product mockup: natural cotton canvas tote bag, front view, hanging straight against
a plain warm off-white studio wall. The bag face carries a flat illustration print:
an abstract canal-town route map with arched bridges and ripple lines in teal, the
two child characters standing at the lower-left corner, an orange band across the
bottom edge. Print occupies about 70% of the bag face with generous margins.
Visible cotton weave texture, soft natural wrinkles, stitched handles, slightly
rounded corners.
Lighting: soft studio, left-top 45°, gentle contact shadow to the lower right.
No text, no letters, no brand marks. Clean e-commerce product photography look
with flat-illustration artwork.
```

## 7. water_bottle — SKU 02 儿童/亲子水杯

- **文件**：`assets/products/sku02-water-bottle.png`（SVG 同名 `.svg`）
- **Prompt**：
```
Product mockup: 450ml insulated children's water bottle standing upright, three-quarter
front view, matte powder-coated body in warm white, silicone grip band around the
middle printed with a repeating flat pattern of lotus leaves and small fish in green
and teal, lid in lotus green with a small persimmon-orange carry loop, subtle
character silhouette (boy with magnifier) printed small near the base.
Plain off-white background, soft left-top 45° studio light, thin vertical highlight
on the bottle, soft contact shadow.
No text, no letters, no logos. Premium kids drinkware catalogue look.
```

## 8. notebook — SKU 03 研学笔记本

- **文件**：`assets/products/sku03-notebook.png`（SVG 同名 `.svg`）
- **Prompt**：
```
Product mockup: A5 hardcover study notebook, slightly angled three-quarter view lying
on an off-white surface, cover in warm off-white with a teal color block at the top
and a lotus-green spine, a die-cut style arched-window shape on the cover framing a
tiny flat illustration of a canal bridge and ripples, elastic band closure in
persimmon orange, visible page edges with cream paper.
Soft window light from upper-left, gentle shadow under the book, linen-like cover
texture. No text, no letters, no logos.
```

## 9. sticker_set — SKU 04 贴纸套装

- **文件**：`assets/products/sku04-sticker-set.png`（SVG 同名 `.svg`）
- **Prompt**：
```
Product mockup: a sheet of die-cut vinyl stickers for kids, flat top-down view on
off-white background, about 12 individual sticker shapes arranged in a loose grid
with clear margins: two child characters in different poses, arched bridge, lotus
leaf, small fish, magnifying glass, compass, folded map, backpack, cloud, boat.
Each sticker has a thin white die-cut border and a very light drop shadow, matte
finish with slight gloss. Colors: teal, lotus green, persimmon, ink navy on cream.
No text, no letters, no numbers. Flat illustration style, clean studio light.
```

## 10. badge — SKU 05 徽章 / 冰箱贴

- **文件**：`assets/products/sku05-badge-magnet.png`（SVG 同名 `.svg`）
- **Prompt**：
```
Product mockup: three round tin badges (44mm) arranged in a loose triangle on a cream
card backer, top-down slightly perspective view. Badge faces show flat illustrations:
one with the boy character head, one with an arched bridge and ripples, one with a
lotus leaf and small fish. Metallic silver rims with soft specular highlight, matte
printed faces, one badge flipped to show the pin back.
Warm off-white paper background with visible fiber texture, soft left-top light,
subtle shadows. No text, no letters, no numbers.
```

## 11. tshirt — SKU 06 研学 T-shirt / 帽子

- **文件**：`assets/products/sku06-tshirt-cap.png`（SVG 同名 `.svg`）
- **Prompt**：
```
Product mockup: kids' cotton T-shirt laid flat, front view, on a warm off-white
surface, ink-navy navy color with an off-white chest pocket area carrying a small
teal arch-bridge icon; a matching six-panel cap in teal with a persimmon button sits
folded at the lower right of the shirt. Soft fabric folds, visible cotton texture,
neat collar, sleeves arranged symmetrically.
Flat-lay photography look, soft diffused light from upper-left, gentle shadows.
No text, no letters, no logos, no hangers.
```

## 12. product_grid — 完整产品矩阵

- **文件**：`assets/mockups/product-grid.png`（SVG：`assets/mockups/product-grid.svg`）
- **Prompt**：
```
Series overview flat-lay: six merchandise items arranged in a strict 3×2 grid with
even margins on a warm off-white background — canvas tote, water bottle, A5 notebook,
sticker sheet, three badges, kids T-shirt with cap. Every item uses the same color
family (teal, lotus green, persimmon, ink navy on cream) and the same illustration
style, seen from a consistent top-down angle with uniform scale and identical soft
shadows. Generous spacing, catalog-style alignment, no text, no labels, no numbers.
Studio softbox lighting, subtle paper grain.
```

## 13. lifestyle_mockup — 研学 / 旅行场景

- **文件**：`assets/mockups/lifestyle-study.png`（SVG：`assets/mockups/lifestyle-study.svg`）
- **Prompt**：
```
Lifestyle scene, modern flat illustration: two children (using [Character Prefix])
standing on an arched stone bridge over a canal in a Jiangnan water town, one holding
a magnifying glass, one writing in a notebook; whitewashed houses with dark tile roofs
along the canal, a small boat, willow branches at the left edge, lotus leaves in the
water. Wide horizontal composition, characters placed on the lower-right third,
large calm sky area above for layout space.
Warm afternoon light from upper-left, long soft shadows, muted teal and cream palette,
subtle paper grain, no text, no letters, no signage characters.
```

## 14. final_hero — 主视觉

- **文件**：`assets/final/hero.png`（SVG：`assets/final/hero.svg`）
- **Prompt**：
```
Key visual poster illustration, wide 16:9: [Character Prefix] both characters seen
from behind-and-side, walking along a canal path toward an arched stone bridge at
sunset; layered silhouettes of water-town rooftops, a boat, willow leaves framing
the top-left corner. Flat vector illustration with soft gradient sky in cream and
pale teal, gentle grain, strong depth from three overlapping planes.
Composition leaves the upper-left third almost empty for a title overlay.
No text, no letters, no logos. Premium cultural-creative brand key visual.
```

---

## 附：文字叠加位置建议

| 画面 | 后期文字 | 建议工具 |
| --- | --- | --- |
| character_sheet | 角色名「小舟 / 小荷」+ 设定 | HTML/SVG |
| logo | 江南小小探索家 + Little Explorers | SVG（已内置） |
| 各 SKU | 产品名 + SKU 编号 | HTML 图注 |
| product_grid | 矩阵标题 + 6 个 SKU 标签 | HTML |
| final_hero | 主标题 + 副标题 | HTML 覆盖层 |
