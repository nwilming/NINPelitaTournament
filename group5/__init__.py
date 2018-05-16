from pelita.player import SimpleTeam
from .harvester import Collector


def factory():
    return SimpleTeam("CollectorZ", Collector(), Collector())
