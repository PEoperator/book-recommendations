/**
 * All | ⚡ Favorites + client-side search on category and View all pages.
 * No persistence (resets to All / empty query on every load).
 * Search composes with Favorites on category and View all pages.
 *
 * Home (data-page="home"):
 *   - Empty query: normal IA (Rushmore → categories → Latest).
 *   - Non-empty query: hide Rushmore + categories + Latest + CTA; show full-catalog Search results.
 * Category / View all: retain the All / Favorites controls and page-scoped search.
 */
(function () {
  var mode = "all";
  var query = "";

  function isHomePage() {
    return document.body && document.body.getAttribute("data-page") === "home";
  }

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

  function favoritesActive() {
    return !isHomePage() && mode === "favorites";
  }

  function cardMatches(card) {
    if (favoritesActive() && card.getAttribute("data-favorite") !== "true") {
      return false;
    }
    if (!query) return true;
    return cardSearchText(card).indexOf(query) !== -1;
  }

  function emptyMessage() {
    if (favoritesActive() && query) {
      return "No favorites match your search.";
    }
    if (query) {
      return "No books match your search.";
    }
    if (favoritesActive()) {
      return "No favorites in this category.";
    }
    return "";
  }

  function setHomeSearchMode(active) {
    var results = document.getElementById("home-search-results");
    var rushmore = document.getElementById("rushmore");
    var categories = document.getElementById("categories");
    var latest = document.getElementById("latest");
    var cta = document.getElementById("home-view-all-cta");

    document.body.classList.toggle("home-search-active", active);

    if (results) {
      if (active) {
        results.removeAttribute("hidden");
        results.setAttribute("aria-hidden", "false");
      } else {
        results.setAttribute("hidden", "");
        results.setAttribute("aria-hidden", "true");
      }
    }

    // Category menu: hide while results show (cleaner than dimming — full catalog replaces browse IA)
    [rushmore, categories, latest, cta].forEach(function (el) {
      if (!el) return;
      if (active) {
        el.setAttribute("hidden", "");
        el.setAttribute("aria-hidden", "true");
      } else {
        el.removeAttribute("hidden");
        el.setAttribute("aria-hidden", "false");
      }
    });
  }

  function cardsToFilter() {
    if (!isHomePage()) {
      return document.querySelectorAll("[data-book-card]");
    }
    if (query) {
      var grid = document.getElementById("home-search-grid");
      return grid ? grid.querySelectorAll("[data-book-card]") : [];
    }
    // Empty query on home: only Rushmore + Latest (not the hidden full catalog)
    var list = [];
    ["rushmore", "latest"].forEach(function (id) {
      var sec = document.getElementById(id);
      if (!sec) return;
      sec.querySelectorAll("[data-book-card]").forEach(function (card) {
        list.push(card);
      });
    });
    return list;
  }

  function applyFilters() {
    document.body.classList.toggle("filter-favorites", favoritesActive());
    document.body.classList.toggle("filter-search-active", !!query);

    document.querySelectorAll(".filter-btn").forEach(function (btn) {
      var active = btn.getAttribute("data-filter") === mode;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });

    if (isHomePage()) {
      setHomeSearchMode(!!query);
    }

    var cards = cardsToFilter();
    var visible = 0;
    // NodeList or Array both support forEach
    Array.prototype.forEach.call(cards, function (card) {
      var match = cardMatches(card);
      card.classList.toggle("is-filtered-out", !match);
      if (match) visible += 1;
    });

    // Keep hidden full-catalog cards out of Favorites empty-state math when not searching
    if (isHomePage() && !query) {
      var homeGrid = document.getElementById("home-search-grid");
      if (homeGrid) {
        homeGrid.querySelectorAll("[data-book-card]").forEach(function (card) {
          card.classList.remove("is-filtered-out");
        });
      }
    }

    var countEl = document.getElementById("home-search-count");
    if (countEl) {
      if (isHomePage() && query) {
        var label =
          visible === 1 ? "1 book" : visible + " books";
        if (favoritesActive()) {
          countEl.textContent = label + " in favorites matching “" + query + "”";
        } else {
          countEl.textContent = label + " matching “" + query + "”";
        }
      } else {
        countEl.textContent = "";
      }
    }

    var empty = document.getElementById("filter-empty");
    if (empty) {
      var showEmpty = visible === 0 && (favoritesActive() || !!query);
      empty.textContent = showEmpty ? emptyMessage() : "";
      empty.classList.toggle("is-visible", showEmpty);

      // Category / view-all single grid
      var grid = document.getElementById("books-grid");
      if (grid) {
        grid.style.display = showEmpty ? "none" : "";
      }

      // Home search grid
      var homeSearchGrid = document.getElementById("home-search-grid");
      if (homeSearchGrid && isHomePage() && query) {
        homeSearchGrid.style.display = showEmpty ? "none" : "";
      } else if (homeSearchGrid) {
        homeSearchGrid.style.display = "";
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
