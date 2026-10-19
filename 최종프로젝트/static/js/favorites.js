/*
상품 상세 화면의 즐겨찾기 버튼 + 메인 화면의 '최근 본 상품'

즐겨찾기  : 로그인한 회원의 즐겨찾기를 서버(DB)에 저장한다. (POST /api/favorites/toggle)
            로그인하지 않았으면 서버가 401을 돌려주고, 여기서 로그인 화면으로 보내준다.
최근 본 상품: 로그인과 상관없이 이 브라우저(localStorage)에만 저장한다.

  localStorage["recent"] = ["상품C", "상품A", ...]   ← 가장 최근에 본 상품이 맨 앞 (최대 4개)

최근 본 카드 화면 자체는 서버(/partials/cards)가 HTML 조각으로 만들어 주고,
여기서는 "어떤 상품을 보여줄지(상품명 목록)"만 정해서 요청한다.
*/

const MAX_RECENT = 4; // 최근 본 상품은 최대 4개까지만 기억 (메인 화면에 보여주는 개수와 같다)

// ── 즐겨찾기 (서버에 저장) ───────────────────────────────

function updateFavoriteButton(btn, isFav) {
  btn.textContent = isFav ? "★ 즐겨찾기됨" : "☆ 즐겨찾기";
  btn.classList.toggle("active", isFav);
}

// 상품 상세 페이지의 즐겨찾기 버튼 연결 (처음 모양은 서버가 이미 그려서 내려준다)
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("favorite-btn");
  if (!btn) return;

  btn.addEventListener("click", async () => {
    btn.disabled = true; // 응답을 기다리는 동안 연타 방지
    try {
      const res = await fetch("/api/favorites/toggle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ product_name: btn.dataset.product }),
      });

      if (res.status === 401) {
        // 로그인 전이면 로그인 화면으로 보내고, 로그인하면 이 상품 페이지로 돌아오게 한다
        const back = location.pathname + location.search;
        location.href = "/login?next=" + encodeURIComponent(back);
        return;
      }
      if (!res.ok) throw new Error("toggle failed");

      const data = await res.json();
      updateFavoriteButton(btn, data.favorite);
    } catch (e) {
      alert("즐겨찾기를 저장하지 못했어요. 잠시 후 다시 시도해주세요.");
    } finally {
      btn.disabled = false;
    }
  });
});

// ── 최근 본 상품 (이 브라우저에만 저장) ─────────────────────

function readList(key) {
  try {
    const raw = localStorage.getItem(key);
    const list = raw ? JSON.parse(raw) : [];
    return Array.isArray(list) ? list : [];
  } catch (e) {
    return []; // 저장값이 깨져 있어도 화면이 죽지 않게 빈 목록으로 처리
  }
}

function writeList(key, list) {
  try {
    localStorage.setItem(key, JSON.stringify(list));
  } catch (e) {
    // 저장이 막힌 환경(시크릿 모드 등)에서는 조용히 넘어간다
  }
}

// 상세 페이지를 열 때 호출: 중복은 지우고 맨 앞에 넣은 뒤 MAX_RECENT개까지만 남긴다.
function addRecent(productName) {
  let list = readList("recent").filter((name) => name !== productName);
  list.unshift(productName);
  writeList("recent", list.slice(0, MAX_RECENT));
}

// 상품명 목록을 서버에 보내서 카드 HTML을 받아 container 안에 넣는다.
// 결과를 문자열로 돌려준다:
//   "ok"    카드를 채웠음
//   "empty" 보여줄 상품이 없음 (목록이 비었거나, 서버에 없는 상품뿐)
//   "error" 서버에서 불러오지 못했음 (이걸 "비었음"과 구분해야 원인을 찾기 쉽다)
async function loadCards(container, names) {
  if (names.length === 0) return "empty";
  try {
    // 상품명에 &, %, + 같은 문자가 있어도 안전하게 보내려고 encodeURIComponent로 감싼다
    const query = names.map((n) => "names=" + encodeURIComponent(n)).join("&");
    const res = await fetch("/partials/cards?" + query);
    if (!res.ok) return "error";
    const html = await res.text();
    container.innerHTML = html;
    return html.trim() === "" ? "empty" : "ok";
  } catch (e) {
    return "error";
  }
}

// 최근 본 상품: 보여줄 게 있을 때만 섹션을 보여준다. (메인 화면에서만 쓴다)
// 예전 버전에서 저장된 값이 더 길어도 MAX_RECENT개까지만 보여준다.
async function renderRecent(sectionId, listId) {
  const section = document.getElementById(sectionId);
  const container = document.getElementById(listId);
  if (!section || !container) return;
  const names = readList("recent").slice(0, MAX_RECENT);
  const status = await loadCards(container, names);
  section.hidden = status !== "ok";
}
