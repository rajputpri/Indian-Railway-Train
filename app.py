"""
RAILDRISHTI (रेल दृष्टि) - ML Train Tier Intelligence for Indian Railways
=========================================================================
Project : Classification and Clustering of Indian Railway Trains Using Machine Learning
Author  : Rajput Prince Singh (Roll No. 83) | BCA Sem-VII | Gujarat University
Model   : Decision Tree Classifier (champion) + StandardScaler, 26 input features

HOW TO RUN (from the project root):  streamlit run app.py

VIVA MAP - which part of this file does what
--------------------------------------------
 0. BOOT SCREEN              first paint: animated train, loading workflow, train sound
 1. CONFIG & DATA TABLES     paths, zones, stations, presets, benchmark numbers, viva Q&A
 2. THEME & HELPERS          one CSS theme, safe HTML rendering, image loading
 3. ML ENGINE                loads scaler + tree, builds the 26-feature vector, predicts,
                             explains the decision path, assigns a cluster, finds look-alikes,
                             runs the advisory (business-rule) engine, makes announcer voices
 4. SHARED JS TOOLKIT        small helpers + a Web-Audio sound engine reused by every visual
 5. HERO SCENE               the animated parallax rail journey (HTML5 canvas): tunnel, bridge,
                             level crossing, station halt, freight train, weather
 6. TICKET & INDICATOR BOARD the stamped e-ticket and the dot-matrix platform board
 7. VISUAL LABS              network radar, decision junction, decision atlas, fleet galaxy,
                             model arena, charts, pipeline, live journey
 8. PAGES                    the ten screens of the app
 9. MAIN                     session state, callbacks, sidebar, navigation

Everything the model needs lives in models/ (scaler.joblib + dt_classifier.joblib).
Every optional file (CSV, images, plots) has a graceful fallback, so the app never crashes
when something is missing.
"""
from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent if _HERE.name.lower() in ("reports", "app", "notebooks") else _HERE
_LOGO = _ROOT / "reports" / "images" / "ir_logo.png"

# ==============================================================================
# 0. BOOT SCREEN
# ==============================================================================
# The very first thing a new browser session sees. It is drawn before the heavy imports and the
# model loading start, and removed again as soon as the engine is ready.
_TREES = "M0 120 V96 " + "".join(f"L{x + 15} {52 + (i * 11) % 26} L{x + 30} 96 " for i, x in enumerate(range(0, 800, 30))) + "V120 Z"
_BOOT_CSS = """
*{box-sizing:border-box;margin:0;padding:0}html,body{background:#070D1F;color:#EAF0FF;font-family:'Hind','Segoe UI',sans-serif;overflow:hidden}
.bt{position:relative;height:540px;border-radius:20px;overflow:hidden;border:1px solid rgba(255,255,255,.14);background:linear-gradient(180deg,#050A1C 0%,#0B1A3F 52%,#1B2A58 74%,#0a1226 74%)}
.st{position:absolute;inset:0;background-image:radial-gradient(1.4px 1.4px at 12% 18%,#fff,transparent),radial-gradient(1.2px 1.2px at 34% 8%,#fff,transparent),radial-gradient(1.4px 1.4px at 58% 22%,#fff,transparent),
radial-gradient(1.2px 1.2px at 77% 11%,#fff,transparent),radial-gradient(1.6px 1.6px at 90% 26%,#fff,transparent),radial-gradient(1px 1px at 22% 30%,#fff,transparent),radial-gradient(1px 1px at 68% 33%,#fff,transparent);animation:tw 3s ease-in-out infinite alternate}
@keyframes tw{from{opacity:.45}to{opacity:1}}
.h{position:absolute;left:0;right:0;height:120px;background-repeat:repeat-x;background-size:800px 120px}
.h1{bottom:158px;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='800' height='120' viewBox='0 0 800 120'><path d='M0 120 V70 Q100 18 200 70 T400 58 T600 76 T800 70 V120 Z' fill='%23142048'/></svg>");animation:m1 40s linear infinite}
.h2{bottom:130px;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='800' height='120' viewBox='0 0 800 120'><path d='__TREES__' fill='%23091030'/></svg>");animation:m2 14s linear infinite}
@keyframes m1{to{background-position-x:-800px}}@keyframes m2{to{background-position-x:-800px}}
.tk{position:absolute;left:0;right:0;bottom:104px;height:12px;background:#59606b;border-top:3px solid #9aa4b3}
.sl{position:absolute;left:0;right:0;bottom:84px;height:20px;background:repeating-linear-gradient(90deg,#4a3b2e 0 16px,transparent 16px 44px);animation:sl .32s linear infinite}
@keyframes sl{to{background-position-x:-44px}}
.gr{position:absolute;left:0;right:0;bottom:0;height:84px;background:linear-gradient(180deg,#0f1a2c,#070b16)}
.tn{position:absolute;left:50%;bottom:108px;width:700px;margin-left:-300px;animation:bob .5s ease-in-out infinite alternate}
@keyframes bob{from{transform:translateY(0)}to{transform:translateY(-1.5px)}}
.wh{transform-box:fill-box;transform-origin:center;animation:sp .45s linear infinite}@keyframes sp{to{transform:rotate(360deg)}}
.bd{position:absolute;left:50%;top:34px;transform:translateX(-50%);text-align:center;background:#FFD21F;color:#14110A;border:3px solid #14110A;border-radius:8px;padding:5px 30px 7px;font-family:'Rajdhani',sans-serif;
box-shadow:0 0 0 2px #FFD21F,0 14px 40px rgba(0,0,0,.5)}.bd b{display:block;font-size:46px;line-height:1;letter-spacing:4px}.bd i{display:block;font-style:normal;font-size:23px;font-weight:600}
.ms{position:absolute;left:0;right:0;top:128px;text-align:center;font-size:19px;color:#FFD21F;font-family:'Rajdhani',sans-serif;font-weight:600;letter-spacing:.5px}
.ms span.d{display:inline-block;width:6px;height:6px;border-radius:50%;background:#FFD21F;margin-left:5px;animation:dt 1s infinite}.ms span.d:nth-child(3){animation-delay:.2s}.ms span.d:nth-child(4){animation-delay:.4s}
@keyframes dt{0%,100%{opacity:.2}50%{opacity:1}}
.fl{position:absolute;left:50%;top:170px;transform:translateX(-50%);list-style:none;width:430px;max-width:92%}
.fl li{font-size:15px;padding:5px 0 5px 32px;position:relative;opacity:.25;transition:opacity .4s;color:#C9D4F2}
.fl li:before{content:'';position:absolute;left:6px;top:8px;width:14px;height:14px;border-radius:50%;border:2px solid #5b6684}
.fl li.on{opacity:1}.fl li.done:before{background:#34D399;border-color:#34D399;content:'\\2713';color:#04210f;font-size:11px;font-weight:700;text-align:center;line-height:10px}
.pg{position:absolute;left:8%;right:8%;bottom:34px;height:5px;border-radius:3px;background:rgba(255,255,255,.12)}.pg i{position:absolute;left:0;top:0;height:5px;border-radius:3px;background:linear-gradient(90deg,#FB792B,#FFD21F);width:6%;transition:width .7s}
.pg u{position:absolute;top:-14px;left:6%;font-size:20px;text-decoration:none;transition:left .7s;margin-left:-10px}
.sn{position:absolute;right:18px;top:16px;background:rgba(7,13,31,.7);color:#EAF0FF;border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:6px 14px;font-size:13px;cursor:pointer}.sn.on{background:#FFD21F;color:#14110A}
.hi{position:absolute;left:0;right:0;bottom:8px;text-align:center;font-size:12.5px;color:#9AA8CC}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""
_BOOT_TRAIN = """<svg viewBox="0 0 700 110" width="700"><defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F4F7FC"/><stop offset="1" stop-color="#B4BFD0"/></linearGradient></defs>
<g id="cc"><rect x="6" y="18" width="200" height="62" rx="7" fill="url(#g1)"/><rect x="10" y="24" width="190" height="5" fill="#34D399"/><rect x="10" y="62" width="190" height="6" fill="#1D4ED8"/>
<g fill="#13203C">{win1}</g></g><use href="#cc" x="212"/>
<path d="M430 80 V30 Q430 18 442 18 H540 C585 18 618 40 648 66 L648 80 Z" fill="url(#g1)"/><rect x="430" y="62" width="218" height="8" fill="#1D4ED8"/><rect x="430" y="71" width="218" height="3" fill="#FB792B"/>
<path d="M560 24 C595 26 622 44 640 62 L590 62 L560 46 Z" fill="#0B1220"/><rect x="448" y="30" width="98" height="26" rx="4" fill="#13203C" opacity=".85"/>
<ellipse cx="646" cy="70" rx="5" ry="3.4" fill="#FFF3C4"/><path d="M520 18 L506 4 M520 18 L536 4" stroke="#8b95a5" stroke-width="2" fill="none"/><line x1="494" y1="4" x2="548" y2="4" stroke="#d1d5db" stroke-width="3"/>
<rect x="6" y="80" width="642" height="8" fill="#0d1016"/>{wheels}</svg>"""


def _boot_doc() -> str:
    wins = "".join(f'<rect x="{18 + i * 26}" y="34" width="17" height="22" rx="3"/>' for i in range(7))
    whs = "".join(f'<g class="wh"><circle cx="{x}" cy="94" r="13" fill="#12151b" stroke="#9aa4b2" stroke-width="2.4"/>'
                  f'<path d="M{x} 83 V105 M{x - 11} 94 H{x + 11} M{x - 8} 86 L{x + 8} 102 M{x + 8} 86 L{x - 8} 102" stroke="#6b7480" stroke-width="1.4"/></g>'
                  for x in (44, 80, 170, 250, 286, 376, 470, 506, 600))
    logo = ""
    try:
        if _LOGO.exists() and _LOGO.stat().st_size < 400_000:
            logo = ('<img alt="" style="position:absolute;left:18px;top:16px;width:52px;height:52px;border-radius:11px;background:#fff;padding:5px;object-fit:contain" '
                    f'src="data:image/png;base64,{base64.b64encode(_LOGO.read_bytes()).decode()}">')
    except Exception:
        pass
    steps = ["Waking up the signal box", "Loading the scaler and the Decision Tree", "Reading 4,466 trains from the dataset", "Checking label mapping and input scaling",
             "Mapping zones, corridors and fleet clusters", "Laying the tracks for the journey scene"]
    lis = "".join(f"<li>{s}</li>" for s in steps)
    body = (f'<div class="bt"><div class="st"></div><div class="h h1"></div><div class="h h2"></div>{logo}<button class="sn" id="sn">Tap for train sound</button>'
            f'<div class="bd"><b>RAILDRISHTI</b><i>रेल दृष्टि</i></div><div class="ms"><span id="m">Platform is getting ready</span><span class="d"></span><span class="d"></span><span class="d"></span></div>'
            f'<ul class="fl" id="fl">{lis}</ul><div class="gr"></div><div class="sl"></div><div class="tk"></div><div class="tn">{_BOOT_TRAIN.format(win1=wins, wheels=whs)}</div>'
            f'<div class="pg"><i id="pb"></i><u id="pt">🚆</u></div><div class="hi">भारतीय रेल के लिए मशीन लर्निंग | first load takes a few seconds</div></div>')
    js = """
const L=[...document.querySelectorAll('#fl li')];let i=0,ctx=null,on=false,tm=null;
function step(){if(i>0)L[i-1].classList.replace('on','done');if(i<L.length){L[i].classList.add('on');document.getElementById('pb').style.width=(10+i*15)+'%';document.getElementById('pt').style.left=(10+i*15)+'%';i++;setTimeout(step,780)}else{document.getElementById('m').textContent='Almost there'}}
step();
function noise(){const n=ctx.sampleRate;const b=ctx.createBuffer(1,n,ctx.sampleRate),d=b.getChannelData(0);for(let k=0;k<n;k++)d[k]=Math.random()*2-1;return b}
function clack(){if(!on)return;const t=ctx.currentTime+.01;[0,.085].forEach((o,k)=>{const s=ctx.createBufferSource();s.buffer=NB;const f=ctx.createBiquadFilter();f.type='bandpass';f.frequency.value=700+Math.random()*400;f.Q.value=1.1;const g=ctx.createGain();
 g.gain.setValueAtTime(.24*(k?.6:1),t+o);g.gain.exponentialRampToValueAtTime(.001,t+o+.07);s.connect(f);f.connect(g);g.connect(ctx.destination);s.start(t+o,Math.random()*.5,.09);
 const q=ctx.createOscillator();q.frequency.setValueAtTime(96,t+o);q.frequency.exponentialRampToValueAtTime(46,t+o+.1);const g2=ctx.createGain();g2.gain.setValueAtTime(.18*(k?.6:1),t+o);g2.gain.exponentialRampToValueAtTime(.001,t+o+.13);q.connect(g2);g2.connect(ctx.destination);q.start(t+o);q.stop(t+o+.15)});
 tm=setTimeout(clack,230+Math.random()*30)}
let NB=null;
function horn(){const t=ctx.currentTime,out=ctx.createGain();out.gain.setValueAtTime(0,t);out.gain.linearRampToValueAtTime(.3,t+.06);out.gain.setValueAtTime(.3,t+.8);out.gain.exponentialRampToValueAtTime(.001,t+1.4);const lp=ctx.createBiquadFilter();lp.type='lowpass';lp.frequency.value=1700;out.connect(lp);lp.connect(ctx.destination);
 [415,523].forEach((fr,k)=>['sawtooth','square'].forEach((ty,j)=>{const o=ctx.createOscillator();o.type=ty;o.frequency.value=fr*(j+1)*(k?1.004:1);const g=ctx.createGain();g.gain.value=j?.1:.45;o.connect(g);g.connect(out);o.start(t);o.stop(t+1.45)}))}
function go(){if(on)return true;try{const AC=window.AudioContext||window.webkitAudioContext;ctx=ctx||new AC();ctx.resume();if(ctx.state!=='running')return false;NB=NB||noise();on=true;document.getElementById('sn').classList.add('on');document.getElementById('sn').textContent='Sound on';horn();clack();return true}catch(e){return false}}
document.getElementById('sn').onclick=()=>{if(on){on=false;clearTimeout(tm);document.getElementById('sn').classList.remove('on');document.getElementById('sn').textContent='Tap for train sound'}else go()};
setTimeout(()=>{if(!go()){const once=()=>{go()};['pointerdown','keydown'].forEach(ev=>{document.addEventListener(ev,once,{once:true});try{window.parent.document.addEventListener(ev,once,{once:true})}catch(e){}})}},300);
"""
    return ("<!DOCTYPE html><html><head><meta charset='utf-8'><style>@import url('https://fonts.googleapis.com/css2?family=Hind:wght@400;600&family=Rajdhani:wght@600;700&display=swap');"
            + _BOOT_CSS.replace("__TREES__", _TREES) + "</style></head><body>" + body + "<script>" + js + "</script></body></html>")


def _early_boot():
    icon = "🚆"
    try:
        if _LOGO.exists():
            from PIL import Image
            icon = Image.open(_LOGO)
    except Exception:
        pass
    st.set_page_config(page_title="RailDrishti | ML Train Tier Intelligence", page_icon=icon, layout="wide", initial_sidebar_state="expanded")
    if st.session_state.get("_booted"):
        return None
    slot = st.empty()
    try:
        with slot:
            components.html(_boot_doc(), height=544)
    except Exception:
        return None
    return slot


BOOT_SLOT = _early_boot()

import base64
import hashlib
import html as _html
import io
import itertools
import json
import math
import re
import time
import warnings
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

try:  # optional: Hindi/English voice announcements as MP3
    from gtts import gTTS
    GTTS_OK = True
except Exception:  # pragma: no cover
    GTTS_OK = False
try:  # optional: natural neural voices (Microsoft Edge online voices)
    import edge_tts  # noqa: F401
    EDGE_OK = True
except Exception:  # pragma: no cover
    EDGE_OK = False
try:  # optional: a real, scannable QR code on the ticket
    import qrcode
    QR_OK = True
except Exception:  # pragma: no cover
    QR_OK = False


# ==============================================================================
# 1. CONFIG & DATA TABLES
# ==============================================================================
PROJECT_META = dict(
    brand="RailDrishti",
    brand_hi="रेल दृष्टि",
    student="Rajput Prince Singh",
    roll="83",
    college="Lokmanya College of Computer Application, Gujarat University",
    course="BCA Semester VII | DSC-C-BCA-473P ML System Design & Implementation",
    guide="Prof. Vidhi Bhatt",
    title="Classification and Clustering of Indian Railway Trains Using Machine Learning",
)

# Numbers locked in the notebooks. If a CSV is present the app recomputes what it can from the data.
FACTS = dict(
    raw=5208, clean=4466, train=3572, test=894, features=26,
    acc=91.50, macro_f1=0.8896, weighted_f1=0.9146, auc=0.9204, cv=0.8743, cv_sd=0.0155,
    share={"Pass": 55.1, "Exp": 28.8, "SF": 16.1},
    km_k=5, km_sil=0.2024, km_inertia=69115.75, db_eps=7.0, db_min=20, db_sil=0.2543, db_noise=13,
    sf_to_exp=25, exp_to_sf=16, corr=0.98,
)

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent if SCRIPT_DIR.name.lower() in ("reports", "app", "notebooks") else SCRIPT_DIR
MODELS_DIR, DATA_DIR = PROJECT_ROOT / "models", PROJECT_ROOT / "data"
VIZ_DIR, IMAGES_DIR = PROJECT_ROOT / "visualizations", PROJECT_ROOT / "reports" / "images"
AUDIO_CACHE_DIR = PROJECT_ROOT / "reports" / "_pa_audio_cache"
SCALER_PATH, DT_MODEL_PATH = MODELS_DIR / "scaler.joblib", MODELS_DIR / "dt_classifier.joblib"
TRAINS_CSV, CLUSTERS_CSV = DATA_DIR / "trains.csv", DATA_DIR / "trains_with_clusters.csv"
LOGO_PATH = IMAGES_DIR / "ir_logo.png"

# Streamlit changed `use_container_width` to `width="stretch"` in 1.50. Support both.
_ST_VER = tuple(int(p) for p in re.findall(r"\d+", st.__version__)[:2]) or (1, 0)
STRETCH = {"width": "stretch"} if _ST_VER >= (1, 50) else {"use_container_width": True}


def sx(fn, *args, **kw):
    """Call a Streamlit element so that it stretches to the container on any Streamlit version."""
    try:
        return fn(*args, **{**kw, **STRETCH})
    except TypeError:
        alt = {"use_container_width": True} if "width" in STRETCH else {"width": "stretch"}
        try:
            return fn(*args, **{**kw, **alt})
        except TypeError:
            return fn(*args, **kw)


DEFAULT_26_FEATURES = [
    "distance", "first_ac", "second_ac", "third_ac", "chair_car", "sleeper", "first_class", "total_duration",
    "zone_CR", "zone_ECoR", "zone_ECR", "zone_ER", "zone_KR", "zone_NCR", "zone_NER", "zone_NFR", "zone_NR",
    "zone_NWR", "zone_SCR", "zone_SECR", "zone_SER", "zone_SR", "zone_SWR", "zone_Unknown", "zone_WCR", "zone_WR",
]
NUM_COLS = ["distance", "first_ac", "second_ac", "third_ac", "chair_car", "sleeper", "first_class", "total_duration"]
FEATURE_LABELS = {
    "distance": "Route distance (km)", "total_duration": "Scheduled duration (min)",
    "first_ac": "Has First AC (1A)", "second_ac": "Has Second AC (2A)", "third_ac": "Has Third AC (3A)",
    "chair_car": "Has AC Chair Car (CC)", "sleeper": "Has Sleeper (SL)", "first_class": "Has First Class (FC)",
}

TIERS = ["Pass", "Exp", "SF"]
TIER_META = {
    "SF": dict(name="Superfast Express", short="Superfast", hi="सुपरफास्ट एक्सप्रेस", color="#FFC83D",
               rgb="255,200,61", loco="aero", rank=3,
               profile="Premium tier, high speed, minimal halts. Built for long intercity runs and carries the Superfast surcharge."),
    "Exp": dict(name="Mail / Express", short="Express", hi="मेल एक्सप्रेस", color="#4DA3FF",
                rgb="77,163,255", loco="wap7", rank=2,
                profile="Medium-to-long distance, balanced halts. Links major junctions with a mix of Sleeper and AC coaches."),
    "Pass": dict(name="Passenger", short="Passenger", hi="पैसेंजर", color="#34D399",
                 rgb="52,211,153", loco="wdm", rank=1,
                 profile="Short distance, frequent halts, ideal for commuters. Stops at almost every station with basic coaches."),
}
# coach flag -> (ticket code, label, colour)
CLASS_DEF = [
    ("first_ac", "1A", "First AC", "#F43F5E"), ("second_ac", "2A", "Second AC", "#F59E0B"),
    ("third_ac", "3A", "Third AC", "#10B981"), ("chair_car", "CC", "AC Chair Car", "#06B6D4"),
    ("sleeper", "SL", "Sleeper", "#3B82F6"), ("first_class", "FC", "First Class", "#A855F7"),
]
SURCHARGE = {"SL": 30, "CC": 45, "3A": 45, "2A": 45, "1A": 75}  # indicative Superfast surcharge in rupees

# zone code -> (name, HQ station, Hindi name, lon, lat)  (HQ positions are schematic)
ZONE_INFO = {
    "NR": ("Northern Railway", "New Delhi", "उत्तरी रेलवे", 77.22, 28.64),
    "WR": ("Western Railway", "Mumbai Churchgate", "पश्चिम रेलवे", 72.45, 19.55),
    "SR": ("Southern Railway", "Chennai Central", "दक्षिण रेलवे", 80.27, 13.08),
    "ER": ("Eastern Railway", "Kolkata Fairlie Place", "पूर्व रेलवे", 88.34, 22.60),
    "CR": ("Central Railway", "Mumbai CSMT", "मध्य रेलवे", 73.55, 18.95),
    "NFR": ("Northeast Frontier Railway", "Guwahati Maligaon", "पूर्वोत्तर सीमांत रेलवे", 91.74, 26.18),
    "SCR": ("South Central Railway", "Secunderabad", "दक्षिण मध्य रेलवे", 78.50, 17.44),
    "ECR": ("East Central Railway", "Hajipur", "पूर्व मध्य रेलवे", 85.20, 25.70),
    "ECoR": ("East Coast Railway", "Bhubaneswar", "पूर्व तट रेलवे", 85.83, 20.27),
    "KR": ("Konkan Railway", "Navi Mumbai Belapur", "कोंकण रेलवे", 73.55, 17.30),
    "NCR": ("North Central Railway", "Prayagraj", "उत्तर मध्य रेलवे", 81.84, 25.44),
    "NER": ("North Eastern Railway", "Gorakhpur", "पूर्वोत्तर रेलवे", 83.37, 26.75),
    "NWR": ("North Western Railway", "Jaipur", "उत्तर पश्चिम रेलवे", 75.80, 26.90),
    "SECR": ("South East Central Railway", "Bilaspur", "दक्षिण पूर्व मध्य रेलवे", 82.15, 22.08),
    "SER": ("South Eastern Railway", "Kolkata Garden Reach", "दक्षिण पूर्व रेलवे", 87.10, 22.30),
    "SWR": ("South Western Railway", "Hubballi", "दक्षिण पश्चिम रेलवे", 75.14, 15.36),
    "WCR": ("West Central Railway", "Jabalpur", "पश्चिम मध्य रेलवे", 79.95, 23.18),
    "Unknown": ("Unmapped / feeder zone", "Regional division", "क्षेत्रीय रेलवे ज़ोन", 0.0, 0.0),
}
PRIORITY_ZONES = ["WR", "NR", "CR", "SR", "ER", "SCR", "ECR", "NFR", "Unknown"]

# (code, name, zone, lon, lat) - used by the route planner and the network radar
STATIONS = [
    ("NDLS", "New Delhi", "NR", 77.22, 28.64), ("NZM", "Hazrat Nizamuddin", "NR", 77.25, 28.59),
    ("MMCT", "Mumbai Central", "WR", 72.82, 18.97), ("CSMT", "Mumbai CSMT", "CR", 72.84, 18.94),
    ("HWH", "Howrah Jn", "ER", 88.34, 22.58), ("MAS", "Chennai Central", "SR", 80.27, 13.08),
    ("SBC", "KSR Bengaluru", "SWR", 77.57, 12.98), ("SC", "Secunderabad Jn", "SCR", 78.50, 17.43),
    ("ADI", "Ahmedabad Jn", "WR", 72.60, 23.02), ("JP", "Jaipur Jn", "NWR", 75.79, 26.92),
    ("LKO", "Lucknow Charbagh", "NR", 80.92, 26.83), ("CNB", "Kanpur Central", "NCR", 80.35, 26.45),
    ("PRYJ", "Prayagraj Jn", "NCR", 81.83, 25.44), ("BSB", "Varanasi Jn", "NER", 83.01, 25.32),
    ("PNBE", "Patna Jn", "ECR", 85.14, 25.60), ("GAYA", "Gaya Jn", "ECR", 84.99, 24.80),
    ("RNC", "Ranchi Jn", "SER", 85.33, 23.36), ("BBS", "Bhubaneswar", "ECoR", 85.84, 20.27),
    ("PURI", "Puri", "ECoR", 85.83, 19.81), ("VSKP", "Visakhapatnam", "ECoR", 83.29, 17.72),
    ("BZA", "Vijayawada Jn", "SCR", 80.62, 16.52), ("GHY", "Guwahati", "NFR", 91.75, 26.18),
    ("NJP", "New Jalpaiguri", "NFR", 88.43, 26.68), ("DBRG", "Dibrugarh", "NFR", 94.91, 27.48),
    ("BPL", "Bhopal Jn", "WCR", 77.41, 23.27), ("JBP", "Jabalpur", "WCR", 79.95, 23.17),
    ("NGP", "Nagpur", "CR", 79.09, 21.15), ("R", "Raipur Jn", "SECR", 81.63, 21.25),
    ("BSP", "Bilaspur Jn", "SECR", 82.14, 22.08), ("PUNE", "Pune Jn", "CR", 73.87, 18.53),
    ("ST", "Surat", "WR", 72.84, 21.21), ("BRC", "Vadodara Jn", "WR", 73.18, 22.31),
    ("KOTA", "Kota Jn", "WCR", 75.84, 25.18), ("JU", "Jodhpur Jn", "NWR", 73.02, 26.28),
    ("ASR", "Amritsar Jn", "NR", 74.87, 31.63), ("JAT", "Jammu Tawi", "NR", 74.87, 32.71),
    ("CDG", "Chandigarh", "NR", 76.80, 30.70), ("GKP", "Gorakhpur Jn", "NER", 83.37, 26.75),
    ("ERS", "Ernakulam Jn", "SR", 76.29, 9.97), ("TVC", "Thiruvananthapuram Central", "SR", 76.95, 8.49),
    ("MDU", "Madurai Jn", "SR", 78.11, 9.92), ("MAQ", "Mangaluru Central", "SR", 74.84, 12.87),
    ("MAO", "Madgaon Jn", "KR", 73.97, 15.27), ("UBL", "Hubballi Jn", "SWR", 75.12, 15.35),
    ("AGC", "Agra Cantt", "NCR", 78.02, 27.16), ("RTM", "Ratlam Jn", "WR", 75.04, 23.33),
]
STATION_BY_CODE = {s[0]: s for s in STATIONS}

# main trunk corridors (lon, lat) drawn on the network radar
CORRIDORS = [
    ("Delhi-Mumbai", [(77.22, 28.64), (77.68, 27.49), (75.84, 25.18), (75.04, 23.33), (73.18, 22.31), (72.84, 21.21), (72.82, 18.97)]),
    ("Delhi-Howrah", [(77.22, 28.64), (80.35, 26.45), (81.83, 25.44), (83.12, 25.28), (84.99, 24.80), (86.43, 23.80), (88.34, 22.58)]),
    ("Mumbai-Chennai", [(72.84, 18.94), (73.87, 18.53), (75.90, 17.67), (77.35, 16.20), (77.37, 15.17), (79.50, 13.63), (80.27, 13.08)]),
    ("Howrah-Chennai", [(88.34, 22.58), (87.32, 22.34), (86.93, 21.49), (85.84, 20.27), (83.29, 17.72), (80.62, 16.52), (80.27, 13.08)]),
    ("Delhi-Chennai", [(77.22, 28.64), (78.02, 27.16), (78.57, 25.45), (77.41, 23.27), (79.09, 21.15), (79.60, 17.97), (80.62, 16.52), (80.27, 13.08)]),
    ("Mumbai-Howrah", [(72.84, 18.94), (75.78, 21.05), (79.09, 21.15), (81.63, 21.25), (82.14, 22.08), (85.00, 22.80), (88.34, 22.58)]),
    ("Delhi-Jammu", [(77.22, 28.64), (76.78, 30.37), (75.85, 30.90), (74.87, 31.63), (74.87, 32.71)]),
    ("Delhi-Ahmedabad", [(77.22, 28.64), (75.79, 26.92), (74.64, 26.45), (72.78, 24.48), (72.60, 23.02)]),
    ("Howrah-Dibrugarh", [(88.34, 22.58), (88.14, 25.00), (88.43, 26.68), (91.75, 26.18), (94.91, 27.48)]),
    ("Konkan coast", [(72.84, 18.94), (73.30, 16.99), (73.97, 15.27), (74.84, 12.87), (75.78, 11.25), (76.29, 9.97), (76.95, 8.49)]),
    ("Chennai-Kanyakumari", [(80.27, 13.08), (78.70, 10.80), (78.11, 9.92), (77.54, 8.08)]),
    ("Chennai-Bengaluru", [(80.27, 13.08), (79.13, 12.93), (77.57, 12.98)]),
    ("Delhi-Gorakhpur", [(77.22, 28.64), (78.77, 28.84), (80.92, 26.83), (83.37, 26.75)]),
]

CLUSTER_PROFILES = {
    0: dict(code="C-0", name="Eastern regional high-density network", zone="Eastern Railway and Gangetic plains", color="#38BDF8",
            summary="Short-to-medium regional passenger and express services concentrated in Eastern Railway, with dense halts and mixed unreserved/sleeper rakes."),
    1: dict(code="C-1", name="Northeast hilly and strategic corridors", zone="Northeast Frontier Railway", color="#F59E0B",
            summary="Strategic Northeast routes over steep gradients, curves and single-line sections, so journey time per kilometre is structurally higher."),
    2: dict(code="C-2", name="Short-distance commuter passenger fleet", zone="Multi-zone suburban and inter-town feeders", color="#34D399",
            summary="Daily commuter lifelines under about 250 km with no AC coaches, frequent halts and general seating."),
    3: dict(code="C-3", name="Long-distance AC premium trunk fleet", zone="Golden Quadrilateral and diagonal corridors", color="#818CF8",
            summary="Flagship intercity Express and Superfast trains over 600 km with full AC rakes (3A, 2A, 1A) and high commercial speed."),
    4: dict(code="C-4", name="Secondary-zone branch-line connectors", zone="Secondary and regional feeder divisions", color="#EC4899",
            summary="Short-to-medium branch lines that link rural junctions to trunk routes with basic sleeper or unreserved coaches."),
}

BENCHMARKS = [
    dict(model="Decision Tree (default)", acc=0.9150, f1=0.8896, wf1=0.9146, auc=0.9204, before=0.8309, champ=True),
    dict(model="Decision Tree (max_depth=10)", acc=0.8859, f1=0.8459, wf1=0.8836, auc=0.9012, before=0.7720, champ=False),
    dict(model="K-Nearest Neighbors (k=5)", acc=0.8523, f1=0.7886, wf1=0.8484, auc=0.9355, before=0.7552, champ=False),
    dict(model="SVM (RBF)", acc=0.8412, f1=0.7651, wf1=0.8343, auc=0.9285, before=0.7168, champ=False),
    dict(model="Dummy (most frequent)", acc=0.5503, f1=0.2367, wf1=0.3907, auc=0.5000, before=0.2367, champ=False),
    dict(model="Gaussian Naive Bayes", acc=0.3702, f1=0.3098, wf1=0.3636, auc=0.6120, before=0.2969, champ=False),
]

# c = coach flags in CLASS_DEF order: (1A, 2A, 3A, CC, SL, FC)
PRESETS = [
    dict(label="Mumbai-Delhi Rajdhani", d=1385, h=15, m=50, z="WR", c=(1, 1, 1, 0, 0, 0), t="Trunk Rajdhani profile", a="MMCT", b="NDLS", dep="16:55"),
    dict(label="Shatabdi day run", d=512, h=6, m=30, z="NR", c=(0, 0, 0, 1, 0, 0), t="Day intercity chair car", a="NDLS", b="LKO", dep="06:10"),
    dict(label="Overnight Mail", d=610, h=12, m=0, z="ECR", c=(0, 0, 1, 0, 1, 0), t="Inter-zonal mail express", a="", b="", dep="21:30"),
    dict(label="Local passenger", d=145, h=4, m=30, z="ER", c=(0, 0, 0, 0, 1, 0), t="Regional passenger feeder", a="", b="", dep="07:15"),
    dict(label="Slow 'Superfast'", d=680, h=12, m=45, z="NR", c=(0, 1, 1, 0, 1, 0), t="Audit case: 53 km/h train", a="", b="", dep="22:10"),
    dict(label="Fast full-AC Express", d=1680, h=26, m=30, z="SCR", c=(1, 1, 1, 0, 1, 0), t="Upgrade candidate: 63 km/h", a="", b="", dep="05:45"),
]

VIVA_QA = [
    ("Dataset", "Which dataset did you use and why?",
     "Indian Railways dataset from Kaggle (sripaadsrinivasan/indian-railways-dataset): 5,208 trains with zone, type, distance, duration, coach-class flags and from/to stations. It is real, public and has a natural 3-class target (Pass, Exp, SF), so both classification and clustering make sense."),
    ("Dataset", "How many records did you finally use?",
     "5,208 raw rows were filtered to 4,466 trains whose type is Pass, Exp or SF. The split is 55.1% Pass, 28.8% Exp and 16.1% SF, so the data is imbalanced and Macro F1 matters more than plain accuracy."),
    ("Preprocessing", "What was the duration problem you discovered?",
     "In the raw data duration_m held only the minute part (0 to 58), not the trip length. I engineered total_duration = duration_h x 60 + duration_m. This single fix improved every supervised model and the clustering scores."),
    ("Preprocessing", "Why exactly 26 features?",
     "8 numeric/binary columns (distance, total_duration and six coach flags) plus 18 one-hot zone columns. The scaler and tree were trained in that order, so the app rebuilds the same vector from scaler.feature_names_in_."),
    ("Preprocessing", "Why scale the features if a tree does not need it?",
     "The same scaler is shared with distance-based models (KNN, SVM, K-Means). The app also auto-detects whether the saved tree expects scaled or raw values, so predictions stay correct either way."),
    ("Models", "Why is the Decision Tree your champion?",
     "The default Decision Tree reached 91.50% accuracy and 0.8896 Macro F1, ahead of KNN (85.23%) and SVM (84.12%). Binary coach flags and thresholds on distance/duration suit a tree, and it is explainable: the Junction page shows the exact path of every prediction."),
    ("Metrics", "Why not judge only by accuracy?",
     "Because 55% of trains are Passenger. A dummy model that always says Pass already scores 55.03% accuracy but only 0.2367 Macro F1."),
    ("Metrics", "Is the result stable or a lucky split?",
     "5-fold stratified cross-validation gives Macro F1 0.8743 +/- 0.0155, close to the single-split 0.8896, so the result is stable."),
    ("Metrics", "Where does the model make mistakes?",
     "8.50% of the hold-out trains are misclassified. The main confusions are 25 SF predicted as Exp and 16 Exp predicted as SF: neighbouring tiers whose schedules overlap. The Explorer audit page lists them."),
    ("Models", "Which features matter most?",
     "From the fitted tree: third_ac, distance, total_duration and chair_car dominate (see the importance bars on the Junction page). Zone dummies matter much less."),
    ("Clustering", "Why k = 5 for K-Means?",
     "The elbow curve flattens near k = 5 (inertia 69,115.75) and the silhouette is 0.2024: overlapping but interpretable fleet segments."),
    ("Clustering", "K-Means versus DBSCAN?",
     "DBSCAN (eps 7.0, min_samples 20) finds natural dense groups and marks 13 trains (0.4%) as noise with silhouette 0.2543. K-Means forces every train into one of five clusters."),
    ("Theory", "What is Gini impurity?",
     "A node's impurity = 1 minus the sum of squared class shares. 0 means a pure node. The tree picks the split that reduces impurity the most; the Junction page shows the class mix getting purer along the path."),
    ("Domain", "What is the 55 km/h rule used in the advisory engine?",
     "Indian Railways treats a service as Superfast when its average speed on broad gauge is about 55 km/h or more. The app flags trains tagged or predicted SF that fall below that line."),
    ("App", "How does the app avoid the 26-feature shape mismatch?",
     "It builds a dict of zeros from scaler.feature_names_in_, fills user values, sets zone_<code> = 1, orders the columns, scales, then predicts. One function builds the vector for the form, the batch upload and the whole dataset."),
    ("Limits", "What are the limitations and future work?",
     "Only schedule and coach features are used: no halt count, track type or delays. The label is the railway's own tag, so the model also learns its inconsistencies. Future work: halts, delay data, tuned ensembles and cloud deployment."),
]


# ------------------------------------------------------------------------------
# small shared helpers
# ------------------------------------------------------------------------------
IST = timezone(timedelta(hours=5, minutes=30))


def esc(v) -> str:
    """HTML-escape any value."""
    return _html.escape(str(v), quote=True)


def ist_now() -> datetime:
    return datetime.now(IST)


def haversine_km(lon1, lat1, lon2, lat2) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def est_rail_km(code_a: str, code_b: str) -> int:
    """Rough rail distance between two stations: great-circle x 1.22, rounded to 5 km."""
    a, b = STATION_BY_CODE.get(code_a), STATION_BY_CODE.get(code_b)
    if not a or not b or code_a == code_b:
        return 0
    return int(max(10, min(4500, round(haversine_km(a[3], a[4], b[3], b[4]) * 1.22 / 5) * 5)))


def fmt_dur(mins: float) -> str:
    mins = int(round(mins))
    return f"{mins // 60}h {mins % 60:02d}m"


# ==============================================================================
# 2. THEME & HELPERS
# ==============================================================================
# Visual language: a night platform. Deep navy base, the yellow safety line and station-board
# yellow, IRCTC saffron for actions, signal green/red for audit states, a paper-white e-ticket.
# Type: Rajdhani (angular, signage-like, has Devanagari) for display + Hind for reading text.
THEME_CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Hind:wght@400;500;600&family=Rajdhani:wght@500;600;700&display=swap');
:root{--bg:#070D1F;--bg2:#0B1530;--ink:#EAF0FF;--mut:#9AA8CC;--line:rgba(255,255,255,.10);
--yellow:#FFD21F;--saf:#FB792B;--blue:#4DA3FF;--green:#34D399;--red:#FF5A5F;--paper:#FBF7EE;color-scheme:dark}
.stApp{background:radial-gradient(1100px 520px at 8% -8%,rgba(77,163,255,.13),transparent 60%),
radial-gradient(900px 480px at 100% 0,rgba(251,121,43,.09),transparent 55%),linear-gradient(180deg,#070D1F,#050A18)!important;color:var(--ink)}
.stApp,.stMarkdown,.stMarkdown p,label,[data-testid="stWidgetLabel"] p,[data-testid="stCaptionContainer"],button,input,textarea,[data-baseweb="select"],.rd-sec p{font-family:'Hind','Segoe UI',sans-serif}
h1,h2,h3,h4,h5{font-family:'Rajdhani','Segoe UI',sans-serif!important;font-weight:700!important;letter-spacing:.2px;color:var(--ink)}
.stMarkdown,.stMarkdown p,.stMarkdown li{color:var(--ink)}
[data-testid="stHeader"]{background:transparent}
[data-testid="stToolbar"]{right:.5rem}
.block-container{padding-top:.8rem;padding-bottom:3rem;max-width:1480px}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0A1230,#060B1A);border-right:1px solid var(--line)}
[data-testid="stSidebar"] .block-container{padding-top:1rem}
hr{border-color:var(--line)!important}
[data-testid="stWidgetLabel"] p{color:var(--mut);font-weight:500;font-size:.92rem}
/* inputs stay readable on any base theme */
[data-baseweb="select"]>div,[data-baseweb="input"]>div,[data-baseweb="textarea"]>div{background:rgba(255,255,255,.06)!important;border-color:var(--line)!important}
[data-baseweb="select"] *,[data-baseweb="input"] input,[data-baseweb="textarea"] textarea{color:var(--ink)!important}
/* the theme's red primary becomes IRCTC saffron on sliders / toggles / checkboxes */
[data-testid="stSlider"],[data-testid="stCheckbox"],[data-testid="stToggle"]{filter:hue-rotate(28deg) saturate(1.15)}
[data-testid="stSlider"] [role="slider"]{box-shadow:0 0 0 6px rgba(251,121,43,.18)}
/* coach checkboxes look like class chips */
[data-testid="stCheckbox"]{background:rgba(255,255,255,.045);border:1px solid var(--line);border-radius:12px;padding:8px 12px;transition:border-color .2s,background .2s}
[data-testid="stCheckbox"]:hover{border-color:var(--yellow)}
[data-testid="stCheckbox"]:has(input:checked){background:rgba(255,210,31,.10);border-color:rgba(255,210,31,.55)}
/* buttons */
.stButton>button,.stDownloadButton>button,[data-testid^="stBaseButton-secondary"]{background:rgba(255,255,255,.05);color:var(--ink);border:1px solid var(--line);border-radius:12px;font-weight:600;transition:all .2s}
.stButton>button:hover,.stDownloadButton>button:hover,[data-testid^="stBaseButton-secondary"]:hover{border-color:var(--yellow);color:var(--yellow);transform:translateY(-1px)}
button[kind="primary"],[data-testid="stBaseButton-primary"],[data-testid="stBaseButton-primaryFormSubmit"]{background:linear-gradient(135deg,#FB792B,#FFB02E)!important;color:#1B0E00!important;border:0!important;
border-radius:14px!important;font-family:'Rajdhani',sans-serif!important;font-weight:700!important;font-size:1.2rem!important;letter-spacing:.4px;padding:.7rem 1.2rem!important;box-shadow:0 10px 30px rgba(251,121,43,.35)}
button[kind="primary"]:hover,[data-testid="stBaseButton-primary"]:hover,[data-testid="stBaseButton-primaryFormSubmit"]:hover{filter:brightness(1.08);transform:translateY(-1px);color:#1B0E00!important}
button:focus-visible,[role="slider"]:focus-visible,summary:focus-visible{outline:2px solid var(--yellow)!important;outline-offset:2px}
/* the page navigation = a row of station-sign pills (all st.radio widgets) */
[data-testid="stRadio"] [role="radiogroup"]{gap:8px;flex-wrap:wrap}
[data-testid="stRadio"] label{background:rgba(255,255,255,.045);border:1px solid var(--line);padding:7px 15px;border-radius:999px;cursor:pointer;transition:all .2s;margin:0}
[data-testid="stRadio"] label>div:first-child{display:none}
[data-testid="stRadio"] label:hover{border-color:var(--yellow)}
[data-testid="stRadio"] label p{font-weight:600;margin:0}
[data-testid="stRadio"] label:has(input:checked){background:var(--yellow);border-color:var(--yellow);box-shadow:0 8px 24px rgba(255,210,31,.25)}
[data-testid="stRadio"] label:has(input:checked) p{color:#14110A!important}
/* surfaces */
[data-testid="stForm"]{border:1px solid var(--line);border-radius:18px;background:linear-gradient(180deg,rgba(255,255,255,.055),rgba(255,255,255,.02));padding:18px 20px}
[data-testid="stExpander"] details{border:1px solid var(--line)!important;border-radius:14px;background:rgba(255,255,255,.03)}
[data-testid="stMetric"]{background:rgba(255,255,255,.04);border:1px solid var(--line);padding:12px 14px;border-radius:14px}
[data-testid="stMetricValue"]{font-family:'Rajdhani',sans-serif;font-weight:700}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:12px;overflow:hidden}
[data-testid="stFileUploaderDropzone"]{background:rgba(255,255,255,.04);border:1px dashed rgba(255,210,31,.5);border-radius:14px}
iframe{border:0;border-radius:16px;color-scheme:dark}
/* building blocks used by the pages */
.rd-sec{margin:6px 0 14px}.rd-sec h3{margin:0;font-size:1.65rem}.rd-sec p{margin:2px 0 0;color:var(--mut);font-size:.98rem}
.rd-line{height:12px;border-radius:3px;margin:22px 0 16px;background:radial-gradient(circle at 6px 6px,rgba(0,0,0,.30) 2.2px,transparent 2.7px) 0 0/12px 12px,var(--yellow);box-shadow:0 0 18px rgba(255,210,31,.25)}
.rd-panel{background:linear-gradient(180deg,rgba(255,255,255,.055),rgba(255,255,255,.022));border:1px solid var(--line);border-radius:16px;padding:16px 18px;margin-bottom:12px}
.rd-panel h4{margin:0 0 6px;font-size:1.2rem}.rd-note{color:var(--mut);font-size:.88rem;line-height:1.5}
.rd-chip{display:inline-block;padding:3px 11px;border-radius:999px;font-size:.82rem;font-weight:600;border:1px solid var(--line);background:rgba(255,255,255,.05);margin:0 6px 6px 0}
.rd-chip.sf{color:#FFC83D;border-color:rgba(255,200,61,.5);background:rgba(255,200,61,.10)}
.rd-chip.exp{color:#4DA3FF;border-color:rgba(77,163,255,.5);background:rgba(77,163,255,.10)}
.rd-chip.pass{color:#34D399;border-color:rgba(52,211,153,.5);background:rgba(52,211,153,.10)}
.rd-chip.bad{color:#FF8A8E;border-color:rgba(255,90,95,.5);background:rgba(255,90,95,.10)}
.rd-kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:8px 0 14px}
.rd-kpis .k{background:rgba(255,255,255,.045);border:1px solid var(--line);border-radius:14px;padding:12px 14px}
.rd-kpis .k b{display:block;font-family:'Rajdhani',sans-serif;font-size:1.9rem;line-height:1.1;color:var(--yellow)}
.rd-kpis .k span{color:var(--mut);font-size:.86rem}
.rd-adv{display:flex;gap:12px;border-radius:14px;padding:13px 15px;margin-bottom:10px;border:1px solid var(--line);border-left-width:5px;background:rgba(255,255,255,.04)}
.rd-adv .ic{font-size:1.4rem;line-height:1.2}.rd-adv .tt{display:block;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.12rem;margin-bottom:2px}
.rd-adv div{font-size:.93rem;line-height:1.5;color:#D5DEF7}
.rd-adv.ok{border-left-color:#34D399;background:rgba(52,211,153,.07)}.rd-adv.warn{border-left-color:#FF5A5F;background:rgba(255,90,95,.08)}
.rd-adv.up{border-left-color:#4DA3FF;background:rgba(77,163,255,.08)}.rd-adv.info{border-left-color:#FFD21F;background:rgba(255,210,31,.07)}
.rd-tbl{width:100%;border-collapse:collapse;font-size:.9rem}.rd-tbl th{text-align:left;color:var(--mut);font-weight:500;padding:6px 8px;border-bottom:1px solid var(--line)}
.rd-tbl td{padding:7px 8px;border-bottom:1px solid rgba(255,255,255,.05)}.rd-tbl tr:hover td{background:rgba(255,255,255,.04)}
.rd-foot{margin-top:28px;color:var(--mut);font-size:.85rem;text-align:center}
.rd-coach{display:grid;grid-template-columns:repeat(8,1fr);gap:6px}
.rd-coach .t{border-radius:10px;padding:6px 4px;text-align:center;font-size:.72rem;border:1px solid var(--line);background:rgba(255,255,255,.04);animation:rdIn .5s both}
.rd-coach .t b{display:block;font-family:'Rajdhani',sans-serif;font-size:1rem}.rd-coach .t.cur{outline:2px solid #fff;outline-offset:1px}
@keyframes rdIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.rake{display:flex;gap:5px;overflow-x:auto;padding:6px 2px 14px}.rake .c{flex:0 0 auto;min-width:54px;text-align:center;border-radius:8px 8px 4px 4px;padding:7px 6px 5px;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.98rem;color:#fff;border:1px solid rgba(255,255,255,.18);position:relative;animation:rkIn .6s both}
.rake .c small{display:block;font-size:.66rem;font-weight:500;opacity:.9}.rake .c:after{content:'';position:absolute;bottom:-6px;left:12px;width:7px;height:7px;border-radius:50%;background:#0d1016;box-shadow:26px 0 #0d1016}.rake .c.e{border-radius:18px 6px 4px 14px;min-width:88px}
@keyframes rkIn{from{opacity:0;transform:translateX(-46px)}to{opacity:1;transform:none}}
@media (max-width:900px){.rd-coach{grid-template-columns:repeat(4,1fr)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

# base CSS for every iframe visual (same fonts and colours as the page)
IFRAME_CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Hind:wght@400;500;600&family=Rajdhani:wght@500;600;700&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#070D1F;color:#EAF0FF;font-family:'Hind','Segoe UI',sans-serif;color-scheme:dark;overflow-x:hidden}
button{font-family:inherit;cursor:pointer}
canvas{display:block}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""
AUTOSIZE_JS = ("(function(){try{var f=window.frameElement;if(!f)return;var h=function(){var H=Math.ceil(document.documentElement.scrollHeight);"
               "if(H>60)f.style.height=H+'px'};if(window.ResizeObserver)new ResizeObserver(h).observe(document.body);"
               "window.addEventListener('load',h);setTimeout(h,300);h();}catch(e){}})();")


def clean_html(raw: str) -> str:
    """Strip comments and per-line indentation, then join lines.
    Streamlit's Markdown parser turns 4-space-indented HTML into a code block; one line avoids that."""
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    return " ".join(line.strip() for line in raw.splitlines() if line.strip())


