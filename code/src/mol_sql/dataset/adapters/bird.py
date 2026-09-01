"""BIRD mini-dev source adapter."""

from .base import SourceAdapter


class BirdAdapter(SourceAdapter):
    source_family = "bird"
