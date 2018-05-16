from pelita.player import SimpleTeam
from .baseplayer import BasePlayer

def factory():
    return SimpleTeam("TeamSP", BasePlayer(), BasePlayer())
