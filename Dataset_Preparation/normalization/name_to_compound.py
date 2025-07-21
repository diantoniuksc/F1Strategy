# Compound presets (compound triplets)
PRESETS = {
    'C1-C3': {'HARD': 'C1', 'MEDIUM': 'C2', 'SOFT': 'C3'},
    'C2-C4': {'HARD': 'C2', 'MEDIUM': 'C3', 'SOFT': 'C4'},
    'C3-C5': {'HARD': 'C3', 'MEDIUM': 'C4', 'SOFT': 'C5'},
    'C4-C6': {'HARD': 'C4', 'MEDIUM': 'C5', 'SOFT': 'C6'},  

    'C2,C3,C5': {'HARD': 'C2', 'MEDIUM': 'C3', 'SOFT': 'C5'}, 
    'Not Happened': {'HARD': '0', 'MEDIUM': '0', 'SOFT': '0'}
}


YEAR_CONFIG = {
    2022: [
        (PRESETS['C1-C3'], {1, 6, 10, 15, 18}),
        (PRESETS['C2-C4'], {2, 4, 5, 12, 13, 14, 16, 19, 20, 21}),
        (PRESETS['C3-C5'], {7, 8, 9, 11, 17, 22}),
        # Australia (round 3) override:
        (PRESETS['C2,C3,C5'], {3}),  # thnx Pirelli for non-consecutive tyres
    ],
    2023: [
        (PRESETS['C1-C3'], {1, 7, 10, 13, 16, 17}),
        (PRESETS['C2-C4'], {2, 5, 12, 18, 20 }),
        (PRESETS['C3-C5'], {3, 4, 6, 8, 9, 11, 14, 15, 19, 21, 22}),
    ],
    2024: [
        (PRESETS['C1-C3'], {1, 4, 10, 12, 15, 23}),
        (PRESETS['C2-C4'], {2, 5, 6, 14, 19}),  
        (PRESETS['C3-C5'], {7, 8, 9, 11, 13, 16, 17, 18, 20, 21, 22, 24}), 
        (PRESETS['C3-C5'], {3}),
    ],
    2025: [
        (PRESETS['C1-C3'], {1}),     # Bahrain
        (PRESETS['C3-C5'], {2}),     # Jeddah
        (PRESETS['C4-C6'], {3}),     # Imola
        # later rounds:
        (PRESETS['Not Happened'], set(range(1, 25)) - {1, 2, 3}),
    ],
}

def get_compound(year: int, gp_round: int, name: str) -> str:
    name = name.upper()
    presets = YEAR_CONFIG.get(year)

    if not presets:
        return "0"
    
    for preset, rounds in presets:
        if gp_round in rounds:
            return preset.get(name, "0")
        
    return "0"

#print(get_compound(2024, 7, "Soft"))