from pelita import datamodel
from pelita.graph import AdjacencyList, NoPathException, diff_pos as diffPos
from pelita.player import AbstractPlayer, SimpleTeam
import numpy as np
import ipd
from UpperLowerSplit import EatingPlayerUpper, EatingPlayerLower

def factory():
    return(SimpleTeam("Upper Lower Split",EatingPlayerUpper(),EatingPlayerLower())
