"""Rendu des pages HTML a partir du manifeste et des fiches markdown."""

from .home import render_index, render_intro, render_search, render_search_index
from .pages import fiche_url, render_fiche, render_rubrique
from .template import render_page

__all__ = [
    "render_index",
    "render_intro",
    "render_search",
    "render_search_index",
    "render_fiche",
    "render_rubrique",
    "render_page",
    "fiche_url",
]
