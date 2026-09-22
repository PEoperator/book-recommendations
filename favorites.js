/**
 * All | ⚡ Favorites + client-side search.
 * No persistence (resets to All / empty query on every load).
 * Search composes with Favorites: when Favorites is on, search filters within favorites.
 */
(function () {
  var mode = "all";
  var query = "";

  function cardSearchText(card) {
    // Title, author, and any visible blurb/notes in the card text block
    var body = card.querySelector(".p-6");
    var raw = body ? body.textContent || "" : "";
    if (!raw) {
      var parts = [];
      card.querySelectorAll("h3, p").forEach(function (el) {
        parts.push(el.textContent || "");
      });
      raw = parts.join(" ");
    }
    return raw.replace(/\s+/g, " ").trim().toLowerCase();
  }

  function cardMatches(card) {
    if (mode === "favorites" && card.getAttribute("data-favorite") !== "true") {
      return false;
    }
    if (!query) return true;
    return cardSearchText(card).indexOf(query) !== -1;
  }

  function emptyMessage() {
    if (mode === "favorites" && query) {
      return "No favorites match your search.";
    }
    if (query) {
      return "No books match your search.";
    }
    if (mode === "favorites") {
      return "No favorites in this category.";
    }
    return "";
  }

  function applyFilters() {
    document.body.classList.toggle("filter-favorites", mode === "favorites");
    document.body.classList.toggle("filter-search-active", !!query);

    document.querySelectorAll(".filter-btn").forEach(function (btn) {
      var active = btn.getAttribute("data-filter") === mode;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });

    var cards = document.querySelectorAll("[data-book-card]");
    var visible = 0;
    cards.forEach(function (card) {
      var match = cardMatches(card);
      card.classList.toggle("is-filtered-out", !match);
      if (match) visible += 1;
    });

    var empty = document.getElementById("filter-empty");
    if (empty) {
      var showEmpty = visible === 0 && (mode === "favorites" || !!query);
      empty.textContent = showEmpty ? emptyMessage() : "";
      empty.classList.toggle("is-visible", showEmpty);

      // Category / view-all single grid
      var grid = document.getElementById("books-grid");
      if (grid) {
        grid.style.display = showEmpty ? "none" : "";
      }
    }
  }

  function init() {
    document.querySelectorAll(".filter-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        mode = btn.getAttribute("data-filter") || "all";
        applyFilters();
      });
    });

    var input = document.getElementById("book-search");
    if (input) {
      input.addEventListener("input", function () {
        query = (input.value || "").trim().toLowerCase();
        applyFilters();
      });
      // Clear (search type=search X) also fires input in modern browsers
    }

    // Default All + empty query every load — no sessionStorage/localStorage/URL
    mode = "all";
    query = "";
    if (input) input.value = "";
    applyFilters();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
