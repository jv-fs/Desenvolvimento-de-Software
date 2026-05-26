import pytest
from unittest.mock import MagicMock
import mido

# Importações do seu projeto
from src.Components.Mapping import initialPausesRule
from src.DataClasses.VoiceSpecs import VoiceSpecs
from src.DataClasses.ProjectConfigs import MappingConstants

@pytest.fixture
def setup_rule_and_mocks():
    rule = initialPausesRule()
    
    mock_voice_specs = MagicMock(spec=VoiceSpecs)
    mock_voice_specs.getVoiceIdentifier.return_value = 0
    
    midi_track = mido.MidiTrack()
    
    # Retorna uma tupla com os objetos que os testes vão precisar
    return rule, mock_voice_specs, midi_track

def test_rule_check_identifica_pausa_corretamente(setup_rule_and_mocks):
    # Desempacota os objetos preparados pela fixture
    rule, _, _ = setup_rule_and_mocks
    
    text = "A[15]B"
    index = 1 
    
    match = rule.RuleCheck(text, index)

    assert match.is_match is True
    assert match.payload == 15
    assert match.consumed_chars == 4

def test_rule_apply_insere_mensagem_midi(setup_rule_and_mocks):
    rule, mock_voice_specs, midi_track = setup_rule_and_mocks
    payload = 5 
    
    rule.RuleApply(payload, midi_track, mock_voice_specs)
    
    assert len(midi_track) == 1
    
    message = midi_track[0]
    assert message.type == 'note_off'
    assert message.velocity == 0
    assert message.time == payload * MappingConstants.TICKS_PER_BEAT