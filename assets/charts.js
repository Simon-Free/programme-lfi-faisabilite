/* Infobulles des figures. Sans dependance, sans reseau.
   Le survol enrichit : toute valeur reste lisible sans lui, sur la marque
   elle-meme ou dans la table de substitution. Le clavier montre la meme
   chose que la souris. */
(function () {
  "use strict";

  var bulle = null;

  function creer() {
    if (bulle) return bulle;
    bulle = document.createElement("div");
    bulle.className = "chart-bulle";
    bulle.setAttribute("role", "status");
    bulle.hidden = true;
    document.body.appendChild(bulle);
    return bulle;
  }

  function remplir(texte) {
    var boite = creer();
    var lignes = texte.split("\n");
    boite.textContent = "";
    var titre = document.createElement("strong");
    titre.textContent = lignes[0];
    boite.appendChild(titre);
    boite.appendChild(
      document.createTextNode(lignes.slice(1).join("\n"))
    );
    return boite;
  }

  /* Placee au-dessus de la marque, ramenee dans la fenetre si elle deborde. */
  function placer(boite, cible) {
    var zone = cible.getBoundingClientRect();
    boite.hidden = false;
    var taille = boite.getBoundingClientRect();
    var marge = 8;
    var x = zone.left + zone.width / 2 - taille.width / 2;
    var y = zone.top - taille.height - marge;
    if (y < marge) y = zone.bottom + marge;
    x = Math.max(marge, Math.min(x, window.innerWidth - taille.width - marge));
    boite.style.left = x + "px";
    boite.style.top = y + "px";
  }

  function montrer(cible) {
    var texte = cible.getAttribute("data-bulle");
    if (!texte) return;
    placer(remplir(texte), cible);
  }

  function cacher() {
    if (bulle) bulle.hidden = true;
  }

  function cibleDe(evenement) {
    var noeud = evenement.target;
    while (noeud && noeud !== document) {
      if (noeud.getAttribute && noeud.getAttribute("data-bulle")) return noeud;
      noeud = noeud.parentNode;
    }
    return null;
  }

  document.addEventListener("mouseover", function (evenement) {
    var cible = cibleDe(evenement);
    if (cible) montrer(cible);
  });
  document.addEventListener("mouseout", function (evenement) {
    if (cibleDe(evenement)) cacher();
  });
  document.addEventListener("focusin", function (evenement) {
    var cible = cibleDe(evenement);
    if (cible) montrer(cible);
  });
  document.addEventListener("focusout", cacher);
  document.addEventListener("keydown", function (evenement) {
    if (evenement.key === "Escape") cacher();
  });
  window.addEventListener("scroll", cacher, { passive: true });
  window.addEventListener("resize", cacher);
})();
