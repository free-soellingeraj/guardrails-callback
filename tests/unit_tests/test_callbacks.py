from guardrails.callback import Callback
from guardrails.rail import Rail


def test_rail_scalar_string_with_callbacks():
    rail_spec = """ 
<rail version="0.1">
<output>
  <string name="string_name" />
</output>

<instructions>
Hello world
</instructions>

<prompt>
Hello world
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
    Rail.from_string(rail_spec, callbacks=test_callbacks)

