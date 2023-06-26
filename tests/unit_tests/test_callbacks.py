from guardrails.callback import Callback

import pytest

import guardrails as gd
from guardrails.utils.constants import constants

INSTRUCTIONS = "You are a helpful bot, who answers only with valid JSON"

PROMPT = "Extract a string from the text"

SIMPLE_RAIL_SPEC = f"""
<rail version="0.1">
<output>
    <string name="test_string" description="A string for testing." />
</output>
<instructions>

{INSTRUCTIONS}

</instructions>

<prompt>

{PROMPT}

</prompt>
</rail>
"""

test_callbacks = (
    Callback(
        before_prepare=lambda **kwargs: print('before_prepare success! 1'),
        after_prepare=lambda **kwargs: print('after_prepare success! 1'),
        before_call=lambda **kwargs: print('before_call success! 1')
    ),
    Callback(
        before_prepare=lambda **kwargs: print('before_prepare success! 2'),
        after_prepare=lambda **kwargs: print('after_prepare success! 2'),
        before_call=lambda **kwargs: print('before_call success! 2')
    )
)

def test_parse_prompt_with_callbacks():
    """Test parsing a prompt."""
    guard = gd.Guard.from_rail_string(SIMPLE_RAIL_SPEC, callbacks=test_callbacks)

    # Strip both, raw and parsed, to be safe
    assert guard.instructions.format().source.strip() == INSTRUCTIONS.strip()
    assert guard.prompt.format().source.strip() == PROMPT.strip()

