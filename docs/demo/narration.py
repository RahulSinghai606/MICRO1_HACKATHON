"""Generate narration WAVs for the solution video via Azure TTS.

Usage: python docs/demo/narration.py   (needs AZURE key in matchpoint/.env as LLM_API_KEY)
Writes docs/demo/audio/s1.wav..s8.wav + durations.json
"""
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
AUDIO = HERE / "audio"
AUDIO.mkdir(exist_ok=True)

sys.path.insert(0, str(HERE.parents[1] / "src"))
from matchpoint.config import load_env  # noqa: E402

load_env()
KEY = os.environ["LLM_API_KEY"]

VOICE = "en-US-AndrewMultilingualNeural"

SECTIONS = {
    "s1": """This is Matchpoint — our submission for the micro1 Agentic Workflows Hackathon.
Agents that close the books. Humans that sign them.""",

    "s2": """Meet the user: an accounts-payable specialist. Before any supplier invoice is paid,
she must three-way match it — invoice, against purchase order, against goods receipt —
then screen for duplicates, tax errors, and changed bank accounts.
Industry research puts manual processing at thirteen to twenty dollars per invoice, and nine days per cycle.
And seventy-six percent of organizations were hit by payments fraud last year.
One miss is money that never comes back.""",

    "s3": """The obvious fix in twenty twenty-six: dump the OCR text and the ERP data into one big prompt,
and ask for a decision. That's our baseline — same model, same written policy,
same thirty-two gold-labeled invoices as the final system.
It scored eighty-one percent. And it silently approved thirty percent of the defective invoices:
every single arithmetic error, and both invoices where the goods were never received.
Language models are bad at multiplying — and worse at noticing what is absent.""",

    "s4": """Here is the final system on one real case, end to end.
Invoice N-I-S twenty-one-oh-seven arrives as an image. Mistral OCR reads it,
and an extraction agent turns it into strict JSON. It is forbidden from fixing numbers —
the printed numbers are the evidence.
Next, the matching agent investigates with deterministic tools: it pulls the purchase order,
sums goods receipts across partial deliveries, searches payment history for duplicates,
and calls an arithmetic checker. The model never does math.
Then an independent verifier — a deterministic match engine — recomputes every check from scratch.
And here it catches the defect: seven point two five percent of four thousand eight hundred forty-three dollars
is three fifty-one thirteen. The invoice claims three eighty-eight twenty-seven. Hold for investigation.
The baseline approved this exact invoice.""",

    "s5": """Nothing is paid by a machine. Every decision lands in a human approval queue,
and payments post only to a sandbox ledger after sign-off.
What the specialist receives is this audit packet — every decision,
with the exact numbers that justify it, ready to sign.""",

    "s6": """The final comparison. Same cases, same model, same policy.
Decision accuracy: eighty-one percent to one hundred.
Missed defects: thirty percent to zero. False holds stayed at zero — recall was not bought with spam.
And cost per invoice went down twenty-nine percent.
On a held-out batch, generated after the system was frozen: one hundred percent again.""",

    "s7": """The changelog connects each jump to evidence.
Scoping context fixed the needle-in-a-haystack misses, and cut cost by two thirds.
Deterministic tools were the single biggest win — missed defects went from thirty percent to zero.
The verifier closed the last gap. And memory plus human-in-the-loop made it operational.
One experiment we removed: we simply asked the model to recompute every number, step by step.
It got worse — exact match dropped eleven points, at over twice the cost.""",

    "s8": """Our hot take: the most reliable agent is the one with the smallest possible LLM surface area.
Every gain we measured came from taking a responsibility away from the model.
Our ablation is the punchline — extraction plus a deterministic engine alone also scores one hundred percent,
at a fifth of the cost. Spend the model only where the world is unstructured.
Code, data, and full agent trajectories are in the repo — reproducible from a clean machine.
Matchpoint. Thanks for watching.""",
}


def tts(name: str, text: str) -> float:
    import requests

    ssml = f"""<speak version='1.0' xml:lang='en-US'>
<voice name='{VOICE}'><prosody rate='+4%'>{text}</prosody></voice></speak>"""
    r = requests.post(
        "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1",
        headers={
            "Ocp-Apim-Subscription-Key": KEY,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
        },
        data=ssml.encode(),
        timeout=120,
    )
    r.raise_for_status()
    out = AUDIO / f"{name}.wav"
    out.write_bytes(r.content)
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(out)]).strip())
    return round(dur, 2)


if __name__ == "__main__":
    durations = {}
    for name, text in SECTIONS.items():
        durations[name] = tts(name, " ".join(text.split()))
        print(name, durations[name], "s")
    (HERE / "durations.json").write_text(json.dumps(durations, indent=2))
    print("total:", round(sum(durations.values()), 1), "s")
