/**
 * All | ⚡ Favorites filter — no persistence (resets to All on every load).
 */
(function () {
  function applyFilter(mode) {
    var isFav = mode === "favorites";
    document.body.classList.toggle("filter-favorites", isFav);

    document.querySelectorAll(".filter-btn").forEach(function (btn) {
      var active = btn.getAttribute("data-filter") === mode;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });

    // Empty-state for category / view-all pages
    var empty = document.getElementById("favorites-empty");
    if (empty) {
      var cards = document.querySelectorAll("[data-book-card]");
      var anyFav = false;
      cards.forEach(function (c) {
        if (c.getAttribute("data-favorite") === "true") anyFav = true;
      });
      var showEmpty = isFav && !anyFav;
      empty.classList.toggle("is-visible", showEmpty);
      // Also hide the grid when empty
      var grid = document.getElementById("books-grid");
      if (grid) {
        grid.style.display = showEmpty ? "none" : "";
      }
    }
  }

  function init() {
    document.querySelectorAll(".filter-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        applyFilter(btn.getAttribute("data-filter") || "all");
      });
    });
    // Default All every load — no sessionStorage/localStorage/URL
    applyFilter("all");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
