class VoiceConstants:
    MAXIMUM_VOLUME = 100
    MINIMUM_VOLUME = 0

    VOLUME_STEP = 20
    BASE_OCTAVE = 6

    MINIMUM_OCTAVE = 0
    MAXIMUM_OCTAVE = 9

    INITIAL_OCTAVE = 6

class MappingConstants:
    RULE_VALID_JUMPING_VALUE = 2
    RULE_VALID_VALUE = 1
    RULE_INVALID_VALUE = 0

    TICKS_PER_BEAT = 480 # one beat is 480 ticks.
    INITIAL_BPM = 120
    MINIMUM_BPM = 10
    MAXIMUM_BPM = 300
    BPM_STEP = 10

class RulesConstants:
    intrument_rules_characters = {
        '!': 22, # Harmonica
        ';': 15, # Tubular Bells
        ',': 20, # Church Organ
    }

class InitialInstruments:
    instruments = {
        0: 0, # Piano
        1: 20, # Organ
        2: 6, # Harpsichord
        3: 71,  # Bassoon
    }