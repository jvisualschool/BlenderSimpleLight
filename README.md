# Simple Light

> ### ⬇️ 애드온 다운로드 (Blender 5.3+)
> **👉 [`simple_light-1.0.0.zip` 바로 다운로드](https://github.com/jvisualschool/BlenderSimpleLight/releases/download/v1.0.0/simple_light-1.0.0.zip)**  
> *(전체 소스를 받을 필요 없이 위 `.zip` 파일 하나만 받아서 Blender에 바로 설치하면 됩니다.)*

![Simple Light Blender 5.3.0 UI](Preview/simple_light_ui.jpg)

클릭 한 번으로 **22가지 시네마틱·스튜디오 조명**을 내 모델에 바로 적용할 수 있는 Blender 5.3+ 애드온입니다.  
수잔(Suzanne) 썸네일을 보고 원하는 분위기를 고르면, 피사체 크기에 맞춰 조명과 소품이 자동으로 배치됩니다.

---

## 미리보기 스크린샷

| 조명 렌더 예시 (3점 조명) | 3D 뷰포트 조명 배치 |
| :---: | :---: |
| <img src="Preview/images/07_three_point.webp" width="360" alt="3점 조명 렌더" /> | <img src="Preview/layouts/07_three_point.webp" width="360" alt="3점 조명 뷰포트 배치" /> |

| 조명 렌더 예시 (블라인드) | 3D 뷰포트 조명 배치 |
| :---: | :---: |
| <img src="Preview/images/14_venetian_blinds.webp" width="360" alt="블라인드 렌더" /> | <img src="Preview/layouts/14_venetian_blinds.webp" width="360" alt="블라인드 뷰포트 배치" /> |

> 전체 22종 조명 비교 갤러리는 [`Preview/index.html`](Preview/index.html)을 브라우저에서 열어 바로 확인할 수 있습니다.

---

## 설치 방법

1. 위 **[`simple_light-1.0.0.zip` 바로 다운로드](https://github.com/jvisualschool/BlenderSimpleLight/releases/download/v1.0.0/simple_light-1.0.0.zip)** 링크를 눌러 `.zip` 파일을 받습니다.
2. Blender **5.3.0 이상**을 실행하고 **Edit → Preferences → Get Extensions** (또는 **Add-ons**)를 엽니다.
3. 우측 상단 메뉴(`⌄`) → **Install from Disk...** 를 클릭합니다.
4. 방금 받은 `simple_light-1.0.0.zip` 파일을 선택해 설치하고, **Simple Light**가 체크되어 있는지 확인합니다.

---

## 사용 방법

1. 3D 뷰포트에서 조명을 비출 오브젝트(또는 컬렉션)를 선택합니다.
2. 키보드 **`N`**을 눌러 우측 사이드바에서 **Simple Light** 탭을 엽니다.
3. **1. 프리셋 선택**에서 수잔 썸네일을 클릭해 원하는 조명 모드를 고릅니다.
4. **2. 피사체 및 촬영 방향**에서 기준(`활성 카메라` 또는 `현재 뷰`)을 선택합니다.
   - 장면에 이미 다른 조명이 있다면 **비교 모드 (기존 조명 격리)**를 켜서 새 조명만 단독으로 확인할 수 있습니다.
5. **적용 / 교체** 버튼을 누르면 조명이 자동 설치됩니다.
   - 다른 프리셋을 고른 뒤 **적용 / 교체**를 다시 누르면 기존 내 오브젝트는 건드리지 않고 조명만 깔끔하게 바뀝니다.
   - 조명을 없애고 싶을 때는 **제거** 버튼을 누릅니다.
6. **3. 공통 및 프리셋별 조절**에서 밝기, 광원 크기, 회전, 좌우 반전 등을 슬라이더로 바로 다듬을 수 있습니다.
7. 빠르게 테스트해 보고 싶다면 **독립 수잔 비교 장면 열기** 버튼을 눌러보세요.

---

## 22가지 조명 모드

| 01. 하이키 (High-Key) | 02. 로우키 (Low-Key) | 03. 실루엣 (Silhouette) | 04. 보색 대비 (Complementary) |
| :---: | :---: | :---: | :---: |
| <img src="Preview/images/01_high_key.webp" width="180" alt="01 하이키" /> | <img src="Preview/images/02_low_key.webp" width="180" alt="02 로우키" /> | <img src="Preview/images/03_silhouette.webp" width="180" alt="03 실루엣" /> | <img src="Preview/images/04_complementary.webp" width="180" alt="04 보색 대비" /> |

| 05. 하드 라이트 (Hard Light) | 06. 소프트 라이트 (Soft Light) | 07. 3점 조명 (Three-Point) | 08. 렘브란트 (Rembrandt) |
| :---: | :---: | :---: | :---: |
| <img src="Preview/images/05_hard.webp" width="180" alt="05 하드 라이트" /> | <img src="Preview/images/06_soft.webp" width="180" alt="06 소프트 라이트" /> | <img src="Preview/images/07_three_point.webp" width="180" alt="07 3점 조명" /> | <img src="Preview/images/08_rembrandt.webp" width="180" alt="08 렘브란트" /> |

| 09. 버터플라이 (Butterfly) | 10. 스플릿 (Split) | 11. 탑 라이트 (Top Light) | 12. 림 라이트 (Rim Light) |
| :---: | :---: | :---: | :---: |
| <img src="Preview/images/09_butterfly.webp" width="180" alt="09 버터플라이" /> | <img src="Preview/images/10_split.webp" width="180" alt="10 스플릿" /> | <img src="Preview/images/11_top_light.webp" width="180" alt="11 탑 라이트" /> | <img src="Preview/images/12_rim_light.webp" width="180" alt="12 림 라이트" /> |

| 13. 언더 라이팅 (Under Lighting) | 14. 블라인드 (Venetian Blinds) | 15. 볼류메트릭 (Volumetric) | 16. 모티베이티드 (Motivated) |
| :---: | :---: | :---: | :---: |
| <img src="Preview/images/13_under_lighting.webp" width="180" alt="13 언더 라이팅" /> | <img src="Preview/images/14_venetian_blinds.webp" width="180" alt="14 블라인드" /> | <img src="Preview/images/15_volumetric.webp" width="180" alt="15 볼류메트릭" /> | <img src="Preview/images/16_motivated.webp" width="180" alt="16 모티베이티드 라이트" /> |

| 17. 프랙티컬 (Practical) | 18. 촛불 (Candlelight) | 19. 스포트라이트 (Spotlight) | 20. 골든아워 (Golden Hour) |
| :---: | :---: | :---: | :---: |
| <img src="Preview/images/17_practical.webp" width="180" alt="17 프랙티컬" /> | <img src="Preview/images/18_candlelight.webp" width="180" alt="18 촛불" /> | <img src="Preview/images/19_spotlight.webp" width="180" alt="19 스포트라이트" /> | <img src="Preview/images/20_golden_hour.webp" width="180" alt="20 골든아워" /> |

| 21. 블루아워 (Blue Hour) | 22. 틸앤오렌지 (Teal & Orange) | | |
| :---: | :---: | :---: | :---: |
| <img src="Preview/images/21_blue_hour.webp" width="180" alt="21 블루아워" /> | <img src="Preview/images/22_teal_and_orange.webp" width="180" alt="22 틸앤오렌지" /> | | |

---

## 라이선스

`GPL-3.0-or-later` · 개발자: Jinho Jung
