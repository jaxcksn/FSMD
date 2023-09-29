# Creating FSM Files

The FSM input file is a YAML file of the following format:

```YAML
filename: OUTPUT_FILE_NAME
states:
    - STATE_NAME
    - STATE_NAME
    - STATE_NAME
startstate: STATE_NAME
finalstates:
    - STATE_NAME
    - STATE_NAME
transitions:
    - FROM_STATE;TO_STATE;LABEL
    - FROM_STATE;TO_STATE;LABEL
    - FROM_STATE;TO_STATE;LABEL
```

## Section Descriptions

### filename

This should be a string, and is what the tool will rename the resulting diagram file.

### states

This is a list of all possible states in the state machine. Smaller names work better. You can subscript a number in the state by adding a underscore before each digit. For example, a state named S_1 in the input file will render as S₁ on the diagram, and a state named S_1_2 will render as S₁₂

When you refer to any states in other sections, they should exactly match the state in this section.

### startstate

This is the state where the state machine will start from. There should be exactly one string, and it should exactly match one of states listed in the [states section](#states).

### finalstates

This is a list of all final or "accepting" states in the machine. It's represented by a double circle on the diagram. The items in the list should exactly match a single state listed in the [states section](#states).

### transitions

This is a list of all the transitions in the state machine. The format is:

    START_STATE;END_STATE;LABEL

where:

- **START_STATE**: Is one of the states listed in the [states section](#states).
- **FINAL_STATE**: Is one of the states listed in the [states section](#states). If this is the same as START_STATE, it will render as transition to itself.
- **LABEL**: This is a string for the label of the transition. You can use most characters, except for a semicolon. If the `-E` CLI flag is set, the character "E" will automatically turn into "ε" to represent an epsilon transition.

## General Tips and Tricks
