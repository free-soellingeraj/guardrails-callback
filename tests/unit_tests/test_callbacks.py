# from typing import Optional, Union, Iterable
from pathlib import Path
import openai

import guardrails as gd
from guardrails.guard import Guard
from guardrails.callback import Callback

class WriteMsgCallback(Callback):
    
    def __init__(self, fp):
        self.fp = Path(fp)

    def before_prepare(self, **kwargs):
        self._append_text_to_file(text=0)

    def after_prepare(self, **kwargs):
        self._append_text_to_file(text=1)

    def before_call(self, **kwargs):
        self._append_text_to_file(text=2)

    def _append_text_to_file(self, text):
        with self.fp.open('a') as f:
            f.write(str(text)+'\n')

def rail_spec():
    return """
<rail version="0.1">
<output>
    <object name="bank_run" format="length: 2">
        <string
            name="explanation"
            description="A paragraph about what a bank run is."
            format="length: 200 280"
            on-fail-length="reask"
        />
        <url
            name="follow_up_url"
            description="A web URL where I can read more about bank runs."
            format="valid-url"
            on-fail-valid-url="filter"
        />
    </object>
</output>

<prompt>
Explain what a bank run is in a tweet.

@xml_prefix_prompt

{output_schema}

@json_suffix_prompt_v2_wo_none
</prompt>
</rail>
"""

test_callbacks = (
    WriteMsgCallback(fp='cb1.txt'),
    WriteMsgCallback(fp='cb2.txt')
)

content = gd.docs_utils.read_pdf("docs/examples/data/chase_card_agreement.pdf")
rail = gd.Rail.from_string(string=rail_spec())
guard = Guard.from_rail_string(rail_spec(), callbacks=test_callbacks)

openai.api_key = os.getenv('OPENAI_API_KEY')
# Wrap the OpenAI API call with the `guard` object
raw_llm_output, validated_output = guard(
    llm_api=openai.Completion.create,
    engine="text-davinci-003",
    max_tokens=1024,
    temperature=0.3,
)

