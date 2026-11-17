import json
import os

PRESETS = [
    {
        "schema_version": 1,
        "id": "01_high_key",
        "number": "01",
        "name_ko": "하이키",
        "name_en": "High-Key",
        "category": "톤과 대비",
        "observation": "눈 안쪽과 턱 밑까지 밝고, 연한 그림자 속에서도 코와 입체감이 남는다.",
        "subtitle_ko": "그림자 없이 밝고 화사하게",
        "subtitle_en": "Bright and even, almost no shadows",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.8,
        "lights": [
            {
                "role": "Key",
                "type": "AREA",
                "position": [-2.0, -3.0, 3.5],
                "target": [0.0, 0.0, 1.2],
                "energy": 500.0,
                "color_srgb": "#FFFFFF",
                "size": 3.0
            },
            {
                "role": "Fill",
                "type": "AREA",
                "position": [2.0, -3.0, 2.5],
                "target": [0.0, 0.0, 1.2],
                "energy": 400.0,
                "color_srgb": "#FFFFFF",
                "size": 3.0
            },
            {
                "role": "Background",
                "type": "AREA",
                "position": [0.0, 0.8, 2.5],
                "target": [0.0, 1.5, 2.0],
                "energy": 400.0,
                "color_srgb": "#FFFFFF",
                "size": 2.0
            }
        ],
        "props": [],
        "render": "images/01_high_key.webp",
        "layout": "layouts/01_high_key.webp",
        "thumbnail": "icons/01_high_key.png"
    },
    {
        "schema_version": 1,
        "id": "02_low_key",
        "number": "02",
        "name_ko": "로우키",
        "name_en": "Low-Key",
        "category": "톤과 대비",
        "observation": "한쪽 눈두덩과 콧등만 떠오르고 얼굴 대부분은 어둡다.",
        "subtitle_ko": "어둠 속 일부만 빛나게",
        "subtitle_en": "Mostly dark, only part is lit",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.02,
        "lights": [
            {
                "role": "Key",
                "type": "AREA",
                "position": [-2.0, -1.0, 3.0],
                "target": [0.0, 0.0, 1.2],
                "energy": 250.0,
                "color_srgb": "#FFFFFF",
                "size": 0.5
            }
        ],
        "props": [],
        "render": "images/02_low_key.webp",
        "layout": "layouts/02_low_key.webp",
        "thumbnail": "icons/02_low_key.png"
    },
    {
        "schema_version": 1,
        "id": "03_silhouette",
        "number": "03",
        "name_ko": "실루엣",
        "name_en": "Silhouette",
        "category": "톤과 대비",
        "observation": "눈코의 묘사가 사라져도 양쪽 귀와 머리의 외곽이 배경에서 읽힌다.",
        "subtitle_ko": "역광만 남겨 형태로 보여주기",
        "subtitle_en": "Backlight only, the subject becomes a shape",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.8,
        "backdrop_offset_y": 2.4,
        "lights": [
            {
                "role": "Background",
                "type": "AREA",
                "position": [0.0, 0.8, 2.0],
                "target": [0.0, 2.4, 2.0],
                "energy": 800.0,
                "color_srgb": "#FFFFFF",
                "size": 2.0
            }
        ],
        "props": [],
        "render": "images/03_silhouette.webp",
        "layout": "layouts/03_silhouette.webp",
        "thumbnail": "icons/03_silhouette.png"
    },
    {
        "schema_version": 1,
        "id": "04_complementary",
        "number": "04",
        "name_ko": "보색 대비",
        "name_en": "Complementary",
        "category": "색과 시간대",
        "observation": "두 볼에 서로 다른 색이 맺히고 코 주변에 두 색의 경계가 생긴다.",
        "subtitle_ko": "보색 두 색을 양쪽에서 쏘아 강렬하게",
        "subtitle_en": "Two opposite colors from both sides",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.04,
        "lights": [
            {
                "role": "Left",
                "type": "AREA",
                "position": [-2.0, -2.0, 2.0],
                "target": [-0.35, -0.1, 1.15],
                "energy": 350.0,
                "color_srgb": "#FF2040",
                "size": 1.0
            },
            {
                "role": "Right",
                "type": "AREA",
                "position": [2.0, -2.0, 2.0],
                "target": [0.35, -0.1, 1.15],
                "energy": 350.0,
                "color_srgb": "#00D9FF",
                "size": 1.0
            }
        ],
        "props": [],
        "render": "images/04_complementary.webp",
        "layout": "layouts/04_complementary.webp",
        "thumbnail": "icons/04_complementary.png"
    },
    {
        "schema_version": 1,
        "id": "05_hard",
        "number": "05",
        "name_ko": "하드 라이트",
        "name_en": "Hard Light",
        "category": "광질",
        "observation": "코가 볼에 드리운 그림자의 경계가 날카롭다.",
        "subtitle_ko": "선명하고 날카로운 그림자",
        "subtitle_en": "Sharp-edged, crisp shadows",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.08,
        "lights": [
            {
                "role": "Key",
                "type": "AREA",
                "position": [-2.0, -3.0, 3.5],
                "target": [0.0, 0.0, 1.2],
                "energy": 500.0,
                "color_srgb": "#FFFFFF",
                "size": 0.08
            }
        ],
        "props": [],
        "render": "images/05_hard.webp",
        "layout": "layouts/05_hard.webp",
        "thumbnail": "icons/05_hard.png"
    },
    {
        "schema_version": 1,
        "id": "06_soft",
        "number": "06",
        "name_ko": "소프트 라이트",
        "name_en": "Soft Light",
        "category": "광질",
        "observation": "같은 방향의 코 그림자가 넓고 부드럽게 퍼진다.",
        "subtitle_ko": "경계가 부드럽게 번지는 그림자",
        "subtitle_en": "Gentle, gradual shadows",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.08,
        "energy_compensation": 1.08,
        "lights": [
            {
                "role": "Key",
                "type": "AREA",
                "position": [-2.0, -3.0, 3.5],
                "target": [0.0, 0.0, 1.2],
                "energy": 540.0,
                "color_srgb": "#FFFFFF",
                "size": 2.0
            }
        ],
        "props": [],
        "render": "images/06_soft.webp",
        "layout": "layouts/06_soft.webp",
        "thumbnail": "icons/06_soft.png"
    },
    {
        "schema_version": 1,
        "id": "07_three_point",
        "number": "07",
        "name_ko": "3점 조명",
        "name_en": "Three-Point Lighting",
        "category": "방향과 인물",
        "observation": "키는 콧등의 방향을 만들고, 필은 반대 눈을 드러내고, 백은 귀 끝을 배경에서 분리한다.",
        "subtitle_ko": "키, 필, 백 세 개로 만드는 조명의 기본",
        "subtitle_en": "Key, Fill, and Back light fundamentals",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.04,
        "backdrop_offset_y": 2.6,
        "lights": [
            {
                "role": "Key",
                "type": "AREA",
                "position": [-2.0, -3.0, 3.5],
                "target": [0.0, 0.0, 1.2],
                "energy": 500.0,
                "color_srgb": "#FFFFFF",
                "size": 1.0
            },
            {
                "role": "Fill",
                "type": "AREA",
                "position": [2.0, -3.0, 2.0],
                "target": [0.0, 0.0, 1.2],
                "energy": 150.0,
                "color_srgb": "#FFFFFF",
                "size": 2.0
            },
            {
                "role": "Back",
                "type": "AREA",
                "position": [1.0, 2.0, 3.0],
                "target": [0.0, 0.0, 1.2],
                "energy": 500.0,
                "color_srgb": "#FFFFFF",
                "size": 0.6
            }
        ],
        "props": [],
        "render": "images/07_three_point.webp",
        "layout": "layouts/07_three_point.webp",
        "thumbnail": "icons/07_three_point.png"
    },
    {
        "schema_version": 1,
        "id": "08_rembrandt",
        "number": "08",
        "name_ko": "렘브란트",
        "name_en": "Rembrandt",
        "category": "방향과 인물",
        "observation": "그늘진 쪽 눈 아래에 작은 삼각형 밝은 면이 남는다.",
        "subtitle_ko": "어두운 뺨에 빛의 삼각형",
        "subtitle_en": "A triangle of light on the shadow side",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.02,
        "calibrated_note": "수평각 58도, 높이 3.6m (위치 [-1.357, -0.848, 3.6], 크기 0.12m)로 수잔 돌출 주둥이 너머 오른쪽 뺨 눈 밑에 삼각형 하이라이트 형성 검증",
        "lights": [
            {
                "role": "Key",
                "type": "AREA",
                "position": [-1.357, -0.848, 3.6],
                "target": [0.0, 0.0, 1.2],
                "energy": 260.0,
                "color_srgb": "#FFFFFF",
                "size": 0.12
            },
            {
                "role": "Fill",
                "type": "AREA",
                "position": [2.0, -3.0, 2.0],
                "target": [0.0, 0.0, 1.2],
                "energy": 15.0,
                "color_srgb": "#FFFFFF",
                "size": 2.0
            }
        ],
        "props": [],
        "render": "images/08_rembrandt.webp",
        "layout": "layouts/08_rembrandt.webp",
        "thumbnail": "icons/08_rembrandt.png"
    },
    {
        "schema_version": 1,
        "id": "09_butterfly",
        "number": "09",
        "name_ko": "버터플라이",
        "name_en": "Butterfly",
        "category": "방향과 인물",
        "observation": "코 바로 아래에 좌우 대칭에 가까운 짧은 그림자가 생긴다.",
        "subtitle_ko": "위에서 비춰 코 밑 나비 그림자",
        "subtitle_en": "Light from above, shadow under the nose",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.05,
        "lights": [
            {
                "role": "Key",
                "type": "AREA",
                "position": [0.0, -3.0, 3.5],
                "target": [0.0, 0.0, 1.2],
                "energy": 500.0,
                "color_srgb": "#FFFFFF",
                "size": 0.7
            }
        ],
        "props": [],
        "render": "images/09_butterfly.webp",
        "layout": "layouts/09_butterfly.webp",
        "thumbnail": "icons/09_butterfly.png"
    },
    {
        "schema_version": 1,
        "id": "10_split",
        "number": "10",
        "name_ko": "스플릿",
        "name_en": "Split",
        "category": "방향과 인물",
        "observation": "이마와 코 중심을 따라 얼굴의 밝은 절반과 어두운 절반이 나뉜다.",
        "subtitle_ko": "얼굴 반쪽만 빛, 반쪽은 어둠",
        "subtitle_en": "Light splits the face in half",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.02,
        "lights": [
            {
                "role": "Key",
                "type": "AREA",
                "position": [-3.0, 0.0, 1.2],
                "target": [0.0, 0.0, 1.2],
                "energy": 350.0,
                "color_srgb": "#FFFFFF",
                "size": 0.4
            }
        ],
        "props": [],
        "render": "images/10_split.webp",
        "layout": "layouts/10_split.webp",
        "thumbnail": "icons/10_split.png"
    },
    {
        "schema_version": 1,
        "id": "11_top_light",
        "number": "11",
        "name_ko": "탑 라이트",
        "name_en": "Top Light",
        "category": "방향과 인물",
        "observation": "정수리와 눈썹 능선이 밝고 두 눈은 깊은 그늘에 들어간다.",
        "subtitle_ko": "머리 위 조명, 눈을 그림자로",
        "subtitle_en": "Overhead light hides the eyes",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.02,
        "lights": [
            {
                "role": "Key",
                "type": "AREA",
                "position": [0.0, -0.15, 4.0],
                "target": [0.0, -0.15, 1.2],
                "energy": 500.0,
                "color_srgb": "#FFFFFF",
                "size": 0.6
            }
        ],
        "props": [],
        "render": "images/11_top_light.webp",
        "layout": "layouts/11_top_light.webp",
        "thumbnail": "icons/11_top_light.png"
    },
    {
        "schema_version": 1,
        "id": "12_rim_light",
        "number": "12",
        "name_ko": "림 라이트",
        "name_en": "Rim Light",
        "category": "방향과 인물",
        "observation": "어두운 얼굴 둘레에 귀와 머리를 따라 가는 밝은 선이 생긴다.",
        "subtitle_ko": "뒤에서 비춰 윤곽선만 빛나게",
        "subtitle_en": "Backlight that outlines the edges",
        "target": [0.0, 0.0, 1.2],
        "backdrop_remove": True,
        "lights": [
            {
                "role": "Rim",
                "type": "AREA",
                "shape": "RECTANGLE",
                "position": [1.5, 2.0, 2.6],
                "target": [0.0, 0.0, 1.2],
                "energy": 900.0,
                "color_srgb": "#FFFFFF",
                "size": 0.25,
                "size_y": 2.0
            },
            {
                "role": "RimLeft",
                "type": "AREA",
                "shape": "RECTANGLE",
                "position": [-1.5, 2.0, 2.4],
                "target": [0.0, 0.0, 1.2],
                "energy": 550.0,
                "color_srgb": "#FFFFFF",
                "size": 0.25,
                "size_y": 2.0
            }
        ],
        "props": [
            {
                "type": "RIM_FLOOR_BLOCKER"
            }
        ],
        "render": "images/12_rim_light.webp",
        "layout": "layouts/12_rim_light.webp",
        "thumbnail": "icons/12_rim_light.png"
    },
    {
        "schema_version": 1,
        "id": "13_under_lighting",
        "number": "13",
        "name_ko": "언더 라이팅",
        "name_en": "Under Lighting",
        "category": "방향과 인물",
        "observation": "주둥이 아랫면이 밝아지고 코 그림자가 이마 쪽으로 올라간다.",
        "subtitle_ko": "아래에서 위로, 섬뜩하게",
        "subtitle_en": "Light from below for an eerie mood",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.02,
        "lights": [
            {
                "role": "Key",
                "type": "AREA",
                "position": [0.0, -1.5, 0.3],
                "target": [0.0, 0.0, 1.35],
                "energy": 200.0,
                "color_srgb": "#FFFFFF",
                "size": 0.4
            }
        ],
        "props": [],
        "render": "images/13_under_lighting.webp",
        "layout": "layouts/13_under_lighting.webp",
        "thumbnail": "icons/13_under_lighting.png"
    },
    {
        "schema_version": 1,
        "id": "14_venetian_blinds",
        "number": "14",
        "name_ko": "블라인드",
        "name_en": "Venetian Blinds",
        "category": "소품과 공간",
        "observation": "밝고 어두운 평행 띠가 얼굴 굴곡을 지나 배경까지 이어진다.",
        "subtitle_ko": "줄무늬 그림자로 누아르 감성",
        "subtitle_en": "Striped shadows for a noir look",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.25,
        "lights": [
            {
                "role": "Key",
                "type": "SPOT",
                "position": [-3.0, -2.0, 3.0],
                "target": [0.0, 0.0, 1.2],
                "energy": 900.0,
                "color_srgb": "#FFFFFF",
                "radius": 0.02,
                "spot_size_deg": 50.0,
                "spot_blend": 0.05
            }
        ],
        "props": [
            {
                "type": "BLINDS",
                "slat_count": 14,
                "slat_length": 4.0,
                "slat_height": 0.10,
                "slat_gap": 0.16,
                "slat_thickness": 0.02,
                "roll_deg": 20.0
            }
        ],
        "render": "images/14_venetian_blinds.webp",
        "layout": "layouts/14_venetian_blinds.webp",
        "thumbnail": "icons/14_venetian_blinds.png"
    },
    {
        "schema_version": 1,
        "id": "15_volumetric",
        "number": "15",
        "name_ko": "볼류메트릭",
        "name_en": "Volumetric",
        "category": "소품과 공간",
        "observation": "수잔 옆 빈 공간에도 빛줄기가 보이고 얼굴 윤곽이 안개에 묻히지 않는다.",
        "subtitle_ko": "안개 속에 보이는 빛줄기",
        "subtitle_en": "Visible beams of light through haze",
        "target": [0.0, 0.0, 1.2],
        "backdrop_remove": True,
        "lights": [
            {
                "role": "BackSpot",
                "type": "SPOT",
                "position": [2.0, 2.0, 4.0],
                "target": [0.0, 0.0, 1.2],
                "energy": 4500.0,
                "color_srgb": "#D5E8FF",
                "radius": 0.02,
                "spot_size_deg": 38.0,
                "spot_blend": 0.08
            },
            {
                "role": "Fill",
                "type": "AREA",
                "position": [-2.0, -3.0, 2.0],
                "target": [0.0, 0.0, 1.2],
                "energy": 35.0,
                "color_srgb": "#D5E8FF",
                "size": 2.0
            }
        ],
        "props": [
            {
                "type": "VOLUME_GOBO",
                "box_center": [0.0, 0.0, 2.0],
                "box_size": [6.0, 6.0, 4.0],
                "density": 0.035,
                "anisotropy": 0.45,
                "bar_width": 0.14,
                "bar_gap": 0.30,
                "bar_count": 5
            }
        ],
        "render": "images/15_volumetric.webp",
        "layout": "layouts/15_volumetric.webp",
        "thumbnail": "icons/15_volumetric.png"
    },
    {
        "schema_version": 1,
        "id": "16_motivated",
        "number": "16",
        "name_ko": "모티베이티드 라이트",
        "name_en": "Motivated Light",
        "category": "소품과 공간",
        "observation": "창의 위치와 밝은 볼의 방향이 일치해 빛이 어디서 들어왔는지 짐작할 수 있다.",
        "subtitle_ko": "창문처럼 화면 속에 이유가 있는 빛",
        "subtitle_en": "Light with a believable source in the scene",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.18,
        "lights": [
            {
                "role": "Window",
                "type": "AREA",
                "position": [-3.0, -0.4, 2.3],
                "target": [0.3, 0.6, 1.3],
                "energy": 950.0,
                "color_srgb": "#FFF0D8",
                "size": 0.25
            },
            {
                "role": "RoomFill",
                "type": "AREA",
                "position": [2.0, -2.5, 2.2],
                "target": [0.0, 0.0, 1.2],
                "energy": 20.0,
                "color_srgb": "#DCE8FF",
                "size": 2.5
            }
        ],
        "props": [
            {
                "type": "WINDOW_WALL",
                "wall_x": -1.8,
                "open_width": 1.5,
                "open_height": 2.0,
                "center_z": 1.5,
                "frame_thickness": 0.08
            }
        ],
        "render": "images/16_motivated.webp",
        "layout": "layouts/16_motivated.webp",
        "thumbnail": "icons/16_motivated.png"
    },
    {
        "schema_version": 1,
        "id": "17_practical",
        "number": "17",
        "name_ko": "프랙티컬",
        "name_en": "Practical",
        "category": "소품과 공간",
        "observation": "화면에 보이는 램프, 램프에 가까운 볼의 밝기, 바닥의 빛 자국이 연결된다.",
        "subtitle_ko": "화면 속 램프가 실제 광원",
        "subtitle_en": "A lamp in the frame is the light source",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.06,
        "lights": [
            {
                "role": "Bulb",
                "type": "POINT",
                "position": [-0.82, -0.7, 1.45],
                "energy": 110.0,
                "color_srgb": "#FFD0A0",
                "radius": 0.06
            }
        ],
        "props": [
            {
                "type": "PRACTICAL_LAMP",
                "position": [-0.82, -0.7, 1.45],
                "bulb_radius": 0.045,
                "emission_strength": 10.0,
                "shade_radius": 0.16,
                "shade_height": 0.18,
                "color_srgb": "#FFD0A0"
            }
        ],
        "render": "images/17_practical.webp",
        "layout": "layouts/17_practical.webp",
        "thumbnail": "icons/17_practical.png"
    },
    {
        "schema_version": 1,
        "id": "18_candlelight",
        "number": "18",
        "name_ko": "촛불",
        "name_en": "Candlelight",
        "category": "소품과 공간",
        "observation": "턱과 볼 아래가 따뜻하게 물든다. 같은 시드로 재생할 때 불꽃과 얼굴 밝기가 함께 흔들린다.",
        "subtitle_ko": "흔들리는 따뜻한 사극 조명",
        "subtitle_en": "Warm flickering light for period drama",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.03,
        "lights": [
            {
                "role": "Candle",
                "type": "POINT",
                "position": [-0.65, -0.8, 0.7],
                "energy": 45.0,
                "color_srgb": "#FFAA55",
                "radius": 0.025,
                "flicker": True,
                "flicker_amp": 0.08,
                "flicker_seed": 18
            }
        ],
        "props": [
            {
                "type": "CANDLE",
                "position": [-0.65, -0.8, 0.7],
                "candle_radius": 0.035,
                "candle_height": 0.30,
                "flame_height": 0.06,
                "emission_strength": 8.0,
                "color_srgb": "#FFAA55",
                "seed": 18
            }
        ],
        "render": "images/18_candlelight.webp",
        "layout": "layouts/18_candlelight.webp",
        "thumbnail": "icons/18_candlelight.png",
        "video": "images/18_candlelight.mp4"
    },
    {
        "schema_version": 1,
        "id": "19_spotlight",
        "number": "19",
        "name_ko": "스포트라이트",
        "name_en": "Spotlight",
        "category": "소품과 공간",
        "observation": "어두운 바닥에 빛의 웅덩이가 생기고 수잔이 그 안에 들어간다.",
        "subtitle_ko": "어둠 속 한 사람만 집중",
        "subtitle_en": "One pool of light in the dark",
        "target": [0.0, 0.0, 0.0],
        "backdrop_color_linear": 0.01,
        "lights": [
            {
                "role": "Spot",
                "type": "SPOT",
                "position": [0.0, -2.0, 4.0],
                "target": [0.0, 0.0, 0.0],
                "energy": 1000.0,
                "color_srgb": "#FFFFFF",
                "radius": 0.05,
                "spot_size_deg": 35.0,
                "spot_blend": 0.15
            }
        ],
        "props": [],
        "render": "images/19_spotlight.webp",
        "layout": "layouts/19_spotlight.webp",
        "thumbnail": "icons/19_spotlight.png"
    },
    {
        "schema_version": 1,
        "id": "20_golden_hour",
        "number": "20",
        "name_ko": "골든아워",
        "name_en": "Golden Hour",
        "category": "색과 시간대",
        "observation": "귀 가장자리는 금빛이고 바닥 그림자는 길게 뻗는다.",
        "subtitle_ko": "해 질 녘 낮고 따뜻한 햇빛",
        "subtitle_en": "Low, warm sunlight at sunset",
        "target": [0.0, 0.0, 1.2],
        "backdrop_remove": True,
        "lights": [
            {
                "role": "Sun",
                "type": "SUN",
                "elevation_deg": 8.0,
                "azimuth_deg": 140.0,
                "energy": 8.0,
                "color_srgb": "#FFAC50",
                "angle_deg": 1.0
            },
            {
                "role": "Fill",
                "type": "AREA",
                "position": [0.0, -2.0, 4.0],
                "target": [0.0, 0.0, 1.2],
                "energy": 60.0,
                "color_srgb": "#FFE2B8",
                "size": 4.0
            }
        ],
        "props": [],
        "render": "images/20_golden_hour.webp",
        "layout": "layouts/20_golden_hour.webp",
        "thumbnail": "icons/20_golden_hour.png"
    },
    {
        "schema_version": 1,
        "id": "21_blue_hour",
        "number": "21",
        "name_ko": "블루아워",
        "name_en": "Blue Hour",
        "category": "색과 시간대",
        "observation": "눈과 주둥이의 굴곡이 낮은 대비의 푸른빛 안에서 읽힌다.",
        "subtitle_ko": "해 진 뒤 차갑고 푸른 빛",
        "subtitle_en": "Cool blue light after sunset",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.06,
        "lights": [
            {
                "role": "Sky",
                "type": "AREA",
                "position": [0.0, 0.0, 5.0],
                "target": [0.0, 0.0, 1.2],
                "energy": 250.0,
                "color_srgb": "#82B7FF",
                "size": 5.0
            },
            {
                "role": "Fill",
                "type": "AREA",
                "position": [0.0, -3.0, 2.0],
                "target": [0.0, 0.0, 1.2],
                "energy": 50.0,
                "color_srgb": "#B8D4FF",
                "size": 3.0
            }
        ],
        "props": [],
        "render": "images/21_blue_hour.webp",
        "layout": "layouts/21_blue_hour.webp",
        "thumbnail": "icons/21_blue_hour.png"
    },
    {
        "schema_version": 1,
        "id": "22_teal_and_orange",
        "number": "22",
        "name_ko": "틸앤오렌지",
        "name_en": "Teal & Orange",
        "category": "색과 시간대",
        "observation": "얼굴이 따뜻한 한 덩어리로 읽히고 청록색 배경에서 분리된다.",
        "subtitle_ko": "따뜻한 피부, 차가운 배경",
        "subtitle_en": "Warm skin against cool shadows",
        "target": [0.0, 0.0, 1.2],
        "backdrop_color_linear": 0.25,
        "lights": [
            {
                "role": "Key",
                "type": "AREA",
                "position": [-1.8, -3.0, 2.4],
                "target": [0.0, 0.0, 1.2],
                "energy": 350.0,
                "color_srgb": "#FF8C3B",
                "size": 1.5
            },
            {
                "role": "Background",
                "type": "AREA",
                "position": [0.0, 0.8, 2.2],
                "target": [0.0, 1.5, 2.0],
                "energy": 700.0,
                "color_srgb": "#00A8B8",
                "size": 3.0
            },
            {
                "role": "RimShadow",
                "type": "AREA",
                "position": [2.2, 1.0, 2.4],
                "target": [0.0, 0.0, 1.2],
                "energy": 200.0,
                "color_srgb": "#00B8C8",
                "size": 1.5
            }
        ],
        "props": [],
        "render": "images/22_teal_and_orange.webp",
        "layout": "layouts/22_teal_and_orange.webp",
        "thumbnail": "icons/22_teal_and_orange.png"
    }
]

out_paths = [
    "/Users/jinhojung/Desktop/블렌더 조명 애드온/py-json/presets.json",
    "/Users/jinhojung/Desktop/블렌더 조명 애드온/py-json/simple_light/presets.json",
]

for p in out_paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump({"schema_version": 1, "d0_width": 1.640625, "presets": PRESETS}, f, ensure_ascii=False, indent=2)
print("Saved presets.json with", len(PRESETS), "presets.")