def render_html(raw: str) -> None:
    st.markdown(clean_html(raw), unsafe_allow_html=True)


def jdump(obj) -> str:
    """JSON that is safe to embed inside a <script> tag."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def wrap_doc(body: str, css: str = "", js: str = "", autosize: bool = False, libs: str = "") -> str:
    """Compose a full HTML document for components.html (isolated iframe, so no Markdown leaks)."""
    tail = AUTOSIZE_JS if autosize else ""
    return ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<style>{IFRAME_CSS}{css}</style></head><body>{body}"
            f"<script>{JS_COMMON}{libs}{js}{tail}</script></body></html>")


def iframe(doc: str, height: int, scrolling: bool = False) -> None:
    try:
        components.html(doc, height=height, scrolling=scrolling)
    except Exception:  # newer Streamlit builds may rename this API
        try:
            st.html(doc)
        except Exception:
            st.warning("This visual needs a newer Streamlit build.")


def section(title: str, sub: str = "") -> None:
    render_html(f'<div class="rd-sec"><h3>{esc(title)}</h3>' + (f"<p>{esc(sub)}</p>" if sub else "") + "</div>")


def platform_line() -> None:
    render_html('<div class="rd-line"></div>')


def advisory_html(items: list) -> str:
    icons = dict(ok="✅", warn="⚠️", up="🚀", info="💡")
    return "".join(
        f'<div class="rd-adv {a["level"]}"><span class="ic">{icons.get(a["level"], "ℹ️")}</span>'
        f'<div><span class="tt">{esc(a["title"])}</span>{a["body"]}</div></div>' for a in items)


# ---- images: downscale + JPEG/PNG data URIs so the HTML stays light ---------------------------
@st.cache_data(show_spinner=False)
def _img_uri(path_str: str, mtime: float, max_w: int, fmt: str, quality: int) -> str:
    try:
        import io
        im = Image.open(path_str)
        im = im.convert("RGB" if fmt == "JPEG" else "RGBA")
        if im.width > max_w:
            im = im.resize((max_w, max(1, int(im.height * max_w / im.width))), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, fmt, quality=quality, optimize=True) if fmt == "JPEG" else im.save(buf, fmt, optimize=True)
        mime = "image/jpeg" if fmt == "JPEG" else "image/png"
        return f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ""


def data_uri(path: Path, max_w: int = 1200, fmt: str = "JPEG", quality: int = 78) -> str:
    try:
        return _img_uri(str(path), path.stat().st_mtime, max_w, fmt, quality) if path.exists() else ""
    except Exception:
        return ""


def logo_uri() -> str:
    return data_uri(LOGO_PATH, 256, "PNG")


# ==============================================================================
# 3. ML ENGINE
# ==============================================================================
FLAG_KEYS = [d[0] for d in CLASS_DEF]  # first_ac, second_ac, third_ac, chair_car, sleeper, first_class


def norm_tier(v):
    """Map any label spelling ('SF', 'Superfast', 'Exp', 'Passenger'...) to Pass / Exp / SF."""
    s = str(v).strip().lower()
    if s == "sf" or "super" in s:
        return "SF"
    if "pass" in s or "local" in s or "memu" in s:
        return "Pass"
    if "exp" in s or "mail" in s:
        return "Exp"
    return None


def _to_num(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s.astype(int)
    return pd.to_numeric(s, errors="coerce").fillna(0)


def file_sig() -> tuple:
    return tuple((p.stat().st_mtime if p.exists() else 0.0) for p in (SCALER_PATH, DT_MODEL_PATH, TRAINS_CSV, CLUSTERS_CSV))


@st.cache_resource(show_spinner=False)
def load_artifacts(sig):
    out = {"scaler": None, "model": None, "errors": []}
    for key, path in (("scaler", SCALER_PATH), ("model", DT_MODEL_PATH)):
        try:
            if path.exists():
                out[key] = joblib.load(path)
            else:
                out["errors"].append(f"{path.name} not found in {path.parent}")
        except Exception as exc:
            out["errors"].append(f"{path.name}: {exc}")
    return out


@st.cache_data(show_spinner=False)
def load_datasets(sig):
    df, dfc = None, None
    try:
        if TRAINS_CSV.exists():
            raw = pd.read_csv(TRAINS_CSV)
            df = raw[raw["type"].isin(TIERS)].copy().reset_index(drop=True) if "type" in raw.columns else raw.copy()
            if "total_duration" not in df.columns and "duration_h" in df.columns:
                df["total_duration"] = _to_num(df["duration_h"]) * 60 + _to_num(df.get("duration_m", pd.Series(0, index=df.index)))
            for c in NUM_COLS:
                if c in df.columns:
                    df[c] = _to_num(df[c])
            if "distance" in df.columns and "total_duration" in df.columns:
                df["speed"] = (df["distance"] / (df["total_duration"].clip(lower=15) / 60.0)).round(1)
            if "zone" in df.columns:
                df["zone"] = df["zone"].fillna("Unknown").astype(str)
    except Exception:
        df = None
    try:
        dfc = pd.read_csv(CLUSTERS_CSV) if CLUSTERS_CSV.exists() else None
    except Exception:
        dfc = None
    return df, dfc


class ClusterSpace:
    """K-Means centroids from trains_with_clusters.csv + a 2-D PCA map for the Galaxy page."""

    def __init__(self, dfc, cols):
        self.ok = False
        if dfc is None or "cluster" not in dfc.columns:
            return
        use = [c for c in cols if c in dfc.columns]
        if len(use) < 8:
            return
        self.use = use
        self.scaled = float(dfc["distance"].max()) < 25.0 if "distance" in dfc.columns else True
        X = dfc[use].astype(float).to_numpy()
        self.lab = dfc["cluster"].astype(int).to_numpy()
        self.ids = sorted(set(self.lab.tolist()))
        self.cent = np.array([X[self.lab == k].mean(axis=0) for k in self.ids])
        self.mu, self.sd = X.mean(axis=0), X.std(axis=0)
        self.sd[self.sd == 0] = 1.0
        Z = (X - self.mu) / self.sd
        _, S, Vt = np.linalg.svd(Z, full_matrices=False)
        self.V = Vt[:2].T
        self.var = (S[:2] ** 2 / np.sum(S ** 2)).tolist()
        self.pts = Z @ self.V
        self.cent2d = ((self.cent - self.mu) / self.sd) @ self.V
        self.ok = True

    def assign(self, X, Xs):
        vec = (Xs if self.scaled else X)[self.use].iloc[0].to_numpy(dtype=float)
        d = np.linalg.norm(self.cent - vec, axis=1)
        k = int(np.argmin(d))
        xy = ((vec - self.mu) / self.sd) @ self.V
        return self.ids[k], float(d[k]), xy


class Engine:
    """Everything that touches the saved model lives here."""

    def __init__(self, art, df, dfc):
        self.model, self.scaler = art["model"], art["scaler"]
        self.errors = list(art["errors"])
        self.df, self.dfc = df, dfc
        self.ready = self.model is not None
        self.cols = self._feature_cols()
        self.zones = [c[5:] for c in self.cols if c.startswith("zone_")]
        self.use_raw, self.int_map, self.str_classes = False, {}, False
        self.cal = dict(acc=None, note="model missing", raw=False, mapping="")
        self._audit = None
        if self.ready:
            self._calibrate()
        self.space = ClusterSpace(dfc, self.cols)

    # ---- setup -----------------------------------------------------------------------------
    def _feature_cols(self):
        for obj in (self.scaler, self.model):
            names = getattr(obj, "feature_names_in_", None)
            if names is not None:
                return [str(x) for x in names]
        return list(DEFAULT_26_FEATURES)

    def _map_text(self):
        return "native labels" if self.str_classes else ", ".join(f"{k}->{v}" for k, v in self.int_map.items())

    def _calibrate(self):
        """Find out (a) whether the tree was trained on scaled or raw values and (b) how integer
        class ids map to Pass/Exp/SF, by checking against the official `type` column of trains.csv."""
        m = self.model
        classes = list(m.classes_)
        self.str_classes = any(isinstance(c, str) for c in classes)
        srt = sorted(classes)
        self.int_map = {c: t for c, t in zip(srt, TIERS)}
        thr_max = float(np.max(m.tree_.threshold)) if hasattr(m, "tree_") else 0.0
        self.use_raw = bool(self.scaler is None or thr_max > 25.0)
        self.cal = dict(acc=None, note="heuristic (no dataset to verify)", raw=self.use_raw, mapping=self._map_text())
        if self.df is None or "type" not in self.df.columns or len(self.df) < 30:
            return
        try:
            X = self.frame(self.df)
            y = self.df["type"].map(norm_tier).to_numpy()
            Xs = pd.DataFrame(self.scaler.transform(X), columns=X.columns, index=X.index) if self.scaler is not None else X
            best = (-1.0, self.use_raw, self.int_map)
            for raw in ([False, True] if self.scaler is not None else [True]):
                pred = m.predict(self._sk(X if raw else Xs))
                if self.str_classes:
                    acc = float(np.mean(np.array([norm_tier(p) for p in pred], dtype=object) == y))
                    if acc > best[0]:
                        best = (acc, raw, self.int_map)
                else:
                    for perm in itertools.permutations(TIERS, len(srt)):
                        mp = dict(zip(srt, perm))
                        acc = float(np.mean(pd.Series(pred).map(mp).to_numpy(dtype=object) == y))
                        if acc > best[0]:
                            best = (acc, raw, mp)
            self.use_raw, self.int_map = best[1], best[2]
            self.cal = dict(acc=best[0], note="verified against trains.csv", raw=self.use_raw, mapping=self._map_text())
        except Exception as exc:
            self.cal["note"] = f"calibration skipped: {exc}"

    # ---- feature vectors -------------------------------------------------------------------
    def vector(self, a, bug=False):
        """The 26-feature row for the form: zeros from feature_names_in_, then user values,
        total_duration = hours x 60 + minutes, and the one-hot zone column set to 1."""
        total = int(a["h"]) * 60 + int(a["m"])
        row = {c: 0.0 for c in self.cols}
        vals = {"distance": float(a["d"]), "total_duration": float(a["m"] if bug else total)}
        for key, on in zip(FLAG_KEYS, a["c"]):
            vals[key] = float(bool(on))
        for k, v in vals.items():
            if k in row:
                row[k] = v
        zc = f"zone_{a['z']}"
        if zc in row:
            row[zc] = 1.0
        return pd.DataFrame([row])[self.cols], total

    def frame(self, df):
        """The same vector for many rows (dataset, batch upload)."""
        X = pd.DataFrame(0.0, index=df.index, columns=self.cols)
        for c in NUM_COLS:
            if c in df.columns and c in X.columns:
                X[c] = _to_num(df[c]).astype(float)
        if "zone" in df.columns:
            z = df["zone"].fillna("Unknown").astype(str)
            for zv in z.unique():
                col = f"zone_{zv}"
                if col in X.columns:
                    X.loc[z == zv, col] = 1.0
        return X

    def frame_grid(self, a, dist, total):
        """Many (distance, duration) points with the coaches and zone of the active schedule."""
        X = pd.DataFrame(0.0, index=range(len(dist)), columns=self.cols)
        X["distance"], X["total_duration"] = np.asarray(dist, dtype=float), np.asarray(total, dtype=float)
        for key, on in zip(FLAG_KEYS, a["c"]):
            if key in X.columns:
                X[key] = float(bool(on))
        zc = f"zone_{a['z']}"
        if zc in X.columns:
            X[zc] = 1.0
        return X

    def _inputs(self, X):
        Xs = pd.DataFrame(self.scaler.transform(X), columns=X.columns, index=X.index) if self.scaler is not None else X
        return (X if (self.use_raw or self.scaler is None) else Xs), Xs

    def _sk(self, Xin):
        return Xin if hasattr(self.model, "feature_names_in_") else Xin.to_numpy()

    def decode(self, c):
        return norm_tier(c) if self.str_classes else self.int_map.get(c)

    # ---- prediction ------------------------------------------------------------------------
    def labels(self, X):
        Xin, _ = self._inputs(X)
        return np.array([self.decode(p) or "?" for p in self.model.predict(self._sk(Xin))], dtype=object)

    def proba(self, X):
        Xin, _ = self._inputs(X)
        P = self.model.predict_proba(self._sk(Xin))
        out = np.zeros((len(X), 3))
        for j, c in enumerate(self.model.classes_):
            t = self.decode(c)
            if t in TIERS:
                out[:, TIERS.index(t)] += P[:, j]
        return out

    def unscale(self, f, thr):
        if self.use_raw or self.scaler is None or not hasattr(self.scaler, "scale_"):
            return float(thr)
        return float(thr * self.scaler.scale_[f] + self.scaler.mean_[f])

    def _mix(self, nid):
        t = self.model.tree_
        v = np.asarray(t.value[nid][0], dtype=float)
        v = v / v.sum() if v.sum() else v
        out = [0.0, 0.0, 0.0]
        for j, c in enumerate(self.model.classes_):
            tt = self.decode(c)
            if tt in TIERS:
                out[TIERS.index(tt)] += float(v[j])
        return out

    def path(self, X):
        """Root-to-leaf decision path of one row (list of split dicts + leaf dict)."""
        m = self.model
        if not hasattr(m, "tree_"):
            return [], {}
        Xin, _ = self._inputs(X)
        t = m.tree_
        ids = m.decision_path(self._sk(Xin)).indices
        steps = []
        for nid in ids:
            if t.children_left[nid] == t.children_right[nid]:
                continue
            f = int(t.feature[nid])
            thr = float(t.threshold[nid])
            vin = float(Xin.iloc[0, f])
            yes = vin <= thr
            left, right = int(t.children_left[nid]), int(t.children_right[nid])
            taken, other = (left, right) if yes else (right, left)
            steps.append(dict(node=int(nid), feature=self.cols[f], thr=thr, thr_raw=self.unscale(f, thr), v_in=vin,
                              v_raw=float(X.iloc[0, f]), yes=bool(yes), gini=float(t.impurity[nid]), n=int(t.n_node_samples[nid]),
                              mix=self._mix(nid), n_taken=int(t.n_node_samples[taken]), n_other=int(t.n_node_samples[other]),
                              mix_other=self._mix(other)))
        leaf = int(ids[-1])
        return steps, dict(node=leaf, n=int(t.n_node_samples[leaf]), gini=float(t.impurity[leaf]), mix=self._mix(leaf),
                           depth=len(steps))

    def importances(self, k=8):
        imp = getattr(self.model, "feature_importances_", None)
        if imp is None:
            return [("third_ac", .3551), ("distance", .2226), ("total_duration", .1799), ("chair_car", .1181), ("first_ac", .0133)]
        order = np.argsort(imp)[::-1][:k]
        return [(self.cols[i], float(imp[i])) for i in order if imp[i] > 0]

    # ---- clusters, look-alikes, audit ------------------------------------------------------
    def cluster(self, a, X, Xs):
        if self.space.ok:
            cid, dist, xy = self.space.assign(X, Xs)
            return dict(id=cid, dist=dist, outlier=dist > 7.0, xy=xy.tolist(), live=True)
        d, ac = a["d"], any(a["c"][:3])
        cid = 1 if a["z"] == "NFR" else 0 if (a["z"] == "ER" and d < 600) else 3 if (ac and d >= 450) else 2 if (not ac and d < 300) else 4
        return dict(id=cid, dist=0.0, outlier=False, xy=None, live=False)

    def neighbors(self, a, total, k=5):
        df = self.df
        if df is None or len(df) == 0:
            return pd.DataFrame()
        q = {"distance": a["d"], "total_duration": total, "first_ac": a["c"][0], "second_ac": a["c"][1], "third_ac": a["c"][2],
             "chair_car": a["c"][3], "sleeper": a["c"][4]}
        cols = [c for c in q if c in df.columns]
        sd = df[cols].std().replace(0, 1).fillna(1)
        D = np.zeros(len(df))
        for c in cols:
            w = 1.0 if c in ("distance", "total_duration") else 0.6
            D += w * ((df[c].to_numpy(dtype=float) - float(q[c])) / float(sd[c])) ** 2
        if "zone" in df.columns:
            D += 0.5 * (df["zone"].to_numpy() != a["z"])
        D = np.sqrt(D)
        idx = np.argsort(D)[:k]
        keep = [c for c in ["number", "name", "type", "zone", "distance", "total_duration", "speed"] if c in df.columns]
        out = df.iloc[idx][keep].copy()
        out["match"] = np.round(np.exp(-D[idx] / 3.0) * 100).astype(int)
        return out.reset_index(drop=True)

    def audit_all(self):
        """Run the model on every train in trains.csv and keep the ML label next to the official one."""
        if self._audit is None and self.ready and self.df is not None and "type" in self.df.columns:
            X = self.frame(self.df)
            w = self.df.copy()
            w["ml"] = self.labels(X)
            w["conf"] = (self.proba(X).max(axis=1) * 100).round(1)
            self._audit = w
        return self._audit


@st.cache_resource(show_spinner=False)
def _build_engine(sig):
    df, dfc = load_datasets(sig)
    return Engine(load_artifacts(sig), df, dfc)


def get_engine() -> Engine:
    return _build_engine(file_sig())


# ------------------------------------------------------------------------------
# advisory (business-rule) engine
# ------------------------------------------------------------------------------
def build_advisories(tier, a, total, speed):
    d = a["d"]
    f1, f2, f3, cc, sl, fc = [bool(x) for x in a["c"]]
    has_ac = f1 or f2 or f3 or cc
    out, flag = [], "OK"

    def add(level, title, body):
        out.append(dict(level=level, title=title, body=body))

    if speed > 130:
        add("warn", "Speed looks unrealistic", f"An average of <b>{speed:.0f} km/h</b> is above anything Indian Railways schedules. Re-check the duration.")
    elif speed < 15:
        add("warn", "Speed looks unrealistic", f"An average of <b>{speed:.1f} km/h</b> is slower than a goods shunt. Re-check the duration.")
    if tier == "Exp" and d > 1500 and f2:
        add("up", "Upgrade to Superfast recommended", f"A <b>{d} km</b> run with Second AC attached has premium features; the Superfast tier fits better.")
        flag = "UPGRADE"
    if tier == "SF" and d < 300:
        add("warn", "Downgrade to Express/Passenger recommended", f"Only <b>{d} km</b>: too short for a Superfast service.")
        flag = "DOWNGRADE"
    if tier == "SF" and speed < 55:
        need = int(d / 55.0 * 60)
        add("warn", f"Sub-benchmark Superfast at {speed:.1f} km/h",
            f"Superfast needs about <b>55 km/h</b> average. Cut the schedule below <b>{fmt_dur(need)}</b> (fewer halts) or reclassify as Express. "
            f"The test set has {FACTS['sf_to_exp']} such SF-to-Exp cases.")
        flag = "DOWNGRADE"
    elif tier == "Exp" and speed >= 55 and has_ac and d >= 500:
        add("up", f"Eligible for Superfast at {speed:.1f} km/h",
            f"AC rolling stock and a speed over the 55 km/h line unlock the Superfast tier ({FACTS['exp_to_sf']} Exp-to-SF candidates in the test set).")
        flag = "UPGRADE"
    if tier == "Pass" and (d >= 550 or has_ac) and speed >= 42:
        add("up", "Candidate for Intercity Express", f"<b>{d} km</b> at <b>{speed:.1f} km/h</b> with reserved coaches is beyond a regional passenger profile.")
        flag = "UPGRADE" if flag == "OK" else flag
    if tier == "SF" and not has_ac and not sl:
        add("info", "Superfast without AC or Sleeper", "No reserved coach class is selected; check the coach composition.")
    if not out:
        art = "an" if TIER_META[tier]["short"][0] in "AEIOU" else "a"
        add("ok", f"Schedule is consistent with {art} {TIER_META[tier]['short']} service",
            f"<b>{d} km</b> in <b>{fmt_dur(total)}</b> ({speed:.1f} km/h) matches the national benchmark for this tier.")
    return out, flag


def _parse_hhmm(s, default="08:00"):
    m = re.match(r"^\s*(\d{1,2}):(\d{2})", str(s or ""))
    return f"{int(m.group(1)) % 24:02d}:{m.group(2)}" if m else default


def analyze(eng: Engine, a: dict, bug: bool = False):
    """One call = everything the pages need about the active schedule."""
    X, total = eng.vector(a, bug)
    total_true = int(a["h"]) * 60 + int(a["m"])
    speed = a["d"] / max(total_true / 60.0, 0.25)
    R = dict(a=a, total=total_true, speed=speed, bug=bug, X=X, ok=eng.ready)
    if eng.ready:
        Xin, Xs = eng._inputs(X)
        P = eng.proba(X)[0]
        tier = str(eng.labels(X)[0])
        if tier not in TIERS:
            tier = TIERS[int(np.argmax(P))]
        steps, leaf = eng.path(X)
        R.update(tier=tier, conf=float(P[TIERS.index(tier)]) * 100.0, proba={t: float(P[i]) for i, t in enumerate(TIERS)},
                 steps=steps, leaf=leaf, Xs=Xs, cluster=eng.cluster(a, X, Xs), neigh=eng.neighbors(a, total_true))
    else:
        tier = "Exp"
        R.update(tier=tier, conf=0.0, proba={t: 0.0 for t in TIERS}, steps=[], leaf={}, Xs=X,
                 cluster=eng.cluster(a, X, X), neigh=pd.DataFrame())
    R["adv"], R["flag"] = build_advisories(R["tier"], a, total_true, speed)
    try:
        dep = datetime.strptime(f"{a['dt']} {a['dep']}", "%Y-%m-%d %H:%M")
    except Exception:
        dep = datetime.now().replace(second=0, microsecond=0)
    arr = dep + timedelta(minutes=total_true)
    R.update(dep=dep, arr=arr, day_off=(arr.date() - dep.date()).days)
    key = json.dumps({k: a[k] for k in ("d", "h", "m", "z", "c", "a", "b", "dep", "dt")}, sort_keys=True, default=str)
    R["pnr"] = f"{int(hashlib.sha1(key.encode()).hexdigest(), 16) % 10**10:010d}"
    return R


def station_label(code: str, fallback: str = "") -> str:
    s = STATION_BY_CODE.get(code)
    return f"{s[1]} ({s[0]})" if s else (fallback or "")


def active_from_row(r) -> dict:
    """Turn one trains.csv row into an `active` schedule dict."""
    def g(k, d=0):
        v = r.get(k, d)
        return d if pd.isna(v) else v
    total = int(g("total_duration", 300))
    h, m = divmod(max(total, 1), 60)
    ft, tt = str(g("from_station_name", "")).title(), str(g("to_station_name", "")).title()
    fc, tc = str(g("from_station_code", "")), str(g("to_station_code", ""))
    return dict(d=int(max(10, min(4500, round(float(g("distance", 500)))))), h=int(min(h, 72)), m=int(m), z=str(g("zone", "WR")),
                c=tuple(bool(int(g(k, 0))) for k in FLAG_KEYS), t=f"{g('number', '')} {str(g('name', '')).title()}".strip(),
                a=fc if fc in STATION_BY_CODE else "", b=tc if tc in STATION_BY_CODE else "", dep=_parse_hhmm(g("departure", ""), "08:00"),
                dt=date.today().isoformat(), off=str(g("type", "")), fa=f"{ft} ({fc})" if ft else "", ta=f"{tt} ({tc})" if tt else "",
                no=str(g("number", "")))


# ------------------------------------------------------------------------------
# announcement text, QR / barcode, voice
# ------------------------------------------------------------------------------
def pa_texts(R: dict):
    a, tier = R["a"], R["tier"]
    zi = ZONE_INFO.get(a["z"], ZONE_INFO["Unknown"])
    tier_en, tier_hi = TIER_META[tier]["name"], TIER_META[tier]["hi"]
    if R["flag"] == "DOWNGRADE":
        tail_hi = f"ऑडिट सूचना: औसत गति {R['speed']:.1f} किलोमीटर प्रति घंटा है, जो सुपरफास्ट मानक से कम है।"
        tail_en = f"Audit notice: average speed is {R['speed']:.1f} kilometres per hour, below the Superfast benchmark."
    elif R["flag"] == "UPGRADE":
        tail_hi = "ऑडिट सूचना: यह सेवा उच्च श्रेणी में उन्नयन के योग्य है।"
        tail_en = "Audit notice: this service qualifies for a higher tier."
    else:
        tail_hi = "यह समय सारणी राष्ट्रीय मानकों के अनुरूप है।"
        tail_en = "The schedule complies with national standards."
    hi = (f"यात्रीगण कृपया ध्यान दें। {zi[2]} की यह गाड़ी, कुल दूरी {a['d']} किलोमीटर, निर्धारित समय {a['h']} घंटे {a['m']} मिनट, "
          f"मशीन लर्निंग के अनुसार {tier_hi} श्रेणी में वर्गीकृत की गई है। {tail_hi}")
    en = (f"Attention please. This {zi[0]} service covers {a['d']} kilometres in {a['h']} hours and {a['m']} minutes and is classified "
          f"as {tier_en} with {R['conf']:.0f} percent model confidence. {tail_en}")
    return hi, en


# announcer voices: Microsoft neural voices through the optional `edge-tts` package (natural, human-like),
# then Google TTS, then whatever voice the browser offers. A deep male and a female voice per language.
VOICE_SETS = {
    "Female (Swara / Neerja)": dict(hi=("hi-IN-SwaraNeural", "F"), en=("en-IN-NeerjaNeural", "F")),
    "Male, deep (Madhur / Prabhat)": dict(hi=("hi-IN-MadhurNeural", "M"), en=("en-IN-PrabhatNeural", "M")),
    "Duet: female Hindi, male English": dict(hi=("hi-IN-SwaraNeural", "F"), en=("en-IN-PrabhatNeural", "M")),
}
_EDGE_DOWN_UNTIL = 0.0


def _edge_tts_bytes(text: str, voice: str, rate: str, pitch: str) -> bytes:
    import asyncio
    import concurrent.futures

    async def run():
        com = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        buf = bytearray()
        async for ch in com.stream():
            if ch.get("type") == "audio":
                buf += ch["data"]
        return bytes(buf)

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        return ex.submit(lambda: asyncio.run(run())).result(timeout=14)


def voice_b64(text: str, lang: str, voice: str, gender: str) -> str:
    """MP3 (base64) of an announcement. Cached on disk. Returns '' if no engine worked, so the browser voice takes over."""
    global _EDGE_DOWN_UNTIL
    if not text.strip():
        return ""
    try:
        AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        key = hashlib.md5(f"{voice}|{gender}|{text}".encode("utf-8")).hexdigest()[:16]
        fp = AUDIO_CACHE_DIR / f"pa_{voice}_{key}.mp3"
        if fp.exists():
            return base64.b64encode(fp.read_bytes()).decode()
        if EDGE_OK and time.time() > _EDGE_DOWN_UNTIL:
            try:
                data = _edge_tts_bytes(text, voice, "-8%" if gender == "M" else "-3%", "-18Hz" if gender == "M" else "+0Hz")
                if len(data) > 1500:
                    fp.write_bytes(data)
                    return base64.b64encode(data).decode()
            except Exception:
                _EDGE_DOWN_UNTIL = time.time() + 120  # offline or blocked: do not retry for two minutes
        if GTTS_OK:
            gp = AUDIO_CACHE_DIR / f"pa_gtts_{lang}_{key}.mp3"
            if not gp.exists():
                gTTS(text=text, lang=lang, tld="co.in", slow=False).save(str(gp))
            return base64.b64encode(gp.read_bytes()).decode()
    except Exception:
        pass
    return ""


def qr_svg(text: str, px: int = 92) -> str:
    """Real QR code when the `qrcode` package is installed, otherwise a decorative code from a hash."""
    cells, n = None, 0
    if QR_OK:
        try:
            q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
            q.add_data(text)
            q.make(fit=True)
            cells = [[bool(v) for v in row] for row in q.get_matrix()]
            n = len(cells)
        except Exception:
            cells = None
    if cells is None:
        n = 21
        bits = hashlib.shake_256(text.encode()).digest(60)
        cells = [[bool((bits[(y * n + x) // 8] >> ((y * n + x) % 8)) & 1) for x in range(n)] for y in range(n)]
        for ox, oy in ((0, 0), (n - 7, 0), (0, n - 7)):
            for y in range(-1, 8):
                for x in range(-1, 8):
                    yy, xx = oy + y, ox + x
                    if 0 <= yy < n and 0 <= xx < n:
                        edge = x in (0, 6) or y in (0, 6)
                        core = 2 <= x <= 4 and 2 <= y <= 4
                        cells[yy][xx] = (0 <= x <= 6 and 0 <= y <= 6) and (edge or core)
    rects = "".join(f'<rect x="{x}" y="{y}" width="1" height="1"/>' for y, row in enumerate(cells) for x, v in enumerate(row) if v)
    return (f'<svg viewBox="0 0 {n} {n}" width="{px}" height="{px}" shape-rendering="crispEdges" fill="#0B1530" '
            f'xmlns="http://www.w3.org/2000/svg">{rects}</svg>')


def barcode_svg(text: str, w: int = 190, h: int = 40) -> str:
    digest = hashlib.sha256(text.encode()).digest()
    x, bars = 0, []
    for i, byte in enumerate(digest):
        for j, nib in enumerate((byte >> 4, byte & 15)):
            width = 1 + nib % 3
            if (i * 2 + j) % 2 == 0:
                bars.append(f'<rect x="{x}" y="0" width="{width}" height="{h}"/>')
            x += width
    return (f'<svg viewBox="0 0 {x} {h}" width="{w}" height="{h}" preserveAspectRatio="none" fill="#0B1530" '
            f'xmlns="http://www.w3.org/2000/svg">{"".join(bars)}</svg>')


# ==============================================================================
# 4. SHARED JS TOOLKIT
# ==============================================================================
# Small helpers used by every canvas / HTML visual. The JS lives in Python strings and is placed
# inside isolated iframes, so Streamlit's Markdown parser can never garble it.
JS_COMMON = r"""
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const clamp=(v,a,b)=>Math.min(b,Math.max(a,v)), lerp=(a,b,t)=>a+(b-a)*t;
const REDUCED=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
const easeOut=t=>1-Math.pow(1-t,3), easeInOut=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
function rng(seed){let a=seed>>>0;return()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function hex2rgb(h){h=h.replace('#','');if(h.length===3)h=h.split('').map(c=>c+c).join('');const n=parseInt(h,16);return[n>>16&255,n>>8&255,n&255]}
function mixc(a,b,t){const A=hex2rgb(a),B=hex2rgb(b);return'rgb('+A.map((v,i)=>Math.round(lerp(v,B[i],t))).join(',')+')'}
function mixArr(a,b,t){const A=hex2rgb(a),B=hex2rgb(b);return A.map((v,i)=>Math.round(lerp(v,B[i],t)))}
function rgba(h,al){const c=hex2rgb(h);return'rgba('+c[0]+','+c[1]+','+c[2]+','+al+')'}
function shade(h,f){const c=hex2rgb(h).map(v=>clamp(Math.round(v*f),0,255));return'rgb('+c.join(',')+')'}
function rr(g,x,y,w,h,r){let tl,tr,br,bl;if(Array.isArray(r)){[tl,tr,br,bl]=r}else{tl=tr=br=bl=r}
tl=Math.min(tl,w/2,h/2);tr=Math.min(tr,w/2,h/2);br=Math.min(br,w/2,h/2);bl=Math.min(bl,w/2,h/2);
g.beginPath();g.moveTo(x+tl,y);g.lineTo(x+w-tr,y);g.quadraticCurveTo(x+w,y,x+w,y+tr);g.lineTo(x+w,y+h-br);g.quadraticCurveTo(x+w,y+h,x+w-br,y+h);
g.lineTo(x+bl,y+h);g.quadraticCurveTo(x,y+h,x,y+h-bl);g.lineTo(x,y+tl);g.quadraticCurveTo(x,y,x+tl,y);g.closePath()}
function fitCanvas(cv,hh){const r=cv.getBoundingClientRect();const dpr=Math.min(window.devicePixelRatio||1,2);const w=Math.max(240,Math.round(r.width||cv.parentElement.clientWidth||600));
const h=hh||Math.round(r.height||300);cv.width=Math.round(w*dpr);cv.height=Math.round(h*dpr);cv.style.height=h+'px';const g=cv.getContext('2d');g.setTransform(dpr,0,0,dpr,0,0);return{g,w,h,dpr}}
function loop(fn){let last=performance.now();function f(t){const dt=Math.min(.05,(t-last)/1000);last=t;if(!document.hidden)fn(dt,t/1000);requestAnimationFrame(f)}requestAnimationFrame(f)}
function countUp(el,to,dur,dec,suf){const t0=performance.now();(function s(t){const k=clamp((t-t0)/dur,0,1);el.textContent=(to*easeOut(k)).toFixed(dec)+(suf||'');if(k<1)requestAnimationFrame(s)})(t0)}
function onResize(fn){let t;window.addEventListener('resize',()=>{clearTimeout(t);t=setTimeout(fn,120)})}
"""

JS_AUDIO = r"""
const RailAudio=(()=>{
 let ctx=null,master=null,on=false,clackT=null,rate=3,nbuf=null,rainSrc=null,bellT=null,vol=1;
 function init(){if(ctx)return ctx;const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return null;
  ctx=new AC();master=ctx.createGain();master.gain.value=0;master.connect(ctx.destination);return ctx}
 function wake(){if(!init())return false;if(ctx.state==='suspended')ctx.resume();return true}
 function noise(){if(!nbuf){const n=Math.floor(ctx.sampleRate*2.6);nbuf=ctx.createBuffer(1,n,ctx.sampleRate);const d=nbuf.getChannelData(0);for(let i=0;i<n;i++)d[i]=Math.random()*2-1}return nbuf}
 function clackOnce(t,g){const s=ctx.createBufferSource();s.buffer=noise();const bp=ctx.createBiquadFilter();bp.type='bandpass';bp.frequency.value=650+Math.random()*500;bp.Q.value=1.1;
  const ga=ctx.createGain();ga.gain.setValueAtTime(.26*g*vol,t);ga.gain.exponentialRampToValueAtTime(.001,t+.07);s.connect(bp);bp.connect(ga);ga.connect(master);s.start(t,Math.random()*1.5,.09);
  const o=ctx.createOscillator();o.frequency.setValueAtTime(96,t);o.frequency.exponentialRampToValueAtTime(46,t+.1);const g2=ctx.createGain();g2.gain.setValueAtTime(.2*g*vol,t);
  g2.gain.exponentialRampToValueAtTime(.001,t+.13);o.connect(g2);g2.connect(master);o.start(t);o.stop(t+.15)}
 function clackLoop(){if(!on||!ctx)return;if(rate===0){clackT=setTimeout(clackLoop,250);return}const t=ctx.currentTime+.01;clackOnce(t,1);clackOnce(t+.085,.6);clackT=setTimeout(clackLoop,1000/rate*(.9+Math.random()*.2))}
 function enable(){if(!wake())return false;on=true;master.gain.setTargetAtTime(.9,ctx.currentTime,.05);clearTimeout(clackT);clackLoop();return true}
 function disable(){on=false;clearTimeout(clackT);stopBell();rain(false);if(ctx)master.gain.setTargetAtTime(0,ctx.currentTime,.05)}
 function setSpeed(kmh){rate=kmh<4?0:clamp(kmh/15,1.6,7.5)}
 function isOn(){return on}
 function horn(kind){if(!wake())return;const f={aero:[415,523],wap7:[330,415],wdm:[233,293]}[kind]||[330,415];const t=ctx.currentTime;
  const out=ctx.createGain();out.gain.setValueAtTime(0,t);out.gain.linearRampToValueAtTime(.34,t+.06);out.gain.setValueAtTime(.34,t+.85);out.gain.exponentialRampToValueAtTime(.001,t+1.5);
  const lp=ctx.createBiquadFilter();lp.type='lowpass';lp.frequency.value=1700;out.connect(lp);lp.connect(ctx.destination);
  f.forEach((fr,i)=>{[['sawtooth',1,.5],['square',2,.12]].forEach(p=>{const o=ctx.createOscillator();o.type=p[0];o.frequency.value=fr*p[1]*(i?1.004:1);const g=ctx.createGain();g.gain.value=p[2];o.connect(g);g.connect(out);o.start(t);o.stop(t+1.55)})})}
 function chime(alert){if(!wake())return;const n=alert?[587.33,440,587.33,440]:[392,493.88,587.33,783.99];const t=ctx.currentTime;
  n.forEach((fr,i)=>{const o=ctx.createOscillator(),o2=ctx.createOscillator(),g=ctx.createGain();o.frequency.value=fr;o2.frequency.value=fr*2;o.type='sine';o2.type='sine';
   const st=t+.04+i*.32;g.gain.setValueAtTime(0,st);g.gain.linearRampToValueAtTime(.3,st+.012);g.gain.exponentialRampToValueAtTime(.001,st+.8);const g2=ctx.createGain();g2.gain.value=.3;
   o.connect(g);o2.connect(g2);g2.connect(g);g.connect(ctx.destination);o.start(st);o2.start(st);o.stop(st+.85);o2.stop(st+.85)})}
 function thud(){if(!wake())return;const t=ctx.currentTime;const o=ctx.createOscillator();o.frequency.setValueAtTime(130,t);o.frequency.exponentialRampToValueAtTime(36,t+.28);
  const g=ctx.createGain();g.gain.setValueAtTime(.7,t);g.gain.exponentialRampToValueAtTime(.001,t+.4);o.connect(g);g.connect(ctx.destination);o.start(t);o.stop(t+.42);
  const s=ctx.createBufferSource();s.buffer=noise();const lp=ctx.createBiquadFilter();lp.type='lowpass';lp.frequency.value=500;const g2=ctx.createGain();g2.gain.setValueAtTime(.5,t);
  g2.gain.exponentialRampToValueAtTime(.001,t+.16);s.connect(lp);lp.connect(g2);g2.connect(ctx.destination);s.start(t,0,.2)}
 function click(){if(!wake())return;const t=ctx.currentTime;const o=ctx.createOscillator();o.type='square';o.frequency.value=1800;const g=ctx.createGain();g.gain.setValueAtTime(.05,t);
  g.gain.exponentialRampToValueAtTime(.001,t+.03);o.connect(g);g.connect(ctx.destination);o.start(t);o.stop(t+.04)}
 function thunder(){if(!ctx||!on)return;const t=ctx.currentTime;const s=ctx.createBufferSource();s.buffer=noise();const lp=ctx.createBiquadFilter();lp.type='lowpass';lp.frequency.value=230;
  const g=ctx.createGain();g.gain.setValueAtTime(.001,t);g.gain.linearRampToValueAtTime(.8,t+.1);g.gain.exponentialRampToValueAtTime(.001,t+2.4);s.connect(lp);lp.connect(g);g.connect(master);s.start(t,0,2.5)}
 function ping(t){const o=ctx.createOscillator();o.frequency.value=1250;const g=ctx.createGain();g.gain.setValueAtTime(.16,t);g.gain.exponentialRampToValueAtTime(.001,t+.2);
  o.connect(g);g.connect(master);o.start(t);o.stop(t+.22);const o2=ctx.createOscillator();o2.frequency.value=2510;const g2=ctx.createGain();g2.gain.setValueAtTime(.06,t);
  g2.gain.exponentialRampToValueAtTime(.001,t+.12);o2.connect(g2);g2.connect(master);o2.start(t);o2.stop(t+.14)}
 function bell(){if(!ctx||!on||bellT)return;bellT=setInterval(()=>ping(ctx.currentTime+.01),260)}
 function stopBell(){clearInterval(bellT);bellT=null}
 function rain(f){if(!ctx)return;if(f&&on&&!rainSrc){rainSrc=ctx.createBufferSource();rainSrc.buffer=noise();rainSrc.loop=true;const hp=ctx.createBiquadFilter();hp.type='highpass';hp.frequency.value=700;
   const lp=ctx.createBiquadFilter();lp.type='lowpass';lp.frequency.value=5200;const g=ctx.createGain();g.gain.value=.07;rainSrc.connect(hp);hp.connect(lp);lp.connect(g);g.connect(master);rainSrc.start()}
  else if(!f&&rainSrc){try{rainSrc.stop()}catch(e){}rainSrc=null}}
 function pick(lang,g){if(!(window.speechSynthesis))return null;const vs=speechSynthesis.getVoices().filter(v=>v.lang.replace('_','-').toLowerCase().startsWith(lang.slice(0,2)));if(!vs.length)return null;
  const fem=/swara|neerja|heera|kalpana|priya|lekha|veena|zira|hazel|susan|samantha|female|aditi|raveena/i,mal=/madhur|prabhat|hemant|ravi|rishi|david|mark|male|kunal/i;
  const sc=v=>(/natural|online|neural/i.test(v.name)?4:0)+(/-in|_in/i.test(v.lang)?2:0)+((g==='F'?fem:mal).test(v.name)?3:0)-((g==='F'?mal:fem).test(v.name)?3:0);return vs.sort((a,b)=>sc(b)-sc(a))[0]}
 function speak(txt,lang,g,cb){if(!(window.speechSynthesis)){cb&&cb();return}const u=new SpeechSynthesisUtterance(txt);u.lang=lang;const v=pick(lang,g);if(v)u.voice=v;u.pitch=g==='M'?.72:1;u.rate=g==='M'?.88:.95;u.onend=()=>cb&&cb();u.onerror=()=>cb&&cb();speechSynthesis.speak(u)}
 function ir(){const n=Math.floor(ctx.sampleRate*1.3),b=ctx.createBuffer(2,n,ctx.sampleRate);for(let c=0;c<2;c++){const d=b.getChannelData(c);for(let i=0;i<n;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/n,2.6)}return b}
 function pa(a){try{if(!ctx||ctx.state!=='running')return;const src=ctx.createMediaElementSource(a),hp=ctx.createBiquadFilter(),lp=ctx.createBiquadFilter();hp.type='highpass';hp.frequency.value=240;lp.type='lowpass';lp.frequency.value=3900;
  const sh=ctx.createWaveShaper(),cv=new Float32Array(256);for(let i=0;i<256;i++){const x=i/128-1;cv[i]=Math.tanh(x*1.7)}sh.curve=cv;const dry=ctx.createGain();dry.gain.value=.85;const cn=ctx.createConvolver();cn.buffer=ir();const wet=ctx.createGain();wet.gain.value=.3;
  src.connect(hp);hp.connect(lp);lp.connect(sh);sh.connect(dry);dry.connect(ctx.destination);sh.connect(cn);cn.connect(wet);wet.connect(ctx.destination)}catch(e){}}
 function mp3(s,cb){if(s.b64&&s.b64.length>50){const a=new Audio('data:audio/mp3;base64,'+s.b64);wake();pa(a);a.onended=()=>cb&&cb();a.onerror=()=>speak(s.txt,s.lang,s.g,cb);a.play().catch(()=>speak(s.txt,s.lang,s.g,cb))}else speak(s.txt,s.lang,s.g,cb)}
 function announce(o){chime(o.alert);const segs=o.segs||[];setTimeout(()=>{(function nx(i){if(i<segs.length)mp3(segs[i],()=>setTimeout(()=>nx(i+1),350))})(0)},1750)}
 function brake(){if(!ctx||!on)return;const t=ctx.currentTime,s=ctx.createBufferSource();s.buffer=noise();s.loop=true;const bp=ctx.createBiquadFilter();bp.type='bandpass';bp.Q.value=9;bp.frequency.setValueAtTime(4200,t);bp.frequency.exponentialRampToValueAtTime(1400,t+3);
  const g=ctx.createGain();g.gain.setValueAtTime(.001,t);g.gain.linearRampToValueAtTime(.15,t+.5);g.gain.exponentialRampToValueAtTime(.001,t+3.2);s.connect(bp);bp.connect(g);g.connect(master);s.start(t);s.stop(t+3.3)}
 function printer(){if(!wake())return;const t=ctx.currentTime;for(let i=0;i<9;i++){const s=ctx.createBufferSource();s.buffer=noise();const bp=ctx.createBiquadFilter();bp.type='bandpass';bp.frequency.value=2600;bp.Q.value=2;const g=ctx.createGain(),st=t+i*.085;
  g.gain.setValueAtTime(.12,st);g.gain.exponentialRampToValueAtTime(.001,st+.07);s.connect(bp);bp.connect(g);g.connect(ctx.destination);s.start(st,Math.random()*1.5,.08)}}
 function reverb(b){vol=b?1.8:1}
 if(window.speechSynthesis)speechSynthesis.getVoices();
 return{enable,disable,isOn,setSpeed,horn,chime,thud,click,thunder,bell,stopBell,rain,announce,speak,wake,brake,printer,reverb,state:()=>ctx?ctx.state:'none'}
})();
"""


# ==============================================================================
# 5. HERO SCENE  (the cinematic rail journey)
# ==============================================================================
# Everything is drawn procedurally on one canvas: sky + sun/moon/stars, clouds, birds, mountains,
# hills, wind turbines, pylons, village, patchwork fields, OHE masts with catenary, signals,
# station canopies with a yellow name board, level crossings with a W/L whistle board, rain, fog,
# lightning, and a train whose loco, coaches and speed come from the model's prediction.
HERO_CSS = r"""
body{background:#070D1F}
.hero{position:relative;height:440px;border-radius:20px;overflow:hidden;border:1px solid rgba(255,255,255,.14);box-shadow:0 24px 60px rgba(0,0,0,.45)}
#cv{position:absolute;inset:0;width:100%;height:100%}
.hud{position:absolute;z-index:3}
.tl{left:22px;top:18px;display:flex;align-items:center;gap:14px}
.logo{width:56px;height:56px;border-radius:12px;background:#fff;padding:5px;object-fit:contain;box-shadow:0 8px 24px rgba(0,0,0,.4)}
.board{background:#FFD21F;color:#14110A;border:3px solid #14110A;border-radius:7px;padding:3px 18px 5px;text-align:center;font-family:'Rajdhani',sans-serif;
box-shadow:0 0 0 2px #FFD21F,0 12px 30px rgba(0,0,0,.5);position:relative}
.board b{display:block;font-size:35px;line-height:1.02;letter-spacing:2.5px;font-weight:700}
.board i{display:block;font-style:normal;font-size:19px;font-weight:600;line-height:1.1}
.board:before,.board:after{content:'';position:absolute;top:7px;width:6px;height:6px;border-radius:50%;background:#14110A;opacity:.7}
.board:before{left:6px}.board:after{right:6px}
.tag{position:absolute;left:92px;top:96px;width:430px;color:#E8EEFF;font-size:15px;line-height:1.45;text-shadow:0 2px 12px rgba(0,0,0,.7)}
.tr{right:22px;top:18px;text-align:right;text-shadow:0 2px 12px rgba(0,0,0,.6)}
.clock{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:34px;line-height:1;letter-spacing:1px}
.date{font-size:13px;color:#C7D3F5}
.bl{left:22px;bottom:44px;display:flex;gap:8px;flex-wrap:wrap;max-width:40%;align-content:flex-end}
.pill{background:rgba(7,13,31,.62);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:5px 13px;font-size:13.5px;font-weight:500;color:#EAF0FF}
.pill.t{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:16px;letter-spacing:.6px}
.br{right:22px;bottom:44px;display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;max-width:58%}
.br button{background:rgba(7,13,31,.66);backdrop-filter:blur(6px);color:#EAF0FF;border:1px solid rgba(255,255,255,.2);border-radius:999px;padding:5px 12px;font-size:12.5px;font-weight:500;transition:all .2s}
.br button:hover{border-color:#FFD21F;color:#FFD21F}.br button.on{background:#FFD21F;color:#14110A;border-color:#FFD21F}
.br button:focus-visible{outline:2px solid #FFD21F;outline-offset:2px}
.tick{position:absolute;left:0;right:0;bottom:0;height:30px;background:rgba(5,9,22,.82);border-top:1px solid rgba(255,210,31,.5);overflow:hidden;z-index:3}
.tick div{display:inline-block;white-space:nowrap;line-height:30px;font-size:13px;color:#FFD21F;letter-spacing:.4px;animation:mq 46s linear infinite;padding-left:100%}
@keyframes mq{to{transform:translateX(-100%)}}
.hint{position:absolute;left:50%;top:74px;transform:translateX(-50%);z-index:3;background:rgba(255,210,31,.95);color:#14110A;border-radius:999px;padding:5px 16px;font-size:13px;font-weight:600;display:none}
@media (max-width:760px){.tag{display:none}.board b{font-size:26px}.bl{max-width:100%;bottom:80px}}
"""

HERO_JS = r"""
const P=__P__;
const cv=$('#cv');let g,W=0,H=0,DPR=1,HZ=0,RAIL=0,U=200,CH=54,LW=210,TW=1500,A=1,V=200,wireY=0,pal,T={},STARS=[],CLOUDS=[];
const S={time:P.time,weather:P.weather,off:0,t:0,flash:0,bolt:null,nextBolt:4,smoke:[],sparks:[],rain:[],events:[],evT:2.4,evN:0,birds:[],bT:5,smT:0,lastPal:0,mult:1,v:150,vc0:200,mode:0,wantStop:false,haltT:0,tun:0,fr:[],frT:5};
const TOD={
 night:{top:'#040916',mid:'#0A1634',hor:'#1B2A58',mtn:'#0C1733',hill:'#09112A',tree:'#060D20',gr:'#0A1124',fld:'#14281F',fld2:'#102019',amb:.5,stars:1,lamp:1},
 dawn:{top:'#2A2D68',mid:'#C45C7C',hor:'#FFB86B',mtn:'#4B4A8C',hill:'#32316A',tree:'#1E2050',gr:'#1E2644',fld:'#2F5A41',fld2:'#264A36',amb:.75,stars:.25,lamp:.6},
 day:{top:'#2A74D9',mid:'#6BB4F2',hor:'#D5ECFF',mtn:'#7F9FC6',hill:'#5F8E70',tree:'#2F6B3F',gr:'#4F7F3F',fld:'#78AE4E',fld2:'#659A42',amb:1,stars:0,lamp:0},
 dusk:{top:'#191B50',mid:'#B3466D',hor:'#FF983F',mtn:'#5A3E72',hill:'#3A2D58',tree:'#241B3E',gr:'#1F1C36',fld:'#3E5236',fld2:'#33432D',amb:.7,stars:.35,lamp:.8}};
const GRAY={top:'#4A5568',mid:'#6B7686',hor:'#98A2B0',mtn:'#5C6674',hill:'#4C5A5A',tree:'#2E3C36',gr:'#3C4A40',fld:'#4B6040',fld2:'#42553A',amb:.62,stars:0,lamp:.5};
const NAMES=[["VADODARA JN","वडोदरा जं.","BRC"],["SURAT","सूरत","ST"],["KOTA JN","कोटा जं.","KOTA"],["MATHURA JN","मथुरा जं.","MTJ"],["AGRA CANTT","आगरा कैंट","AGC"],["BHOPAL JN","भोपाल जं.","BPL"],
 ["NAGPUR","नागपुर","NGP"],["ITARSI JN","इटारसी जं.","ET"],["RATLAM JN","रतलाम जं.","RTM"],["AHMEDABAD JN","अहमदाबाद जं.","ADI"],["KANPUR CENTRAL","कानपुर सेंट्रल","CNB"],
 ["PRAYAGRAJ JN","प्रयागराज जं.","PRYJ"],["GAYA JN","गया जं.","GAYA"],["ASANSOL JN","आसनसोल जं.","ASN"],["VIJAYAWADA JN","विजयवाड़ा जं.","BZA"],["PUNE JN","पुणे जं.","PUNE"],["RAIPUR JN","रायपुर जं.","R"]];
const KIND_NAME={'1A':'AC FIRST','2A':'AC 2 TIER','3A':'AC 3 TIER','CC':'AC CHAIR CAR','SL':'SLEEPER','FC':'FIRST CLASS','GEN':'GENERAL','GRD':'GUARD'};
const LIV={SF:{base:'#E9EEF7',roof:'#B9C3D3',low:'#1D4ED8',win:'#13203C'},Exp:{base:'#2C5FC4',roof:'#8FA7D6',low:'#F2F5FA',win:'#0E1830'},Pass:{base:'#7B3326',roof:'#5A241B',low:'#E8C34E',win:'#1B0F0C'}};
const L=LIV[P.tier]||LIV.Exp;

function mixHex(a,b,t){const A_=hex2rgb(a),B_=hex2rgb(b);return'#'+A_.map((v,i)=>Math.round(lerp(v,B_[i],t)).toString(16).padStart(2,'0')).join('')}
function mixPal(a,b,t){const o={};for(const k in a)o[k]=typeof a[k]==='string'?mixHex(a[k],b[k],t):lerp(a[k],b[k],t);return o}
function hourIST(){const d=new Date();const ist=new Date(d.getTime()+d.getTimezoneOffset()*60000+19800000);return ist.getHours()+ist.getMinutes()/60+ist.getSeconds()/3600}
function palAt(h){const k=[[0,'night'],[5,'night'],[6.2,'dawn'],[7.8,'day'],[17,'day'],[18.4,'dusk'],[19.8,'night'],[24,'night']];
 for(let i=0;i<k.length-1;i++)if(h>=k[i][0]&&h<=k[i+1][0])return mixPal(TOD[k[i][1]],TOD[k[i+1][1]],(h-k[i][0])/(k[i+1][0]-k[i][0]));return TOD.night}
function curPal(){let p=S.time==='auto'?palAt(hourIST()):TOD[S.time];const w=S.weather,k=w==='storm'?.62:w==='rain'?.38:w==='fog'?.45:0;
 if(k){const gray=mixPal(GRAY,TOD.night,1-clamp((p.amb-.5)/.5,0,1));p=mixPal(p,gray,k)}return p}

/* ---------- static layers pre-rendered into tiles ---------- */
function tile(yTop,th,fn){const c=document.createElement('canvas');c.width=Math.round(TW*DPR);c.height=Math.round(th*DPR);const x=c.getContext('2d');x.setTransform(DPR,0,0,DPR,0,0);fn(x,TW,th);return{c,yTop,th}}
function blit(t,par){const o=(((S.off*par)%TW)+TW)%TW;for(let x=-o;x<W;x+=TW)g.drawImage(t.c,Math.floor(x),t.yTop,TW+1,t.th)}
function ridge(x,w,h,seed,amp,base,ks,fill){const R=rng(seed),ph=ks.map(()=>R()*6.283);x.beginPath();x.moveTo(0,h);
 for(let i=0;i<=w;i+=5){let y=0;ks.forEach((k,j)=>{y+=Math.sin(i/w*6.2832*k+ph[j])*amp/(j*.7+1)});x.lineTo(i,base-y)}x.lineTo(w,h);x.closePath();x.fillStyle=fill;x.fill()}
function trees(x,w,h){const R=rng(77),by=h-8,col=pal.tree;const at=(px,wd,fn)=>{fn(px);if(px+wd>w)fn(px-w)};
 for(let i=0;i<44;i++){const px=R()*w,k=R(),hh=24+R()*38,sh=.8+R()*.35;
  if(k<.18)at(px,50,q=>{x.strokeStyle=shade(col,sh*.9);x.lineWidth=3;x.beginPath();x.moveTo(q,by);x.quadraticCurveTo(q+8,by-hh*.6,q+4,by-hh-10);x.stroke();x.lineWidth=2;
   for(let j=0;j<7;j++){const a=-Math.PI*.95+j*(Math.PI*.9/6);x.beginPath();x.moveTo(q+4,by-hh-10);x.quadraticCurveTo(q+4+Math.cos(a)*14,by-hh-16+Math.sin(a)*12,q+4+Math.cos(a)*24,by-hh-2+Math.sin(a)*14);x.stroke()}});
  else if(k<.3)at(px,40,q=>{x.fillStyle=shade(pal.hill,.7);x.fillRect(q,by-16,28,16);x.fillStyle=shade(col,.8);x.beginPath();x.moveTo(q-4,by-16);x.lineTo(q+14,by-30);x.lineTo(q+32,by-16);x.closePath();x.fill();
   if(pal.lamp>.3){x.fillStyle='rgba(255,200,110,.9)';x.fillRect(q+10,by-11,5,6)}});
  else at(px,hh,q=>{x.fillStyle=shade(col,sh*.8);x.fillRect(q-2,by-hh*.45,4,hh*.45);x.fillStyle=shade(col,sh);
   [[0,-hh*.62,hh*.34],[-hh*.2,-hh*.5,hh*.26],[hh*.2,-hh*.5,hh*.27]].forEach(c=>{x.beginPath();x.arc(q+c[0],by+c[1],c[2],0,6.283);x.fill()})})}
 at(w*.52,40,q=>{x.fillStyle=shade(pal.hill,.6);x.fillRect(q,by-56,3,56);x.fillRect(q+22,by-56,3,56);x.beginPath();x.ellipse(q+12,by-62,17,10,0,0,6.283);x.fill()})}
function fields(x,w,h){const R=rng(5);let y=0;while(y<h){const bh=4+(y/h)*34;let xx=0;while(xx<w){const pw=(40+R()*120)*(1+y/h*1.6);x.fillStyle=shade(R()<.5?pal.fld:pal.fld2,.82+R()*.4);x.fillRect(xx,y,pw+1,bh+1);xx+=pw}y+=bh}
 const hz=x.createLinearGradient(0,0,0,h*.4);hz.addColorStop(0,rgba(pal.hor,.6));hz.addColorStop(1,rgba(pal.hor,0));x.fillStyle=hz;x.fillRect(0,0,w,h*.4)}
function foreground(x,w,h){const gr=x.createLinearGradient(0,0,0,h);gr.addColorStop(0,shade(pal.fld2,.55));gr.addColorStop(1,shade(pal.gr,.7));x.fillStyle=gr;x.fillRect(0,0,w,h);
 const R=rng(31);for(let i=0;i<150;i++){const px=R()*w,py=R()*h*.9+4,hh=7+R()*18;x.strokeStyle=shade(pal.fld,.5+R()*.4);x.lineWidth=1.6;x.beginPath();x.moveTo(px,py+hh);x.lineTo(px-3,py);x.moveTo(px,py+hh);x.lineTo(px+1,py-2);x.moveTo(px,py+hh);x.lineTo(px+4,py+1);x.stroke()}
 for(let i=0;i<7;i++){const px=R()*w,py=h*.5+R()*h*.4,rad=10+R()*14;x.fillStyle=shade(pal.tree,.8+R()*.3);x.beginPath();x.arc(px,py,rad,Math.PI,0);x.fill()}}
function build(){pal=curPal();A=clamp(pal.amb,.4,1);TW=Math.max(1500,Math.round(W*1.35));
 T.mtn=tile(HZ-160,170,(x,w,h)=>{const gr=x.createLinearGradient(0,20,0,h);gr.addColorStop(0,pal.mtn);gr.addColorStop(1,mixHex(pal.mtn,pal.hor,.6));ridge(x,w,h,11,26,h-70,[2,3,5],gr)});
 T.hill=tile(HZ-100,120,(x,w,h)=>{const gr=x.createLinearGradient(0,30,0,h);gr.addColorStop(0,pal.hill);gr.addColorStop(1,mixHex(pal.hill,pal.hor,.35));ridge(x,w,h,23,16,h-42,[3,4,7],gr)});
 T.tree=tile(HZ-70,100,trees);T.field=tile(HZ,RAIL-HZ+6,fields);T.fg=tile(RAIL+16,H-RAIL-16,foreground);S.lastPal=S.t}
function layout(){const r=fitCanvas(cv);g=r.g;W=r.w;H=r.h;DPR=r.dpr;HZ=H*.54;RAIL=H*.80;U=clamp(W/5.4,150,250);CH=U*.27;LW=U*1.06;wireY=RAIL-CH*1.78;
 const R=rng(9);STARS=[];for(let i=0;i<140;i++)STARS.push({x:R(),y:R(),r:R()<.15?2:1,f:1+R()*3,p:R()*6,a:.4+R()*.6});
 CLOUDS=[];for(let i=0;i<7;i++)CLOUDS.push({x:R()*W*1.5,y:HZ*(.08+R()*.5),s:.6+R()*1.0,sp:5+R()*9,o:[0,.9,1.8,-.9,.4].map(v=>v+R()*.3)});
 S.rain=[];for(let i=0;i<clamp(W/4,120,340);i++)S.rain.push({x:R()*W,y:R()*H,l:8+R()*12,v:650+R()*250});build()}

/* ---------- sky ---------- */
function drawSky(){const gr=g.createLinearGradient(0,0,0,HZ+12);gr.addColorStop(0,pal.top);gr.addColorStop(.55,pal.mid);gr.addColorStop(1,pal.hor);g.fillStyle=gr;g.fillRect(0,0,W,HZ+14);
 if(pal.stars>.02)STARS.forEach(s=>{g.fillStyle='rgba(255,255,255,'+(pal.stars*s.a*(.55+.45*Math.sin(S.t*s.f+s.p))).toFixed(3)+')';g.fillRect(s.x*W,s.y*HZ*.92,s.r,s.r)});
 const hr=S.time==='auto'?hourIST():({dawn:6.5,day:12,dusk:18.2,night:23}[S.time]);
 if(hr>5.9&&hr<19){const f=clamp((hr-6)/13,0,1),x=W*(.08+.84*f),y=HZ-Math.sin(f*Math.PI)*HZ*.8+8,k=Math.sin(f*Math.PI),col=mixHex('#FF8A3D','#FFF1B8',Math.pow(k,.5));
  const gl=g.createRadialGradient(x,y,4,x,y,150);gl.addColorStop(0,rgba(col,.55*(S.weather==='clear'?1:.4)));gl.addColorStop(1,rgba(col,0));g.fillStyle=gl;g.fillRect(x-150,y-150,300,300);
  g.fillStyle=col;g.beginPath();g.arc(x,y,17,0,6.283);g.fill()}
 else{const h2=hr<12?hr+24:hr,f=clamp((h2-18.8)/10.6,0,1),x=W*(.1+.8*f),y=HZ-Math.sin(f*Math.PI)*HZ*.75+10;
  const gl=g.createRadialGradient(x,y,3,x,y,90);gl.addColorStop(0,'rgba(200,220,255,.35)');gl.addColorStop(1,'rgba(200,220,255,0)');g.fillStyle=gl;g.fillRect(x-90,y-90,180,180);
  g.fillStyle='#E9EEF8';g.beginPath();g.arc(x,y,14,0,6.283);g.fill();g.fillStyle='rgba(150,165,195,.45)';[[-4,-3,3.2],[4,2,2.6],[-2,6,2]].forEach(c=>{g.beginPath();g.arc(x+c[0],y+c[1],c[2],0,6.283);g.fill()})}}
function drawClouds(dt){const col=mixHex(pal.mid,'#FFFFFF',pal.amb*.55);g.fillStyle=col;
 CLOUDS.forEach(c=>{c.x-=(c.sp+V*.02)*dt;if(c.x<-160)c.x=W+160;g.globalAlpha=.25+pal.amb*.4;
  c.o.forEach((o,i)=>{g.beginPath();g.ellipse(c.x+o*38*c.s,c.y+(i%2)*5*c.s,34*c.s,15*c.s,0,0,6.283);g.fill()})});g.globalAlpha=1}
function drawBirds(dt){if(pal.amb>.85&&S.weather==='clear'){S.bT-=dt;if(S.bT<=0){S.bT=13+Math.random()*10;const n=4+(Math.random()*3|0),y=HZ*(.2+Math.random()*.3);for(let i=0;i<n;i++)S.birds.push({x:W+30+i*26,y:y+(i%2?1:-1)*i*7,v:50+Math.random()*20,p:Math.random()*6})}}
 g.strokeStyle='rgba(30,40,60,.75)';g.lineWidth=1.4;S.birds=S.birds.filter(b=>b.x>-30);S.birds.forEach(b=>{b.x-=b.v*dt;const f=Math.sin(S.t*9+b.p)*3.5;g.beginPath();g.moveTo(b.x-7,b.y+f);g.quadraticCurveTo(b.x-3,b.y-3,b.x,b.y);g.quadraticCurveTo(b.x+3,b.y-3,b.x+7,b.y+f);g.stroke()})}
function turbines(){const sp=520,off=S.off*.08;g.strokeStyle=shade('#E8EDF5',A*.8);g.fillStyle=g.strokeStyle;
 for(let x=-(off%sp)+60;x<W+60;x+=sp){const k=Math.floor((x+off)/sp),hh=64+(k*37%24),by=HZ+2;g.lineWidth=2.4;g.beginPath();g.moveTo(x,by);g.lineTo(x,by-hh);g.stroke();
  g.lineWidth=1.6;for(let j=0;j<3;j++){const a=S.t*.9+j*2.094+k;g.beginPath();g.moveTo(x,by-hh);g.lineTo(x+Math.cos(a)*30,by-hh+Math.sin(a)*30);g.stroke()}g.beginPath();g.arc(x,by-hh,2.4,0,6.283);g.fill()}}
function pylons(){const sp=760,off=S.off*.16,col=shade('#394659',A*.9);g.strokeStyle=col;let prev=null;
 for(let x=-(off%sp)-60;x<W+sp;x+=sp){const by=HZ+14,hh=86;g.lineWidth=1.4;g.beginPath();g.moveTo(x-14,by);g.lineTo(x,by-hh);g.lineTo(x+14,by);g.moveTo(x-9,by-30);g.lineTo(x+9,by-30);g.moveTo(x-6,by-52);g.lineTo(x+6,by-52);g.moveTo(x-22,by-hh+8);g.lineTo(x+22,by-hh+8);g.stroke();
  if(prev!==null){[-22,0,22].forEach(dx=>{g.beginPath();g.moveTo(prev+dx,by-hh+8);g.quadraticCurveTo((prev+x)/2+dx,by-hh+30,x+dx,by-hh+8);g.stroke()})}prev=x}}

/* ---------- track level ---------- */
function track(){const gr=g.createLinearGradient(0,RAIL,0,RAIL+18);gr.addColorStop(0,shade('#7a7f88',A));gr.addColorStop(1,shade('#2f333a',A));g.fillStyle=gr;g.fillRect(0,RAIL+1,W,17);
 g.fillStyle=shade('#4a3b2e',A);const sp=26,so=S.off%sp;for(let x=-so;x<W;x+=sp)g.fillRect(x,RAIL+2,14,7)}
function rails(){g.fillStyle=shade('#8a94a3',A);g.fillRect(0,RAIL-1,W,3);g.fillStyle='rgba(255,255,255,.35)';g.fillRect(0,RAIL-1,W,1)}
function ohe(){if(P.loco==='wdm'){const sp=300,so=S.off%sp;g.strokeStyle=shade('#5a4a3a',A);g.lineWidth=3;for(let x=-so;x<W+sp;x+=sp){g.beginPath();g.moveTo(x,RAIL);g.lineTo(x,RAIL-CH*2.5);g.moveTo(x-16,RAIL-CH*2.3);g.lineTo(x+16,RAIL-CH*2.3);g.stroke()}
  g.lineWidth=1;g.strokeStyle='rgba(30,30,40,.7)';g.beginPath();g.moveTo(0,RAIL-CH*2.3+2);g.lineTo(W,RAIL-CH*2.3+2);g.stroke();return}
 const sp=250,so=S.off%sp,col=shade('#58667a',A);let px=null;
 for(let x=-so;x<W+sp;x+=sp){g.strokeStyle=col;g.lineWidth=3;g.beginPath();g.moveTo(x,RAIL-4);g.lineTo(x,wireY-26);g.stroke();g.lineWidth=2;g.beginPath();g.moveTo(x,wireY-18);g.lineTo(x-30,wireY-8);g.moveTo(x,wireY-26);g.lineTo(x-30,wireY-12);g.stroke();
  if(px!==null){g.strokeStyle=shade('#93a0b4',A);g.lineWidth=1;g.beginPath();g.moveTo(px-30,wireY-12);g.quadraticCurveTo((px+x)/2-30,wireY+4,x-30,wireY-12);g.stroke();
   for(let k=1;k<4;k++){const tt=k/4,mx=lerp(px-30,x-30,tt),my=lerp(wireY-12,wireY-12,tt)+4*Math.sin(tt*Math.PI)*1.0;g.beginPath();g.moveTo(mx,my);g.lineTo(mx,wireY);g.stroke()}}px=x}
 g.strokeStyle=shade('#b6c0d0',A);g.lineWidth=1.4;g.beginPath();g.moveTo(0,wireY);g.lineTo(W,wireY);g.stroke()}
function signals(){const sp=1500,so=(S.off*1)%sp;for(let x=W*.18-so+sp;x<W+sp;x+=sp){const k=Math.floor((x+S.off)/sp),on=k%3===0?'y':'g';g.strokeStyle=shade('#4b5563',A);g.lineWidth=3;g.beginPath();g.moveTo(x,RAIL-2);g.lineTo(x,RAIL-CH*1.7);g.stroke();
  g.fillStyle='#0b0f18';rr(g,x-9,RAIL-CH*1.7-38,18,40,5);g.fill();[['#FF5A5F',0],['#FFC83D',1],['#34D399',2]].forEach(c=>{const lit=(on==='g'&&c[1]===2)||(on==='y'&&c[1]===1);g.fillStyle=lit?c[0]:'#1c2230';g.beginPath();g.arc(x,RAIL-CH*1.7-28+c[1]*12,4,0,6.283);g.fill();
   if(lit&&A<.9){g.fillStyle=rgba(c[0],.28);g.beginPath();g.arc(x,RAIL-CH*1.7-28+c[1]*12,12,0,6.283);g.fill()}})}}

/* ---------- events: station canopy, level crossing ---------- */
/* ---------- events: station canopy, level crossing ---------- */
function evBack(sx,e){const L_=e.len;if(e.type==='st'){const cy=RAIL-CH*2.15;
  g.fillStyle=shade('#2c3442',A);g.fillRect(sx,cy,L_,8);g.fillStyle=shade('#1c222d',A);g.fillRect(sx,cy+8,L_,4);
  for(let x=sx+30;x<sx+L_;x+=130){g.fillStyle=shade('#3a4455',A);g.fillRect(x,cy+12,6,CH*1.45);if(A<.9){g.fillStyle='rgba(255,236,170,.95)';g.fillRect(x-24,cy+14,54,3);const lg=g.createLinearGradient(0,cy+14,0,cy+CH*1.1);lg.addColorStop(0,'rgba(255,226,150,.22)');lg.addColorStop(1,'rgba(255,226,150,0)');g.fillStyle=lg;g.fillRect(x-30,cy+14,66,CH)}}
  const fx=sx+L_*.16;g.fillStyle=shade('#4a5568',A);g.fillRect(fx,cy-CH*.55,L_*.18,9);g.fillRect(fx,cy-CH*.55-24,L_*.18,3);g.fillRect(fx+L_*.18-5,cy-CH*.55,5,CH*.55+10);g.fillRect(fx,cy-CH*.55,5,CH*.55+10);
  for(let x=fx+8;x<fx+L_*.18;x+=18){g.fillRect(x,cy-CH*.55-24,2,24)}
  const bx=sx+L_*.5-CH*1.9,by=cy+16,bw=CH*3.8,bh=CH*.95;g.strokeStyle=shade('#6b7280',A);g.lineWidth=2;g.beginPath();g.moveTo(bx+bw*.2,cy+12);g.lineTo(bx+bw*.2,by);g.moveTo(bx+bw*.8,cy+12);g.lineTo(bx+bw*.8,by);g.stroke();
  g.fillStyle=shade('#FFD21F',Math.max(A,.8));rr(g,bx,by,bw,bh,5);g.fill();g.strokeStyle='#14110A';g.lineWidth=2.4;rr(g,bx+2,by+2,bw-4,bh-4,4);g.stroke();g.fillStyle='#14110A';g.textAlign='center';
  g.font='700 '+(bh*.44)+'px Rajdhani,sans-serif';g.fillText(e.n[0],bx+bw/2,by+bh*.50);g.font='600 '+(bh*.28)+'px Rajdhani,Hind,sans-serif';g.fillText(e.n[1]+'   '+e.n[2],bx+bw/2,by+bh*.84);g.textAlign='left'}
 else if(e.type==='lc'){const x0=sx+L_/2;g.fillStyle=shade('#59606b',A);g.beginPath();g.moveTo(x0-16,HZ+8);g.lineTo(x0+16,HZ+8);g.lineTo(x0+60,RAIL);g.lineTo(x0-60,RAIL);g.closePath();g.fill();
  g.fillStyle=shade('#6b4a36',A);g.fillRect(x0+84,RAIL-CH*.9,CH*.9,CH*.9);g.fillStyle=shade('#3a2a20',A);g.beginPath();g.moveTo(x0+80,RAIL-CH*.9);g.lineTo(x0+84+CH*.45,RAIL-CH*1.25);g.lineTo(x0+88+CH*.9,RAIL-CH*.9);g.closePath();g.fill();
  const wx=sx-440;g.strokeStyle=shade('#6b7280',A);g.lineWidth=3;g.beginPath();g.moveTo(wx,RAIL);g.lineTo(wx,RAIL-CH*1.25);g.stroke();g.fillStyle='#F8FAFC';rr(g,wx-17,RAIL-CH*1.25-24,34,26,3);g.fill();g.fillStyle='#0b0f18';g.font='700 15px Rajdhani,sans-serif';g.textAlign='center';g.fillText('W/L',wx,RAIL-CH*1.25-5);g.textAlign='left';
  if(!e.w1&&wx<W*.7&&wx>0){e.w1=true;if(RailAudio.isOn())RailAudio.horn(P.loco)}}}
function evFront(sx,e){if(e.type==='br'){evBrFront(sx,e);return}if(e.type!=='lc')return;const x0=sx+e.len/2,bl=Math.floor(S.t*2)%2===0;g.fillStyle=shade('#4b525c',A);g.beginPath();g.moveTo(x0-60,RAIL+16);g.lineTo(x0+60,RAIL+16);g.lineTo(x0+130,H);g.lineTo(x0-130,H);g.closePath();g.fill();
 g.strokeStyle='rgba(255,255,255,.55)';g.lineWidth=2;g.setLineDash([12,10]);g.beginPath();g.moveTo(x0,RAIL+18);g.lineTo(x0,H);g.stroke();g.setLineDash([]);
 [[x0-84,0],[x0+84,1]].forEach(p=>{g.strokeStyle=shade('#6b7280',A);g.lineWidth=3;g.beginPath();g.moveTo(p[0],RAIL+14);g.lineTo(p[0],RAIL-CH*.95);g.stroke();g.fillStyle='#F8FAFC';g.save();g.translate(p[0],RAIL-CH*1.1);g.rotate(.785);g.fillRect(-14,-3,28,6);g.rotate(-1.57);g.fillRect(-14,-3,28,6);g.restore();
  const on=(p[1]===0)===bl;[-9,9].forEach(dx=>{g.fillStyle=on?'#FF5A5F':'#3a1215';g.beginPath();g.arc(p[0]+dx,RAIL-CH*.85,5,0,6.283);g.fill();if(on){g.fillStyle='rgba(255,90,95,.3)';g.beginPath();g.arc(p[0]+dx,RAIL-CH*.85,16,0,6.283);g.fill()}})});
 if(x0>-40&&x0<W+40)RailAudio.bell();return true}
const SEQ=['st','tn','lc','br','st','lc'],XF=()=>W*.86;
const base=()=>Math.max(S.off+W+560,S.events.reduce((m,e)=>Math.max(m,e.x+e.len+330),0));
function spawnEv(t){const x=base();if(t==='st'){const n=NAMES[(Math.random()*NAMES.length)|0];S.events.push({type:'st',x,len:1150,n,stopX:x+1150*.6})}
 else if(t==='lc')S.events.push({type:'lc',x:x+440,len:260,w1:false});else if(t==='tn')S.events.push({type:'tn',x,len:1000,no:1+((Math.random()*40)|0),w1:false});else S.events.push({type:'br',x,len:820})}
function spawn(){spawnEv(SEQ[S.evN++%SEQ.length])}
function events(dt){S.evT-=dt;if(S.evT<=0){spawn();S.evT=8+Math.random()*5}
 if(S.wantStop&&!S.events.some(e=>e.type==='st'&&e.stopX-(S.off+XF())>S.v*S.v/380+140))spawnEv('st');S.events=S.events.filter(e=>e.x-S.off+e.len>-700)}
/* tunnel: a dark cut-away with a hill above it, lamps and a stone portal at each end */
function evTun(sx,e){const L_=e.len,top=wireY-46;const hg=g.createLinearGradient(0,top-215,0,top);hg.addColorStop(0,shade(pal.hill,.8));hg.addColorStop(1,shade(pal.hill,.5));g.fillStyle=hg;
 g.beginPath();g.moveTo(sx-120,top+8);g.quadraticCurveTo(sx+L_*.2,top-220,sx+L_*.5,top-225);g.quadraticCurveTo(sx+L_*.8,top-220,sx+L_+120,top+8);g.closePath();g.fill();
 const ig=g.createLinearGradient(0,top,0,RAIL+16);ig.addColorStop(0,'#03050a');ig.addColorStop(1,'#10151f');g.fillStyle=ig;g.fillRect(sx,top,L_,RAIL+16-top);
 for(let x=sx+90;x<sx+L_-50;x+=150){g.fillStyle='rgba(255,196,110,.95)';g.fillRect(x-14,top+14,28,4);const lg=g.createRadialGradient(x,top+18,2,x,top+18,100);lg.addColorStop(0,'rgba(255,190,100,.32)');lg.addColorStop(1,'rgba(255,190,100,0)');g.fillStyle=lg;g.fillRect(x-100,top,200,170)}
 g.strokeStyle='rgba(130,140,160,.28)';g.lineWidth=2;g.beginPath();g.moveTo(sx,top+52);g.lineTo(sx+L_,top+52);g.moveTo(sx,RAIL-12);g.lineTo(sx+L_,RAIL-12);g.stroke();
 g.strokeStyle=shade('#b6c0d0',A*.8);g.lineWidth=1.4;g.beginPath();g.moveTo(sx,wireY);g.lineTo(sx+L_,wireY);g.stroke();
 [sx-6,sx+L_-8].forEach(px=>{g.fillStyle=shade('#6b6f78',A);g.fillRect(px,top-10,14,RAIL+26-top);g.fillStyle='rgba(0,0,0,.35)';for(let y=top;y<RAIL+16;y+=16)g.fillRect(px,y,14,2)});
 g.fillStyle='#F8FAFC';rr(g,sx-2,top-38,98,24,3);g.fill();g.fillStyle='#0b0f18';g.font='700 13px Rajdhani,sans-serif';g.fillText('TUNNEL No. '+e.no,sx+6,top-21)}
/* river bridge: water, piers, and a steel truss that flickers across the train windows */
function evBrBack(sx,e){const L_=e.len,x0=sx+L_/2,wg=g.createLinearGradient(0,HZ,0,RAIL);wg.addColorStop(0,mixHex(pal.hor,'#5aa0d8',.5));wg.addColorStop(1,shade('#2d6fa8',A));g.fillStyle=wg;
 g.beginPath();g.moveTo(x0-34,HZ+2);g.lineTo(x0+34,HZ+2);g.lineTo(x0+L_*.46,RAIL+14);g.lineTo(x0-L_*.46,RAIL+14);g.closePath();g.fill();g.fillStyle=shade('#3b4452',A);g.fillRect(sx,RAIL+6,L_,12)}
function evBrFront(sx,e){const L_=e.len,top=RAIL-CH*1.52,fg=g.createLinearGradient(0,RAIL+16,0,H);fg.addColorStop(0,shade('#2a6ea8',A));fg.addColorStop(1,shade('#123a63',A));g.fillStyle=fg;
 g.beginPath();g.moveTo(sx+L_*.06,RAIL+16);g.lineTo(sx+L_*.94,RAIL+16);g.lineTo(sx+L_*1.08,H);g.lineTo(sx-L_*.08,H);g.closePath();g.fill();
 g.strokeStyle='rgba(255,255,255,.2)';g.lineWidth=1.2;for(let k=0;k<7;k++){const y=RAIL+30+k*((H-RAIL-30)/7),o=(S.t*22+k*37)%80;g.beginPath();for(let x=sx+L_*.1-o;x<sx+L_*.9;x+=80){g.moveTo(x,y);g.quadraticCurveTo(x+20,y-3,x+40,y)}g.stroke()}
 [.18,.5,.82].forEach(f=>{const px=sx+L_*f;g.fillStyle=shade('#8a8f98',A);g.fillRect(px-12,RAIL+16,24,H-RAIL-16);g.fillStyle='rgba(0,0,0,.25)';g.fillRect(px+4,RAIL+16,8,H-RAIL-16)});
 g.strokeStyle=shade('#4a5260',A);g.lineWidth=4;g.beginPath();g.moveTo(sx,top);g.lineTo(sx+L_,top);g.moveTo(sx,RAIL+5);g.lineTo(sx+L_,RAIL+5);g.stroke();
 g.lineWidth=3;const n=Math.floor(L_/64);g.beginPath();for(let i=0;i<=n;i++){const x=sx+i*L_/n;g.moveTo(x,top);g.lineTo(x,RAIL+5);if(i<n){const x2=sx+(i+1)*L_/n;if(i%2===0){g.moveTo(x,top);g.lineTo(x2,RAIL+5)}else{g.moveTo(x,RAIL+5);g.lineTo(x2,top)}}}g.stroke()}
/* a distant freight train on the far line, running the opposite way */
function freight(dt){S.frT-=dt;if(S.frT<=0){S.frT=24+Math.random()*14;const n=10+(Math.random()*8|0),cl=['#7a4a2a','#3d5a80','#8a8f98','#5a3a2a','#2f6f4f'];S.fr.push({x:W+40,n,col:Array.from({length:n},()=>cl[(Math.random()*5)|0])})}
 S.fr=S.fr.filter(f=>f.x>-f.n*30-80);S.fr.forEach(f=>{f.x-=(60+V*.35)*dt;const y=HZ+44,w=26,h=13;g.fillStyle='rgba(20,20,26,.75)';g.fillRect(f.x-22,y,f.n*(w+2)+34,2);g.fillStyle=shade('#2a2f38',A);g.fillRect(f.x-20,y-14,24,14);g.fillStyle=shade('#d0a020',A);g.fillRect(f.x-20,y-14,24,3);
  for(let i=0;i<f.n;i++){const x=f.x+8+i*(w+2);g.fillStyle=shade(f.col[i],A);g.fillRect(x,y-h,w,h);g.fillStyle='#0d1016';g.fillRect(x+3,y,4,2);g.fillRect(x+w-7,y,4,2)}})}
/* ---------- train ---------- */
function wheel(x,y,r,ang){g.fillStyle='#12151b';g.beginPath();g.arc(x,y,r,0,6.283);g.fill();g.strokeStyle='#9aa4b2';g.lineWidth=Math.max(1,r*.16);g.beginPath();g.arc(x,y,r*.82,0,6.283);g.stroke();
 const sa=clamp(1-V/430,.12,1);g.strokeStyle='rgba(120,130,145,'+sa+')';g.lineWidth=1;for(let i=0;i<6;i++){const a=ang+i*1.0472;g.beginPath();g.moveTo(x,y);g.lineTo(x+Math.cos(a)*r*.8,y+Math.sin(a)*r*.8);g.stroke()}
 g.fillStyle='#cbd5e1';g.beginPath();g.arc(x,y,r*.18,0,6.283);g.fill()}
function wheels(x,w,bb,pairs){const r=CH*.15,cy=RAIL-r-1,ang=S.off/r;g.fillStyle='#0d1016';pairs.forEach(p=>{g.fillRect(x+w*p[0]-r*.4,bb,w*(p[p.length-1]-p[0])+r*.8,CH*.1);for(const q of p)wheel(x+w*q,cy,r,ang)})}
function beam(xn,yn){const I=clamp(1.1-pal.amb,0,1)+(S.weather!=='clear'?.3:0)+S.tun*.8;g.globalCompositeOperation='lighter';
 if(I>.1){const gr=g.createLinearGradient(xn,0,xn+W*.42,0);gr.addColorStop(0,'rgba(255,240,200,'+(.5*I)+')');gr.addColorStop(1,'rgba(255,240,200,0)');g.fillStyle=gr;g.beginPath();g.moveTo(xn,yn-2);g.lineTo(xn+W*.42,yn-CH*.8);g.lineTo(xn+W*.42,yn+CH*.9);g.lineTo(xn,yn+3);g.closePath();g.fill()}
 const bl=g.createRadialGradient(xn,yn,1,xn,yn,CH*(.3+I*.7));bl.addColorStop(0,'rgba(255,248,220,'+(.5+.5*I)+')');bl.addColorStop(1,'rgba(255,248,220,0)');g.fillStyle=bl;g.fillRect(xn-CH,yn-CH,CH*2,CH*2);g.globalCompositeOperation='source-over'}
function panto(px,roofY,dt){g.strokeStyle=shade('#8b95a5',A);g.lineWidth=2;const kx=px+CH*.1,ky=roofY-(roofY-wireY)*.52;g.beginPath();g.moveTo(px-CH*.16,roofY);g.lineTo(kx,ky);g.lineTo(px-CH*.02,wireY);g.moveTo(px+CH*.12,roofY);g.lineTo(kx,ky);g.stroke();
 g.fillStyle='#d1d5db';g.fillRect(px-CH*.12,wireY-2,CH*.2,3);g.fillStyle=shade('#e5e7eb',A);g.fillRect(px-CH*.2,roofY-4,CH*.4,4);
 if((A<.85||S.weather!=='clear')&&Math.random()<.3)S.sparks.push({x:px-CH*.02,y:wireY,vx:-60-Math.random()*120,vy:-30+Math.random()*90,l:.3})}
function locoAero(x,dt){const w=LW,bb=RAIL-CH*.2,y0=bb-CH,p=new Path2D();p.moveTo(x,bb);p.lineTo(x,y0+CH*.08);p.quadraticCurveTo(x,y0,x+CH*.12,y0);p.lineTo(x+w*.56,y0);p.bezierCurveTo(x+w*.8,y0,x+w*.96,y0+CH*.46,x+w,y0+CH*.7);p.lineTo(x+w,bb);p.closePath();
 const gr=g.createLinearGradient(0,y0,0,bb);gr.addColorStop(0,shade('#F4F7FC',A*1.05));gr.addColorStop(1,shade('#B4BFD0',A));g.fillStyle=gr;g.fill(p);g.save();g.clip(p);g.fillStyle=shade('#1D4ED8',A);g.fillRect(x,y0+CH*.64,w,CH*.14);g.fillStyle=shade('#FB792B',A);g.fillRect(x,y0+CH*.8,w,CH*.04);g.restore();
 g.fillStyle='#0B1220';g.beginPath();g.moveTo(x+w*.6,y0+CH*.1);g.bezierCurveTo(x+w*.8,y0+CH*.12,x+w*.92,y0+CH*.36,x+w*.975,y0+CH*.56);g.lineTo(x+w*.8,y0+CH*.56);g.lineTo(x+w*.6,y0+CH*.4);g.closePath();g.fill();
 g.strokeStyle='rgba(255,255,255,.25)';g.lineWidth=1;g.beginPath();g.moveTo(x+w*.64,y0+CH*.16);g.lineTo(x+w*.84,y0+CH*.2);g.stroke();
 g.fillStyle=shade('#13203C',A);for(let i=0;i<4;i++)rr(g,x+w*(.12+i*.1),y0+CH*.2,w*.07,CH*.26,3),g.fill();
 g.fillStyle=shade('#1D4ED8',A);g.font='700 '+(CH*.12)+'px Rajdhani,sans-serif';g.fillText('SUPERFAST',x+w*.14,y0+CH*.58);panto(x+w*.34,y0,dt);wheels(x,w,bb,[[.12,.2],[.74,.82]]);beam(x+w-2,y0+CH*.66)}
function locoWap(x,dt){const w=LW,bb=RAIL-CH*.2,y0=bb-CH,p=new Path2D();p.moveTo(x,bb);p.lineTo(x,y0+CH*.04);p.lineTo(x+w*.8,y0);p.lineTo(x+w*.93,y0+CH*.2);p.lineTo(x+w,y0+CH*.3);p.lineTo(x+w,bb);p.closePath();
 const gr=g.createLinearGradient(0,y0,0,bb);gr.addColorStop(0,shade('#D3DAE5',A));gr.addColorStop(.5,shade('#A9B4C4',A));gr.addColorStop(1,shade('#2147A8',A));g.fillStyle=gr;g.fill(p);
 g.save();g.clip(p);g.fillStyle=shade('#1E4FB5',A);g.fillRect(x,y0+CH*.55,w,CH*.45);g.fillStyle=shade('#FFD21F',A);g.fillRect(x+w*.9,y0,w*.12,CH);g.fillStyle='#14110A';for(let i=0;i<5;i++)g.fillRect(x+w*.9,y0+CH*.2+i*CH*.16,w*.12,CH*.06);g.restore();
 g.strokeStyle=shade('#5B6779',A);g.lineWidth=1.4;for(let i=0;i<10;i++){const lx=x+w*(.12+i*.05);g.beginPath();g.moveTo(lx,y0+CH*.16);g.lineTo(lx,y0+CH*.46);g.stroke()}
 g.fillStyle='#0B1220';g.beginPath();g.moveTo(x+w*.82,y0+CH*.04);g.lineTo(x+w*.92,y0+CH*.22);g.lineTo(x+w*.9,y0+CH*.34);g.lineTo(x+w*.8,y0+CH*.34);g.closePath();g.fill();g.fillRect(x+w*.7,y0+CH*.1,w*.07,CH*.24);
 g.fillStyle='#F8FAFC';g.font='700 '+(CH*.13)+'px Rajdhani,sans-serif';g.fillText('WAP-7',x+w*.1,y0+CH*.82);panto(x+w*.3,y0,dt);panto(x+w*.6,y0,dt);wheels(x,w,bb,[[.1,.17,.24],[.66,.73,.8]]);beam(x+w-2,y0+CH*.42)}
function locoWdm(x,dt){const w=LW,bb=RAIL-CH*.2,y0=bb-CH,p=new Path2D();p.moveTo(x,bb);p.lineTo(x,y0);p.lineTo(x+w*.3,y0);p.lineTo(x+w*.3,y0+CH*.24);p.lineTo(x+w*.96,y0+CH*.24);p.lineTo(x+w,y0+CH*.34);p.lineTo(x+w,bb);p.closePath();
 const gr=g.createLinearGradient(0,y0,0,bb);gr.addColorStop(0,shade('#2F7A4C',A));gr.addColorStop(1,shade('#173B27',A));g.fillStyle=gr;g.fill(p);g.save();g.clip(p);g.fillStyle=shade('#F2C230',A);g.fillRect(x,y0+CH*.62,w,CH*.1);g.restore();
 g.fillStyle='#0B1220';rr(g,x+w*.04,y0+CH*.14,w*.09,CH*.3,3);g.fill();rr(g,x+w*.16,y0+CH*.14,w*.09,CH*.3,3);g.fill();
 g.strokeStyle=shade('#0f2a1b',A);g.lineWidth=1.4;for(let i=0;i<9;i++){const lx=x+w*(.36+i*.06);g.beginPath();g.moveTo(lx,y0+CH*.32);g.lineTo(lx,y0+CH*.54);g.stroke()}
 g.fillStyle=shade('#10161d',A);g.fillRect(x+w*.62,y0+CH*.06,CH*.1,CH*.2);g.beginPath();g.ellipse(x+w*.48,y0+CH*.22,CH*.2,CH*.05,0,0,6.283);g.fill();
 g.fillStyle=shade('#111827',A);rr(g,x+w*.9,y0+CH*.12,CH*.18,CH*.13,2);g.fill();
 if(Math.random()<dt*22)S.smoke.push({x:x+w*.62+CH*.05,y:y0+CH*.04,vx:-V*.5,vy:-24-Math.random()*14,r:4,l:0,mx:2.1});
 wheels(x,w,bb,[[.1,.17,.24],[.68,.75,.82]]);beam(x+w-2,y0+CH*.18)}
function coach(x,u,idx){const w=U-5,bb=RAIL-CH*.2,bob=Math.sin(S.t*5+idx*1.3)*.5*Math.min(1,V/300),y0=bb-CH+bob;
 const gr=g.createLinearGradient(0,y0,0,y0+CH);gr.addColorStop(0,shade(L.base,1.12*A));gr.addColorStop(.55,shade(L.base,A));gr.addColorStop(1,shade(L.base,.7*A));g.fillStyle=gr;rr(g,x,y0,w,CH,CH*.1);g.fill();
 g.fillStyle=shade(L.roof,A);rr(g,x+2,y0,w-4,CH*.09,[CH*.09,CH*.09,0,0]);g.fill();
 if(u.k!=='GEN'&&u.k!=='GRD'&&u.k!=='SL'){g.fillStyle=shade('#9aa4b2',A);rr(g,x+w*.28,y0-CH*.05,w*.14,CH*.07,2);g.fill();rr(g,x+w*.58,y0-CH*.05,w*.14,CH*.07,2);g.fill()}
 g.fillStyle=u.c;g.fillRect(x+3,y0+CH*.13,w-6,CH*.045);g.fillStyle=shade(L.low,A);g.fillRect(x+3,y0+CH*.74,w-6,CH*.055);
 const n=u.k==='GEN'?8:u.k==='SL'?9:7,R=rng(idx*977+13),wx0=x+w*.13,ww=w*.74/n,night=A<.85;
 for(let i=0;i<n;i++){const lit=R()>.2,head=R()>.5,wx=wx0+i*ww;if(night&&lit){g.fillStyle='#FFD98A';rr(g,wx+ww*.1,y0+CH*.23,ww*.72,CH*.34,3);g.fill();if(head){g.fillStyle='rgba(40,28,20,.8)';g.beginPath();g.arc(wx+ww*.46,y0+CH*.37,ww*.17,0,6.283);g.fill();g.fillRect(wx+ww*.3,y0+CH*.41,ww*.32,CH*.16)}}
  else{const wg=g.createLinearGradient(0,y0+CH*.23,0,y0+CH*.57);wg.addColorStop(0,shade(mixHex(L.win,pal.mid,.45),1));wg.addColorStop(1,L.win);g.fillStyle=night?shade(L.win,.8):wg;rr(g,wx+ww*.1,y0+CH*.23,ww*.72,CH*.34,3);g.fill()}}
 if(night){g.globalCompositeOperation='lighter';g.fillStyle='rgba(255,180,80,.07)';g.fillRect(x+w*.1,y0+CH*.18,w*.8,CH*.45);g.globalCompositeOperation='source-over'}
 g.fillStyle=shade('#1a1f29',A);g.fillRect(x+w*.015,y0+CH*.22,w*.06,CH*.55);g.fillRect(x+w*.925,y0+CH*.22,w*.06,CH*.55);
 g.fillStyle=u.c;rr(g,x+w*.5-w*.07,y0+CH*.8,w*.14,CH*.15,3);g.fill();g.fillStyle='#fff';g.textAlign='center';g.font='700 '+(CH*.13)+'px Rajdhani,sans-serif';g.fillText(u.l,x+w*.5,y0+CH*.915);
 g.fillStyle='rgba(255,255,255,.55)';g.font='600 '+(CH*.095)+'px Hind,sans-serif';g.fillText(KIND_NAME[u.k]||'',x+w*.5,y0+CH*.67);g.textAlign='left';
 g.fillStyle='#0d1016';g.fillRect(x+4,bb,w-8,CH*.07);wheels(x,w,bb,[[.13,.23],[.77,.87]]);g.fillStyle='#2b2f36';g.fillRect(x+w,bb-CH*.04,6,4)}
function train(dt){const xF=W*.86,lx=xF-LW;g.fillStyle='rgba(0,0,0,.28)';g.fillRect(0,RAIL+1,W,5);
 P.cons.forEach((u,i)=>{const cx=lx-(i+1)*U;if(cx+U>-10&&cx<W)coach(cx,u,i)});(P.loco==='aero'?locoAero:P.loco==='wdm'?locoWdm:locoWap)(lx,dt);
 S.smoke=S.smoke.filter(s=>s.l<s.mx);S.smoke.forEach(s=>{s.l+=dt;s.x+=s.vx*dt;s.y+=s.vy*dt;s.r+=dt*16;const k=s.l/s.mx;g.fillStyle='rgba(52,56,64,'+(.5*(1-k)).toFixed(3)+')';g.beginPath();g.arc(s.x,s.y,s.r,0,6.283);g.fill()});
 g.globalCompositeOperation='lighter';S.sparks=S.sparks.filter(s=>s.l>0);S.sparks.forEach(s=>{s.l-=dt;s.x+=s.vx*dt;s.y+=s.vy*dt;g.fillStyle='rgba(255,240,170,'+clamp(s.l*3,0,1)+')';g.fillRect(s.x,s.y,2.2,2.2)});g.globalCompositeOperation='source-over'}

/* ---------- weather ---------- */
function weather(dt){const w=S.weather;
 if(w==='rain'||w==='storm'){const vx=-(V*.22+90);g.strokeStyle='rgba(195,215,245,.4)';g.lineWidth=1;g.beginPath();S.rain.forEach(r=>{r.y+=r.v*dt;r.x+=vx*dt;if(r.y>H){r.y=-20;r.x=Math.random()*(W+200)}if(r.x<-30)r.x=W+Math.random()*60;g.moveTo(r.x,r.y);g.lineTo(r.x+vx*.022,r.y+r.l)});g.stroke()}
 if(w==='fog'||w==='rain'||w==='storm'){const a=w==='fog'?.5:.2,gr=g.createLinearGradient(0,HZ-70,0,RAIL);gr.addColorStop(0,rgba(pal.hor,0));gr.addColorStop(.6,rgba(pal.hor,a));gr.addColorStop(1,rgba(pal.hor,a*.6));g.fillStyle=gr;g.fillRect(0,HZ-70,W,RAIL-HZ+70);
  if(w==='fog')for(let i=0;i<4;i++){const x=((S.off*(.05+i*.03)+i*400)%(W+400))*-1+W+200-i*130;const rg=g.createRadialGradient(x,RAIL-30-i*22,10,x,RAIL-30-i*22,220);rg.addColorStop(0,rgba(pal.hor,.35));rg.addColorStop(1,rgba(pal.hor,0));g.fillStyle=rg;g.fillRect(x-220,RAIL-260-i*22,440,440)}}
 if(w==='storm'){S.nextBolt-=dt;if(S.nextBolt<=0){S.flash=1;S.nextBolt=4+Math.random()*6;let x=W*(.1+Math.random()*.8),y=0;const pts=[[x,y]];while(y<HZ+10){y+=14+Math.random()*22;x+=(Math.random()-.5)*34;pts.push([x,y])}S.bolt=pts;setTimeout(()=>RailAudio.thunder(),350+Math.random()*700)}
  if(S.flash>0){S.flash=Math.max(0,S.flash-dt*2.6);g.fillStyle='rgba(215,228,255,'+(S.flash*.32)+')';g.fillRect(0,0,W,H);if(S.bolt){g.strokeStyle='rgba(255,255,255,'+S.flash+')';g.lineWidth=2.2;g.beginPath();S.bolt.forEach((p,i)=>i?g.lineTo(p[0],p[1]):g.moveTo(p[0],p[1]));g.stroke()}}}
 const vg=g.createRadialGradient(W/2,H*.55,H*.35,W/2,H*.55,W*.75);vg.addColorStop(0,'rgba(5,9,22,0)');vg.addColorStop(1,'rgba(5,9,22,.5)');g.fillStyle=vg;g.fillRect(0,0,W,H)}

/* ---------- main loop ---------- */
function setStat(t){const q=$('#stat');q.textContent=t;q.style.display=t?'inline-block':'none'}
function physics(dt){const vC0=clamp(60+P.speed*3.4,110,520),vC=vC0*S.mult*(REDUCED?.25:1);let vT=vC;const xf=S.off+XF();S.vc0=vC0;
 if(S.wantStop&&S.mode!==2){const st=S.events.filter(e=>e.type==='st'&&e.stopX-xf>-4).sort((a,b)=>a.stopX-b.stopX)[0];
  if(st){const d=st.stopX-xf;vT=Math.min(vT,Math.sqrt(2*230*Math.max(0,d)));if(S.mode===0||S.mode===3){S.mode=1;RailAudio.brake()}
   if(d<=6&&S.v<40){S.v=0;S.mode=2;S.haltT=4.8;S.wantStop=false;RailAudio.chime(false);setStat('Halted at '+st.n[0]+'. Doors open.')}}else if(S.mode===1)S.mode=0}
 if(S.mode===2){vT=0;S.haltT-=dt;if(S.haltT<=0){S.mode=3;setStat('Departing')}}
 if(S.mode===3&&S.v>vC*.9){S.mode=0;setStat('')}
 S.v+=clamp(vT-S.v,-230*dt,120*dt);V=S.v}
function hud(dt){S.ht=(S.ht||0)-dt;if(S.ht>0)return;S.ht=.25;const kmh=P.speed*S.v/S.vc0;$('#spd').textContent=Math.round(kmh)+' km/h';RailAudio.setSpeed(kmh)}
function frame(dt){S.t+=dt;physics(dt);S.off+=S.v*dt;if(S.time==='auto'&&S.t-S.lastPal>40)build();
 drawSky();drawClouds(dt);drawBirds(dt);blit(T.mtn,.035);blit(T.hill,.08);turbines();pylons();blit(T.tree,.2);blit(T.field,.38);
 freight(dt);events(dt);let lc=false;
 S.events.forEach(e=>{const sx=e.x-S.off;if(e.type==='st'||e.type==='lc')evBack(sx,e);else if(e.type==='br')evBrBack(sx,e)});
 signals();ohe();S.events.forEach(e=>{if(e.type==='tn')evTun(e.x-S.off,e)});track();
 S.events.forEach(e=>{if(e.type==='lc'){const sx=e.x-S.off;g.fillStyle=shade('#6b717b',A);g.fillRect(sx+e.len/2-62,RAIL-1,124,19)}});rails();
 S.tun=0;S.events.forEach(e=>{if(e.type==='tn'){const sx=e.x-S.off;S.tun=Math.max(S.tun,clamp((XF()-sx)/(LW*.5),0,1)*clamp((sx+e.len-(XF()-LW))/(LW*.5),0,1));
  if(!e.w1&&sx>XF()&&sx-XF()<260){e.w1=true;if(RailAudio.isOn())RailAudio.horn(P.loco)}}});
 const A0=A;A=A0*(1-.42*S.tun);train(dt);A=A0;
 RailAudio.reverb(S.tun>.3||S.events.some(e=>e.type==='br'&&e.x-S.off<XF()&&e.x-S.off+e.len>XF()-LW*3));
 blit(T.fg,1.5);S.events.forEach(e=>{if(evFront(e.x-S.off,e))lc=true});if(!lc)RailAudio.stopBell();weather(dt);hud(dt)}

/* ---------- HUD + controls ---------- */
function clock(){const d=new Date();$('#clk').textContent=d.toLocaleTimeString('en-GB',{timeZone:'Asia/Kolkata'});$('#dt').textContent=d.toLocaleDateString('en-GB',{timeZone:'Asia/Kolkata',weekday:'short',day:'2-digit',month:'short',year:'numeric'})+' IST'}
clock();setInterval(clock,1000);
const TIMES=['auto','dawn','day','dusk','night'],WX=['clear','rain','fog','storm'];
function label(){$('#bT').textContent='Time: '+S.time;$('#bW').textContent='Weather: '+S.weather;const on=RailAudio.isOn();$('#bS').textContent=on?'Sound on':'Sound off';$('#bS').classList.toggle('on',on);$('#bF').textContent='Pace x'+S.mult.toFixed(2)}
$('#bT').onclick=()=>{S.time=TIMES[(TIMES.indexOf(S.time)+1)%TIMES.length];build();label()};
$('#bW').onclick=()=>{S.weather=WX[(WX.indexOf(S.weather)+1)%WX.length];build();RailAudio.rain(S.weather==='rain'||S.weather==='storm');label()};
$('#bS').onclick=()=>{if(RailAudio.isOn()){RailAudio.disable()}else{RailAudio.enable();RailAudio.setSpeed(P.speed);RailAudio.rain(S.weather==='rain'||S.weather==='storm');$('#hint').style.display='none'}label()};
$('#bH').onclick=()=>RailAudio.horn(P.loco);
$('#bSl').onclick=()=>{S.mult=clamp(S.mult-.25,.25,1.75);label()};$('#bFa').onclick=()=>{S.mult=clamp(S.mult+.25,.25,1.75);label()};
$('#bSt').onclick=()=>{if(S.mode!==2){S.wantStop=true;setStat('Stopping at the next station')}};
S.v=clamp(60+P.speed*3.4,110,520);S.vc0=S.v;
layout();label();onResize(layout);RailAudio.setSpeed(P.speed);
if(P.sound){RailAudio.enable();setTimeout(()=>{if(RailAudio.state()!=='running'){RailAudio.disable();label();$('#hint').style.display='block'}},900)}
if(P.reveal&&P.sound)setTimeout(()=>RailAudio.horn(P.loco),500);
loop(frame);
"""


def build_consist(a: dict, tier: str) -> list:
    """Coaches behind the loco, in the order a real rake is formed. Each coach: class code, label, colour."""
    plan = [("first_ac", "1A", "H", 1), ("second_ac", "2A", "A", 2), ("third_ac", "3A", "B", 3), ("chair_car", "CC", "C", 2),
            ("sleeper", "SL", "S", 3), ("first_class", "FC", "F", 1)]
    colors = {c[1]: c[3] for c in CLASS_DEF}
    out = []
    for (key, code, pre, n), on in zip(plan, a["c"]):
        if on:
            out += [dict(k=code, l=f"{pre}{i + 1}", c=colors[code]) for i in range(n)]
    gen = 3 if not out else (2 if tier == "Pass" else 1)
    out += [dict(k="GEN", l=f"GS{i + 1}" if i else "GS", c="#64748B") for i in range(gen)]
    out.append(dict(k="GRD", l="SLR", c="#475569"))
    return out[:12]


def render_hero(R: dict, scene: dict, reveal: bool = False) -> None:
    a, tier, meta = R["a"], R["tier"], TIER_META[R["tier"]]
    cons = build_consist(a, tier)
    P = dict(tier=tier, loco=meta["loco"], speed=int(round(min(R["speed"], 200))), cons=cons, time=scene["time"], weather=scene["weather"],
             sound=bool(scene.get("sound")), reveal=bool(reveal))
    logo = logo_uri()
    logo_html = f'<img class="logo" src="{logo}" alt="Indian Railways logo">' if logo else '<div class="logo" style="display:flex;align-items:center;justify-content:center;font-size:28px">🚆</div>'
    ticker = (f"{FACTS['clean']:,} real trains classified into Pass, Exp and SF  |  {FACTS['features']} input features  |  Decision Tree {FACTS['acc']:.2f}% accuracy  |  "
              f"भारतीय रेल के लिए मशीन लर्निंग  |  Active schedule: {a['t']}  |  {TIER_META[tier]['name']} at {R['speed']:.0f} km/h  |  ")
    body = f"""
    <div class="hero">
      <canvas id="cv"></canvas>
      <div class="hud tl">{logo_html}<div class="board"><b>RAILDRISHTI</b><i>रेल दृष्टि</i></div></div>
      <div class="tag">Feed in a schedule. The model decides whether it is a Passenger, an Express or a Superfast, and the train below changes to match.</div>
      <div class="hud tr"><div class="clock" id="clk">--:--:--</div><div class="date" id="dt"></div></div>
      <div class="hint" id="hint">Browser blocked auto-sound. Tap "Sound off" to enable it.</div>
      <div class="hud bl"><span class="pill t" style="color:{meta['color']};border-color:{meta['color']}">{esc(meta['name'])}</span>
        <span class="pill" id="spd">{R['speed']:.0f} km/h</span><span class="pill">{len(cons)} coaches</span><span class="pill" id="stat" style="display:none;background:#FFD21F;color:#14110A"></span><span class="pill">{esc(a['t'])}</span></div>
      <div class="hud br"><button id="bSl">Slower</button><button id="bF" style="pointer-events:none">Pace x1.00</button><button id="bFa">Faster</button><button id="bSt">Stop at next station</button><button id="bT">Time: auto</button><button id="bW">Weather: clear</button><button id="bH">Horn</button><button id="bS">Sound off</button></div>
      <div class="tick"><div>{esc(ticker * 2)}</div></div>
    </div>"""
    js = HERO_JS.replace("__P__", jdump(P))
    iframe(wrap_doc(body, HERO_CSS, js, libs=JS_AUDIO), 442)


# ==============================================================================
# 6. TICKET & INDICATOR BOARD
# ==============================================================================
PA_MODES = ["Hindi + English", "Hindi only", "English only", "Chime only", "Mute"]
INK = dict(SF="#A16207", Exp="#1D4ED8", Pass="#047857")

TICKET_CSS = r"""
body{background:#070D1F;padding:6px 4px 14px;font-family:'Hind',sans-serif}
.tk{position:relative;display:grid;grid-template-columns:1fr 196px;animation:feed 1s cubic-bezier(.2,.8,.2,1);background:linear-gradient(135deg,#FFFDF7,#F4ECD8);color:#0B1530;border-radius:20px;
box-shadow:0 0 0 2px #C9A227,0 0 0 5px rgba(201,162,39,.25),0 28px 70px rgba(255,200,61,.14),0 0 70px rgba(255,200,61,.10);overflow:hidden}
.tk.hit{animation:thud .5s ease}
@keyframes feed{from{opacity:0;transform:translateY(-8%);clip-path:inset(0 0 100% 0)}to{opacity:1;transform:none;clip-path:inset(0)}}
@keyframes thud{0%,100%{transform:translateY(0)}25%{transform:translateY(5px) scale(.998)}55%{transform:translateY(-2px)}}
.main{padding:20px 24px 18px;position:relative}
.stub{padding:20px 18px;border-left:2px dashed #C9B77A;position:relative;display:flex;flex-direction:column;align-items:center;gap:10px;background:rgba(201,162,39,.07);text-align:center}
.stub:before,.stub:after{content:'';position:absolute;left:-13px;width:24px;height:24px;border-radius:50%;background:#070D1F}
.stub:before{top:-12px}.stub:after{bottom:-12px}
.hd{display:flex;align-items:center;gap:12px;padding-bottom:12px;border-bottom:1.5px solid #0B1530}
.hd img,.hd .lg{width:44px;height:44px;object-fit:contain;border-radius:8px;border:1px solid #d8cfae;background:#fff;padding:3px;display:flex;align-items:center;justify-content:center}
.hd h1{font-family:'Rajdhani',sans-serif;font-size:21px;line-height:1.05;font-weight:700}.hd p{font-size:12px;color:#5b6684}
.pnr{margin-left:auto;text-align:right}.pnr small{display:block;font-size:11px;color:#5b6684}.pnr b{font-family:'Rajdhani',sans-serif;font-size:22px;letter-spacing:1.5px}
.rt{display:grid;grid-template-columns:1fr 1.15fr 1fr;gap:10px;align-items:center;padding:16px 0 10px}
.st b{display:block;font-family:'Rajdhani',sans-serif;font-size:22px;line-height:1.05;font-weight:700}.st span{font-size:12px;color:#5b6684}
.st .tm{font-family:'Rajdhani',sans-serif;font-size:22px;font-weight:600;margin-top:4px;color:#0B1530}.st.r{text-align:right}
.way{position:relative;height:54px;text-align:center}
.way .ln{position:absolute;left:0;right:0;top:20px;border-top:2.5px dotted #8f98b3}
.way .tn{position:absolute;top:-2px;left:0;font-size:22px;animation:go 4s linear infinite}
@keyframes go{from{left:0}to{left:calc(100% - 26px)}}
.way .mid{position:absolute;left:0;right:0;top:32px;font-size:12px;color:#33405f;font-weight:600}
.cls{display:inline-block;min-width:38px;text-align:center;padding:3px 8px;margin-right:6px;border-radius:7px;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:15px;
border:1.5px solid #cfc7ac;color:#b3ab90}.cls.on{color:#fff;border-color:var(--c);background:var(--c)}
.mg{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:10px 0 4px;padding:10px 12px;background:rgba(11,21,48,.045);border-radius:12px}
.mg span{display:block;font-size:11px;color:#5b6684}.mg b{font-family:'Rajdhani',sans-serif;font-size:17px}
.vd{position:relative;display:grid;grid-template-columns:1fr 128px;gap:14px;align-items:center;margin-top:10px;padding:14px 16px;border-radius:14px;border:1.5px solid #0B1530;background:#fff}
.vd small{font-size:12px;color:#5b6684}.vd h2{font-family:'Rajdhani',sans-serif;font-size:34px;line-height:1.02;font-weight:700;margin:2px 0 8px}
.pb{display:grid;grid-template-columns:78px 1fr 52px;gap:8px;align-items:center;font-size:12.5px;margin:3px 0}.pb b{font-family:'Rajdhani',sans-serif;font-size:14px;text-align:right}
.bar{height:8px;background:#e8e2cf;border-radius:6px;overflow:hidden}.bar i{display:block;height:100%;width:0;border-radius:6px;transition:width 1.3s cubic-bezier(.2,.8,.2,1)}
.ring{position:relative;width:118px;height:118px;justify-self:center}.ring svg{transform:rotate(-90deg)}.ring .v{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.ring .v b{font-family:'Rajdhani',sans-serif;font-size:30px;line-height:1}.ring .v span{font-size:11px;color:#5b6684}
.stamp{position:absolute;right:150px;top:8px;padding:5px 16px 4px;border:4px double;border-radius:8px;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:26px;letter-spacing:3px;
text-align:center;line-height:1.05;opacity:0;transform:rotate(-12deg) scale(3);pointer-events:none;mix-blend-mode:multiply}
.stamp small{display:block;font-size:12px;letter-spacing:1px;color:inherit}.stamp.go{animation:stp .55s cubic-bezier(.2,.9,.3,1.2) forwards}
@keyframes stp{0%{opacity:0;transform:rotate(-24deg) scale(3)}55%{opacity:.95;transform:rotate(-12deg) scale(.9)}75%{transform:rotate(-12deg) scale(1.06)}100%{opacity:.93;transform:rotate(-12deg) scale(1)}}
.rm{display:block;border-left:4px solid #9aa4bf;background:rgba(11,21,48,.045);border-radius:8px;padding:7px 11px;margin-top:7px;font-size:12.8px;line-height:1.4}
.rm .tt{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:15px;display:block}.rm.ok{border-color:#059669}.rm.warn{border-color:#DC2626;background:rgba(220,38,38,.07)}.rm.up{border-color:#2563EB;background:rgba(37,99,235,.07)}.rm.info{border-color:#CA8A04}
.stub .lbl{font-size:11px;color:#5b6684}.stub .big{font-family:'Rajdhani',sans-serif;font-size:19px;font-weight:700;letter-spacing:1px}
.sur{display:flex;flex-wrap:wrap;gap:4px;justify-content:center}.sur span{font-size:11.5px;border:1px solid #cfc7ac;border-radius:6px;padding:1px 6px}
.fine{font-size:10.5px;color:#7a8299;line-height:1.35}
.act{display:flex;gap:10px;margin-top:14px;flex-wrap:wrap}
.act button{background:rgba(255,255,255,.06);color:#EAF0FF;border:1px solid rgba(255,255,255,.2);border-radius:12px;padding:9px 18px;font-size:14px;font-weight:600;transition:all .2s}
.act button:hover{border-color:#FFD21F;color:#FFD21F}.act button:focus-visible{outline:2px solid #FFD21F;outline-offset:2px}
.act button.p{background:linear-gradient(135deg,#FB792B,#FFB02E);color:#1B0E00;border:0}
@media (max-width:620px){.tk{grid-template-columns:1fr}.stub{border-left:0;border-top:2px dashed #C9B77A}.stub:before,.stub:after{display:none}.rt{grid-template-columns:1fr}.st.r{text-align:left}
.mg{grid-template-columns:repeat(2,1fr)}.vd{grid-template-columns:1fr}.stamp{right:12px;top:-4px;font-size:20px}}
@media print{body{background:#fff}.act{display:none}.tk{box-shadow:none}}
"""

TICKET_JS = r"""
const P=__P__;
if(P.auto)RailAudio.printer();
countUp($('#cf'),P.conf,1500,0,'');
setTimeout(()=>{$('#rg').style.strokeDashoffset=(276.46*(1-P.conf/100)).toFixed(2);$$('.bar i').forEach(b=>b.style.width=b.dataset.w+'%')},180);
setTimeout(()=>{$('#sp').classList.add('go');setTimeout(()=>{$('#tk').classList.add('hit');if(P.auto)RailAudio.thud()},330)},900);
function say(){RailAudio.wake();RailAudio.announce(P.pa)}
if(P.auto)setTimeout(say,1900);
const bp=$('#bPlay');if(bp)bp.onclick=say;
$('#bPrint').onclick=()=>window.print();
"""


def _split_station(label: str):
    m = re.match(r"^(.*?)\s*\(([A-Z0-9]+)\)\s*$", label or "")
    return (m.group(1), m.group(2)) if m else (label or "Not set", "")


def render_ticket(R: dict, pa_mode: str, reveal: bool, voice: str = "") -> str:
    a, tier, meta = R["a"], R["tier"], TIER_META[R["tier"]]
    zinfo = ZONE_INFO.get(a["z"], ZONE_INFO["Unknown"])
    frm = a.get("fa") or station_label(a.get("a", "")) or f"{zinfo[1]} (zone HQ)"
    to = a.get("ta") or station_label(a.get("b", "")) or "Not set"
    (fn, fc), (tn, tc) = _split_station(frm), _split_station(to)
    chips = "".join(f'<span class="cls{" on" if on else ""}" style="--c:{col}" title="{esc(lab)}">{code}</span>'
                    for (key, code, lab, col), on in zip(CLASS_DEF, a["c"]))
    sel = [code for (key, code, lab, col), on in zip(CLASS_DEF, a["c"]) if on]
    sur = "".join(f"<span>{c} Rs {SURCHARGE[c]}</span>" for c in sel if c in SURCHARGE) if tier == "SF" else ""
    sur_html = f'<div><div class="lbl">Superfast surcharge (indicative)</div><div class="sur">{sur or "<span>no reserved class</span>"}</div></div>' if tier == "SF" else ""
    bars = "".join(
        f'<div class="pb"><span>{TIER_META[t]["short"]}</span><div class="bar"><i data-w="{R["proba"][t] * 100:.1f}" style="background:{TIER_META[t]["color"]}"></i></div>'
        f'<b>{R["proba"][t] * 100:.1f}%</b></div>' for t in ("SF", "Exp", "Pass"))
    rem = "".join(f'<div class="rm {x["level"]}"><span class="tt">{esc(x["title"])}</span>{x["body"]}</div>' for x in R["adv"][:3])
    cl = CLUSTER_PROFILES.get(R["cluster"]["id"], CLUSTER_PROFILES[3])
    day = "" if R["day_off"] == 0 else f' <span style="font-size:12px">(+{R["day_off"]}d)</span>'
    logo = logo_uri()
    logo_html = f'<img src="{logo}" alt="">' if logo else '<div class="lg">🚆</div>'
    qr = qr_svg(f"RAILDRISHTI|PNR:{R['pnr']}|{tier}|{R['conf']:.1f}|{a['d']}km|{R['total']}min|{a['z']}")
    now = ist_now().strftime("%d %b %Y, %H:%M IST")
    hi_txt, en_txt = pa_texts(R)
    want_hi, want_en = pa_mode in PA_MODES[:2], pa_mode in (PA_MODES[0], PA_MODES[2])
    muted = pa_mode == PA_MODES[4]
    vs = VOICE_SETS.get(voice, next(iter(VOICE_SETS.values())))
    pa = dict(alert=R["flag"] == "DOWNGRADE", segs=[])
    if not muted and (want_hi or want_en):
        with st.spinner("Recording the station announcement..."):
            if want_hi:
                pa["segs"].append(dict(txt=hi_txt, lang="hi-IN", g=vs["hi"][1], b64=voice_b64(hi_txt, "hi", *vs["hi"])))
            if want_en:
                pa["segs"].append(dict(txt=en_txt, lang="en-IN", g=vs["en"][1], b64=voice_b64(en_txt, "en", *vs["en"])))
    P = dict(conf=round(R["conf"], 1), auto=bool(reveal and not muted), pa=pa)
    play_btn = '<button class="p" id="bPlay">Play announcement (हिंदी + English)</button>' if not muted else ""
    body = f"""
    <div class="tk" id="tk">
     <div class="main">
      <div class="hd">{logo_html}<div><h1>Indian Railways · भारतीय रेल</h1><p>ML classification e-ticket · वर्गीकरण ई-टिकट</p></div>
        <div class="pnr"><small>PNR (simulated)</small><b>{R['pnr']}</b></div></div>
      <div class="rt">
        <div class="st"><span>From</span><b>{esc(fn)}</b><span>{esc(fc)}</span><div class="tm">{R['dep'].strftime('%H:%M')}</div><span>{R['dep'].strftime('%a, %d %b %Y')}</span></div>
        <div class="way"><div class="ln"></div><div class="tn">🚆</div><div class="mid">{fmt_dur(R['total'])} · {a['d']} km</div></div>
        <div class="st r"><span>To</span><b>{esc(tn)}</b><span>{esc(tc)}</span><div class="tm">{R['arr'].strftime('%H:%M')}{day}</div><span>{R['arr'].strftime('%a, %d %b %Y')}</span></div>
      </div>
      <div>{chips}</div>
      <div class="mg"><div><span>Zone</span><b>{esc(a['z'])}</b></div><div><span>Average speed</span><b>{R['speed']:.1f} km/h</b></div>
        <div><span>total_duration</span><b>{R['total']} min</b></div><div><span>Fleet segment</span><b>{cl['code']}</b></div></div>
      <div class="vd">
        <div><small>Model verdict · Decision Tree</small><h2 style="color:{INK[tier]}">{esc(meta['name'])}</h2>{bars}</div>
        <div class="ring"><svg width="118" height="118" viewBox="0 0 118 118"><circle cx="59" cy="59" r="44" fill="none" stroke="#e8e2cf" stroke-width="10"/>
          <circle id="rg" cx="59" cy="59" r="44" fill="none" stroke="{INK[tier]}" stroke-width="10" stroke-linecap="round" stroke-dasharray="276.46" stroke-dashoffset="276.46"
          style="transition:stroke-dashoffset 1.5s cubic-bezier(.2,.8,.2,1)"/></svg><div class="v"><b><span id="cf" style="font-size:inherit;color:inherit">0</span>%</b><span>confidence</span></div></div>
        <div class="stamp" id="sp" style="color:{INK[tier]};border-color:{INK[tier]}"><small>{meta['hi']}</small>{esc(meta['short'].upper())}</div>
      </div>
      {rem}
     </div>
     <div class="stub">
      <div class="lbl">Scan to verify</div>{qr}
      <div class="lbl">Audit ID</div><div class="big">IR83-{esc(a['z'])}-{a['d']:04d}</div>
      <div style="width:100%">{barcode_svg(R['pnr'] + a['z'], 160, 38)}</div>
      {sur_html}
      <div class="fine">Generated {esc(now)}<br>Decision Tree · {FACTS['features']} features<br>Simulation for a college project. Not a valid travel ticket.</div>
     </div>
    </div>
    <div class="act">{play_btn}<button id="bPrint">Print / save as PDF</button></div>"""
    js = TICKET_JS.replace("__P__", jdump(P))
    doc = wrap_doc(body, TICKET_CSS, js, libs=JS_AUDIO)
    iframe(doc, 690 + 100 * min(3, len(R["adv"])), scrolling=True)
    return doc


# ------------------------------------------------------------------------------
# dot-matrix platform indicator board
# ------------------------------------------------------------------------------
LED_CSS = r"""
body{background:#070D1F;padding:2px}
.case{position:relative;background:linear-gradient(180deg,#1d2028,#0a0c11);border:2px solid #3b414d;border-radius:16px;padding:10px 14px 12px;
box-shadow:inset 0 0 0 4px #0a0c11,inset 0 2px 0 rgba(255,255,255,.12),0 18px 44px rgba(0,0,0,.5)}
.case:after{content:'';position:absolute;inset:0;border-radius:14px;pointer-events:none;background:linear-gradient(115deg,rgba(255,255,255,.07) 0,rgba(255,255,255,0) 35%)}
.top{display:flex;justify-content:space-between;font-family:'Rajdhani',sans-serif;font-weight:600;font-size:13px;color:#8d96a8;letter-spacing:.6px;padding:0 4px 7px}
.row{display:flex;gap:14px;align-items:stretch}
#led{flex:1;min-width:0;height:150px;background:#05060a;border-radius:8px;border:1px solid #20242d}
.clk{width:136px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#05060a;border-radius:8px;border:1px solid #20242d}
.clk small{color:#8d96a8;font-size:11px;margin-top:2px}
@media (max-width:640px){.clk{display:none}}
"""

LED_JS = r"""
const P=__P__;
const F5={' ':[0,0,0,0,0],'!':[0,0,0x5F,0,0],'%':[0x23,0x13,8,0x64,0x62],'(':[0,0x1C,0x22,0x41,0],')':[0,0x41,0x22,0x1C,0],'+':[8,8,0x3E,8,8],',':[0,0x50,0x30,0,0],'-':[8,8,8,8,8],'.':[0,0x60,0x60,0,0],
'/':[0x20,0x10,8,4,2],'0':[0x3E,0x51,0x49,0x45,0x3E],'1':[0,0x42,0x7F,0x40,0],'2':[0x42,0x61,0x51,0x49,0x46],'3':[0x21,0x41,0x45,0x4B,0x31],'4':[0x18,0x14,0x12,0x7F,0x10],'5':[0x27,0x45,0x45,0x45,0x39],
'6':[0x3C,0x4A,0x49,0x49,0x30],'7':[1,0x71,9,5,3],'8':[0x36,0x49,0x49,0x49,0x36],'9':[6,0x49,0x49,0x29,0x1E],':':[0,0x36,0x36,0,0],'?':[2,1,0x51,9,6],'A':[0x7E,0x11,0x11,0x11,0x7E],'B':[0x7F,0x49,0x49,0x49,0x36],
'C':[0x3E,0x41,0x41,0x41,0x22],'D':[0x7F,0x41,0x41,0x22,0x1C],'E':[0x7F,0x49,0x49,0x49,0x41],'F':[0x7F,9,9,9,1],'G':[0x3E,0x41,0x49,0x49,0x7A],'H':[0x7F,8,8,8,0x7F],'I':[0,0x41,0x7F,0x41,0],'J':[0x20,0x40,0x41,0x3F,1],
'K':[0x7F,8,0x14,0x22,0x41],'L':[0x7F,0x40,0x40,0x40,0x40],'M':[0x7F,2,0x0C,2,0x7F],'N':[0x7F,4,8,0x10,0x7F],'O':[0x3E,0x41,0x41,0x41,0x3E],'P':[0x7F,9,9,9,6],'Q':[0x3E,0x41,0x51,0x21,0x5E],
'R':[0x7F,9,0x19,0x29,0x46],'S':[0x46,0x49,0x49,0x49,0x31],'T':[1,1,0x7F,1,1],'U':[0x3F,0x40,0x40,0x40,0x3F],'V':[0x1F,0x20,0x40,0x20,0x1F],'W':[0x3F,0x40,0x38,0x40,0x3F],'X':[0x63,0x14,8,0x14,0x63],
'Y':[7,8,0x70,8,7],'Z':[0x61,0x51,0x49,0x45,0x43]};
function cols(t){const o=[];for(const ch of t.toUpperCase()){const gl=F5[ch]||F5['?'];gl.forEach(c=>o.push(c));o.push(0)}return o}
const COL={amber:'#FFB000',green:'#3DFF9A',red:'#FF4B3E'};
const cv=$('#led');let g,w,h,pd,gc,LN=[],off=null;
const lines=P.lines.map(l=>({c:cols(l.t),color:COL[l.color]||COL.amber,scroll:!!l.scroll,x:0}));
function layout(){const r=fitCanvas(cv,150);g=r.g;w=r.w;h=r.h;pd=clamp(w/250,3.4,5.2);gc=Math.floor((w-8)/pd);
 off=document.createElement('canvas');off.width=Math.round(w*r.dpr);off.height=Math.round(h*r.dpr);const o=off.getContext('2d');o.setTransform(r.dpr,0,0,r.dpr,0,0);o.fillStyle='#14171e';
 const rows=Math.floor((h-6)/pd);for(let y=0;y<rows;y++)for(let x=0;x<gc;x++){o.beginPath();o.arc(4+x*pd+pd/2,4+y*pd+pd/2,pd*.3,0,6.283);o.fill()}
 lines.forEach(l=>{l.scroll=l.scroll||l.c.length>gc-2;l.x=l.scroll?gc:2})}
function draw(dt){g.clearRect(0,0,w,h);g.drawImage(off,0,0,w,h);const rowsPerLine=9;
 lines.forEach((l,li)=>{const y0=1+li*rowsPerLine;if(l.scroll&&!REDUCED){l.x-=dt*22;if(l.x<-(l.c.length+14))l.x=gc}
  const gap=l.c.length+14;g.fillStyle=l.color;g.globalAlpha=.15;g.beginPath();const lit=[];
  for(let x=0;x<gc;x++){let cx=Math.floor(x-l.x);if(l.scroll){cx=((cx%gap)+gap)%gap}if(cx<0||cx>=l.c.length)continue;const b=l.c[cx];if(!b)continue;
   for(let r=0;r<7;r++)if(b>>r&1){const px=4+x*pd+pd/2,py=4+(y0+r)*pd+pd/2;lit.push(px,py);g.moveTo(px+pd*.6,py);g.arc(px,py,pd*.6,0,6.283)}}
  g.fill();g.globalAlpha=1;g.beginPath();for(let i=0;i<lit.length;i+=2){g.moveTo(lit[i]+pd*.34,lit[i+1]);g.arc(lit[i],lit[i+1],pd*.34,0,6.283)}g.fill()})}
const ck=$('#ck');const cg=ck.getContext('2d');
function clock(){const d=new Date(),ist=new Date(d.getTime()+d.getTimezoneOffset()*60000+19800000);const s=ist.getSeconds()+d.getMilliseconds()/1000,m=ist.getMinutes()+s/60,hr=ist.getHours()%12+m/60;
 cg.clearRect(0,0,120,120);cg.fillStyle='#F6F3EA';cg.beginPath();cg.arc(60,60,57,0,6.283);cg.fill();cg.strokeStyle='#14110A';cg.lineWidth=4;cg.stroke();
 for(let i=0;i<60;i++){const a=i*Math.PI/30,l=i%5?4:9;cg.lineWidth=i%5?1:2.4;cg.beginPath();cg.moveTo(60+Math.sin(a)*(52-l),60-Math.cos(a)*(52-l));cg.lineTo(60+Math.sin(a)*52,60-Math.cos(a)*52);cg.stroke()}
 function hand(a,len,wd,col){cg.strokeStyle=col;cg.lineWidth=wd;cg.lineCap='round';cg.beginPath();cg.moveTo(60-Math.sin(a)*8,60+Math.cos(a)*8);cg.lineTo(60+Math.sin(a)*len,60-Math.cos(a)*len);cg.stroke()}
 hand(hr*Math.PI/6,30,4.5,'#14110A');hand(m*Math.PI/30,43,3,'#14110A');hand(s*Math.PI/30,47,1.6,'#D7261E');cg.fillStyle='#D7261E';cg.beginPath();cg.arc(60,60,3.4,0,6.283);cg.fill()}
layout();onResize(layout);loop(dt=>{draw(dt);clock()});
"""


def _led_text(s: str, n: int = 200) -> str:
    return re.sub(r"[^A-Z0-9 .,:;!?%/()+\-]", "", str(s).upper().replace("_", " "))[:n]


def render_led(R: dict) -> None:
    a, tier = R["a"], R["tier"]
    zi = ZONE_INFO.get(a["z"], ZONE_INFO["Unknown"])
    title = _led_text(a["t"] or "SIMULATED SCHEDULE", 44)
    col2 = "red" if R["flag"] == "DOWNGRADE" else "green" if R["flag"] == "OK" else "amber"
    msg = (f"ATTENTION PLEASE. {zi[0]} SERVICE, {a['d']} KM IN {a['h']} HRS {a['m']} MINS, CLASSIFIED AS {TIER_META[tier]['name']} BY MACHINE LEARNING "
           f"WITH {R['conf']:.0f} PERCENT CONFIDENCE. {R['adv'][0]['title']}.  ")
    msg = _led_text(re.sub(r"<[^>]+>", "", msg), 400)
    lines = [dict(t=title, color="amber"), dict(t=f"{TIER_META[tier]['name']}  {R['conf']:.0f}%  {R['speed']:.0f} KMPH", color=col2),
             dict(t=msg, color="amber", scroll=True)]
    body = ('<div class="case"><div class="top"><span>INDIAN RAILWAYS · TRAIN INDICATOR</span><span>SIMULATED</span></div>'
            '<div class="row"><canvas id="led"></canvas><div class="clk"><canvas id="ck" width="120" height="120" style="width:120px;height:120px"></canvas><small>Platform clock, IST</small></div></div></div>')
    iframe(wrap_doc(body, LED_CSS, LED_JS.replace("__P__", jdump(dict(lines=lines)))), 212)


# ==============================================================================
# 7. VISUAL LABS
# ==============================================================================
def feature_label(name: str) -> str:
    if name in FEATURE_LABELS:
        return FEATURE_LABELS[name]
    if name.startswith("zone_"):
        z = name[5:]
        return f"Runs in zone {z} ({ZONE_INFO.get(z, (z,))[0]})"
    return name


TIER_COLORS = [TIER_META[t]["color"] for t in TIERS]  # Pass, Exp, SF order

# ------------------------------------------------------------------------------
# 7a. Network radar
# ------------------------------------------------------------------------------
NET_CSS = "body{background:#070D1F;padding:2px}#wrap{position:relative;border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,.12);background:#060B1B}#cv{width:100%;height:520px}"
NET_JS = r"""
const P=__P__;
const cv=$('#cv');let g,W,H,sc,ox,oy,CP=[],ZN=[],ST=[],mouse=null,TR=[];
const LON0=67.8,LON1=97.6,LAT0=6.4,LAT1=35.4,KX=.934;
const proj=(lo,la)=>[ox+(lo-LON0)*KX*sc,oy+(LAT1-la)*sc];
function layout(){const r=fitCanvas(cv,520);g=r.g;W=r.w;H=r.h;const mw=W>780?W-270:W;sc=Math.min((mw-30)/((LON1-LON0)*KX),(H-24)/(LAT1-LAT0));ox=(mw-(LON1-LON0)*KX*sc)/2;oy=(H-(LAT1-LAT0)*sc)/2;
 CP=P.cor.map(c=>{const pts=c.pts.map(p=>proj(p[0],p[1]));const cum=[0];for(let i=1;i<pts.length;i++)cum.push(cum[i-1]+Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]));return{n:c.n,pts,cum,len:cum[cum.length-1]}});
 ZN=P.zones.map(z=>({...z,p:proj(z.x,z.y),r:4+Math.sqrt(z.p+z.e+z.s)/5.5}));ST=P.st.map(s=>({c:s[0],n:s[1],p:proj(s[2],s[3])}));
 if(!TR.length){const R=rng(4);for(let i=0;i<18;i++)TR.push({ci:i%CP.length,t:R(),dir:R()<.5?1:-1,sp:26+R()*34,col:P.tc[(R()*3)|0],tail:[]})}}
function at(c,d){let i=1;while(i<c.cum.length-1&&c.cum[i]<d)i++;const a=c.pts[i-1],b=c.pts[i],k=(d-c.cum[i-1])/Math.max(1,c.cum[i]-c.cum[i-1]);return[lerp(a[0],b[0],k),lerp(a[1],b[1],k)]}
function ctc(c,q){const d0=q.t*c.len;[[d0-14,d0+14,'rgba(255,90,95,.95)',4.5],[d0+q.dir*14,d0+q.dir*76,'rgba(255,200,61,.8)',3]].forEach(s=>{const a=Math.max(0,Math.min(s[0],s[1])),b=Math.min(c.len,Math.max(s[0],s[1]));
 g.strokeStyle=s[2];g.lineWidth=s[3];g.beginPath();for(let k=a;k<=b;k+=5){const pp=at(c,k);k===a?g.moveTo(pp[0],pp[1]):g.lineTo(pp[0],pp[1])}g.stroke()})}
function frame(dt,t){g.clearRect(0,0,W,H);const bg=g.createRadialGradient(W*.35,H*.45,40,W*.35,H*.45,W*.7);bg.addColorStop(0,'#0E1B3F');bg.addColorStop(1,'#050A18');g.fillStyle=bg;g.fillRect(0,0,W,H);
 g.fillStyle='rgba(120,150,220,.16)';for(let lo=68;lo<=97;lo+=2)for(let la=8;la<=35;la+=2){const p=proj(lo,la);g.fillRect(p[0],p[1],1.4,1.4)}
 CP.forEach(c=>{g.lineCap='round';g.strokeStyle='rgba(77,163,255,.10)';g.lineWidth=7;g.beginPath();c.pts.forEach((p,i)=>i?g.lineTo(p[0],p[1]):g.moveTo(p[0],p[1]));g.stroke();g.strokeStyle='rgba(150,190,255,.45)';g.lineWidth=1.2;g.stroke()});
 ST.forEach(s=>{g.fillStyle='rgba(200,215,255,.55)';g.beginPath();g.arc(s.p[0],s.p[1],1.8,0,6.283);g.fill()});
 TR.forEach(q=>{const c=CP[q.ci];q.t+=q.dir*q.sp*dt/c.len;if(q.t>1){q.t=1;q.dir=-1}if(q.t<0){q.t=0;q.dir=1}const p=at(c,q.t*c.len);ctc(c,q);q.tail.push(p);if(q.tail.length>14)q.tail.shift();
  q.tail.forEach((tp,i)=>{g.fillStyle=rgba(q.col,i/q.tail.length*.5);g.beginPath();g.arc(tp[0],tp[1],1+i*.12,0,6.283);g.fill()});g.fillStyle=q.col;g.beginPath();g.arc(p[0],p[1],3,0,6.283);g.fill()});
 const sel=ZN.find(z=>z.c===P.sel);
 if(sel){const rad=170;for(let k=0;k<26;k++){const a=t*1.4-k*.04;g.strokeStyle='rgba(255,210,31,'+(.16*(1-k/26)).toFixed(3)+')';g.lineWidth=3;g.beginPath();g.moveTo(sel.p[0],sel.p[1]);g.lineTo(sel.p[0]+Math.cos(a)*rad,sel.p[1]+Math.sin(a)*rad);g.stroke()}
  for(let k=0;k<3;k++){const ph=(t*.6+k/3)%1;g.strokeStyle='rgba(255,210,31,'+(.5*(1-ph))+')';g.lineWidth=2;g.beginPath();g.arc(sel.p[0],sel.p[1],sel.r+ph*60,0,6.283);g.stroke()}}
 if(P.route){const a=proj(P.route.a[2],P.route.a[3]),b=proj(P.route.b[2],P.route.b[3]),mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2,dx=b[0]-a[0],dy=b[1]-a[1],len=Math.hypot(dx,dy)||1,cx=mx-dy/len*len*.22,cy=my+dx/len*len*.22-len*.05;
  g.strokeStyle=rgba(P.tc[2],.25);g.lineWidth=9;g.beginPath();g.moveTo(a[0],a[1]);g.quadraticCurveTo(cx,cy,b[0],b[1]);g.stroke();g.setLineDash([8,7]);g.lineDashOffset=-t*30;g.strokeStyle=P.rc;g.lineWidth=2.6;g.stroke();g.setLineDash([]);
  const k=(t*.12)%1,px=(1-k)*(1-k)*a[0]+2*(1-k)*k*cx+k*k*b[0],py=(1-k)*(1-k)*a[1]+2*(1-k)*k*cy+k*k*b[1];g.fillStyle='#fff';g.beginPath();g.arc(px,py,5,0,6.283);g.fill();g.fillStyle=P.rc;g.beginPath();g.arc(px,py,9,0,6.283);g.globalAlpha=.3;g.fill();g.globalAlpha=1;
  [[a,P.route.a],[b,P.route.b]].forEach(e=>{g.fillStyle='#fff';g.beginPath();g.arc(e[0][0],e[0][1],5,0,6.283);g.fill();g.fillStyle='#EAF0FF';g.font='600 13px Hind,sans-serif';g.fillText(e[1][1]+' ('+e[1][0]+')',e[0][0]+9,e[0][1]-8)})}
 let hov=null,hd=16;ZN.forEach(z=>{const d=mouse?Math.hypot(mouse[0]-z.p[0],mouse[1]-z.p[1]):99;if(d<hd){hd=d;hov=z}});
 ZN.forEach(z=>{const on=z.c===P.sel||z===hov;g.fillStyle=on?'#FFD21F':'#7FB5FF';g.beginPath();g.arc(z.p[0],z.p[1],z.r*(on?1.25:1),0,6.283);g.fill();g.strokeStyle='rgba(255,255,255,.7)';g.lineWidth=1.2;g.stroke();
  g.fillStyle='#EAF0FF';g.font='700 12px Rajdhani,sans-serif';g.fillText(z.c,z.p[0]+z.r+4,z.p[1]+4)});
 const info=hov||sel;if(W>780&&info){const x0=W-250,y0=20,tot=info.p+info.e+info.s;g.fillStyle='rgba(255,255,255,.05)';rr(g,x0,y0,232,190,14);g.fill();g.strokeStyle='rgba(255,255,255,.14)';g.stroke();
  g.fillStyle='#FFD21F';g.font='700 22px Rajdhani,sans-serif';g.fillText(info.c,x0+16,y0+32);g.fillStyle='#EAF0FF';g.font='600 14px Hind,sans-serif';g.fillText(info.n,x0+16,y0+54);
  g.fillStyle='#9AA8CC';g.font='13px Hind,sans-serif';g.fillText(info.hi,x0+16,y0+74);g.fillText('HQ: '+info.hq,x0+16,y0+94);g.fillText(tot?tot.toLocaleString()+' trains in dataset':'no dataset rows',x0+16,y0+118);
  if(tot){let bx=x0+16;[['p',P.tc[0]],['e',P.tc[1]],['s',P.tc[2]]].forEach(c=>{const w=(info[c[0]]/tot)*200;g.fillStyle=c[1];g.fillRect(bx,y0+130,w,10);bx+=w});
   g.fillStyle='#9AA8CC';g.font='12px Hind,sans-serif';g.fillText('Pass '+Math.round(info.p/tot*100)+'%  Exp '+Math.round(info.e/tot*100)+'%  SF '+Math.round(info.s/tot*100)+'%',x0+16,y0+162)}}
 if(W>780){g.fillStyle='#9AA8CC';g.font='12.5px Hind,sans-serif';g.fillText('Moving dots are simulated trains on trunk corridors.',W-250,H-26);g.fillText('Zone HQ positions are schematic.',W-250,H-10)}}
cv.addEventListener('mousemove',e=>{const r=cv.getBoundingClientRect();mouse=[e.clientX-r.left,e.clientY-r.top]});cv.addEventListener('mouseleave',()=>mouse=null);
layout();onResize(layout);loop(frame);
"""


def render_network(R: dict, eng: Engine, route: dict | None) -> None:
    zs = {}
    if eng.df is not None and "zone" in eng.df.columns and "type" in eng.df.columns:
        ct = eng.df.groupby(["zone", "type"]).size().unstack(fill_value=0)
        for z, row in ct.iterrows():
            zs[str(z)] = {t: int(row.get(t, 0)) for t in TIERS}
    zones = []
    for code, (name, hq, hi, lon, lat) in ZONE_INFO.items():
        if code == "Unknown":
            continue
        s = zs.get(code, {})
        zones.append(dict(c=code, n=name, hq=hq, hi=hi, x=lon, y=lat, p=s.get("Pass", 0), e=s.get("Exp", 0), s=s.get("SF", 0)))
    rt = None
    if route:
        a, b = STATION_BY_CODE[route["a"]], STATION_BY_CODE[route["b"]]
        rt = dict(a=[a[0], a[1], a[3], a[4]], b=[b[0], b[1], b[3], b[4]])
    P = dict(zones=zones, cor=[dict(n=n, pts=pts) for n, pts in CORRIDORS], st=[[s[0], s[1], s[3], s[4]] for s in STATIONS],
             sel=R["a"]["z"], route=rt, tc=TIER_COLORS, rc=TIER_META[R["tier"]]["color"])
    iframe(wrap_doc('<div id="wrap"><canvas id="cv"></canvas></div>', NET_CSS, NET_JS.replace("__P__", jdump(P))), 530)


# ------------------------------------------------------------------------------
# 7b. Decision junction: the decision-tree path drawn as a railway line with switches
# ------------------------------------------------------------------------------
JUNC_CSS = r"""
body{padding:4px}
.wrap{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(240px,1fr);gap:18px}
.rail{position:relative;padding-left:64px}
.rail:before{content:'';position:absolute;left:26px;top:12px;bottom:60px;width:6px;background:repeating-linear-gradient(180deg,#5b6684 0 14px,#2a3350 14px 18px);border-radius:3px}
.stp{position:relative;margin-bottom:14px;opacity:0;transform:translateX(-12px);transition:all .5s}.stp.on{opacity:1;transform:none}
.nd{position:absolute;left:-50px;top:14px;width:30px;height:30px;border-radius:50%;background:#0B1530;border:3px solid #5b6684;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;font-family:'Rajdhani',sans-serif;transition:all .4s}
.stp.on .nd{border-color:var(--c);box-shadow:0 0 16px var(--c);color:var(--c)}
.sw{position:absolute;left:-20px;top:26px;width:44px;height:3px;background:#5b6684;transform-origin:left center;transition:transform .5s .2s;border-radius:2px}
.stp.on .sw{background:var(--c);transform:rotate(var(--r))}
.cd{background:linear-gradient(180deg,rgba(255,255,255,.07),rgba(255,255,255,.03));border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:11px 14px;margin-left:20px}
.cd b{font-family:'Rajdhani',sans-serif;font-size:18px;display:block;line-height:1.2}.cd .sub{font-size:12.5px;color:#9AA8CC;margin-top:2px}
.pill{display:inline-block;font-size:12px;font-weight:600;padding:2px 10px;border-radius:999px;margin-left:8px;vertical-align:middle}
.yes{background:rgba(52,211,153,.15);color:#34D399}.no{background:rgba(255,90,95,.15);color:#FF8A8E}
.mix{display:flex;height:9px;border-radius:5px;overflow:hidden;margin-top:8px;background:#1b2440}.mix i{display:block;height:100%;transition:width 1s}
.side{font-size:11.5px;color:#7f8bb0;margin-top:5px}
.trn{position:absolute;left:12px;top:0;font-size:26px;transition:top .7s ease;z-index:3;filter:drop-shadow(0 4px 8px rgba(0,0,0,.6))}
.end{margin-left:20px;border-radius:16px;padding:16px 18px;border:2px solid var(--c);background:rgba(255,255,255,.05);opacity:0;transition:opacity .6s}.end.on{opacity:1}
.end h2{font-family:'Rajdhani',sans-serif;font-size:30px;color:var(--c);line-height:1.05}.end p{font-size:13px;color:#C9D4F2;margin-top:4px}
aside{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:14px 16px;align-self:start}
aside h3{font-family:'Rajdhani',sans-serif;font-size:20px;margin-bottom:8px}
.ib{display:grid;grid-template-columns:1fr 46px;gap:8px;align-items:center;margin:7px 0;font-size:12.5px}.ib .t{height:7px;background:#1b2440;border-radius:5px;overflow:hidden;margin-top:3px}.ib .t i{display:block;height:100%;background:linear-gradient(90deg,#FB792B,#FFD21F);width:0;transition:width 1.1s}
.rp{margin-top:12px;background:#FFD21F;color:#14110A;border:0;border-radius:10px;padding:7px 16px;font-weight:600}
@media (max-width:820px){.wrap{grid-template-columns:1fr}}
"""
JUNC_JS = r"""
const P=__P__;
const root=$('#rail');
function build(){root.innerHTML='<div class="trn" id="trn">🚆</div>';
 P.steps.forEach((s,i)=>{const d=document.createElement('div');d.className='stp';d.style.setProperty('--c',s.yes?'#34D399':'#FF8A8E');d.style.setProperty('--r',s.yes?'-24deg':'24deg');
  const mix=s.mix.map((m,j)=>'<i style="width:'+(m*100).toFixed(1)+'%;background:'+P.tc[j]+'"></i>').join('');
  d.innerHTML='<div class="nd">'+(i+1)+'</div><div class="sw"></div><div class="cd"><b>'+s.q+'<span class="pill '+(s.yes?'yes':'no')+'">'+s.a+'</span></b><div class="sub">'+s.v+'</div>'
   +'<div class="mix">'+mix+'</div><div class="side">'+s.n.toLocaleString()+' training trains at this junction, impurity '+s.g.toFixed(2)+'. Other branch: '+s.no.toLocaleString()+' trains.</div></div>';root.appendChild(d)});
 const e=document.createElement('div');e.className='end';e.id='end';e.style.setProperty('--c',P.color);e.innerHTML='<h2>'+P.name+'</h2><p>'+P.leaf+'</p><div class="mix">'+P.lm.map((m,j)=>'<i style="width:'+(m*100).toFixed(1)+'%;background:'+P.tc[j]+'"></i>').join('')+'</div>';root.appendChild(e)}
function run(){build();const st=$$('.stp'),trn=$('#trn');let i=0;trn.style.top='0px';
 function next(){if(i<st.length){const s=st[i];s.classList.add('on');trn.style.top=(s.offsetTop+4)+'px';RailAudio.click();i++;setTimeout(next,REDUCED?60:720)}else{const en=$('#end');en.classList.add('on');trn.style.top=(en.offsetTop+10)+'px'}}
 setTimeout(next,300);setTimeout(()=>$$('.ib i').forEach(b=>b.style.width=b.dataset.w+'%'),400)}
$('#imp').innerHTML=P.imp.map(x=>'<div class="ib"><div>'+x[0]+'<div class="t"><i data-w="'+(x[1]*100/P.imp[0][1]).toFixed(1)+'"></i></div></div><b>'+(x[1]*100).toFixed(1)+'%</b></div>').join('');
$('#rp').onclick=run;run();
"""


def render_junction(R: dict, eng: Engine) -> None:
    steps = []
    for s in R["steps"]:
        f = s["feature"]
        label = feature_label(f)
        binary = f in FLAG_KEYS or f.startswith("zone_")
        if binary:
            has = s["v_raw"] >= 0.5
            q = f"{label}?" if f in FLAG_KEYS else f"{label}?"
            ans, vtxt = ("Yes" if has else "No"), f"Input value {int(round(s['v_raw']))}; the tree splits at {s['thr_raw']:.2f}"
        else:
            q = f"{label} at most {s['thr_raw']:.0f}?"
            ans = "Yes" if s["yes"] else "No"
            vtxt = f"This schedule has {s['v_raw']:.0f}"
        steps.append(dict(q=esc(q), a=ans, yes=bool(s["yes"] if not binary else (s["v_raw"] >= 0.5)), v=esc(vtxt), mix=s["mix"], n=s["n"], g=s["gini"], no=s["n_other"]))
    leaf = R["leaf"]
    P = dict(steps=steps, tc=TIER_COLORS, color=TIER_META[R["tier"]]["color"], name=TIER_META[R["tier"]]["name"],
             leaf=f"Terminus reached after {len(steps)} junctions. {leaf.get('n', 0):,} training trains ended here, impurity {leaf.get('gini', 0):.2f}.",
             lm=leaf.get("mix", [0, 0, 0]), imp=[[feature_label(n), w] for n, w in eng.importances(8)])
    body = ('<div class="wrap"><div class="rail" id="rail"></div><aside><h3>What the tree cares about</h3><div id="imp"></div>'
            '<div class="side">Gini importance from the fitted model. Bars under each junction show the Pass / Exp / SF mix of training trains that reach it.</div>'
            '<button class="rp" id="rp">Replay journey</button></aside></div>')
    iframe(wrap_doc(body, JUNC_CSS, JUNC_JS.replace("__P__", jdump(P)), libs=JS_AUDIO), max(760, 240 + 160 * len(steps)))


# ------------------------------------------------------------------------------
# 7c. Decision atlas: predicted tier over (distance x average speed)
# ------------------------------------------------------------------------------
ATLAS_CSS = "body{padding:2px}#wrap{border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,.12);background:#060B1B;position:relative}#cv{width:100%;height:470px}"
ATLAS_JS = r"""
const P=__P__;
const cv=$('#cv');let g,W,H,mouse=null,prog=0;const ML=58,MB=40,MT=14,MR=16;
function layout(){const r=fitCanvas(cv,470);g=r.g;W=r.w;H=r.h;prog=REDUCED?1:0}
const px=d=>ML+(d-P.x0)/(P.x1-P.x0)*(W-ML-MR), py=s=>H-MB-(s-P.y0)/(P.y1-P.y0)*(H-MB-MT);
function frame(dt,t){g.clearRect(0,0,W,H);prog=Math.min(1,prog+dt*.7);const cw=(W-ML-MR)/P.nx,ch=(H-MB-MT)/P.ny;
 for(let j=0;j<P.ny;j++)for(let i=0;i<P.nx;i++){if(i/P.nx>prog)continue;const k=j*P.nx+i,c=P.tc[P.cls[k]],a=.2+.6*P.conf[k]/100;g.fillStyle=rgba(c,a);g.fillRect(ML+i*cw,H-MB-(j+1)*ch,cw+.6,ch+.6)}
 g.strokeStyle='rgba(255,255,255,.12)';g.fillStyle='#9AA8CC';g.font='12px Hind,sans-serif';g.lineWidth=1;
 for(let d=0;d<=P.x1;d+=500){const x=px(d);g.beginPath();g.moveTo(x,MT);g.lineTo(x,H-MB);g.stroke();g.fillText(d,x-10,H-MB+16)}
 for(let s=P.y0;s<=P.y1;s+=20){const y=py(s);g.beginPath();g.moveTo(ML,y);g.lineTo(W-MR,y);g.stroke();g.fillText(s,ML-28,y+4)}
 g.fillStyle='#EAF0FF';g.font='600 13px Hind,sans-serif';g.fillText('Route distance (km)',ML+(W-ML-MR)/2-60,H-8);g.save();g.translate(14,MT+(H-MB-MT)/2+50);g.rotate(-Math.PI/2);g.fillText('Average speed (km/h)',0,0);g.restore();
 const y55=py(P.norm);g.setLineDash([7,6]);g.strokeStyle='#FFD21F';g.lineWidth=1.6;g.beginPath();g.moveTo(ML,y55);g.lineTo(W-MR,y55);g.stroke();g.setLineDash([]);g.fillStyle='rgba(6,11,27,.88)';rr(g,W-MR-168,y55-25,162,20,6);g.fill();g.fillStyle='#FFD21F';g.font='600 12.5px Hind,sans-serif';g.fillText('55 km/h Superfast line',W-MR-160,y55-10);
 const cx=px(P.cur[0]),cy=py(P.cur[1]),pu=(t*.9)%1;g.strokeStyle='rgba(255,255,255,.55)';g.setLineDash([4,5]);g.beginPath();g.moveTo(cx,MT);g.lineTo(cx,H-MB);g.moveTo(ML,cy);g.lineTo(W-MR,cy);g.stroke();g.setLineDash([]);
 g.strokeStyle='rgba(255,255,255,'+(.7*(1-pu))+')';g.lineWidth=2;g.beginPath();g.arc(cx,cy,8+pu*22,0,6.283);g.stroke();g.fillStyle='#fff';g.beginPath();g.arc(cx,cy,7,0,6.283);g.fill();g.fillStyle=P.tc[P.curCls];g.beginPath();g.arc(cx,cy,4.5,0,6.283);g.fill();
 g.fillStyle='rgba(6,11,27,.88)';rr(g,cx+10,cy-28,92,20,6);g.fill();g.fillStyle='#fff';g.font='700 13px Rajdhani,sans-serif';g.fillText('This schedule',cx+16,cy-13);
 g.fillStyle='rgba(6,11,27,.88)';rr(g,ML+6,MT+4,372,26,8);g.fill();P.names.forEach((n,i)=>{const x=ML+16+i*120;g.fillStyle=P.tc[i];g.fillRect(x,MT+11,12,12);g.fillStyle='#EAF0FF';g.font='600 13px Hind,sans-serif';g.fillText(n,x+18,MT+22)});
 if(mouse&&mouse[0]>ML&&mouse[0]<W-MR&&mouse[1]>MT&&mouse[1]<H-MB){const i=Math.min(P.nx-1,Math.floor((mouse[0]-ML)/cw)),j=Math.min(P.ny-1,Math.floor((H-MB-mouse[1])/ch)),k=j*P.nx+i;
  const d=P.x0+(i+.5)/P.nx*(P.x1-P.x0),s=P.y0+(j+.5)/P.ny*(P.y1-P.y0),tx=Math.min(mouse[0]+14,W-190),ty=Math.max(mouse[1]-70,MT+30);g.fillStyle='rgba(8,13,30,.94)';rr(g,tx,ty,176,64,10);g.fill();g.strokeStyle=P.tc[P.cls[k]];g.lineWidth=1.5;g.stroke();
  g.fillStyle=P.tc[P.cls[k]];g.font='700 16px Rajdhani,sans-serif';g.fillText(P.names[P.cls[k]]+'  '+P.conf[k]+'%',tx+12,ty+22);g.fillStyle='#C9D4F2';g.font='12.5px Hind,sans-serif';
  g.fillText(Math.round(d)+' km at '+s.toFixed(0)+' km/h',tx+12,ty+40);g.fillText('duration '+Math.floor(d/s)+'h '+Math.round((d/s%1)*60)+'m',tx+12,ty+56)}}
cv.addEventListener('mousemove',e=>{const r=cv.getBoundingClientRect();mouse=[e.clientX-r.left,e.clientY-r.top]});cv.addEventListener('mouseleave',()=>mouse=null);
layout();onResize(layout);loop(frame);
"""


def render_atlas(R: dict, eng: Engine) -> None:
    nx, ny, x0, x1, y0, y1 = 60, 48, 20, 3000, 12, 112
    dist = np.linspace(x0 + (x1 - x0) / nx / 2, x1 - (x1 - x0) / nx / 2, nx)
    spd = np.linspace(y0 + (y1 - y0) / ny / 2, y1 - (y1 - y0) / ny / 2, ny)
    D, Sp = np.meshgrid(dist, spd)
    X = eng.frame_grid(R["a"], D.ravel(), D.ravel() / Sp.ravel() * 60.0)
    Pm = eng.proba(X)
    cls = Pm.argmax(axis=1)
    P = dict(nx=nx, ny=ny, x0=x0, x1=x1, y0=y0, y1=y1, cls=cls.tolist(), conf=np.round(Pm.max(axis=1) * 100).astype(int).tolist(), tc=TIER_COLORS,
             names=["Passenger", "Express", "Superfast"], norm=55, cur=[min(R["a"]["d"], x1), min(max(R["speed"], y0), y1)], curCls=TIERS.index(R["tier"]))
    iframe(wrap_doc('<div id="wrap"><canvas id="cv"></canvas></div>', ATLAS_CSS, ATLAS_JS.replace("__P__", jdump(P))), 480)


# ------------------------------------------------------------------------------
# 7d. Fleet galaxy: K-Means clusters in a 2-D PCA map
# ------------------------------------------------------------------------------
GAL_CSS = "body{padding:2px}#wrap{border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,.12);background:#050A18;position:relative}#cv{width:100%;height:500px}"
GAL_JS = r"""
const P=__P__;
const cv=$('#cv');let g,W,H,mouse=null,BG=[];const M=40;
function layout(){const r=fitCanvas(cv,500);g=r.g;W=r.w;H=r.h;const R=rng(5);BG=[];for(let i=0;i<120;i++)BG.push([R()*W,R()*H,R()<.2?1.6:.9,R()*6])}
const X=v=>M+v*(W-2*M-(W>760?210:0)),Y=v=>H-M-v*(H-2*M);
function star(x,y,r,n){g.beginPath();for(let i=0;i<n*2;i++){const a=i*Math.PI/n-Math.PI/2,rad=i%2?r*.45:r;g.lineTo(x+Math.cos(a)*rad,y+Math.sin(a)*rad)}g.closePath()}
function frame(dt,t){g.clearRect(0,0,W,H);const bg=g.createRadialGradient(W*.4,H*.5,30,W*.4,H*.5,W*.7);bg.addColorStop(0,'#0D1838');bg.addColorStop(1,'#04070F');g.fillStyle=bg;g.fillRect(0,0,W,H);
 BG.forEach(s=>{g.fillStyle='rgba(255,255,255,'+(.25+.25*Math.sin(t*1.5+s[3])).toFixed(2)+')';g.fillRect(s[0],s[1],s[2],s[2])});
 P.pts.forEach((p,i)=>{const c=P.prof[p[2]]||P.prof[0];g.fillStyle=rgba(c.color,.55+.25*Math.sin(t*2+i));g.fillRect(X(p[0]),Y(p[1]),2.2,2.2)});
 let hov=null,hd=28;P.cent.forEach(c=>{const d=mouse?Math.hypot(mouse[0]-X(c.x),mouse[1]-Y(c.y)):99;if(d<hd){hd=d;hov=c}});
 P.cent.forEach(c=>{const pr=P.prof[c.id]||P.prof[0],x=X(c.x),y=Y(c.y);g.strokeStyle=pr.color;g.lineWidth=2.5;g.beginPath();g.arc(x,y,13+(c===hov?4:0),0,6.283);g.stroke();g.fillStyle='rgba(5,10,24,.8)';g.beginPath();g.arc(x,y,10,0,6.283);g.fill();
  g.fillStyle=pr.color;g.font='700 12px Rajdhani,sans-serif';g.textAlign='center';g.fillText(pr.code,x,y+4);g.textAlign='left'});
 if(P.q){const qx=X(P.q[0]),qy=Y(P.q[1]),c=P.cent.find(k=>k.id===P.qc);if(c){g.setLineDash([5,5]);g.strokeStyle='rgba(255,255,255,.6)';g.lineWidth=1.4;g.lineDashOffset=-t*20;g.beginPath();g.moveTo(qx,qy);g.lineTo(X(c.x),Y(c.y));g.stroke();g.setLineDash([])}
  const ph=(t*.8)%1;g.strokeStyle='rgba(255,210,31,'+(.8*(1-ph))+')';g.lineWidth=2;g.beginPath();g.arc(qx,qy,8+ph*34,0,6.283);g.stroke();g.fillStyle='#FFD21F';star(qx,qy,13,5);g.fill();g.strokeStyle='#fff';g.lineWidth=1.2;g.stroke();
  g.fillStyle='#fff';g.font='700 14px Rajdhani,sans-serif';g.fillText('Your schedule',qx+16,qy-8)}
 if(W>760){const x0=W-210;g.fillStyle='rgba(255,255,255,.05)';rr(g,x0-8,16,200,H-32,14);g.fill();g.strokeStyle='rgba(255,255,255,.12)';g.stroke();g.font='700 15px Rajdhani,sans-serif';g.fillStyle='#EAF0FF';g.fillText('Fleet segments',x0+6,40);
  P.cent.forEach((c,i)=>{const pr=P.prof[c.id]||P.prof[0],y=62+i*70;g.fillStyle=pr.color;g.beginPath();g.arc(x0+12,y+6,6,0,6.283);g.fill();g.fillStyle=c===hov||c.id===P.qc?'#FFD21F':'#EAF0FF';g.font='600 13px Hind,sans-serif';
   const words=pr.name.split(' ');let line='',yy=y+10,n=0;words.forEach(w=>{if((line+w).length>22){g.fillText(line,x0+26,yy);line=w+' ';yy+=15;n++}else line+=w+' '});g.fillText(line,x0+26,yy);g.fillStyle='#9AA8CC';g.font='12px Hind,sans-serif';g.fillText(c.share+'% of fleet',x0+26,yy+15)});
  g.fillStyle='#9AA8CC';g.font='11.5px Hind,sans-serif';g.fillText('PCA: '+P.var[0]+'% + '+P.var[1]+'% variance',x0+6,H-26)}
 if(hov){const pr=P.prof[hov.id]||P.prof[0];const tx=Math.min(X(hov.x)+18,W-300),ty=Math.max(Y(hov.y)-70,20);g.fillStyle='rgba(8,13,30,.95)';rr(g,tx,ty,270,58,10);g.fill();g.strokeStyle=pr.color;g.lineWidth=1.4;g.stroke();
  g.fillStyle=pr.color;g.font='700 15px Rajdhani,sans-serif';g.fillText(pr.code+'  '+pr.name.slice(0,34),tx+10,ty+22);g.fillStyle='#C9D4F2';g.font='12px Hind,sans-serif';g.fillText(pr.zone.slice(0,48),tx+10,ty+42)}}
cv.addEventListener('mousemove',e=>{const r=cv.getBoundingClientRect();mouse=[e.clientX-r.left,e.clientY-r.top]});cv.addEventListener('mouseleave',()=>mouse=null);
layout();onResize(layout);loop(frame);
"""


def render_galaxy(R: dict, eng: Engine) -> None:
    sp = eng.space
    if not sp.ok:
        st.info("data/trains_with_clusters.csv was not found, so the galaxy map is unavailable. The cluster label still works from rule-based fallbacks.")
        return
    rnd = np.random.default_rng(3)
    idx = rnd.choice(len(sp.pts), size=min(2600, len(sp.pts)), replace=False)
    q = np.array(R["cluster"]["xy"]) if R["cluster"].get("xy") is not None else None
    stack = [sp.pts, sp.cent2d] + ([q[None]] if q is not None else [])
    allp = np.vstack(stack)
    lo, hi = np.percentile(allp, 1, axis=0), np.percentile(allp, 99, axis=0)
    span = np.where(hi - lo == 0, 1, hi - lo)
    nm = lambda a: np.clip((a - lo) / span, -0.04, 1.04)
    pts = np.c_[nm(sp.pts[idx]), sp.lab[idx]]
    cent, total = [], len(sp.lab)
    for k, cid in enumerate(sp.ids):
        c = nm(sp.cent2d[k])
        cent.append(dict(id=int(cid), x=round(float(c[0]), 3), y=round(float(c[1]), 3), share=round(100 * float(np.mean(sp.lab == cid)), 1)))
    prof = {str(c): CLUSTER_PROFILES.get(c, CLUSTER_PROFILES[4]) for c in sp.ids}
    prof_list = {int(k): v for k, v in prof.items()}
    P = dict(pts=np.round(pts, 3).tolist(), cent=cent, prof=prof_list, var=[round(v * 100) for v in sp.var],
             q=[round(float(v), 3) for v in nm(q)] if q is not None else None, qc=int(R["cluster"]["id"]))
    iframe(wrap_doc('<div id="wrap"><canvas id="cv"></canvas></div>', GAL_CSS, GAL_JS.replace("__P__", jdump(P))), 510)


# ------------------------------------------------------------------------------
# 7e. Model arena: racing bars + before/after duration fix
# ------------------------------------------------------------------------------
ARENA_CSS = r"""
body{padding:4px}.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;align-items:center}
.tabs button{background:rgba(255,255,255,.05);color:#EAF0FF;border:1px solid rgba(255,255,255,.16);border-radius:999px;padding:7px 16px;font-size:14px;font-weight:600;transition:all .2s}
.tabs button.on{background:#FFD21F;color:#14110A;border-color:#FFD21F}.tabs .sp{flex:1}.tabs button:focus-visible{outline:2px solid #FFD21F;outline-offset:2px}
.board{position:relative;height:330px}
.row{position:absolute;left:0;right:0;height:46px;transition:transform .9s cubic-bezier(.2,.8,.2,1);display:grid;grid-template-columns:210px 1fr 70px;gap:12px;align-items:center}
.row .nm{font-weight:600;font-size:14.5px;display:flex;align-items:center;gap:8px}.row .nm em{font-style:normal;font-family:'Rajdhani',sans-serif;font-size:13px;background:rgba(255,255,255,.1);border-radius:6px;padding:0 7px}
.trk{height:22px;background:rgba(255,255,255,.07);border-radius:12px;overflow:hidden}.trk i{display:block;height:100%;width:0;border-radius:12px;background:linear-gradient(90deg,#3b5bdb,#4DA3FF);transition:width 1s cubic-bezier(.2,.8,.2,1)}
.row.champ .trk i{background:linear-gradient(90deg,#FB792B,#FFD21F);box-shadow:0 0 18px rgba(255,210,31,.45)}
.row b{font-family:'Rajdhani',sans-serif;font-size:21px;text-align:right}
h3{font-family:'Rajdhani',sans-serif;font-size:22px;margin:18px 0 4px}.sub{font-size:13px;color:#9AA8CC;margin-bottom:12px}
.db{display:grid;grid-template-columns:210px 1fr 76px;gap:12px;align-items:center;margin:9px 0;font-size:14px}.db .t{position:relative;height:6px;background:rgba(255,255,255,.1);border-radius:4px}
.db .ln{position:absolute;top:0;height:6px;background:rgba(255,210,31,.55);border-radius:4px;transition:all 1.1s}.db .d{position:absolute;top:-5px;width:16px;height:16px;border-radius:50%;transition:left 1.1s}
.db .b{background:#6b7490;border:2px solid #0b1020}.db .a{background:#FFD21F;border:2px solid #0b1020;box-shadow:0 0 12px rgba(255,210,31,.6)}.db b{font-family:'Rajdhani',sans-serif;color:#34D399;text-align:right}
.lg{font-size:12.5px;color:#9AA8CC;display:flex;gap:16px;margin-top:6px}.lg span:before{content:'';display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}.lg .g:before{background:#6b7490}.lg .y:before{background:#FFD21F}
@media (max-width:700px){.row,.db{grid-template-columns:120px 1fr 56px}}
"""
ARENA_JS = r"""
const P=__P__;
const MET=[['acc','Accuracy'],['f1','Macro F1'],['wf1','Weighted F1'],['auc','ROC-AUC']];let cur='f1';
const tabs=$('#tabs'),board=$('#board');
MET.forEach(m=>{const b=document.createElement('button');b.textContent=m[1];b.dataset.k=m[0];b.onclick=()=>show(m[0]);tabs.appendChild(b)});
const rp=document.createElement('button');rp.textContent='Replay race';rp.className='';rp.onclick=()=>{$$('.trk i').forEach(i=>i.style.width='0');setTimeout(()=>show(cur),200)};const sp=document.createElement('span');sp.className='sp';tabs.appendChild(sp);tabs.appendChild(rp);
P.m.forEach((m,i)=>{const r=document.createElement('div');r.className='row'+(m.champ?' champ':'');r.id='r'+i;r.innerHTML='<div class="nm">'+m.model+'<em></em></div><div class="trk"><i></i></div><b></b>';board.appendChild(r)});
function show(k){cur=k;$$('#tabs button').forEach(b=>b.classList.toggle('on',b.dataset.k===k));const ord=P.m.map((m,i)=>[i,m[k]]).sort((a,b)=>b[1]-a[1]);
 ord.forEach((o,rank)=>{const r=$('#r'+o[0]);r.style.transform='translateY('+(rank*52)+'px)';r.querySelector('i').style.width=(o[1]*100)+'%';r.querySelector('b').textContent=o[1].toFixed(4);r.querySelector('em').textContent=rank<3?['1st','2nd','3rd'][rank]:''})}
const db=$('#db');P.m.forEach((m,i)=>{const r=document.createElement('div');r.className='db';r.innerHTML='<div>'+m.model+'</div><div class="t"><div class="ln" id="l'+i+'"></div><div class="d b" id="b'+i+'"></div><div class="d a" id="a'+i+'"></div></div><b>+'+(m.f1-m.before).toFixed(4)+'</b>';db.appendChild(r)});
setTimeout(()=>{P.m.forEach((m,i)=>{const bx=m.before*100,ax=m.f1*100;$('#b'+i).style.left='calc('+bx+'% - 8px)';$('#a'+i).style.left='calc('+ax+'% - 8px)';const l=$('#l'+i);l.style.left=bx+'%';l.style.width=(ax-bx)+'%'})},500);
show('f1');
"""


def render_arena() -> None:
    m = [dict(model=b["model"], acc=b["acc"], f1=b["f1"], wf1=b["wf1"], auc=b["auc"], before=b["before"], champ=b["champ"]) for b in BENCHMARKS]
    body = ('<div class="tabs" id="tabs"></div><div class="board" id="board"></div>'
            '<h3>What the duration fix was worth</h3><div class="sub">Macro F1 before and after replacing duration_m with total_duration = duration_h x 60 + duration_m.</div>'
            '<div id="db"></div><div class="lg"><span class="g">before the fix</span><span class="y">after the fix</span></div>')
    iframe(wrap_doc(body, ARENA_CSS, ARENA_JS.replace("__P__", jdump(dict(m=m)))), 830)


# ------------------------------------------------------------------------------
# 7f. Fleet charts (donut, stacked zone bars, speed histogram)
# ------------------------------------------------------------------------------
CHART_CSS = r"""
body{padding:2px}.g{display:grid;grid-template-columns:1fr 1.5fr;gap:14px}.c{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:12px 14px}
.c h4{font-family:'Rajdhani',sans-serif;font-size:19px;margin-bottom:4px}.c.w{grid-column:1/-1}canvas{width:100%}.lg{display:flex;gap:14px;font-size:12.5px;color:#9AA8CC;margin-top:4px}.lg span:before{content:'';display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px;background:var(--c)}
@media (max-width:760px){.g{grid-template-columns:1fr}}
"""
CHART_JS = r"""
const P=__P__;const TC=P.tc,NM=['Passenger','Express','Superfast'];let prog=0;
const A=fitCanvas($('#c1'),250),B=fitCanvas($('#c2'),250),C=fitCanvas($('#c3'),220);
function donut(){const g=A.g,w=A.w,h=A.h,cx=w/2,cy=h/2,R=Math.min(w,h)*.38,tot=P.share.reduce((a,b)=>a+b,0);g.clearRect(0,0,w,h);let a0=-Math.PI/2;
 P.share.forEach((v,i)=>{const a1=a0+v/tot*6.2832*easeOut(prog);g.strokeStyle=TC[i];g.lineWidth=R*.38;g.beginPath();g.arc(cx,cy,R,a0,a1);g.stroke();a0=a1});
 g.fillStyle='#EAF0FF';g.textAlign='center';g.font='700 30px Rajdhani,sans-serif';g.fillText(Math.round(tot*easeOut(prog)).toLocaleString(),cx,cy+6);g.fillStyle='#9AA8CC';g.font='12.5px Hind,sans-serif';g.fillText('trains',cx,cy+24);g.textAlign='left'}
function bars(){const g=B.g,w=B.w,h=B.h,n=P.zones.length,rh=(h-14)/n,x0=54,mx=Math.max(...P.zones.map(z=>z.p+z.e+z.s));g.clearRect(0,0,w,h);g.font='600 12.5px Hind,sans-serif';
 P.zones.forEach((z,i)=>{const y=6+i*rh;g.fillStyle='#EAF0FF';g.fillText(z.z,6,y+rh*.62);let x=x0;[z.p,z.e,z.s].forEach((v,j)=>{const ww=v/mx*(w-x0-48)*easeOut(prog);g.fillStyle=TC[j];g.fillRect(x,y+2,ww,rh-5);x+=ww});g.fillStyle='#9AA8CC';g.fillText((z.p+z.e+z.s).toLocaleString(),x+6,y+rh*.62)})}
function hist(){const g=C.g,w=C.w,h=C.h,m=36,mx=Math.max(...P.hist.v.flat());g.clearRect(0,0,w,h);g.strokeStyle='rgba(255,255,255,.1)';g.fillStyle='#9AA8CC';g.font='12px Hind,sans-serif';
 P.hist.x.forEach((x,i)=>{if(i%2===0){const px=m+i/(P.hist.x.length-1)*(w-m-10);g.fillText(x,px-8,h-8);g.beginPath();g.moveTo(px,8);g.lineTo(px,h-24);g.stroke()}});
 P.hist.v.forEach((arr,j)=>{g.beginPath();arr.forEach((v,i)=>{const px=m+i/(arr.length-1)*(w-m-10),py=h-24-(v/mx)*(h-40)*easeOut(prog);i?g.lineTo(px,py):g.moveTo(px,py)});g.strokeStyle=TC[j];g.lineWidth=2.4;g.stroke();g.lineTo(w-10,h-24);g.lineTo(m,h-24);g.closePath();g.fillStyle=rgba(TC[j],.14);g.fill()});
 g.fillStyle='#9AA8CC';g.fillText('average speed (km/h)',w/2-50,h-0)}
loop(dt=>{if(prog<1){prog=Math.min(1,prog+dt*.8);donut();bars();hist()}});
"""


def render_charts(eng: Engine) -> None:
    df = eng.df
    if df is None or "type" not in df.columns:
        st.info("data/trains.csv is needed for the fleet charts.")
        return
    share = [int((df["type"] == t).sum()) for t in TIERS]
    zones = []
    if "zone" in df.columns:
        ct = df.groupby(["zone", "type"]).size().unstack(fill_value=0)
        ct["tot"] = ct.sum(axis=1)
        for z, row in ct.sort_values("tot", ascending=False).head(10).iterrows():
            zones.append(dict(z=str(z), p=int(row.get("Pass", 0)), e=int(row.get("Exp", 0)), s=int(row.get("SF", 0))))
    bins = np.arange(0, 126, 6)
    hv = [np.histogram(df.loc[df["type"] == t, "speed"].clip(upper=125), bins=bins)[0].astype(int).tolist() for t in TIERS] if "speed" in df.columns else [[0] * 20] * 3
    P = dict(share=share, zones=zones, hist=dict(x=[int(b) for b in bins[:-1]], v=hv), tc=TIER_COLORS)
    legend = "".join(f'<span style="--c:{TIER_COLORS[i]}">{n}</span>' for i, n in enumerate(["Passenger", "Express", "Superfast"]))
    body = (f'<div class="g"><div class="c"><h4>Tier share</h4><canvas id="c1"></canvas><div class="lg">{legend}</div></div>'
            f'<div class="c"><h4>Busiest zones, split by tier</h4><canvas id="c2"></canvas></div>'
            f'<div class="c w"><h4>Where each tier sits on average speed</h4><canvas id="c3"></canvas><div class="lg">{legend}</div></div></div>')
    iframe(wrap_doc(body, CHART_CSS, CHART_JS.replace("__P__", jdump(P))), 640)


# ------------------------------------------------------------------------------
# 7g. Radar compare (two trains)  and  7h. project pipeline
# ------------------------------------------------------------------------------
RADAR_JS = r"""
const P=__P__;const r=fitCanvas($('#cv'),380),g=r.g,W=r.w,H=r.h,cx=W/2,cy=H/2+6,R=Math.min(W,H)*.34,n=P.ax.length;let prog=0;
const ang=i=>-Math.PI/2+i*6.2832/n;
loop(dt=>{prog=Math.min(1,prog+dt*.9);g.clearRect(0,0,W,H);g.strokeStyle='rgba(255,255,255,.14)';g.lineWidth=1;
 for(let k=1;k<=4;k++){g.beginPath();for(let i=0;i<n;i++){const a=ang(i);g.lineTo(cx+Math.cos(a)*R*k/4,cy+Math.sin(a)*R*k/4)}g.closePath();g.stroke()}
 g.fillStyle='#C9D4F2';g.font='600 13px Hind,sans-serif';g.textAlign='center';for(let i=0;i<n;i++){const a=ang(i);g.beginPath();g.moveTo(cx,cy);g.lineTo(cx+Math.cos(a)*R,cy+Math.sin(a)*R);g.stroke();g.fillText(P.ax[i],cx+Math.cos(a)*(R+34),cy+Math.sin(a)*(R+24)+4)}
 [[P.a,'#FFD21F'],[P.b,'#4DA3FF']].forEach(s=>{g.beginPath();s[0].v.forEach((v,i)=>{const a=ang(i),d=R*clamp(v,0,1)*easeOut(prog);g.lineTo(cx+Math.cos(a)*d,cy+Math.sin(a)*d)});g.closePath();g.fillStyle=rgba(s[1],.18);g.fill();g.strokeStyle=s[1];g.lineWidth=2.4;g.stroke();
  s[0].v.forEach((v,i)=>{const a=ang(i),d=R*clamp(v,0,1)*easeOut(prog);g.fillStyle=s[1];g.beginPath();g.arc(cx+Math.cos(a)*d,cy+Math.sin(a)*d,3.6,0,6.283);g.fill()})});
 g.textAlign='left';g.font='700 14px Rajdhani,sans-serif';g.fillStyle='#FFD21F';g.fillText(P.a.n,10,18);g.fillStyle='#4DA3FF';g.fillText(P.b.n,10,36)});
"""


def render_radar(axes: list, a: dict, b: dict) -> None:
    iframe(wrap_doc('<canvas id="cv" style="width:100%"></canvas>', "body{padding:2px}", RADAR_JS.replace("__P__", jdump(dict(ax=axes, a=a, b=b)))), 392)


PIPE_CSS = r"""
body{padding:4px}.pp{position:relative;padding:34px 0 8px}.ln{position:absolute;left:3%;right:3%;top:48px;height:5px;background:repeating-linear-gradient(90deg,#5b6684 0 14px,#26304f 14px 18px);border-radius:3px}
.st{display:grid;grid-template-columns:repeat(8,1fr);gap:6px;position:relative}.s{text-align:center;opacity:.45;transition:all .5s;padding:0 2px}.s.on{opacity:1}
.dot{width:30px;height:30px;border-radius:50%;margin:0 auto 10px;background:#0B1530;border:3px solid #5b6684;display:flex;align-items:center;justify-content:center;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:13px;position:relative;z-index:2;transition:all .4s}
.s.on .dot{border-color:#FFD21F;color:#FFD21F;box-shadow:0 0 16px rgba(255,210,31,.6)}.s b{display:block;font-family:'Rajdhani',sans-serif;font-size:16px;line-height:1.1}.s span{font-size:12px;color:#9AA8CC;line-height:1.3;display:block;margin-top:2px}
.tr{position:absolute;top:0;left:3%;font-size:26px;transition:left 1s ease;z-index:3}
@media (max-width:760px){.st{grid-template-columns:repeat(4,1fr);row-gap:20px}.ln,.tr{display:none}}
"""
PIPE_JS = r"""
const S=$$('.s'),tr=$('#tr');let i=0;
function go(){S.forEach((s,k)=>s.classList.toggle('on',k<=i));tr.style.left=(3+(94*(i+.5)/S.length)-1.5)+'%';i=(i+1)%(S.length+2);if(i===0)S.forEach(s=>s.classList.remove('on'));setTimeout(go,REDUCED?400:1100)}
go();
"""


def render_pipeline() -> None:
    st_ = [("Raw JSON", f"{FACTS['raw']:,} trains from Kaggle"), ("Clean", f"{FACTS['clean']:,} trains: Pass, Exp, SF"), ("Engineer", "total_duration fix, 26 features"),
           ("Split", f"{FACTS['train']:,} train / {FACTS['test']} test, stratified"), ("Compare", "Tree, KNN, SVM, NB, dummy"),
           ("Champion", f"Decision Tree {FACTS['acc']:.2f}%"), ("Cluster", "K-Means k=5 and DBSCAN"), ("Deploy", "this Streamlit app")]
    cells = "".join(f'<div class="s"><div class="dot">{i + 1}</div><b>{n}</b><span>{d}</span></div>' for i, (n, d) in enumerate(st_))
    body = f'<div class="pp"><div class="tr" id="tr">🚆</div><div class="ln"></div><div class="st">{cells}</div></div>'
    iframe(wrap_doc(body, PIPE_CSS, PIPE_JS), 170)


# ------------------------------------------------------------------------------
# 7i. Live journey: an NTES-style running-status board with a time-warp slider
# ------------------------------------------------------------------------------
# Named junctions on the trunk corridors. Stops are found by routing over the CORRIDORS graph,
# so the halts follow the real corridor (for example Mumbai to Delhi goes via Surat, Vadodara,
# Ratlam, Kota and Mathura) instead of a straight line. They are illustrative, not a timetable.
WP_NAMES = {
    (77.68, 27.49): "Mathura Jn", (75.84, 25.18): "Kota Jn", (75.04, 23.33): "Ratlam Jn", (73.18, 22.31): "Vadodara Jn", (72.84, 21.21): "Surat",
    (80.35, 26.45): "Kanpur Central", (81.83, 25.44): "Prayagraj Jn", (83.12, 25.28): "Pt DD Upadhyaya Jn", (84.99, 24.80): "Gaya Jn", (86.43, 23.80): "Dhanbad Jn",
    (73.87, 18.53): "Pune Jn", (75.90, 17.67): "Solapur", (77.35, 16.20): "Raichur Jn", (77.37, 15.17): "Guntakal Jn", (79.50, 13.63): "Renigunta Jn",
    (87.32, 22.34): "Kharagpur Jn", (86.93, 21.49): "Balasore", (85.84, 20.27): "Bhubaneswar", (83.29, 17.72): "Visakhapatnam", (80.62, 16.52): "Vijayawada Jn",
    (78.02, 27.16): "Agra Cantt", (78.57, 25.45): "Jhansi Jn", (77.41, 23.27): "Bhopal Jn", (79.09, 21.15): "Nagpur", (79.60, 17.97): "Warangal",
    (75.78, 21.05): "Bhusawal Jn", (81.63, 21.25): "Raipur Jn", (82.14, 22.08): "Bilaspur Jn", (76.78, 30.37): "Ambala Cantt", (75.85, 30.90): "Ludhiana Jn",
    (74.87, 31.63): "Amritsar Jn", (74.87, 32.71): "Jammu Tawi", (75.79, 26.92): "Jaipur Jn", (74.64, 26.45): "Ajmer Jn", (72.78, 24.48): "Abu Road",
    (88.14, 25.00): "Malda Town", (88.43, 26.68): "New Jalpaiguri", (91.75, 26.18): "Guwahati", (94.91, 27.48): "Dibrugarh",
    (73.30, 16.99): "Ratnagiri", (73.97, 15.27): "Madgaon Jn", (74.84, 12.87): "Mangaluru Central", (75.78, 11.25): "Kozhikode", (76.29, 9.97): "Ernakulam Jn",
    (76.95, 8.49): "Thiruvananthapuram Central", (78.70, 10.80): "Tiruchirappalli Jn", (78.11, 9.92): "Madurai Jn", (77.54, 8.08): "Kanyakumari",
    (79.13, 12.93): "Katpadi Jn", (78.77, 28.84): "Moradabad Jn", (80.92, 26.83): "Lucknow Charbagh", (83.37, 26.75): "Gorakhpur Jn",
}


@st.cache_resource(show_spinner=False)
def rail_graph():
    nodes, adj = [], {}

    def nid(lon, lat):
        for i, (x, y, n) in enumerate(nodes):
            if abs(x - lon) < 0.35 and abs(y - lat) < 0.35:
                if not n and (lon, lat) in WP_NAMES:
                    nodes[i] = (x, y, WP_NAMES[(lon, lat)])
                return i
        nodes.append((lon, lat, WP_NAMES.get((lon, lat), "")))
        return len(nodes) - 1

    for _, pts in CORRIDORS:
        ids = [nid(*p) for p in pts]
        for a, b in zip(ids, ids[1:]):
            if a != b:
                d = haversine_km(nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1]) * 1.15
                adj.setdefault(a, []).append((b, d))
                adj.setdefault(b, []).append((a, d))
    return nodes, adj


def route_stops(a_code: str, b_code: str, total_km: float) -> list:
    """[(name, km)] from station A to station B along the corridor graph, scaled to total_km."""
    import heapq
    A, B = STATION_BY_CODE[a_code], STATION_BY_CODE[b_code]
    direct = [(A[1], 0.0), (B[1], float(total_km))]
    nodes, adj = rail_graph()
    near = lambda s: min(range(len(nodes)), key=lambda i: haversine_km(nodes[i][0], nodes[i][1], s[3], s[4]))
    i0, i1 = near(A), near(B)
    if i0 == i1 or haversine_km(nodes[i0][0], nodes[i0][1], A[3], A[4]) > 170 or haversine_km(nodes[i1][0], nodes[i1][1], B[3], B[4]) > 170:
        return direct
    dist, prev, heap = {i0: 0.0}, {}, [(0.0, i0)]
    while heap:
        d, u = heapq.heappop(heap)
        if u == i1:
            break
        if d > dist.get(u, 1e18):
            continue
        for v, w in adj.get(u, []):
            if d + w < dist.get(v, 1e18):
                dist[v], prev[v] = d + w, u
                heapq.heappush(heap, (d + w, v))
    if i1 not in dist:
        return direct
    path = [i1]
    while path[-1] != i0:
        path.append(prev[path[-1]])
    path.reverse()
    scale = total_km / max(dist[i1], 1.0)
    out = [(A[1], 0.0)]
    for n in path[1:-1]:
        nm = nodes[n][2]
        if nm and nm not in (A[1], B[1]) and nm not in [o[0] for o in out]:
            out.append((nm, dist[n] * scale))
    out.append((B[1], float(total_km)))
    if len(out) > 12:
        keep = {0, len(out) - 1} | {round(i * (len(out) - 1) / 11) for i in range(12)}
        out = [o for i, o in enumerate(out) if i in keep]
    return out


JR_CSS = r"""
body{padding:4px}.jr{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(250px,1fr);gap:18px}
.tl{position:relative;padding-left:56px}.tl:before{content:'';position:absolute;left:22px;top:20px;bottom:20px;width:6px;background:#2a3350;border-radius:3px}
.fill{position:absolute;left:22px;top:20px;width:6px;background:linear-gradient(180deg,#FB792B,#FFD21F);border-radius:3px;height:0}
.rw{position:relative;height:64px;display:flex;align-items:center}
.rw .dt{position:absolute;left:-44px;width:22px;height:22px;border-radius:50%;background:#0B1530;border:3px solid #5b6684;transition:all .3s}
.rw.ps .dt{background:#34D399;border-color:#34D399;box-shadow:0 0 12px rgba(52,211,153,.6)}
.rw .nm{font-family:'Rajdhani',sans-serif;font-size:19px;font-weight:700;line-height:1.1}.rw .sb{font-size:12.5px;color:#9AA8CC}
.rw .tm{margin-left:auto;text-align:right;font-family:'Rajdhani',sans-serif;font-size:19px;font-weight:600}.rw .tm small{display:block;font-size:11.5px;color:#9AA8CC;font-family:'Hind',sans-serif;font-weight:400}
.rw.ps .nm{color:#34D399}
.trn{position:absolute;left:8px;top:0;font-size:26px;z-index:3;filter:drop-shadow(0 3px 6px rgba(0,0,0,.6))}
aside{background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:16px 18px;align-self:start;position:sticky;top:6px}
.now{font-family:'Rajdhani',sans-serif;font-size:27px;line-height:1.1;font-weight:700;color:#FFD21F}.sub{font-size:13.5px;color:#C9D4F2;margin:6px 0 12px;line-height:1.45}
input[type=range]{width:100%;accent-color:#FB792B}.ctl{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
.ctl button,.ctl select{background:rgba(255,255,255,.07);color:#EAF0FF;border:1px solid rgba(255,255,255,.2);border-radius:10px;padding:7px 14px;font-size:13.5px}.ctl button.p{background:#FFD21F;color:#14110A;border:0;font-weight:600}
.bar{position:relative;height:8px;background:rgba(255,255,255,.1);border-radius:5px;margin:22px 0 6px}.bar i{display:block;height:100%;width:0;border-radius:5px;background:linear-gradient(90deg,#FB792B,#FFD21F)}.bar u{position:absolute;top:-17px;left:0;text-decoration:none;font-size:20px;margin-left:-10px}
.kp{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px}.kp div{background:rgba(255,255,255,.05);border-radius:10px;padding:8px 10px;font-size:12px;color:#9AA8CC}.kp b{display:block;font-family:'Rajdhani',sans-serif;font-size:19px;color:#EAF0FF}
@media (max-width:780px){.jr{grid-template-columns:1fr}aside{position:static}}
"""
JR_JS = r"""
const P=__P__;const tl=$('#tl'),RH=64;let m=0,playing=false;
P.stops.forEach((s,i)=>{const r=document.createElement('div');r.className='rw';r.id='r'+i;r.innerHTML='<div class="dt"></div><div><div class="nm">'+s.n+'</div><div class="sb">'+(i===0?'Origin':i===P.stops.length-1?'Destination':'Halt')+' | '+Math.round(s.km)+' km</div></div><div class="tm">'+s.clk+'<small>'+(s.day?'+'+s.day+' day':P.date)+'</small></div>';tl.appendChild(r)});
const fill=document.createElement('div');fill.className='fill';tl.appendChild(fill);const trn=document.createElement('div');trn.className='trn';trn.textContent='🚆';tl.appendChild(trn);
let lastPassed=-1;
function fmt(mins){const d=new Date(P.t0+mins*60000);return d.toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit',timeZone:'UTC'})}
function upd(){m=clamp(m,0,P.total);let seg=0;for(let i=0;i<P.stops.length-1;i++)if(m>=P.stops[i].m)seg=i;const a=P.stops[seg],b=P.stops[seg+1],f=clamp((m-a.m)/Math.max(1,b.m-a.m),0,1),km=lerp(a.km,b.km,f);
 const cy=(seg+f)*RH+RH/2;trn.style.top=(cy-16)+'px';fill.style.height=Math.max(0,cy-20)+'px';
 P.stops.forEach((s,i)=>$('#r'+i).classList.toggle('ps',m>=s.m&&i>0||i===0&&m>0));const passed=P.stops.filter(s=>m>=s.m).length-1;if(passed!==lastPassed){if(passed>0)RailAudio.click();lastPassed=passed}
 const done=m>=P.total;$('#now').textContent=done?'Arrived at '+P.stops[P.stops.length-1].n:(m<=0?'Ready at '+a.n:'Between '+a.n+' and '+b.n);
 $('#sub').innerHTML=done?'Journey complete in '+Math.floor(P.total/60)+'h '+(P.total%60)+'m. Running on time (schedule simulation).':'Clock '+fmt(m)+' | '+Math.round(km)+' of '+Math.round(P.km)+' km covered | next halt '+b.n+' at '+b.clk+'. Running on time.';
 $('#bi').style.width=(m/P.total*100)+'%';$('#bt').style.left=(m/P.total*100)+'%';$('#rg').value=m;$('#k1').textContent=Math.round(km)+' km';$('#k2').textContent=Math.round(m/P.total*100)+'%';
 $('#k3').textContent=Math.round(P.km/Math.max(P.total,1)*60)+' km/h';$('#k4').textContent=done?'0 min':Math.floor((P.total-m)/60)+'h '+Math.round((P.total-m)%60)+'m'}
$('#rg').max=P.total;$('#rg').oninput=e=>{m=+e.target.value;upd()};
$('#pp').onclick=()=>{if(m>=P.total)m=0;playing=!playing;$('#pp').textContent=playing?'Pause':'Play'};$('#rs').onclick=()=>{m=0;playing=false;$('#pp').textContent='Play';upd()};
loop(dt=>{if(playing){m+=dt*(+$('#wp').value);if(m>=P.total){m=P.total;playing=false;$('#pp').textContent='Play'}upd()}});upd();
"""


def render_journey(R: dict, stops: list) -> None:
    a, total = R["a"], R["total"]
    rows = []
    for name, km in stops:
        mins = total * km / max(a["d"], 1)
        t = R["dep"] + timedelta(minutes=mins)
        rows.append(dict(n=name, km=round(km, 1), m=round(mins, 1), clk=t.strftime("%H:%M"), day=(t.date() - R["dep"].date()).days))
    P = dict(stops=rows, total=total, km=a["d"], date=R["dep"].strftime("%a, %d %b"), t0=int(R["dep"].replace(tzinfo=timezone.utc).timestamp() * 1000))
    body = ('<div class="jr"><div class="tl" id="tl"></div><aside><div class="now" id="now"></div><div class="sub" id="sub"></div>'
            '<div class="bar"><i id="bi"></i><u id="bt">🚆</u></div><input type="range" id="rg" min="0" max="100" value="0" aria-label="Journey time">'
            '<div class="ctl"><button class="p" id="pp">Play</button><select id="wp" aria-label="Time warp"><option value="30">1 s = 30 min</option><option value="90" selected>1 s = 1.5 h</option>'
            '<option value="240">1 s = 4 h</option></select><button id="rs">Reset</button></div>'
            '<div class="kp"><div><b id="k1">0 km</b>covered</div><div><b id="k2">0%</b>of the journey</div><div><b id="k3">-</b>average speed</div><div><b id="k4">-</b>time to go</div></div></aside></div>')
    iframe(wrap_doc(body, JR_CSS, JR_JS.replace("__P__", jdump(P)), libs=JS_AUDIO), max(430, 80 + 64 * len(rows) + 40))


def page_journey(eng: Engine, R: dict) -> None:
    section("Live journey", "A running-status board for your schedule. Drag the slider or press Play to fast-forward the clock.")
    ss = st.session_state
    codes = [s[0] for s in STATIONS]
    ss.setdefault("jr_from", R["a"].get("a") or "MMCT")
    ss.setdefault("jr_to", R["a"].get("b") or "NDLS")
    fmt = lambda c: f"{STATION_BY_CODE[c][1]} ({c})"
    c1, c2, c3 = st.columns([1, 1, 1])
    c1.selectbox("From", codes, format_func=fmt, key="jr_from")
    c2.selectbox("To", codes, format_func=fmt, key="jr_to")
    c3.markdown(f'<div class="rd-note" style="padding-top:26px">Using your schedule: <b>{R["a"]["d"]} km</b> in <b>{fmt_dur(R["total"])}</b>, departing <b>{R["dep"].strftime("%H:%M")}</b></div>', unsafe_allow_html=True)
    if ss.jr_from == ss.jr_to:
        st.info("Pick two different stations.")
        return
    stops = route_stops(ss.jr_from, ss.jr_to, R["a"]["d"])
    render_journey(R, stops)
    st.caption("Halts are found by routing over the trunk-corridor graph, so they follow the real corridor, but they are illustrative: an actual train's halts depend on its timetable.")


# ==============================================================================
# 8. PAGES
# ==============================================================================
PAGES = ["🎫 Classify", "🧠 Junction", "🗺️ Network", "🛤️ Journey", "🌌 Galaxy", "🔬 What-If", "🔎 Explorer", "📦 Batch", "🏁 Arena", "🎓 Viva"]
FORM_FLAGS = ["f_1a", "f_2a", "f_3a", "f_cc", "f_sl", "f_fc"]  # same order as CLASS_DEF / FLAG_KEYS
CHIP = dict(SF="sf", Exp="exp", Pass="pass")


# ---- state helpers and callbacks (callbacks run BEFORE the script reruns) -----------------
def zone_options(eng: Engine) -> list:
    zs = eng.zones or list(ZONE_INFO)
    pri = [z for z in PRIORITY_ZONES if z in zs]
    return pri + sorted(z for z in zs if z not in pri)


def active_from_preset(i: int) -> dict:
    p = PRESETS[i]
    return dict(d=p["d"], h=p["h"], m=p["m"], z=p["z"], c=tuple(bool(x) for x in p["c"]), t=p["t"], a=p["a"], b=p["b"], dep=p["dep"],
                dt=date.today().isoformat(), fa="", ta="", off="", no="")


def push_widgets(a: dict) -> None:
    ss = st.session_state
    zones = zone_options(get_engine())
    ss.f_d, ss.f_h, ss.f_m = int(a["d"]), int(a["h"]), int(a["m"])
    ss.f_z = a["z"] if a["z"] in zones else ("Unknown" if "Unknown" in zones else zones[0])
    for k, v in zip(FORM_FLAGS, a["c"]):
        ss[k] = bool(v)
    hh, mm = (a["dep"] or "08:00").split(":")[:2]
    ss.f_dep = datetime.strptime(f"{hh}:{mm}", "%H:%M").time()
    ss.f_dt = date.fromisoformat(a["dt"])


def sync_form_from_active() -> None:
    """Widget keys vanish when their page is not shown; rebuild them from the active schedule."""
    if "f_d" not in st.session_state or "f_dep" not in st.session_state:
        push_widgets(st.session_state.active)


def cb_preset(i: int) -> None:
    a = active_from_preset(i)
    st.session_state.active = a
    push_widgets(a)
    st.session_state.reveal = True


def cb_submit() -> None:
    ss = st.session_state
    old = ss.active
    new = dict(old)
    new.update(d=int(ss.f_d), h=int(ss.f_h), m=int(ss.f_m), z=ss.f_z, c=tuple(bool(ss[k]) for k in FORM_FLAGS),
               dep=ss.f_dep.strftime("%H:%M"), dt=ss.f_dt.isoformat())
    if (new["d"], new["h"], new["m"], new["z"], new["c"]) != (old["d"], old["h"], old["m"], old["z"], old["c"]):
        new.update(t="Custom schedule", fa="", ta="", off="", no="")
    ss.active, ss.reveal = new, True


def cb_apply_route(kf: str, kt: str) -> None:
    ss = st.session_state
    ca, cb_ = ss[kf], ss[kt]
    km = est_rail_km(ca, cb_)
    if not km:
        return
    eng = get_engine()
    zone = STATION_BY_CODE[ca][2]
    zone = zone if (not eng.zones or zone in eng.zones) else "Unknown"
    h, m = divmod(min(km, 72 * 60), 60)
    a = dict(ss.active)
    a.update(d=km, h=h, m=m, z=zone, a=ca, b=cb_, fa="", ta="", off="", no="", t=f"{STATION_BY_CODE[ca][1]} to {STATION_BY_CODE[cb_][1]}")
    ss.active, ss.reveal = a, True
    push_widgets(a)


def cb_load_train() -> None:
    ss = st.session_state
    idx = ss.get("_ex_map", {}).get(ss.get("ex_pick"))
    eng = get_engine()
    if idx is None or eng.df is None:
        return
    a = active_from_row(eng.df.loc[idx])
    ss.active, ss.reveal = a, True
    push_widgets(a)
    ss.nav = PAGES[0]


def cb_nav(page: str) -> None:
    st.session_state.nav = page


def rake_html(R: dict) -> str:
    """Platform-style coach position strip: engine first, guard van last."""
    meta = TIER_META[R["tier"]]
    loco = dict(aero="Aero set", wap7="WAP-7", wdm="Diesel")[meta["loco"]]
    cells = f'<div class="c e" style="background:{meta["color"]};color:#14110A">Engine<small>{loco}</small></div>'
    for i, c in enumerate(build_consist(R["a"], R["tier"])):
        cells += f'<div class="c" style="background:{c["c"]};animation-delay:{(i + 1) * 70}ms">{esc(c["l"])}<small>{esc(c["k"])}</small></div>'
    return f'<div class="rd-panel"><h4>Coach position</h4><div class="rake">{cells}</div><div class="rd-note">Engine on the left, guard van on the right, like a platform coach indicator.</div></div>'


# ---- page 1: classify ----------------------------------------------------------------------
def page_classify(eng: Engine, R: dict) -> None:
    ss = st.session_state
    sync_form_from_active()
    if R["bug"]:
        st.warning("Legacy bug mode is ON: the model is fed only duration_m (0-59) instead of total_duration. Switch it off in the sidebar.")
    render_led(R)

    with st.expander("Route assist: choose From and To to fill distance and zone", expanded=False):
        codes = [s[0] for s in STATIONS]
        c1, c2, c3 = st.columns([1, 1, 0.8])
        fmt = lambda c: f"{STATION_BY_CODE[c][1]} ({c})"
        c1.selectbox("From station", codes, format_func=fmt, key="ra_from")
        c2.selectbox("To station", codes, format_func=fmt, key="ra_to")
        km = est_rail_km(ss.ra_from, ss.ra_to)
        c3.markdown(f'<div class="rd-note" style="padding-top:28px">Estimated rail distance<br><b style="font-size:1.5rem;color:#FFD21F">{km or "-"} km</b></div>', unsafe_allow_html=True)
        sx(st.button, "Apply route to the form", key="btn_route", on_click=cb_apply_route, args=("ra_from", "ra_to"), disabled=not km)
        st.caption("Distance is the great-circle distance x 1.22 (a rough rail estimate) and duration is set for about 60 km/h. Tune both below.")

    st.markdown("**Quick scenarios**")
    cols = st.columns(len(PRESETS))
    for i, (col, p) in enumerate(zip(cols, PRESETS)):
        with col:
            sx(st.button, p["label"], key=f"pre{i}", on_click=cb_preset, args=(i,))

    if eng.df is not None and len(eng.df):
        with st.expander("Load a real train from the dataset", expanded=False):
            d = eng.df
            lab = (d["number"].astype(str) + "  " + d["name"].astype(str).str.title() + "  [" + d["type"].astype(str) + ", " + d["zone"].astype(str) + "]").tolist() if {"number", "name", "type", "zone"} <= set(d.columns) else []
            if lab:
                ss["_ex_map"] = dict(zip(lab, d.index))
                st.selectbox("Pick any of the real trains", lab, key="ex_pick")
                sx(st.button, "Load this train into the form", key="btn_load", on_click=cb_load_train)

    zones = zone_options(eng)
    with st.form("booking"):
        st.markdown("#### Schedule details")
        left, right = st.columns([1.2, 1], gap="large")
        with left:
            st.slider("Route distance (km)", 10, 4500, step=5, key="f_d")
            a1, a2 = st.columns(2)
            a1.slider("Duration: hours", 0, 72, key="f_h")
            a2.slider("Duration: minutes", 0, 59, key="f_m")
            b1, b2 = st.columns(2)
            b1.time_input("Departure time", key="f_dep", step=300)
            b2.date_input("Journey date", key="f_dt")
        with right:
            st.selectbox("Railway zone", zones, key="f_z", format_func=lambda z: f"{z} - {ZONE_INFO.get(z, (z,))[0]}")
            st.markdown("**Coach classes on the rake**")
            k1, k2 = st.columns(2)
            k1.checkbox("First AC (1A)", key="f_1a")
            k1.checkbox("Second AC (2A)", key="f_2a")
            k1.checkbox("Third AC (3A)", key="f_3a")
            k2.checkbox("AC Chair Car (CC)", key="f_cc")
            k2.checkbox("Sleeper (SL)", key="f_sl")
            k2.checkbox("First Class (FC)", key="f_fc")
        sx(st.form_submit_button, "Classify and stamp the ticket", type="primary", on_click=cb_submit)

    platform_line()
    reveal = bool(ss.get("reveal"))
    ss["reveal"] = False
    left, right = st.columns([1.55, 1], gap="large")
    with left:
        doc = render_ticket(R, ss.get("sb_pa", PA_MODES[0]), reveal, ss.get("sb_voice", ""))
        sx(st.download_button, "Download ticket (HTML)", data=doc, file_name=f"raildrishti_{R['pnr']}.html", mime="text/html", key="dl_ticket")
    with right:
        render_html("<div class='rd-sec'><h3>Advisory engine</h3></div>" + advisory_html(R["adv"]))
        render_html(rake_html(R))
        cl = CLUSTER_PROFILES.get(R["cluster"]["id"], CLUSTER_PROFILES[4])
        out = ('<span class="rd-chip bad">Far from every centroid: behaves like a DBSCAN noise train</span>' if R["cluster"]["outlier"] else "")
        render_html(f'<div class="rd-panel" style="border-left:5px solid {cl["color"]}"><h4>Fleet segment {cl["code"]}: {esc(cl["name"])}</h4>'
                    f'<div class="rd-note">{esc(cl["summary"])}</div><div style="margin-top:8px">{out}</div></div>')
        if len(R["neigh"]):
            rows = "".join(
                f'<tr><td>{esc(r.get("number", ""))}<br><span class="rd-note">{esc(str(r.get("name", ""))[:26])}</span></td>'
                f'<td><span class="rd-chip {CHIP.get(str(r.get("type")), "")}">{esc(r.get("type", ""))}</span></td><td>{int(r.get("distance", 0))} km</td>'
                f'<td>{float(r.get("speed", 0)):.0f}</td><td><b>{int(r["match"])}%</b></td></tr>' for _, r in R["neigh"].iterrows())
            render_html('<div class="rd-panel"><h4>Five most similar real trains</h4><table class="rd-tbl"><tr><th>Train</th><th>Tag</th><th>Dist</th><th>km/h</th><th>Match</th></tr>'
                        + rows + "</table></div>")
        sx(st.button, "Open the decision junction", key="go_j", on_click=cb_nav, args=(PAGES[1],))


# ---- page 2: junction ----------------------------------------------------------------------
def page_junction(eng: Engine, R: dict) -> None:
    section("Decision junction", "Every Decision Tree prediction is a journey through yes/no junctions. This is the exact route your schedule took.")
    if not R["steps"]:
        st.info("The saved model is not a single decision tree, so the path cannot be drawn.")
    else:
        render_junction(R, eng)
    platform_line()
    section("Bug forensics", "The raw dataset's duration_m held only the minute remainder. See what the model says with and without the engineering fix.")
    a = R["a"]
    Xb, _ = eng.vector(a, bug=True)
    Pb = eng.proba(Xb)[0]
    tb = str(eng.labels(Xb)[0])
    cb_, ca_ = Pb[TIERS.index(tb)] * 100 if tb in TIERS else 0, R["conf"]
    c1, c2 = st.columns(2, gap="large")
    c1.markdown(f'<div class="rd-adv warn"><span class="ic">🐞</span><div><span class="tt">Before the fix: model sees {a["m"]} min</span>It ignores {a["h"]} hours. '
                f'Prediction: <b>{TIER_META.get(tb, TIER_META["Exp"])["name"]}</b> at {cb_:.1f}% confidence.</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="rd-adv ok"><span class="ic">🔧</span><div><span class="tt">After the fix: model sees {R["total"]} min</span>total_duration = {a["h"]} x 60 + {a["m"]}. '
                f'Prediction: <b>{TIER_META[R["tier"]]["name"]}</b> at {ca_:.1f}% confidence.</div></div>', unsafe_allow_html=True)
    with st.expander("The 26-feature input vector (raw and scaled)", expanded=False):
        vec = pd.DataFrame({"raw value": R["X"].iloc[0], "scaled value": R["Xs"].iloc[0]})
        sx(st.dataframe, vec[(vec["raw value"] != 0) | (vec.index.isin(["distance", "total_duration"]))].round(4))
        st.caption(f"Model expects scaled input: {not eng.use_raw}. Class mapping: {eng.cal['mapping']}.")


# ---- page 3: network -----------------------------------------------------------------------
def page_network(eng: Engine, R: dict) -> None:
    section("Rail network radar", "Zone headquarters, trunk corridors and moving trains. Pick a route to draw it and estimate its distance.")
    ss = st.session_state
    codes = [s[0] for s in STATIONS]
    ss.setdefault("nw_from", R["a"].get("a") or "MMCT")
    ss.setdefault("nw_to", R["a"].get("b") or "NDLS")
    fmt = lambda c: f"{STATION_BY_CODE[c][1]} ({c})"
    c1, c2, c3 = st.columns([1, 1, 1])
    c1.selectbox("From", codes, format_func=fmt, key="nw_from")
    c2.selectbox("To", codes, format_func=fmt, key="nw_to")
    km = est_rail_km(ss.nw_from, ss.nw_to)
    with c3:
        st.markdown(f'<div class="rd-note" style="padding-top:26px">Estimated rail distance<br><b style="font-size:1.5rem;color:#FFD21F">{km or "-"} km</b></div>', unsafe_allow_html=True)
    route = dict(a=ss.nw_from, b=ss.nw_to) if km else None
    render_network(R, eng, route)
    cc1, cc2 = st.columns([1, 2])
    with cc1:
        sx(st.button, "Send this route to the classifier", key="nw_send", on_click=cb_apply_route, args=("nw_from", "nw_to"), disabled=not km)
    with cc2:
        z = ZONE_INFO.get(R["a"]["z"], ZONE_INFO["Unknown"])
        st.caption(f"Highlighted zone: {R['a']['z']} - {z[0]} ({z[2]}), headquartered at {z[1]}.")


# ---- page 4: galaxy ------------------------------------------------------------------------
def cluster_dna(eng: Engine) -> pd.DataFrame:
    sp, dfc = eng.space, eng.dfc
    if not sp.ok:
        return pd.DataFrame()
    X = dfc[sp.use].astype(float).to_numpy()
    if sp.scaled and eng.scaler is not None and len(sp.use) == len(eng.cols):
        try:
            X = eng.scaler.inverse_transform(X)
        except Exception:
            pass
    raw = pd.DataFrame(X, columns=sp.use)
    raw["cluster"] = sp.lab
    rows = []
    zc = [c for c in sp.use if c.startswith("zone_")]
    for cid in sp.ids:
        g = raw[raw["cluster"] == cid]
        top = g[zc].mean().idxmax()[5:] if zc else "-"
        pr = CLUSTER_PROFILES.get(cid, CLUSTER_PROFILES[4])
        rows.append({"Segment": f"{pr['code']} {pr['name']}", "Trains": len(g), "Avg km": round(g["distance"].mean()) if "distance" in g else None,
                     "Avg duration": fmt_dur(g["total_duration"].mean()) if "total_duration" in g else "-",
                     "3A %": round(g["third_ac"].mean() * 100) if "third_ac" in g else None, "Sleeper %": round(g["sleeper"].mean() * 100) if "sleeper" in g else None,
                     "Top zone": top})
    return pd.DataFrame(rows)


def page_galaxy(eng: Engine, R: dict) -> None:
    section("Fleet galaxy", "Unsupervised learning groups trains that look alike, with no labels used. Your schedule is the star.")
    render_html(f'<div class="rd-kpis"><div class="k"><b>{FACTS["km_k"]}</b><span>K-Means clusters (elbow)</span></div><div class="k"><b>{FACTS["km_sil"]:.4f}</b><span>K-Means silhouette</span></div>'
                f'<div class="k"><b>{FACTS["db_sil"]:.4f}</b><span>DBSCAN silhouette</span></div><div class="k"><b>{FACTS["db_noise"]}</b><span>DBSCAN noise trains (0.4%)</span></div></div>')
    render_galaxy(R, eng)
    cl = CLUSTER_PROFILES.get(R["cluster"]["id"], CLUSTER_PROFILES[4])
    render_html(f'<div class="rd-panel" style="border-left:5px solid {cl["color"]}"><h4>Your schedule lives in {cl["code"]}: {esc(cl["name"])}</h4>'
                f'<div class="rd-note">{esc(cl["summary"])} Main corridor: {esc(cl["zone"])}.</div></div>')
    dna = cluster_dna(eng)
    if len(dna):
        st.markdown("##### Segment DNA, computed from the clustered file")
        sx(st.dataframe, dna, hide_index=True)
    platform_line()
    section("Fleet at a glance", "Tier share, busiest zones and the speed profile of each tier, straight from trains.csv.")
    render_charts(eng)


# ---- page 5: what-if lab -------------------------------------------------------------------
def find_flips(eng: Engine, R: dict) -> list:
    """Smallest single changes that move the schedule into another tier (coach toggles + duration)."""
    a, cur, total = R["a"], R["tier"], R["total"]
    out, rank = [], lambda t: TIER_META[t]["rank"]

    def card(t, title, body):
        out.append(dict(level="up" if rank(t) > rank(cur) else "warn", title=title, body=body))

    vs = []
    for i in range(6):
        c = list(a["c"])
        c[i] = not c[i]
        vs.append(tuple(c))
    Xv = pd.concat([eng.vector({**a, "c": c})[0] for c in vs], ignore_index=True)
    labs, P = eng.labels(Xv), eng.proba(Xv)
    for i, (key, code, lab, col) in enumerate(CLASS_DEF):
        if labs[i] != cur and labs[i] in TIERS:
            verb = "Add" if vs[i][i] else "Remove"
            card(labs[i], f"{verb} {lab} ({code}): becomes {TIER_META[labs[i]]['name']}", f"With that one coach class changed the model is {P[i].max() * 100:.0f}% sure of the new tier.")
    mult = np.linspace(0.35, 2.2, 371)
    tot = np.maximum(total * mult, 20.0)
    lab = eng.labels(eng.frame_grid(a, np.full(len(tot), float(a["d"])), tot))
    i0 = int(np.argmin(np.abs(mult - 1.0)))
    for name, rng_ in (("faster", range(i0 - 1, -1, -1)), ("slower", range(i0 + 1, len(mult)))):
        for i in rng_:
            if lab[i] != cur and lab[i] in TIERS:
                spd = a["d"] / (tot[i] / 60.0)
                diff = int(round(abs(tot[i] - total)))
                verb = f"Cut {fmt_dur(diff)} from the schedule" if name == "faster" else f"Stretch the schedule by {fmt_dur(diff)}"
                card(lab[i], f"{verb}: becomes {TIER_META[lab[i]]['name']}", f"New duration {fmt_dur(tot[i])}, that is {spd:.1f} km/h on {a['d']} km.")
                break
    return out


def page_whatif(eng: Engine, R: dict) -> None:
    section("What-if lab", "Probe the model: where are its tier boundaries, and what is the smallest change that flips your verdict?")
    st.markdown("##### Decision atlas: predicted tier for every distance and average speed")
    st.caption("Same coaches and zone as your active schedule. Brighter cells mean higher confidence. Hover to inspect a cell.")
    render_atlas(R, eng)
    platform_line()
    section("Flip finder", "Single changes that would move this schedule to another tier.")
    flips = find_flips(eng, R)
    if flips:
        render_html(advisory_html(flips))
    else:
        render_html(advisory_html([dict(level="ok", title="A stable verdict", body="No single coach toggle or duration change within -65% to +120% flips the tier.")]))
    platform_line()
    section("Coach combination matrix", "All 64 combinations of the six coach classes, with your distance, duration and zone held fixed.")
    combos = [tuple(bool((n >> k) & 1) for k in range(6)) for n in range(64)]
    Xc = pd.concat([eng.vector({**R["a"], "c": c})[0] for c in combos], ignore_index=True)
    lc, pc = eng.labels(Xc), eng.proba(Xc)
    tiles = ""
    for i, c in enumerate(combos):
        t = lc[i] if lc[i] in TIERS else "Exp"
        codes = " ".join(code for (k, code, lab, col), on in zip(CLASS_DEF, c) if on) or "none"
        meta = TIER_META[t]
        cur = " cur" if c == tuple(R["a"]["c"]) else ""
        tiles += (f'<div class="t{cur}" title="{esc(codes)}: {meta["name"]} {pc[i].max() * 100:.0f}%" style="border-color:{meta["color"]};'
                  f'background:rgba({meta["rgb"]},.14);animation-delay:{i * 14}ms"><b>{esc(codes)}</b><span style="color:{meta["color"]}">{meta["short"]}</span></div>')
    render_html(f'<div class="rd-coach">{tiles}</div>')
    st.caption("White outline = your current combination.")
    platform_line()
    section("Speed sweep", "Hold distance and coaches fixed and only change how fast the schedule runs.")
    rows = []
    for spd in (20, 30, 40, 50, 55, 60, 70, 80, 100):
        mins = int(round(R["a"]["d"] / spd * 60))
        h, m = divmod(min(mins, 72 * 60 + 59), 60)
        aa = {**R["a"], "h": min(h, 72), "m": m}
        X, tt = eng.vector(aa)
        P = eng.proba(X)[0]
        tier = str(eng.labels(X)[0])
        _, flag = build_advisories(tier, aa, tt, aa["d"] / max(tt / 60, .25))
        rows.append({"Average speed": f"{spd} km/h", "Duration": fmt_dur(mins), "Predicted tier": TIER_META.get(tier, TIER_META["Exp"])["name"],
                     "Confidence": f"{P.max() * 100:.1f}%", "Audit flag": flag.title()})
    sx(st.dataframe, pd.DataFrame(rows), hide_index=True)


# ---- page 6: explorer ----------------------------------------------------------------------
def page_explorer(eng: Engine, R: dict) -> None:
    section("Train explorer and audit radar", "Search all real trains, see where the model disagrees with the railway's own tag, and compare two trains.")
    audit = eng.audit_all()
    if audit is None:
        st.info("data/trains.csv is needed for the explorer.")
        return
    mode = st.radio("View", ["Browse", "Audit radar", "Compare"], horizontal=True, key="ex_mode", label_visibility="collapsed")
    show = [c for c in ["number", "name", "type", "ml", "zone", "distance", "total_duration", "speed", "conf"] if c in audit.columns]
    ren = {"number": "No.", "name": "Name", "type": "Official", "ml": "ML tier", "zone": "Zone", "distance": "km", "total_duration": "Minutes", "speed": "km/h", "conf": "Conf %"}
    if mode == "Browse":
        c1, c2, c3, c4 = st.columns([1.2, 1, 1.5, 1.3])
        zsel = c1.multiselect("Zone", sorted(audit["zone"].unique()), key="ex_z")
        tsel = c2.multiselect("Official tier", TIERS, key="ex_t")
        dmin, dmax = int(audit["distance"].min()), int(audit["distance"].max())
        drng = c3.slider("Distance (km)", dmin, dmax, (dmin, dmax), key="ex_d")
        q = c4.text_input("Search name or number", key="ex_q")
        k1, k2 = st.columns(2)
        ac_only = k1.checkbox("Only trains with AC coaches", key="ex_ac")
        mism = k2.checkbox("Only trains where the model disagrees with the official tag", key="ex_mm")
        f = audit[(audit["distance"] >= drng[0]) & (audit["distance"] <= drng[1])]
        if zsel:
            f = f[f["zone"].isin(zsel)]
        if tsel:
            f = f[f["type"].isin(tsel)]
        if ac_only:
            f = f[(f.get("first_ac", 0) + f.get("second_ac", 0) + f.get("third_ac", 0) + f.get("chair_car", 0)) > 0]
        if mism:
            f = f[f["type"] != f["ml"]]
        if q.strip():
            f = f[f["name"].astype(str).str.contains(q.strip(), case=False, na=False) | f["number"].astype(str).str.contains(q.strip(), na=False)]
        st.caption(f"{len(f):,} of {len(audit):,} trains match")
        sx(st.dataframe, f[show].rename(columns=ren).head(600), hide_index=True)
        top = f.head(300)
        if len(top):
            lab = (top["number"].astype(str) + "  " + top["name"].astype(str).str.title() + "  [" + top["type"].astype(str) + " / ML " + top["ml"].astype(str) + "]").tolist()
            st.session_state["_ex_map"] = dict(zip(lab, top.index))
            sel = st.selectbox("Train passport", lab, key="ex_pick")
            r = top.loc[st.session_state["_ex_map"][sel]]
            agree = r["type"] == r["ml"]
            frm, to = str(r.get("from_station_name", "")).title(), str(r.get("to_station_name", "")).title()
            route = f'<p class="rd-note">{esc(frm)} to {esc(to)}</p>' if frm and frm != "Nan" else ""
            render_html(f'<div class="rd-panel"><h4>{esc(str(r["name"]).title())} <span class="rd-note">#{esc(r["number"])}</span></h4>{route}'
                        f'<span class="rd-chip {CHIP.get(str(r["type"]), "")}">Official: {esc(r["type"])}</span><span class="rd-chip {CHIP.get(str(r["ml"]), "")}">ML: {esc(r["ml"])} ({r["conf"]:.0f}%)</span>'
                        f'<span class="rd-chip {"pass" if agree else "bad"}">{"Model agrees" if agree else "Model disagrees"}</span>'
                        f'<p class="rd-note">{int(r["distance"])} km in {fmt_dur(r["total_duration"])} ({r["speed"]:.1f} km/h), zone {esc(r["zone"])}</p></div>')
            sx(st.button, "Load this train into the classifier", key="ex_load", on_click=cb_load_train)
    elif mode == "Audit radar":
        agree = float((audit["type"] == audit["ml"]).mean() * 100)
        sf_e = audit[(audit["type"] == "SF") & (audit["ml"] == "Exp")]
        e_sf = audit[(audit["type"] == "Exp") & (audit["ml"] == "SF")]
        render_html(f'<div class="rd-kpis"><div class="k"><b>{len(audit):,}</b><span>Trains audited</span></div><div class="k"><b>{agree:.2f}%</b><span>Agreement on the whole file</span></div>'
                    f'<div class="k"><b>{len(sf_e)}</b><span>Tagged SF, model says Exp</span></div><div class="k"><b>{len(e_sf)}</b><span>Tagged Exp, model says SF</span></div></div>')
        st.caption(f"The whole file includes the {FACTS['train']:,} training rows, which a default tree fits almost perfectly, so most disagreements come from the hold-out part. "
                   f"The honest generalisation number is {FACTS['acc']:.2f}% on the {FACTS['test']} test trains.")
        cols = [c for c in ["number", "name", "zone", "distance", "total_duration", "speed", "type", "ml", "conf"] if c in audit.columns]
        c1, c2 = st.columns(2, gap="large")
        c1.markdown("##### Official SF but the model says Express: surcharge audit candidates")
        with c1:
            sx(st.dataframe, sf_e[cols].rename(columns=ren), hide_index=True)
        c2.markdown("##### Official Express but the model says SF: upgrade candidates")
        with c2:
            sx(st.dataframe, e_sf[cols].rename(columns=ren), hide_index=True)
    else:
        opts = (audit["number"].astype(str) + "  " + audit["name"].astype(str).str.title()).tolist()
        c1, c2 = st.columns(2)
        pa = c1.selectbox("Train A", opts, index=0, key="cmp_a")
        pb = c2.selectbox("Train B", opts, index=min(1, len(opts) - 1), key="cmp_b")
        ra, rb = audit.iloc[opts.index(pa)], audit.iloc[opts.index(pb)]
        mx = dict(d=float(audit["distance"].max()), t=float(audit["total_duration"].max()))

        def vals(r):
            ac = sum(float(r.get(k, 0)) for k in ("first_ac", "second_ac", "third_ac", "chair_car"))
            return [r["distance"] / mx["d"], min(r["speed"], 100) / 100, r["total_duration"] / mx["t"], ac / 4, float(r.get("sleeper", 0)), r["conf"] / 100]
        axes = ["Distance", "Speed", "Duration", "AC coaches", "Sleeper", "ML confidence"]
        l, r_ = st.columns([1.2, 1], gap="large")
        with l:
            render_radar(axes, dict(n=str(ra["name"]).title()[:28], v=vals(ra)), dict(n=str(rb["name"]).title()[:28], v=vals(rb)))
        with r_:
            tb = pd.DataFrame({"": ["Official", "ML tier", "Distance (km)", "Duration", "Speed (km/h)", "Zone"],
                               "Train A": [ra["type"], ra["ml"], int(ra["distance"]), fmt_dur(ra["total_duration"]), ra["speed"], ra["zone"]],
                               "Train B": [rb["type"], rb["ml"], int(rb["distance"]), fmt_dur(rb["total_duration"]), rb["speed"], rb["zone"]]}).astype(str)
            sx(st.dataframe, tb, hide_index=True)


# ---- page 7: batch -------------------------------------------------------------------------
def batch_predict(eng: Engine, df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d.columns = [str(c).strip() for c in d.columns]
    if "distance" not in d.columns:
        raise ValueError("The CSV needs a 'distance' column.")
    if "total_duration" not in d.columns:
        if "duration_h" not in d.columns:
            raise ValueError("Provide 'total_duration' (minutes) or 'duration_h' + 'duration_m'.")
        d["total_duration"] = _to_num(d["duration_h"]) * 60 + _to_num(d.get("duration_m", pd.Series(0, index=d.index)))
    for k in FLAG_KEYS:
        if k not in d.columns:
            d[k] = 0
    if "zone" not in d.columns:
        d["zone"] = "Unknown"
    X = eng.frame(d)
    P = eng.proba(X)
    out = d.copy()
    out["ml_tier"] = eng.labels(X)
    out["confidence"] = (P.max(axis=1) * 100).round(1)
    out["speed_kmh"] = (_to_num(d["distance"]) / (_to_num(d["total_duration"]).clip(lower=15) / 60)).round(1)
    for i, t in enumerate(TIERS):
        out[f"p_{t}"] = (P[:, i] * 100).round(1)
    return out


def page_batch(eng: Engine, R: dict) -> None:
    section("Batch audit", "Upload a CSV of timetables and classify every row at once, then download the audited file.")
    tmpl = pd.DataFrame([["Sample Rajdhani", 1385, 15, 50, "WR", 1, 1, 1, 0, 0, 0, "SF"], ["Sample Passenger", 145, 4, 30, "ER", 0, 0, 0, 0, 1, 0, "Pass"],
                         ["Sample Mail", 610, 12, 0, "ECR", 0, 0, 1, 0, 1, 0, "Exp"]],
                        columns=["name", "distance", "duration_h", "duration_m", "zone", "first_ac", "second_ac", "third_ac", "chair_car", "sleeper", "first_class", "type"])
    c1, c2 = st.columns([1, 2])
    with c1:
        sx(st.download_button, "Download CSV template", tmpl.to_csv(index=False), file_name="raildrishti_template.csv", mime="text/csv", key="dl_tmpl")
    up = c2.file_uploader("Upload your CSV", type=["csv"], key="batch_up", label_visibility="collapsed")
    src, note = (None, "")
    if up is not None:
        try:
            src, note = pd.read_csv(up), f"Uploaded file: {up.name}"
        except Exception as exc:
            st.error(f"Could not read that CSV: {exc}")
    else:
        src, note = tmpl, "No file uploaded yet, showing the template rows as a demo."
    if src is None:
        return
    try:
        res = batch_predict(eng, src)
    except Exception as exc:
        st.error(str(exc))
        return
    st.caption(note)
    cnt = res["ml_tier"].value_counts()
    render_html('<div class="rd-kpis"><div class="k"><b>' + f"{len(res):,}" + "</b><span>Rows classified</span></div>"
                + "".join(f'<div class="k"><b style="color:{TIER_META[t]["color"]}">{int(cnt.get(t, 0))}</b><span>{TIER_META[t]["name"]}</span></div>' for t in ("SF", "Exp", "Pass"))
                + f'<div class="k"><b>{res["confidence"].mean():.1f}%</b><span>Average confidence</span></div></div>')
    cfg = {}
    try:
        cfg = {"confidence": st.column_config.ProgressColumn("Confidence", min_value=0, max_value=100, format="%.1f%%")}
    except Exception:
        pass
    try:
        sx(st.dataframe, res, hide_index=True, column_config=cfg)
    except TypeError:
        sx(st.dataframe, res, hide_index=True)
    if "type" in res.columns:
        known = res["type"].map(norm_tier)
        ok = float((known == res["ml_tier"]).mean() * 100)
        mis = res[known != res["ml_tier"]]
        st.markdown(f"**Agreement with the `type` column: {ok:.1f}%.** {len(mis)} row(s) disagree and deserve a manual timetable audit.")
    sx(st.download_button, "Download audited CSV", res.to_csv(index=False), file_name="raildrishti_audited.csv", mime="text/csv", key="dl_res")


# ---- page 8: arena -------------------------------------------------------------------------
PLOTS = [("model_comparison.png", "Supervised model comparison"), ("before_after_duration_fix.png", "Before and after the duration fix"),
         ("confusion_matrix_best.png", "Decision Tree confusion matrix"), ("roc_curves.png", "One-vs-rest ROC curves"),
         ("feature_importance.png", "Gini feature importance"), ("cross_validation.png", "5-fold cross-validation"),
         ("error_analysis.png", "Error analysis"), ("elbow_curve.png", "K-Means elbow curve"), ("clusters_k5_fixed_pca.png", "K-Means clusters in PCA space"),
         ("dbscan_vs_kmeans.png", "DBSCAN versus K-Means"), ("eda_class_zone_distribution.png", "Class and zone distribution"),
         ("correlation_heatmap.png", "Correlation heatmap")]


def page_arena(eng: Engine, R: dict) -> None:
    section("Model arena", "Six models, one race. Switch the metric and watch the Decision Tree hold the lead.")
    ca = eng.cal["acc"]
    render_html(f'<div class="rd-kpis"><div class="k"><b>{FACTS["acc"]:.2f}%</b><span>Hold-out accuracy</span></div><div class="k"><b>{FACTS["macro_f1"]:.4f}</b><span>Macro F1</span></div>'
                f'<div class="k"><b>{FACTS["cv"]:.4f}</b><span>5-fold CV, +/- {FACTS["cv_sd"]:.4f}</span></div><div class="k"><b>{FACTS["auc"]:.4f}</b><span>ROC-AUC (OvR)</span></div>'
                f'<div class="k"><b>{FACTS["features"]}</b><span>Input features</span></div></div>')
    render_arena()
    platform_line()
    section("Plot gallery", "Saved figures from the notebooks (visualizations folder).")
    found = [(VIZ_DIR / f, c) for f, c in PLOTS if (VIZ_DIR / f).exists()]
    if not found:
        st.info("No plot images found in the visualizations folder.")
    cols = st.columns(2, gap="large")
    for i, (p, cap) in enumerate(found):
        with cols[i % 2]:
            st.markdown(f"**{cap}**")
            sx(st.image, str(p))
    if ca is not None:
        st.caption(f"Live check: on the full trains.csv the loaded model agrees with the official tag on {ca * 100:.1f}% of rows (training rows included).")


# ---- page 9: viva --------------------------------------------------------------------------
def cb_viva_next() -> None:
    st.session_state.viva_i = int(np.random.randint(0, len(VIVA_QA)))


def page_viva(eng: Engine, R: dict) -> None:
    section("Viva mode", "The project story and the questions an examiner is likely to ask, with short answers you can say out loud.")
    render_pipeline()
    m = PROJECT_META
    render_html(f'<div class="rd-panel"><h4>{esc(m["title"])}</h4><div class="rd-note">{esc(m["student"])}, Roll No. {m["roll"]} | {esc(m["course"])}<br>'
                f'{esc(m["college"])} | Guide: {esc(m["guide"])}</div></div>')
    ss = st.session_state
    ss.setdefault("viva_i", 0)
    cat, q, ans = VIVA_QA[ss.viva_i]
    c1, c2 = st.columns([3, 1])
    with c1:
        render_html(f'<div class="rd-panel" style="border-left:5px solid #FFD21F"><span class="rd-chip">{esc(cat)}</span><h4 style="margin-top:6px">{esc(q)}</h4></div>')
        with st.expander("Reveal the answer"):
            st.write(ans)
    with c2:
        sx(st.button, "Ask me another", key="viva_next", on_click=cb_viva_next)
    platform_line()
    cats = ["All"] + sorted({c for c, _, _ in VIVA_QA})
    pick = st.radio("Topic", cats, horizontal=True, key="viva_cat", label_visibility="collapsed")
    for c, qq, aa in VIVA_QA:
        if pick in ("All", c):
            with st.expander(f"{qq}"):
                st.write(aa)
    imp = ", ".join(f"{feature_label(n)} {w * 100:.0f}%" for n, w in eng.importances(4))
    st.caption(f"Live from the loaded model: top features are {imp}. Class mapping: {eng.cal['mapping']}.")


# ==============================================================================
# 9. MAIN
# ==============================================================================
SCENE_TIMES = {"Auto (IST clock)": "auto", "Dawn": "dawn", "Day": "day", "Dusk": "dusk", "Night": "night"}
SCENE_WX = {"Clear": "clear", "Rain": "rain", "Fog": "fog", "Storm": "storm"}


def sidebar(eng: Engine) -> None:
    with st.sidebar:
        render_html(f'<div class="rd-sec"><h3>{PROJECT_META["brand"]} <span style="color:#FFD21F">{PROJECT_META["brand_hi"]}</span></h3><p>Scene, sound and voice controls</p></div>')
        st.selectbox("Time of day", list(SCENE_TIMES), key="sb_time")
        st.selectbox("Weather", list(SCENE_WX), key="sb_wx")
        st.toggle("Try to start scene sound automatically", key="sb_sound", help="Browsers often block sound until you click. The Sound button inside the scene always works.")
        st.selectbox("Announcement language", PA_MODES, key="sb_pa")
        st.selectbox("Announcer voice", list(VOICE_SETS), key="sb_voice", help="Female or deep male Microsoft neural voices (needs: pip install edge-tts and internet). Without it, the browser's best voice is used.")
        st.toggle("Simulate the legacy duration_m bug", key="sb_bug", help="Feeds only duration_m (0-59 min) to the model, the data-quality bug you fixed.")
        with st.expander("System health", expanded=False):
            checks = [("scaler.joblib", SCALER_PATH), ("dt_classifier.joblib", DT_MODEL_PATH), ("trains.csv", TRAINS_CSV),
                      ("trains_with_clusters.csv", CLUSTERS_CSV), ("ir_logo.png", LOGO_PATH)]
            for name, p in checks:
                st.caption(f"{'🟢' if p.exists() else '🔴'} {name}")
            for msg in eng.errors:
                st.caption(msg)
            if eng.ready:
                acc = eng.cal["acc"]
                st.caption(f"Features: {len(eng.cols)} | scaled input: {not eng.use_raw} | classes: {eng.cal['mapping']} | "
                           + (f"check vs trains.csv: {acc * 100:.1f}%" if acc is not None else eng.cal["note"]))
            st.caption(f"Voices: {'neural (edge-tts)' if EDGE_OK else 'edge-tts not installed'} | gTTS: {'yes' if GTTS_OK else 'no'} | QR: {'real code' if QR_OK else 'decorative (pip install qrcode)'}")
        st.caption(f"{PROJECT_META['student']} | Roll No. {PROJECT_META['roll']}")


def main() -> None:
    render_html(f"<style>{THEME_CSS}</style>")
    ss = st.session_state
    eng = get_engine()
    if "active" not in ss:
        ss.active = active_from_preset(0)
    ss.setdefault("reveal", False)
    ss.setdefault("nav", PAGES[0])
    ss.setdefault("ra_from", "MMCT")
    ss.setdefault("ra_to", "NDLS")
    ss.setdefault("sb_time", "Auto (IST clock)")
    ss.setdefault("sb_wx", "Clear")
    ss.setdefault("sb_pa", PA_MODES[0])
    ss.setdefault("sb_voice", list(VOICE_SETS)[0])
    sidebar(eng)

    R = analyze(eng, ss.active, bool(ss.get("sb_bug", False)))
    if BOOT_SLOT is not None:  # the loading screen has done its job
        BOOT_SLOT.empty()
    ss["_booted"] = True
    scene = dict(time=SCENE_TIMES.get(ss.sb_time, "auto"), weather=SCENE_WX.get(ss.sb_wx, "clear"), sound=bool(ss.get("sb_sound", False)))
    render_hero(R, scene, reveal=bool(ss.get("reveal", False)))

    if not eng.ready:
        st.error("The model could not be loaded, so predictions are switched off.")
        for msg in eng.errors:
            st.write(f"- {msg}")
        st.write(f"Expected files: `{SCALER_PATH}` and `{DT_MODEL_PATH}`. Run the app from the project root: `streamlit run app.py`.")
        st.stop()

    st.radio("Page", PAGES, horizontal=True, key="nav", label_visibility="collapsed")
    router = dict(zip(PAGES, [page_classify, page_junction, page_network, page_journey, page_galaxy, page_whatif, page_explorer, page_batch, page_arena, page_viva]))
    router.get(ss.nav, page_classify)(eng, R)
    m = PROJECT_META
    render_html(f'<div class="rd-line"></div><div class="rd-foot">{m["brand"]} | {esc(m["title"])}<br>{esc(m["student"])}, Roll No. {m["roll"]} | {esc(m["course"])} | Guide: {esc(m["guide"])}</div>')


main()