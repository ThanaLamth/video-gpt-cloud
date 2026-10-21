import sys, os
case_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Users\admin\Tools\VoiceMC_App")
os.environ["HF_HOME"]              = r"C:\Users\admin\Tools\VoiceMC_App\models\hf"
os.environ["HF_HUB_OFFLINE"]       = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
import engine

engine.render(
    raw_text    = open(os.path.join(case_dir, "vo_script.txt"),      encoding="utf-8").read(),
    ref_wav     = os.path.join(case_dir, "ref_voice_8s.wav"),
    ref_text    = open(os.path.join(case_dir, "ref_transcript.txt"), encoding="utf-8").read(),
    out_path    = os.path.join(case_dir, "vo_raw.wav"),
    speed       = 1.06,
    pause_scale = 0.65,
    qc          = False,
    log         = print,
)
print("vo_raw.wav done")