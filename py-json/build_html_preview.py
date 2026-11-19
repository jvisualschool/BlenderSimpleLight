import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRESETS_JSON = os.path.join(ROOT_DIR, "py-json", "presets.json")
HTML_OUT = os.path.join(ROOT_DIR, "Preview", "index.html")

with open(PRESETS_JSON, "r", encoding="utf-8") as f:
    presets_data = json.load(f)

presets_json_str = json.dumps(presets_data["presets"], ensure_ascii=False, indent=2)

HTML_TEMPLATE = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Simple Light 1.0.0 - 조명 프리셋 갤러리 (Jinho Jung)</title>
  <style>
    :root {{
      --bg-base: #0b0f17;
      --bg-panel: #131b2b;
      --bg-card: #182236;
      --bg-hover: #1f2d47;
      --accent: #3b82f6;
      --accent-strong: #2563eb;
      --accent-soft: rgba(59, 130, 246, 0.16);
      --border: #263552;
      --text-main: #f1f5f9;
      --text-sub: #94a3b8;
      --text-muted: #64748b;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Pretendard", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
      background-color: var(--bg-base);
      color: var(--text-main);
      line-height: 1.5;
      padding-bottom: 64px;
    }}

    header {{
      background: linear-gradient(180deg, #111a2e 0%, var(--bg-base) 100%);
      border-bottom: 1px solid var(--border);
      padding: 28px 24px 22px;
      position: sticky;
      top: 0;
      z-index: 50;
      backdrop-filter: blur(12px);
    }}

    .container {{
      max-width: 1360px;
      margin: 0 auto;
    }}

    .header-top {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      margin-bottom: 18px;
    }}

    .brand-title {{
      display: flex;
      align-items: baseline;
      gap: 12px;
    }}

    .brand-title h1 {{
      font-size: 1.65rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: #ffffff;
    }}

    .badge {{
      background: var(--accent-soft);
      color: #60a5fa;
      border: 1px solid rgba(59, 130, 246, 0.35);
      padding: 3px 10px;
      border-radius: 999px;
      font-size: 0.78rem;
      font-weight: 600;
    }}

    .meta-info {{
      color: var(--text-sub);
      font-size: 0.88rem;
    }}

    .controls-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      justify-content: space-between;
    }}

    .search-box {{
      flex: 1 1 280px;
      max-width: 420px;
      position: relative;
    }}

    .search-box input {{
      width: 100%;
      padding: 10px 14px;
      background: var(--bg-panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text-main);
      font-size: 0.92rem;
      outline: none;
      transition: border-color 0.15s;
    }}

    .search-box input:focus {{
      border-color: var(--accent);
    }}

    .filter-group {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .btn {{
      background: var(--bg-panel);
      color: var(--text-sub);
      border: 1px solid var(--border);
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 0.86rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }}

    .btn:hover {{
      background: var(--bg-hover);
      color: var(--text-main);
    }}

    .btn.active {{
      background: var(--accent);
      border-color: var(--accent);
      color: #ffffff;
    }}

    /* Workspace Split: Detail + Compare */
    .workspace {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin: 28px auto;
      padding: 0 24px;
    }}

    @media (max-width: 1024px) {{
      .workspace {{
        grid-template-columns: 1fr;
      }}
    }}

    .panel-card {{
      background: var(--bg-panel);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    .panel-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .panel-title {{
      font-size: 1.15rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .viewer-frame {{
      position: relative;
      width: 100%;
      aspect-ratio: 1 / 1;
      background: #05070b;
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .viewer-frame.layout-mode {{
      aspect-ratio: 4 / 3;
    }}

    .viewer-frame img,
    .viewer-frame video {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: block;
      user-select: none;
      -webkit-user-drag: none;
    }}

    .missing-fallback {{
      padding: 24px;
      text-align: center;
      color: #f87171;
      font-size: 0.9rem;
      background: rgba(127, 29, 29, 0.25);
      border: 1px dashed #ef4444;
      border-radius: 8px;
    }}

    .observation-box {{
      background: var(--bg-card);
      border-left: 4px solid var(--accent);
      padding: 12px 14px;
      border-radius: 6px;
      font-size: 0.92rem;
    }}

    .observation-box strong {{
      color: #60a5fa;
      display: block;
      font-size: 0.8rem;
      margin-bottom: 4px;
    }}

    .recipe-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      font-size: 0.8rem;
      color: var(--text-sub);
    }}

    .recipe-tag {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      padding: 4px 10px;
      border-radius: 6px;
    }}

    /* Comparison Slider */
    .compare-selects {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      width: 100%;
    }}

    .compare-selects select {{
      flex: 1 1 180px;
      background: var(--bg-card);
      color: var(--text-main);
      border: 1px solid var(--border);
      padding: 8px 10px;
      border-radius: 8px;
      font-size: 0.88rem;
    }}

    .compare-container {{
      position: relative;
      width: 100%;
      aspect-ratio: 1 / 1;
      background: #05070b;
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid var(--border);
      touch-action: pan-y;
      cursor: ew-resize;
      outline: none;
    }}

    .compare-container:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.4);
    }}

    .compare-layer {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
    }}

    .compare-layer img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      pointer-events: none;
      user-select: none;
    }}

    .compare-left {{
      clip-path: inset(0 50% 0 0);
    }}

    .compare-handle {{
      position: absolute;
      top: 0;
      bottom: 0;
      left: 50%;
      width: 3px;
      background: var(--accent);
      transform: translateX(-50%);
      pointer-events: none;
    }}

    .compare-knob {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: var(--accent);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 0.85rem;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }}

    .compare-badge {{
      position: absolute;
      top: 12px;
      padding: 4px 10px;
      background: rgba(11, 15, 23, 0.82);
      border: 1px solid var(--border);
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 600;
      pointer-events: none;
    }}

    .compare-badge.left {{ left: 12px; color: #93c5fd; }}
    .compare-badge.right {{ right: 12px; color: #cbd5e1; }}

    /* Grid */
    .grid-section {{
      padding: 0 24px;
    }}

    .grid-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }}

    .preset-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
      gap: 18px;
    }}

    .preset-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      cursor: pointer;
      transition: transform 0.15s, border-color 0.15s;
      display: flex;
      flex-direction: column;
    }}

    .preset-card:hover {{
      transform: translateY(-2px);
      border-color: #476291;
    }}

    .preset-card.selected {{
      border-color: var(--accent);
      box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.35);
    }}

    .card-thumb {{
      position: relative;
      width: 100%;
      aspect-ratio: 1 / 1;
      background: #05070b;
      overflow: hidden;
    }}

    .card-thumb img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}

    .card-num {{
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(11, 15, 23, 0.85);
      color: #60a5fa;
      border: 1px solid rgba(59, 130, 246, 0.4);
      padding: 2px 8px;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 700;
    }}

    .card-cat {{
      position: absolute;
      top: 10px;
      right: 10px;
      background: rgba(11, 15, 23, 0.78);
      color: var(--text-sub);
      padding: 2px 8px;
      border-radius: 6px;
      font-size: 0.72rem;
    }}

    .card-body {{
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      flex: 1;
    }}

    .card-title {{
      font-size: 1rem;
      font-weight: 700;
      color: var(--text-main);
    }}

    .card-en {{
      font-size: 0.78rem;
      color: var(--text-sub);
    }}

    .card-obs {{
      font-size: 0.8rem;
      color: var(--text-sub);
      margin-top: 4px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    .card-actions {{
      display: flex;
      gap: 6px;
      margin-top: auto;
      padding-top: 8px;
    }}

    .mini-btn {{
      flex: 1;
      background: var(--bg-panel);
      color: var(--text-sub);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 5px 6px;
      font-size: 0.74rem;
      font-weight: 600;
      cursor: pointer;
    }}

    .mini-btn:hover {{
      border-color: var(--accent);
      color: #fff;
    }}
  </style>
</head>
<body>
  <header>
    <div class="container">
      <div class="header-top">
        <div class="brand-title">
          <h1>Simple Light</h1>
          <span class="badge">v1.0.0</span>
          <span class="badge">Blender 5.3+</span>
        </div>
        <div class="meta-info">
          개발자: <strong>Jinho Jung</strong> | 수잔(Suzanne) 비교 조명 프리셋 22종 오프라인 미리보기
        </div>
      </div>
      <div class="controls-bar">
        <div class="search-box">
          <input type="text" id="searchInput" placeholder="번호, 한글 이름, 영문 이름, 관찰 포인트 검색 (예: 08, 렘브란트, Rembrandt)..." />
        </div>
        <div class="filter-group" id="categoryFilters">
          <button class="btn active" data-cat="ALL">전체 (22)</button>
          <button class="btn" data-cat="톤과 대비">톤과 대비</button>
          <button class="btn" data-cat="광질">광질</button>
          <button class="btn" data-cat="방향과 인물">방향과 인물</button>
          <button class="btn" data-cat="소품과 공간">소품과 공간</button>
          <button class="btn" data-cat="색과 시간대">색과 시간대</button>
        </div>
      </div>
    </div>
  </header>

  <main class="container">
    <section class="workspace">
      <!-- Left: Selected Preset Detail Viewer -->
      <div class="panel-card">
        <div class="panel-header">
          <div class="panel-title" id="detailTitle">05 하드 라이트 (Hard Light)</div>
          <div class="filter-group">
            <button class="btn active" id="btnViewRender">렌더 결과 보기</button>
            <button class="btn" id="btnViewLayout">조명 배치 보기</button>
            <button class="btn" id="btnViewVideo" style="display:none;">반복 영상 보기 (1~48f)</button>
          </div>
        </div>
        <div class="viewer-frame" id="detailViewer"></div>
        <div class="observation-box">
          <strong>수잔에서 확인할 특징 (관찰 포인트)</strong>
          <span id="detailObservation"></span>
        </div>
        <div class="recipe-tags" id="detailRecipe"></div>
      </div>

      <!-- Right: Two-Preset Comparison Slider -->
      <div class="panel-card">
        <div class="panel-header">
          <div class="panel-title">두 조명 비교 슬라이더 (드래그 또는 좌우 화살표 키)</div>
          <div class="filter-group">
            <button class="btn" id="btnPair0506">05 하드 vs 06 소프트</button>
            <button class="btn" id="btnPair0312">03 실루엣 vs 12 림</button>
            <button class="btn" id="btnPair0911">09 버터플라이 vs 11 탑</button>
            <button class="btn" id="btnPair0422">04 보색 vs 22 틸앤오렌지</button>
          </div>
        </div>
        <div class="compare-selects">
          <select id="selectLeft" aria-label="왼쪽 비교 프리셋"></select>
          <select id="selectRight" aria-label="오른쪽 비교 프리셋"></select>
        </div>
        <div class="compare-container" id="compareBox" tabindex="0" role="slider" aria-label="두 조명 비교 경계선" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">
          <div class="compare-layer compare-right" id="compareRightLayer"></div>
          <div class="compare-layer compare-left" id="compareLeftLayer"></div>
          <div class="compare-handle" id="compareHandle">
            <div class="compare-knob">&#8596;</div>
          </div>
          <div class="compare-badge left" id="badgeLeft">05 하드 라이트</div>
          <div class="compare-badge right" id="badgeRight">06 소프트 라이트</div>
        </div>
        <div class="observation-box">
          <strong>비교 안내</strong>
          <span>동일한 카메라(70mm)와 수잔 구도에서 촬영된 두 프리셋의 그림자 경계, 밝기 대비, 색상 분리를 좌우로 움직여 대조할 수 있습니다.</span>
        </div>
      </div>
    </section>

    <section class="grid-section">
      <div class="grid-header">
        <h2>전체 조명 프리셋 목록 (<span id="countLabel">22</span> / 22)</h2>
      </div>
      <div class="preset-grid" id="presetGrid"></div>
    </section>
  </main>

  <script>
    const PRESETS = {presets_json_str};

    let currentPresetId = "05_hard";
    let currentViewMode = "RENDER"; // RENDER | LAYOUT | VIDEO
    let compareLeftId = "05_hard";
    let compareRightId = "06_soft";
    let sliderPercent = 50;
    let activeCategory = "ALL";
    let searchQuery = "";

    const detailTitle = document.getElementById("detailTitle");
    const detailViewer = document.getElementById("detailViewer");
    const detailObservation = document.getElementById("detailObservation");
    const detailRecipe = document.getElementById("detailRecipe");
    const btnViewRender = document.getElementById("btnViewRender");
    const btnViewLayout = document.getElementById("btnViewLayout");
    const btnViewVideo = document.getElementById("btnViewVideo");

    const selectLeft = document.getElementById("selectLeft");
    const selectRight = document.getElementById("selectRight");
    const compareBox = document.getElementById("compareBox");
    const compareLeftLayer = document.getElementById("compareLeftLayer");
    const compareRightLayer = document.getElementById("compareRightLayer");
    const compareHandle = document.getElementById("compareHandle");
    const badgeLeft = document.getElementById("badgeLeft");
    const badgeRight = document.getElementById("badgeRight");

    const presetGrid = document.getElementById("presetGrid");
    const countLabel = document.getElementById("countLabel");
    const searchInput = document.getElementById("searchInput");

    function getPreset(id) {{
      return PRESETS.find(p => p.id === id) || PRESETS[0];
    }}

    function createImageWithFallback(src, fallbackSrc, altText) {{
      const img = document.createElement("img");
      img.alt = altText;
      img.src = src;
      img.onerror = function() {{
        if (fallbackSrc && img.src.indexOf(fallbackSrc) === -1) {{
          img.src = fallbackSrc;
        }} else {{
          const msg = document.createElement("div");
          msg.className = "missing-fallback";
          msg.textContent = "이미지를 찾을 수 없습니다: " + src;
          if (img.parentNode) {{
            img.parentNode.replaceChild(msg, img);
          }}
        }}
      }};
      return img;
    }}

    function renderDetail() {{
      const p = getPreset(currentPresetId);
      detailTitle.textContent = `${{p.number}} ${{p.name_ko}} (${{p.name_en}})`;
      detailObservation.textContent = p.observation;

      btnViewVideo.style.display = p.video ? "inline-block" : "none";
      if (!p.video && currentViewMode === "VIDEO") {{
        currentViewMode = "RENDER";
      }}

      btnViewRender.classList.toggle("active", currentViewMode === "RENDER");
      btnViewLayout.classList.toggle("active", currentViewMode === "LAYOUT");
      btnViewVideo.classList.toggle("active", currentViewMode === "VIDEO");
      detailViewer.classList.toggle("layout-mode", currentViewMode === "LAYOUT");
      detailViewer.innerHTML = "";

      if (currentViewMode === "VIDEO" && p.video) {{
        const vid = document.createElement("video");
        vid.src = p.video;
        vid.autoplay = true;
        vid.loop = true;
        vid.muted = true;
        vid.playsInline = true;
        vid.controls = true;
        detailViewer.appendChild(vid);
      }} else if (currentViewMode === "LAYOUT") {{
        const pngFallback = p.layout.replace(/\\.webp$/, ".png");
        detailViewer.appendChild(createImageWithFallback(p.layout, pngFallback, p.name_ko + " 조명 배치"));
      }} else {{
        const pngFallback = p.render.replace(/\\.webp$/, ".png");
        detailViewer.appendChild(createImageWithFallback(p.render, pngFallback, p.name_ko + " 렌더"));
      }}

      detailRecipe.innerHTML = "";
      const catTag = document.createElement("span");
      catTag.className = "recipe-tag";
      catTag.textContent = `분류: ${{p.category}}`;
      detailRecipe.appendChild(catTag);

      (p.lights || []).forEach(l => {{
        const t = document.createElement("span");
        t.className = "recipe-tag";
        const unit = l.type === "SUN" ? "W/m²" : "W";
        t.textContent = `${{l.role}} (${{l.type}}): ${{l.energy}} ${{unit}} / ${{l.color_srgb}}`;
        detailRecipe.appendChild(t);
      }});
    }}

    function updateComparison() {{
      const pL = getPreset(compareLeftId);
      const pR = getPreset(compareRightId);
      selectLeft.value = pL.id;
      selectRight.value = pR.id;
      badgeLeft.textContent = `${{pL.number}} ${{pL.name_ko}}`;
      badgeRight.textContent = `${{pR.number}} ${{pR.name_ko}}`;

      compareLeftLayer.innerHTML = "";
      compareRightLayer.innerHTML = "";
      compareLeftLayer.appendChild(
        createImageWithFallback(pL.render, pL.render.replace(/\\.webp$/, ".png"), pL.name_ko)
      );
      compareRightLayer.appendChild(
        createImageWithFallback(pR.render, pR.render.replace(/\\.webp$/, ".png"), pR.name_ko)
      );
      setSliderPosition(sliderPercent);
    }}

    function setSliderPosition(pct) {{
      sliderPercent = Math.max(0, Math.min(100, pct));
      compareLeftLayer.style.clipPath = `inset(0 ${{100 - sliderPercent}}% 0 0)`;
      compareHandle.style.left = `${{sliderPercent}}%`;
      compareBox.setAttribute("aria-valuenow", Math.round(sliderPercent));
    }}

    function populateCompareSelects() {{
      selectLeft.innerHTML = "";
      selectRight.innerHTML = "";
      PRESETS.forEach(p => {{
        const o1 = document.createElement("option");
        o1.value = p.id;
        o1.textContent = `${{p.number}} ${{p.name_ko}} (${{p.name_en}})`;
        const o2 = o1.cloneNode(true);
        selectLeft.appendChild(o1);
        selectRight.appendChild(o2);
      }});
    }}

    function renderGrid() {{
      presetGrid.innerHTML = "";
      const q = searchQuery.trim().toLowerCase();
      const filtered = PRESETS.filter(p => {{
        if (activeCategory !== "ALL" && p.category !== activeCategory) return false;
        if (!q) return true;
        const hay = `${{p.number}} ${{p.name_ko}} ${{p.name_en}} ${{p.category}} ${{p.observation}} ${{p.subtitle_ko || ""}}`.toLowerCase();
        return hay.includes(q);
      }});

      countLabel.textContent = filtered.length;

      filtered.forEach(p => {{
        const card = document.createElement("div");
        card.className = "preset-card" + (p.id === currentPresetId ? " selected" : "");
        card.onclick = () => {{
          currentPresetId = p.id;
          renderDetail();
          renderGrid();
        }};

        const thumb = document.createElement("div");
        thumb.className = "card-thumb";
        thumb.appendChild(
          createImageWithFallback(p.render, p.render.replace(/\\.webp$/, ".png"), p.name_ko)
        );

        const num = document.createElement("span");
        num.className = "card-num";
        num.textContent = p.number;
        thumb.appendChild(num);

        const cat = document.createElement("span");
        cat.className = "card-cat";
        cat.textContent = p.category;
        thumb.appendChild(cat);

        const body = document.createElement("div");
        body.className = "card-body";

        const title = document.createElement("div");
        title.className = "card-title";
        title.textContent = p.name_ko;

        const en = document.createElement("div");
        en.className = "card-en";
        en.textContent = p.name_en;

        const obs = document.createElement("div");
        obs.className = "card-obs";
        obs.textContent = p.observation;

        const actions = document.createElement("div");
        actions.className = "card-actions";

        const btnL = document.createElement("button");
        btnL.className = "mini-btn";
        btnL.textContent = "비교 왼쪽에 놓기";
        btnL.onclick = (e) => {{
          e.stopPropagation();
          compareLeftId = p.id;
          updateComparison();
        }};

        const btnR = document.createElement("button");
        btnR.className = "mini-btn";
        btnR.textContent = "비교 오른쪽에 놓기";
        btnR.onclick = (e) => {{
          e.stopPropagation();
          compareRightId = p.id;
          updateComparison();
        }};

        actions.appendChild(btnL);
        actions.appendChild(btnR);

        body.appendChild(title);
        body.appendChild(en);
        body.appendChild(obs);
        body.appendChild(actions);

        card.appendChild(thumb);
        card.appendChild(body);
        presetGrid.appendChild(card);
      }});
    }}

    // Events
    btnViewRender.onclick = () => {{ currentViewMode = "RENDER"; renderDetail(); }};
    btnViewLayout.onclick = () => {{ currentViewMode = "LAYOUT"; renderDetail(); }};
    btnViewVideo.onclick = () => {{ currentViewMode = "VIDEO"; renderDetail(); }};

    selectLeft.onchange = (e) => {{ compareLeftId = e.target.value; updateComparison(); }};
    selectRight.onchange = (e) => {{ compareRightId = e.target.value; updateComparison(); }};

    document.getElementById("btnPair0506").onclick = () => {{ compareLeftId = "05_hard"; compareRightId = "06_soft"; updateComparison(); }};
    document.getElementById("btnPair0312").onclick = () => {{ compareLeftId = "03_silhouette"; compareRightId = "12_rim_light"; updateComparison(); }};
    document.getElementById("btnPair0911").onclick = () => {{ compareLeftId = "09_butterfly"; compareRightId = "11_top_light"; updateComparison(); }};
    document.getElementById("btnPair0422").onclick = () => {{ compareLeftId = "04_complementary"; compareRightId = "22_teal_and_orange"; updateComparison(); }};

    let isDragging = false;
    function updateFromPointer(clientX) {{
      const rect = compareBox.getBoundingClientRect();
      const pct = ((clientX - rect.left) / rect.width) * 100;
      setSliderPosition(pct);
    }}

    compareBox.addEventListener("pointerdown", (e) => {{
      isDragging = true;
      compareBox.setPointerCapture(e.pointerId);
      updateFromPointer(e.clientX);
    }});
    compareBox.addEventListener("pointermove", (e) => {{
      if (isDragging) updateFromPointer(e.clientX);
    }});
    compareBox.addEventListener("pointerup", () => {{ isDragging = false; }});
    compareBox.addEventListener("pointercancel", () => {{ isDragging = false; }});

    compareBox.addEventListener("keydown", (e) => {{
      if (e.key === "ArrowLeft") {{
        e.preventDefault();
        setSliderPosition(sliderPercent - 4);
      }} else if (e.key === "ArrowRight") {{
        e.preventDefault();
        setSliderPosition(sliderPercent + 4);
      }}
    }});

    searchInput.addEventListener("input", (e) => {{
      searchQuery = e.target.value;
      renderGrid();
    }});

    document.querySelectorAll("#categoryFilters .btn").forEach(btn => {{
      btn.addEventListener("click", () => {{
        document.querySelectorAll("#categoryFilters .btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        activeCategory = btn.getAttribute("data-cat");
        renderGrid();
      }});
    }});

    populateCompareSelects();
    renderDetail();
    updateComparison();
    renderGrid();
  </script>
</body>
</html>
"""

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(HTML_TEMPLATE)

print("Generated HTML gallery:", HTML_OUT)
