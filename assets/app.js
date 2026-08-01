/* Bascule de theme + recherche cote client. Aucune dependance. */
(function () {
  "use strict";

  var STORAGE_KEY = "aec-theme";
  var COMBINING_MARKS = /[̀-ͯ]/g;

  /* ---- Theme --------------------------------------------------------- */
  function systemPrefersDark() {
    return (
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
    );
  }

  function currentTheme() {
    var forced = document.documentElement.getAttribute("data-theme");
    if (forced === "dark" || forced === "light") return forced;
    return systemPrefersDark() ? "dark" : "light";
  }

  function readStoredTheme() {
    try {
      return window.localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function storeTheme(theme) {
    try {
      window.localStorage.setItem(STORAGE_KEY, theme);
    } catch (e) {
      /* mode prive : la bascule reste valable pour la page courante */
    }
  }

  function applyTheme(theme, button) {
    document.documentElement.setAttribute("data-theme", theme);
    if (!button) return;
    var nextLabel =
      theme === "dark" ? "Passer au thème clair" : "Passer au thème sombre";
    button.setAttribute("aria-label", nextLabel);
    button.setAttribute("title", nextLabel);
    button.textContent = theme === "dark" ? "Thème clair" : "Thème sombre";
  }

  function setUpTheme() {
    var button = document.querySelector("[data-theme-toggle]");
    var stored = readStoredTheme();
    var initial =
      stored === "dark" || stored === "light" ? stored : currentTheme();
    applyTheme(initial, button);
    if (!button) return;
    button.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      storeTheme(next);
      applyTheme(next, button);
    });
  }

  /* ---- Recherche ------------------------------------------------------ */
  /* Les ligatures ne se decomposent pas en NFD : « main-d'oeuvre » doit
     retrouver « main-d'œuvre ». */
  function normalise(value) {
    return value
      .toLowerCase()
      .normalize("NFD")
      .replace(COMBINING_MARKS, "")
      .replace(/œ/g, "oe")
      .replace(/æ/g, "ae")
      .replace(/['’]/g, "'");
  }

  function matchesAllTerms(entry, terms) {
    for (var i = 0; i < terms.length; i += 1) {
      if (entry.haystack.indexOf(terms[i]) === -1) return false;
    }
    return true;
  }

  function renderResults(list, entries, base) {
    list.textContent = "";
    entries.forEach(function (entry) {
      var item = document.createElement("li");
      var link = document.createElement("a");
      link.href = base + entry.url;
      var title = document.createElement("strong");
      title.textContent = entry.titre;
      var summary = document.createElement("span");
      summary.textContent = entry.rubrique + " — " + entry.resume;
      link.appendChild(title);
      link.appendChild(summary);
      item.appendChild(link);
      list.appendChild(item);
    });
  }

  function describe(total, found, hasQuery) {
    if (!hasQuery) return total + " fiches au sommaire.";
    if (found === 0) return "Aucune fiche ne correspond à cette recherche.";
    if (found === 1) return "1 fiche trouvée.";
    return found + " fiches trouvées.";
  }

  function setUpSearch() {
    var field = document.querySelector("[data-search-field]");
    var list = document.querySelector("[data-search-results]");
    var status = document.querySelector("[data-search-status]");
    if (!field || !list || !window.SEARCH_INDEX) return;

    var base = field.getAttribute("data-base") || "";
    var entries = window.SEARCH_INDEX.map(function (entry) {
      var copy = {};
      for (var key in entry) copy[key] = entry[key];
      copy.haystack = normalise(
        [entry.titre, entry.resume, entry.rubrique, entry.mots || ""].join(" ")
      );
      return copy;
    });

    function update() {
      var query = normalise(field.value.trim());
      var terms = query ? query.split(/\s+/) : [];
      var found = terms.length
        ? entries.filter(function (entry) {
            return matchesAllTerms(entry, terms);
          })
        : entries;
      renderResults(list, found, base);
      if (status) {
        status.textContent = describe(
          entries.length,
          found.length,
          terms.length > 0
        );
      }
    }

    field.addEventListener("input", update);
    update();
  }

  function boot() {
    setUpTheme();
    setUpSearch();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
