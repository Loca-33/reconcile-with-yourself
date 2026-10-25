# 素材清单 · 与内耗共处

## 命名规则

文件名固定，**直接覆盖同名文件即可生效**，不用改 HTML。

- 图片：HTML 里默认引用 `.jpg`，覆盖同名 jpg 即可。如需用 webp/png，改 [scripts/inject_assets.py](../scripts/inject_assets.py) 里的扩展名后 `python3 scripts/inject_assets.py` 重跑。
- 音频：统一 `.mp3`，已在 HTML 里注册好，**只要把同名 mp3 放进 `assets/audio/` 即可启用**（见下文"启用音频"）。

## 图片清单（10 张 · 已配 Pexels 免费图）

当前所有图来自 [Pexels](https://www.pexels.com)，**Pexels License 允许商用、无需署名**。下表 ID 列可点开原图。

| 文件 | 用在哪 | 当前配图 | Pexels ID |
|---|---|---|---|
| `img/prologue.jpg`         | 序幕 · 早晨的抉择       | 伸手关闹钟                       | [1028741](https://www.pexels.com/photo/1028741) |
| `img/act1-work.jpg`        | 第一幕 · 工作的沼泽     | 凌乱办公桌·burnout 主题          | [8386516](https://www.pexels.com/photo/8386516) |
| `img/act2-social.jpg`      | 第二幕 · 人际的显微镜   | 咖啡馆里看手机                   | [5917575](https://www.pexels.com/photo/5917575) |
| `img/act3-night.jpg`       | 第三幕 · 深夜的复盘     | 深夜独自站在窗前                 | [6943998](https://www.pexels.com/photo/6943998) |
| `img/ending-1-shutdown.jpg`| 结局一 · 断电关机       | 趴在写着 Burnout 的笔记本上     | [6837647](https://www.pexels.com/photo/6837647) |
| `img/ending-2-helpless.jpg`| 结局二 · 习得性无助     | 裹着毯子坐床上的孤独感           | [6754013](https://www.pexels.com/photo/6754013) |
| `img/ending-3-lowpower.jpg`| 结局三 · 低能量续航     | 用手臂遮住眼睛躺床上             | [7445347](https://www.pexels.com/photo/7445347) |
| `img/ending-4-reconcile.jpg`| 结局四 · 自我和解      | 温暖的卧室床头灯                 | [5968800](https://www.pexels.com/photo/5968800) |
| `img/ending-5-warrior.jpg` | 结局五 · 反内耗战士     | 床上摊开的笔记本与笔             | [5546890](https://www.pexels.com/photo/5546890) |
| `img/finale.jpg`           | 全剧终                 | 抽象神经网络渲染                 | [17483867](https://www.pexels.com/photo/17483867) |

## 音频清单（6 段 · 已配 Mixkit 免费音频）

来源：[Mixkit](https://mixkit.co)，**Mixkit License 允许商用、无需署名**（但不得转售音频本身）。

| 文件 | 用在哪 | 当前配音 | 时长 | Mixkit ID |
|---|---|---|---|---|
| `audio/bgm-prologue.mp3`   | 序幕～7:30           | Silent Descent (Eugenio Mininni) — 沉郁 film-score 钢琴   | 2:40 | [music/614](https://mixkit.co) |
| `audio/bgm-act1.mp3`       | 第一幕～11:30        | Skyline (Eugenio Mininni) — 沉重大提琴 + 钢琴             | 3:26 | [music/601](https://mixkit.co) |
| `audio/bgm-act2.mp3`       | 第二幕～13:00        | Beautiful Dream — 餐厅 jazz，带轻微紧张                    | 1:37 | [music/493](https://mixkit.co) |
| `audio/bgm-act3.mp3`       | 第三幕（含所有结局） | Vastness (Andrew Ev) — 空灵 ambient                       | 3:50 | [music/184](https://mixkit.co) |
| `audio/sfx-alarm.mp3`      | 序幕开场闹钟         | Digital clock digital alarm buzzer                        | 0:08 | [sfx/992](https://mixkit.co)   |
| `audio/sfx-message.mp3`    | 第二幕收消息         | Message pop alert                                          | 0:01 | [sfx/2354](https://mixkit.co)  |

## 浏览器自动播放限制

主流浏览器禁止页面在用户首次点击/交互前自动播放音频。这意味着：

- **序幕的闹钟 + BGM 可能要到玩家点了第一个选项后才响起。** 这是浏览器策略，不是 bug。
- 想强制开场就有声，需要加一个 "点击开始" 按钮先收集一次用户交互，再跳到序幕。需要时告诉我加。

## 替换音频

放新 mp3 时**保持文件名不变**直接覆盖即可。如果想换走 Mixkit、用别的曲：
1. 把新 mp3 改成上面表里的同名文件
2. 在 [story.html](../story.html) 里搜对应文件名，确认引用路径没问题
3. 不需要重跑注入脚本

## 免费素材推荐来源

- 图：[Unsplash](https://unsplash.com)、[Pexels](https://pexels.com) —— CC0 可商用
- 音乐：[Pixabay Music](https://pixabay.com/music/)、[Free Music Archive](https://freemusicarchive.org) —— 注意挑 CC0 / CC-BY
- 音效：[freesound.org](https://freesound.org)（注册免费）
