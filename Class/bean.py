# -*- coding: utf-8 -*-

class PokemonBean:
    
    def __init__(self):
        self.yakkunId = None
        self.dexNumber = None
        self.name = None
        self.englishName = None
        #status ... ["メガゲンガー", 99]
        self.status = None
        self.baseStats = None
        #type ... [String type1, String type2]
        self.type = None
        #eggGroup ... ["怪獣", "植物"]
        self.eggGroup = None
        self.height = None
        self.weight = None
        #ability ... [[String ability1, String description], [String ability2, ...], [String hiddenAbility, ...]]
        self.ability = None
        self.effortValue = None
        self.imagePath = None
        self.imagePathSmall = None
        self.captureRate = None
        self.baseEggSteps = None
        self.baseHappiness = None
        self.malePercentage = None
        #growth_rate ... "1050k"
        self.growthRate = None
        #capture_location ... [[String(location), String(sublocation), String(help call), String(capture time), String(cartridge peculiar), String(note1), String(note2), String(note3)], [....]] None if null
        self.captureLocation = None
        #evolution ... [int(previous pokemon yakkunId), String(evolution process)] no null
        self.evolution = None
        #move ... [[String(move name), String(type), String(damage_category), int(power), int(accuracy), int(pp), Boolean(contact), String(description), String(acquiring state)],[ ... ]] no null
        self.move = None

class MoveBean:
    
    def __init__(self):
        self.name = None
        self.type = None
        self.damageCategory = None
        self.power = None
        self.powerZ = None
        self.accuracy = None
        self.pp = None
        self.contact = None
        self.target = None
        self.description = None
        self.descriptionZ = None
        
class PglBean:
    
    def __init__(self):
        self.updatedTime = None
        self.name = None
        self.pglId = None
        #type ... [String, String]
        self.type = None
        #move ... [[int(ranking), String(move name), float(percentage)], [ ... ]] no null
        self.move = None
        #ability ... [[int(ranking), String(ability name), float(percentage)], [ ... ]] no null
        self.ability = None
        #nature ... [[int(ranking), String(nature name), float(percentage)], [ ... ]] no null
        self.nature = None
        #item ... [[int(ranking), String(item name), float(percentage)], [ ... ]] no null
        self.item = None
        #pokemon_with ... [[int(ranking), String(pokemon_with id)], [ ... ]] no null
        self.pokemonWith = None
        #pokemon_victorious ... [[int(ranking), String(pokemon_victorious id)], [ ... ]] no null
        self.pokemonVictorious = None
        #move_victorious ... [[int(ranking), String(move_victorious name), float(percentage)], [ ... ]] no null
        self.moveVictorious = None
        #pokemon_defeated ... [[int(ranking), String(pokemon_defeated id)], [ ... ]] no null
        self.pokemonDefeated = None
        #move_defeated ... [[int(ranking), String(move_defeated name), float(percentage)], [ ... ]] no null
        self.moveDefeated = None
