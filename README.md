# NINPelitaTournament
A place for Pelita bots created during 2018 Intro 2 Pythonc course


# Instructions

Create a folder 'groupN' where N is your group ID. Place your players inside this folder. Importantly: Each group folder should be a python package and export a Pelita team. To do this create an `__init__.py` file and define a method called factory inside. This method needs to return your team:

    from pelita.player import SimpleTeam
    from .harvester import Collector
    
    def factory():
        return SimpleTeam("TeamName", Collector(), Collector())

This assumes that a module harvester.py exists in the group directory which defines a player called Collector.
