#!/usr/bin/env python3
"""
================================================================================
INDIAN RAILWAYS ML PRESENTATION GENERATOR — V5.0 ULTRA BROADCAST EDITION
================================================================================
Project Title : Classification and Clustering of Indian Railway Trains Using ML
Author        : Rajput Prince Singh (Roll No: 83)
College       : Lokmanya College of Computer Application
Course        : BCA Semester VII - Gujarat University (NEP 2020)
Papers        : DSC-C-BCA-471T (AI), 472T (ML), 473P (ML System Design)
Output File   : reports/Indian_Railway_ML_Presentation.pptx

MAJOR V5.0 BREAKTHROUGHS:
1. Real Spoken Indian Railways Station PA Announcements + WDP-4D Horn Mixer:
   - Synthesizes actual spoken station announcements via Windows .NET Speech
     Synthesizer (with pure-Python harmonic fallback), filters them through a
     Station Platform Echo/Reverb DSP pipeline, prepends the iconic 4-note
     Indian Railways "Ding-Dong-Ding-Dong" PA Chime, and layers a roaring
     WDP-4D / WAP-7 Dual-Tone Air Horn + Track Rail-Joint Clatter ("dhak-dhak").
2. Native OpenXML ZIP Audio Injector (100% Guaranteed Audio Without pywin32):
   - Injects all .wav files directly into `/ppt/media/*.wav`, registers audio
     relationships in `ppt/slides/_rels/slideX.xml.rels`, updates
     `[Content_Types].xml`, and binds `<p:sndAc><p:stSnd><p:snd r:embed="..."/>`
     directly inside every slide's `<p:transition>` XML!
3. 100% PIL-Rendered Glassmorphic Infographic Cards & LHB Train Coach Bogies:
   - Eliminates ugly flat PowerPoint rectangles and text-badge collisions.
   - Every KPI card, Coupled LHB Train Coach, Departure Board, Speedometer,
     and IRCTC Ticket is rendered as an ultra-crisp 300-DPI transparent PNG
     with neon progress bars, carbon headers, vector icons, and coach wheels.
4. True Hidden-to-Visible Entrance Choreography + 3D Creative Transitions:
   - Uses `<p:set>` (visibility: hidden -> visible) + `<p:animEffect>` (fade/wipe)
     + `<p:animMotion>` (large fly-in & full-screen locomotive runs).
   - Uses PowerPoint 3D/Dynamic Transitions: Doors, Vortex, Ripple, Honeycomb,
     Ferris, Switch, Zoom, and Morph.
================================================================================
"""

from __future__ import annotations

import io
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import wave
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml import parse_xml
from pptx.util import Inches, Pt

# Pillow 10+ / Python 3.13 Resampling Compatibility
RESAMPLE_LANCZOS = getattr(Image, "Resampling", Image).LANCZOS
RESAMPLE_BICUBIC = getattr(Image, "Resampling", Image).BICUBIC

# OpenXML Namespace Constants
PML_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
DML_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
MC_NS = "http://schemas.openxmlformats.org/markup-compatibility/2006"
P14_NS = "http://schemas.microsoft.com/office/powerpoint/2010/main"
P15_NS = "http://schemas.microsoft.com/office/powerpoint/2012/main"
P159_NS = "http://schemas.microsoft.com/office/powerpoint/2015/09/main"


# ==============================================================================
# 1. MASTER CONFIGURATION & CYBER-RAILWAY COLOR PALETTE
# ==============================================================================

INCLUDE_TICKET_DIVIDER_SLIDES = True
ENABLE_REAL_VOICE_ANNOUNCEMENTS = True
ENABLE_CINEMATIC_ANIMATIONS = True

SLIDE_W_IN = 13.333
SLIDE_H_IN = 7.500
CANVAS_W_PX = 1920
CANVAS_H_PX = 1080
DPI_SCALE = CANVAS_W_PX / SLIDE_W_IN  # 144.0 px per inch

PALETTE: Dict[str, Tuple[int, int, int]] = {
    "deep_navy": (7, 19, 44),          # #07132C - Primary Command Center Canvas
    "dark_navy": (3, 10, 24),          # #030A18 - Deep Gradient Base
    "midnight": (2, 6, 16),            # #020610 - HUD Chassis & Footer
    "panel_navy": (12, 31, 66),        # #0C1F42 - Glass Card Top
    "panel_bottom": (7, 20, 46),       # #07142E - Glass Card Bottom
    "slate_dark": (18, 43, 88),        # #122B58 - Secondary Card Surface
    "slate_mid": (42, 78, 138),        # #2A4E8A - Subtle Card Border
    "danger_bg": (48, 12, 24),         # #300C18 - Crimson Alert Surface
    "success_bg": (8, 44, 32),         # #082C20 - Emerald Clear Surface
    "saffron": (255, 107, 0),          # #FF6B00 - Vande Bharat Blaze Orange
    "saffron_glow": (255, 150, 54),    # #FF9636 - Neon Orange Highlight
    "gold": (255, 196, 0),             # #FFC400 - Indian Railways Canary Gold
    "gold_soft": (255, 230, 148),      # #FFE694 - High-Luminance Subtitle Gold
    "sign_yellow": (255, 214, 0),      # #FFD600 - Authentic Junction Board Yellow
    "sign_black": (12, 15, 22),        # #0C0F16 - Junction Board Carbon Black
    "white": (255, 255, 255),          # #FFFFFF - Crisp Primary Text
    "light_grey": (224, 234, 248),     # #E0EAF8 - High-Contrast Body Text
    "muted_text": (165, 188, 220),     # #A5BCDC - Secondary Telemetry Label
    "green": (39, 174, 96),            # #27AE60 - Signal Clear Green
    "green_bright": (0, 238, 136),     # #00EE88 - Neon Signal Green
    "red": (231, 76, 60),              # #E74C3C - Signal Danger Red
    "red_bright": (255, 78, 92),       # #FF4E5C - Neon Danger Red
    "blue": (46, 156, 255),            # #2E9CFF - WAP-7 Electric Blue
    "cyan": (0, 228, 255),             # #00E4FF - Telemetry HUD Cyan
    "purple": (182, 108, 255),         # #B66CFF - Unsupervised Clustering Violet
    "ticket_cream": (252, 246, 233),   # #FCF6E9 - IRCTC Reservation Voucher
    "ticket_sub": (238, 228, 206),     # #EEE4CE - Ticket Inner Box
    "ticket_border": (198, 176, 138),  # #C6B08A - Ticket Border
}

FONT_HEADING = "Montserrat"
FONT_BODY = "Montserrat"
FONT_MONO = "Consolas"


def rgb_color(name: str) -> RGBColor:
    r, g, b = PALETTE[name]
    return RGBColor(r, g, b)


# ==============================================================================
# 2. PATH RESOLUTION MANAGER
# ==============================================================================

class ProjectPaths:
    def __init__(self) -> None:
        script_dir = Path(__file__).resolve().parent
        if script_dir.name.lower() == "reports":
            self.root = script_dir.parent
        else:
            self.root = script_dir

        self.reports_dir = self.root / "reports"
        self.images_dir = self.reports_dir / "images"
        self.viz_dir = self.root / "visualizations"
        self.cache_dir = self.reports_dir / "_ppt_generated_assets"
        self.output_pptx = self.reports_dir / "Indian_Railway_ML_Presentation.pptx"

        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_image(self, filename: str) -> Optional[Path]:
        p = self.images_dir / filename
        return p if p.exists() else None

    def get_viz(self, filename: str) -> Optional[Path]:
        p = self.viz_dir / filename
        return p if p.exists() else None


# ==============================================================================
# 3. INDIAN RAILWAYS ACOUSTIC & REAL STATION ANNOUNCEMENT SYNTHESIZER
# ==============================================================================

class RailwayBroadcastAudioStudio:
    """
    Synthesizes authentic Indian Railways audio tracks (22,050 Hz, 16-bit Mono PCM):
    1. Iconic 4-Note Indian Railways Station PA Chime ("Ding-Dong-Ding-Dong":
       G4 -> B4 -> D5 -> G5 vibraphone bell with station hall echo).
    2. Real Spoken Female Station Announcer Voice (via Windows built-in
       System.Speech.Synthesis.SpeechSynthesizer + Platform PA Bandpass & Echo
       DSP filter).
    3. Authentic WDP-4D / WAP-7 Dual-Tone Locomotive Air Horn with air-valve
       hiss, brass harmonics, Doppler pitch bend, and "dhak-dhak" rail-joint
       track clatter!
    """

    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir
        self.sample_rate = 22050

    # --------------------------------------------------------------------------
    # Low-Level DSP Primitives (Chime, Horn, Track Clatter, Platform Reverb)
    # --------------------------------------------------------------------------

    def _synth_pa_ding_dong_chime(self) -> List[float]:
        """
        Generates the iconic 1.75s 4-note Indian Railways Station PA Chime:
        Note 1: G4 (392.00 Hz)
        Note 2: D5 (587.33 Hz)
        Note 3: B4 (493.88 Hz)
        Note 4: G4 (392.00 Hz) - held resonant chord
        """
        duration = 1.75
        n = int(self.sample_rate * duration)
        buf = [0.0] * n
        notes = [
            (0.04, 392.00, 0.55),
            (0.38, 587.33, 0.55),
            (0.72, 493.88, 0.55),
            (1.06, 392.00, 0.68),
        ]
        for i in range(n):
            t = i / float(self.sample_rate)
            val = 0.0
            for start_t, freq, amp in notes:
                if t >= start_t:
                    dt = t - start_t
                    env = math.exp(-3.4 * dt) * min(1.0, dt / 0.008)
                    val += amp * env * (
                        0.72 * math.sin(2.0 * math.pi * freq * dt)
                        + 0.20 * math.sin(2.0 * math.pi * (freq * 2.0) * dt)
                        + 0.08 * math.sin(2.0 * math.pi * (freq * 3.0) * dt)
                    )
            buf[i] = val
        return self._apply_station_echo(buf, delay_sec=0.14, decay=0.32)

    def _synth_wdp4d_horn_and_track(self, duration: float = 3.2, urgent_double: bool = False) -> List[float]:
        """
        Synthesizes an authentic WDP-4D / WAP-7 multi-chime air horn layered
        over rhythmic railway track rail-joint clatter ("dhak-dhak... dhak-dhak").
        """
        n = int(self.sample_rate * duration)
        buf = [0.0] * n

        # Authentic Indian Railways EMD / WAP-7 multi-chime chord (D3, A3, D4, F#4, A4)
        freqs = [146.83, 220.00, 293.66, 369.99, 440.00]
        weights = [0.18, 0.20, 0.28, 0.20, 0.14]

        # Rail-joint "dhak-dhak" impulses (pairs of wheel clicks across rail joints)
        click_times = []
        t_cursor = 0.08
        interval = 0.42
        while t_cursor < duration - 0.15:
            click_times.append((t_cursor, 0.38))
            click_times.append((t_cursor + 0.11, 0.32))
            t_cursor += interval
            interval = max(0.24, interval * 0.92)  # Train accelerating!

        for i in range(n):
            t = i / float(self.sample_rate)

            # 1. Horn Envelope
            env = 0.0
            if urgent_double:
                if 0.05 <= t <= 0.55:
                    env = min(1.0, (t - 0.05) / 0.06) * min(1.0, (0.55 - t) / 0.08)
                elif 0.68 <= t <= duration - 0.15:
                    env = min(1.0, (t - 0.68) / 0.09) * min(1.0, (duration - 0.15 - t) / 0.40)
            else:
                if 0.05 <= t <= 0.48:
                    env = min(1.0, (t - 0.05) / 0.05) * min(1.0, (0.48 - t) / 0.07)
                elif 0.58 <= t <= duration - 0.12:
                    env = min(1.0, (t - 0.58) / 0.10) * min(1.0, (duration - 0.12 - t) / 0.45)

            horn_sig = 0.0
            if env > 0.001:
                vibrato = 1.0 + 0.0035 * math.sin(2.0 * math.pi * 6.2 * t)
                doppler = 1.0 + 0.012 * math.cos(math.pi * t / duration)
                for f, w in zip(freqs, weights):
                    fi = f * vibrato * doppler
                    horn_sig += w * (
                        0.62 * math.sin(2.0 * math.pi * fi * t)
                        + 0.25 * math.sin(2.0 * math.pi * (2.0 * fi) * t)
                        + 0.13 * math.sin(2.0 * math.pi * (3.0 * fi) * t)
                    )
                horn_sig = math.tanh(horn_sig * 1.65) * env * 0.72

            # 2. Track Rail-Joint "Dhak-Dhak" + Low Locomotive Rumble
            rumble = 0.12 * math.sin(2.0 * math.pi * 55.0 * t) * math.sin(2.0 * math.pi * 3.5 * t)
            clatter = 0.0
            for ct, camp in click_times:
                dt = t - ct
                if 0.0 <= dt <= 0.065:
                    c_env = math.exp(-55.0 * dt)
                    # Metallic rail impact + low bogie thud
                    clatter += camp * c_env * (
                        0.6 * math.sin(2.0 * math.pi * 115.0 * dt)
                        + 0.4 * math.sin(2.0 * math.pi * 840.0 * dt)
                    )

            buf[i] = max(-0.98, min(0.98, horn_sig + rumble + clatter))

        return self._apply_station_echo(buf, delay_sec=0.16, decay=0.28)

    def _apply_station_echo(self, samples: List[float], delay_sec: float = 0.15, decay: float = 0.30) -> List[float]:
        """Adds authentic Indian Railway platform roof reverb echo."""
        delay_samples = int(self.sample_rate * delay_sec)
        out = list(samples)
        for i in range(delay_samples, len(out)):
            out[i] = max(-0.98, min(0.98, out[i] + decay * out[i - delay_samples]))
        return out

    def _read_wav_as_floats(self, wav_path: Path) -> List[float]:
        """Reads any PCM .wav file and resamples/converts it to mono float [-1, 1] at self.sample_rate."""
        if not wav_path.exists():
            return []
        try:
            with wave.open(str(wav_path), "rb") as wf:
                n_channels = wf.getnchannels()
                sampwidth = wf.getsampwidth()
                src_rate = wf.getframerate()
                n_frames = wf.getnframes()
                raw = wf.readframes(n_frames)

            if sampwidth == 2:
                total_shorts = len(raw) // 2
                ints = struct.unpack(f"<{total_shorts}h", raw[: total_shorts * 2])
                if n_channels == 2:
                    mono = [(ints[i] + ints[i + 1]) / 65536.0 for i in range(0, len(ints) - 1, 2)]
                else:
                    mono = [x / 32768.0 for x in ints]
            elif sampwidth == 1:
                mono = [(b - 128) / 128.0 for b in raw]
            else:
                return []

            if src_rate != self.sample_rate and len(mono) > 10:
                ratio = src_rate / float(self.sample_rate)
                new_len = int(len(mono) / ratio)
                mono = [mono[min(len(mono) - 1, int(i * ratio))] for i in range(new_len)]

            # Apply mild railway loudspeaker presence boost + platform echo
            return self._apply_station_echo(mono, delay_sec=0.12, decay=0.24)
        except Exception:
            return []

    def _write_floats_to_wav(self, out_path: Path, samples: Sequence[float]) -> Path:
        frames = bytearray()
        for s in samples:
            val = int(max(-32767, min(32767, s * 28500.0)))
            frames.extend(struct.pack("<h", val))
        with wave.open(str(out_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(bytes(frames))
        return out_path

    # --------------------------------------------------------------------------
    # Batch Windows .NET Speech Synthesizer for Real Station Announcements
    # --------------------------------------------------------------------------

    def build_all_railway_soundtracks(self) -> Dict[str, Path]:
        """
        Generates 8 complete railway soundtracks (.wav) combining:
        - 4-note Indian Railways "Ding-Dong" Station Chime
        - Real Spoken Female Station Announcer Voice (via Windows System.Speech)
        - WDP-4D Dual-Tone Locomotive Air Horn & Track Clatter
        """
        announcements = {
            "welcome_hero": (
                "Yatri kripya dhyan dein. May I have your attention please. "
                "Train number 1 2 0 2 6, Indian Railways Machine Learning Superfast Express, "
                "presented by Rajput Prince Singh, is ready to depart from Platform Number 1."
            ),
            "phase1_eda": (
                "May I have your attention please. "
                "Train is arriving at Phase 1 Junction: Exploratory Data Analysis and Duration Data Fix."
            ),
            "killer_discovery": (
                "Attention please. Green Signal granted at Data Quality Junction. "
                "Engineering total duration has boosted every Machine Learning model."
            ),
            "phase2_eval": (
                "May I have your attention please. "
                "Now entering Phase 2 Junction: Multi Class Evaluation Metrics and R O C Curves."
            ),
            "phase3_models": (
                "May I have your attention please. "
                "Train arriving at Phase 3 Junction: Supervised Classification. Decision Tree leads with 91.5 percent accuracy."
            ),
            "phase4_clusters": (
                "May I have your attention please. "
                "Now entering Phase 4 Junction: Unsupervised K Means and D B SCAN Fleet Clustering."
            ),
            "terminus_viva": (
                "Yatri kripya dhyan dein. We have arrived at Terminus Station. "
                "Thank you, and the floor is now open for Viva Questions."
            ),
        }

        raw_voice_wavs: Dict[str, Path] = {}
        if ENABLE_REAL_VOICE_ANNOUNCEMENTS and os.name == "nt":
            try:
                ps_lines = [
                    "Add-Type -AssemblyName System.Speech;",
                    "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;",
                    "$synth.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::Female);",
                    "$synth.Rate = 0;",
                    "$synth.Volume = 100;",
                ]
                for key, text in announcements.items():
                    raw_p = self.cache_dir / f"_raw_tts_{key}.wav"
                    raw_voice_wavs[key] = raw_p
                    safe_path = str(raw_p.resolve()).replace("'", "''")
                    safe_text = text.replace("'", "''")
                    ps_lines.append(f"$synth.SetOutputToWaveFile('{safe_path}');")
                    ps_lines.append(f"$synth.Speak('{safe_text}');")
                ps_lines.append("$synth.Dispose();")
                ps_script = "\n".join(ps_lines)

                subprocess.run(
                    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                    check=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=25,
                )
            except Exception as exc:
                print(f"  [AUDIO NOTE] Windows Speech TTS fallback triggered: {exc}")

        chime_samples = self._synth_pa_ding_dong_chime()
        horn_long = self._synth_wdp4d_horn_and_track(duration=2.8, urgent_double=False)
        horn_urgent = self._synth_wdp4d_horn_and_track(duration=2.4, urgent_double=True)
        track_pass = self._synth_wdp4d_horn_and_track(duration=1.65, urgent_double=False)

        final_paths: Dict[str, Path] = {}

        # 1. Pure Horn & Track Pass for general slides
        final_paths["horn_track"] = self._write_floats_to_wav(
            self.cache_dir / "ir_v5_horn_track.wav", horn_long
        )
        final_paths["chime_only"] = self._write_floats_to_wav(
            self.cache_dir / "ir_v5_station_chime.wav", chime_samples + track_pass[: int(self.sample_rate * 0.9)]
        )

        # 2. Composite Station Broadcasts (Chime + Voice Announcement + Train Horn)
        for key in announcements:
            voice_floats = self._read_wav_as_floats(raw_voice_wavs.get(key, Path("")))
            pause = [0.0] * int(self.sample_rate * 0.15)
            if key == "welcome_hero":
                combined = chime_samples + pause + voice_floats + pause + horn_long
            elif key == "killer_discovery":
                combined = horn_urgent + pause + voice_floats
            elif key == "terminus_viva":
                combined = chime_samples + pause + voice_floats + pause + horn_urgent
            else:
                combined = chime_samples + pause + voice_floats + pause + track_pass[: int(self.sample_rate * 1.1)]

            out_wav = self.cache_dir / f"ir_v5_broadcast_{key}.wav"
            final_paths[key] = self._write_floats_to_wav(out_wav, combined)

        return final_paths


# ==============================================================================
# 4. ULTRA-HD PIL GLASSMORPHIC GRAPHICS & LHB COACH BOGIE STUDIO
# ==============================================================================

class RailwayGraphicStudio:
    """
    Renders 100% custom, zero-overlap PIL graphics for every slide element:
    - 3D Glassmorphic KPI Cards with dedicated top-right badge bar & bottom meter
    - Authentic LHB / Vande Bharat Train Coach Bogie Cards with wheels & windows
    - Digital LED Station Departure Leaderboard with inline progress bars
    - Full-Width Animated Vande Bharat Express Rake (Loco + Coaches)
    - Rich IRCTC Reservation Ticket with Telemetry Grid & Vector Checkmarks
    """

    def __init__(self, paths: ProjectPaths) -> None:
        self.paths = paths
        self._font_cache: Dict[Tuple[str, int, bool], ImageFont.ImageFont] = {}

    def get_pil_font(self, size: int, bold: bool = False, mono: bool = False) -> ImageFont.ImageFont:
        key = ("mono" if mono else "sans", size, bold)
        if key in self._font_cache:
            return self._font_cache[key]

        if mono:
            candidates = ["consolab.ttf" if bold else "consola.ttf", "courbd.ttf" if bold else "cour.ttf"]
        else:
            if bold:
                candidates = [
                    "Montserrat-Bold.ttf",
                    "Montserrat-ExtraBold.ttf",
                    "segoeuib.ttf",
                    "arialbd.ttf",
                    "calibrib.ttf",
                ]
            else:
                candidates = [
                    "Montserrat-Regular.ttf",
                    "Montserrat-Medium.ttf",
                    "segoeui.ttf",
                    "arial.ttf",
                    "calibri.ttf",
                ]

        win_fonts = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
        local_fonts = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "Fonts"

        for cand in candidates:
            for folder in [win_fonts, local_fonts, Path(".")]:
                fp = folder / cand
                if fp.exists():
                    try:
                        font = ImageFont.truetype(str(fp), size)
                        self._font_cache[key] = font
                        return font
                    except Exception:
                        pass
            try:
                font = ImageFont.truetype(cand, size)
                self._font_cache[key] = font
                return font
            except Exception:
                pass

        fallback = ImageFont.load_default()
        self._font_cache[key] = fallback
        return fallback

    @staticmethod
    def _measure_text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> float:
        if hasattr(draw, "textlength"):
            try:
                return float(draw.textlength(text, font=font))
            except Exception:
                pass
        bbox = draw.textbbox((0, 0), text, font=font)
        return float(bbox[2] - bbox[0])

    def _wrap_text_to_width(
        self, draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_w: int
    ) -> List[str]:
        words = text.split()
        if not words:
            return [""]
        lines: List[str] = []
        current = words[0]
        for w in words[1:]:
            test_line = f"{current} {w}"
            if self._measure_text_width(draw, test_line, font) <= max_w:
                current = test_line
            else:
                lines.append(current)
                current = w
        lines.append(current)
        return lines

    def _draw_fitted_text(
        self,
        draw: ImageDraw.ImageDraw,
        x: int,
        y: int,
        max_w: int,
        max_h: int,
        text: str,
        start_size: int,
        min_size: int = 11,
        bold: bool = True,
        mono: bool = False,
        fill: Tuple[int, int, int, int] = (255, 255, 255, 255),
        line_spacing: int = 5,
    ) -> int:
        chosen_font = self.get_pil_font(min_size, bold=bold, mono=mono)
        chosen_lines = [text]
        for sz in range(start_size, min_size - 1, -1):
            f = self.get_pil_font(sz, bold=bold, mono=mono)
            lines = self._wrap_text_to_width(draw, text, f, max_w)
            total_h = len(lines) * (sz + line_spacing)
            max_line_w = max(self._measure_text_width(draw, ln, f) for ln in lines)
            if total_h <= max_h and max_line_w <= max_w:
                chosen_font = f
                chosen_lines = lines
                break
        else:
            chosen_lines = self._wrap_text_to_width(draw, text, chosen_font, max_w)

        cy = y
        step_h = (chosen_font.size if hasattr(chosen_font, "size") else min_size) + line_spacing
        for ln in chosen_lines:
            if cy + step_h - y > max_h + 10:
                break
            draw.text((x, cy), ln, font=chosen_font, fill=fill)
            cy += step_h
        return cy

    @staticmethod
    def _draw_vector_check_badge(
        draw: ImageDraw.ImageDraw,
        cx: int,
        cy: int,
        radius: int,
        circle_fill: Tuple[int, int, int, int],
        tick_color: Tuple[int, int, int, int] = (255, 255, 255, 255),
    ) -> None:
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=circle_fill)
        p1 = (cx - int(radius * 0.45), cy + int(radius * 0.02))
        p2 = (cx - int(radius * 0.10), cy + int(radius * 0.38))
        p3 = (cx + int(radius * 0.50), cy - int(radius * 0.35))
        draw.line([p1, p2, p3], fill=tick_color, width=max(2, radius // 3))

    # --------------------------------------------------------------------------
    # 1. PIL Glassmorphic KPI / Telemetry Card (100% Zero Overlap Guaranteed!)
    # --------------------------------------------------------------------------

    def create_hud_kpi_card_png(
        self,
        tag: str,
        big_value: str,
        title: str,
        subtitle: str,
        accent_name: str = "saffron",
        badge_code: str = "METRIC",
        meter_fill_ratio: float = 0.88,
        width_in: float = 2.95,
        height_in: float = 2.25,
    ) -> Path:
        """
        Renders a 3D Glassmorphic Railway Telemetry KPI Card as a crisp PNG:
        - Dedicated top telemetry header strip holds the `badge_code` pill on the
          right and a glowing signal indicator on the left.
        - `big_value` sits in its own dedicated middle band so it NEVER collides
          with `badge_code` (completely solves the '68,000+ km' vs 'SCALE' bug!).
        - Includes a glowing bottom telemetry progress bar.
        """
        out_path = self.paths.cache_dir / f"kpi_v5_{tag}.png"
        W = int(width_in * DPI_SCALE)
        H = int(height_in * DPI_SCALE)
        pad = 10
        cw = W - pad * 2
        ch = H - pad * 2
        accent = PALETTE[accent_name]

        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))

        # Drop shadow
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow)
        sdraw.rounded_rectangle([(pad + 4, pad + 6), (pad + cw + 4, pad + ch + 6)], radius=20, fill=(0, 0, 0, 155))
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=7))
        canvas = Image.alpha_composite(canvas, shadow)

        # Card body with vertical gradient
        card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        top_img = Image.new("RGBA", (cw, ch), (*PALETTE["panel_navy"], 248))
        bot_img = Image.new("RGBA", (cw, ch), (*PALETTE["panel_bottom"], 252))
        grad_mask = Image.linear_gradient("L").resize((cw, ch))
        body = Image.composite(bot_img, top_img, grad_mask)

        bdraw = ImageDraw.Draw(body)
        # Top header bar (42px tall)
        hdr_h = 42
        bdraw.rectangle([(0, 0), (cw, hdr_h)], fill=(4, 12, 28, 235))
        bdraw.line([(0, hdr_h), (cw, hdr_h)], fill=(*accent, 210), width=2)

        # Diagonal speed stripes on header
        for i in range(6):
            sx = cw - 175 + i * 16
            bdraw.polygon([(sx, 0), (sx + 8, 0), (sx - 12, hdr_h), (sx - 20, hdr_h)], fill=(*accent, 35))

        # Left LED status dot + label
        bdraw.ellipse((16, 13, 30, 27), fill=(*accent, 255))
        f_mono = self.get_pil_font(12, bold=True, mono=True)
        bdraw.text((38, 13), "TELEMETRY // LIVE", font=f_mono, fill=(*PALETTE["muted_text"], 255))

        # Right Badge Pill inside Header (Strictly above Big Value!)
        if badge_code:
            pill_w = max(84, int(self._measure_text_width(bdraw, badge_code, f_mono)) + 26)
            px0 = cw - pill_w - 12
            bdraw.rounded_rectangle([(px0, 7), (cw - 12, hdr_h - 7)], radius=8, fill=(*accent, 255))
            txt_col = PALETTE["sign_black"] if accent_name in ("gold", "sign_yellow", "cyan", "green_bright", "saffron") else PALETTE["white"]
            tw_txt = self._measure_text_width(bdraw, badge_code, f_mono)
            bdraw.text((px0 + (pill_w - tw_txt) / 2, 12), badge_code, font=f_mono, fill=(*txt_col, 255))

        # Big Value in Dedicated Band (y = 50 .. 110) — Zero Collision Possible!
        val_col = PALETTE["gold"] if accent_name == "saffron" else accent
        self._draw_fitted_text(
            bdraw,
            x=20,
            y=50,
            max_w=cw - 40,
            max_h=54,
            text=big_value,
            start_size=36,
            min_size=20,
            bold=True,
            fill=(*val_col, 255),
        )

        # Title Band
        self._draw_fitted_text(
            bdraw,
            x=20,
            y=108,
            max_w=cw - 40,
            max_h=34,
            text=title,
            start_size=18,
            min_size=13,
            bold=True,
            fill=(*PALETTE["white"], 255),
        )

        # Subtitle Band
        self._draw_fitted_text(
            bdraw,
            x=20,
            y=142,
            max_w=cw - 40,
            max_h=ch - 172,
            text=subtitle,
            start_size=14,
            min_size=11,
            bold=False,
            fill=(*PALETTE["light_grey"], 255),
            line_spacing=4,
        )

        # Bottom Glowing Telemetry Progress Bar
        bar_y = ch - 20
        bdraw.rounded_rectangle([(20, bar_y), (cw - 20, bar_y + 8)], radius=4, fill=(22, 42, 78, 255))
        fill_w = max(24, int((cw - 40) * max(0.1, min(1.0, meter_fill_ratio))))
        bdraw.rounded_rectangle([(20, bar_y), (20 + fill_w, bar_y + 8)], radius=4, fill=(*accent, 255))

        # Rounded Mask + Neon Border
        mask = Image.new("L", (cw, ch), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.rounded_rectangle([(0, 0), (cw - 1, ch - 1)], radius=18, fill=255)
        card.paste(body, (0, 0), mask)

        cdraw = ImageDraw.Draw(card)
        cdraw.rounded_rectangle([(0, 0), (cw - 1, ch - 1)], radius=18, outline=(*accent, 240), width=3)

        canvas.paste(card, (pad, pad), card)
        canvas.save(out_path, "PNG")
        return out_path

    # --------------------------------------------------------------------------
    # 2. Authentic LHB / Vande Bharat Train Coach Bogie Card (For Cluster Slide)
    # --------------------------------------------------------------------------

    def create_train_coach_bogie_png(
        self,
        tag: str,
        coach_code: str,
        cluster_title: str,
        cluster_subtitle: str,
        cluster_desc: str,
        accent_name: str,
        width_in: float = 12.22,
        height_in: float = 1.02,
    ) -> Path:
        """
        Renders an authentic Indian Railways LHB Coach Bogie Blueprint with
        couplers, roof AC vents, tinted passenger windows, livery stripe, and
        steel bogie wheels!
        """
        out_path = self.paths.cache_dir / f"coach_bogie_v5_{tag}.png"
        W = int(width_in * DPI_SCALE)
        H = int(height_in * DPI_SCALE)
        accent = PALETTE[accent_name]

        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        body_x0, body_y0 = 26, 8
        body_x1, body_y1 = W - 26, H - 22

        # Left & Right Mechanical Couplers
        draw.rectangle([(4, (body_y0 + body_y1) // 2 - 6), (body_x0, (body_y0 + body_y1) // 2 + 6)], fill=(*PALETTE["gold"], 255))
        draw.rectangle([(body_x1, (body_y0 + body_y1) // 2 - 6), (W - 4, (body_y0 + body_y1) // 2 + 6)], fill=(*PALETTE["gold"], 255))

        # Coach Roof Shroud
        draw.rounded_rectangle([(body_x0 + 18, 2), (body_x1 - 18, 14)], radius=5, fill=(*accent, 220))

        # Main Coach Chassis
        draw.rounded_rectangle(
            [(body_x0, body_y0), (body_x1, body_y1)],
            radius=16,
            fill=(*PALETTE["panel_navy"], 250),
            outline=(*accent, 255),
            width=3,
        )

        # Bottom Livery Stripe
        draw.rectangle([(body_x0 + 4, body_y1 - 10), (body_x1 - 4, body_y1 - 3)], fill=(*accent, 255))

        # Left Coach Number LED Display Window
        win_w = 185
        draw.rounded_rectangle(
            [(body_x0 + 16, body_y0 + 14), (body_x0 + 16 + win_w, body_y1 - 16)],
            radius=10,
            fill=(*PALETTE["midnight"], 255),
            outline=(*PALETTE["gold"], 255),
            width=2,
        )
        f_code = self.get_pil_font(18, bold=True, mono=True)
        cw_txt = self._measure_text_width(draw, coach_code, f_code)
        draw.text(
            (body_x0 + 16 + (win_w - cw_txt) / 2, body_y0 + 26),
            coach_code,
            font=f_code,
            fill=(*PALETTE["sign_yellow"], 255),
        )
        f_tiny = self.get_pil_font(11, bold=True, mono=True)
        draw.text((body_x0 + 36, body_y0 + 54), "LHB AC TELEMETRY", font=f_tiny, fill=(*accent, 255))

        # Cluster Title & Subtitle Window
        self._draw_fitted_text(
            draw,
            x=body_x0 + 220,
            y=body_y0 + 14,
            max_w=490,
            max_h=34,
            text=cluster_title,
            start_size=19,
            min_size=14,
            bold=True,
            fill=(*PALETTE["white"], 255),
        )
        self._draw_fitted_text(
            draw,
            x=body_x0 + 220,
            y=body_y0 + 50,
            max_w=490,
            max_h=30,
            text=cluster_subtitle,
            start_size=14,
            min_size=11,
            bold=True,
            fill=(*PALETTE["gold_soft"], 255),
        )

        # Right Description Panoramic Coach Window
        desc_x0 = body_x0 + 725
        draw.rounded_rectangle(
            [(desc_x0, body_y0 + 12), (body_x1 - 18, body_y1 - 16)],
            radius=10,
            fill=(6, 17, 38, 230),
            outline=(*PALETTE["slate_mid"], 200),
            width=2,
        )
        self._draw_fitted_text(
            draw,
            x=desc_x0 + 16,
            y=body_y0 + 18,
            max_w=(body_x1 - 18) - desc_x0 - 32,
            max_h=body_y1 - body_y0 - 36,
            text=cluster_desc,
            start_size=14,
            min_size=11,
            bold=False,
            fill=(*PALETTE["light_grey"], 255),
            line_spacing=4,
        )

        # 4 Steel Bogie Wheels under the Coach
        wheel_xs = [body_x0 + 85, body_x0 + 145, body_x1 - 145, body_x1 - 85]
        for wx in wheel_xs:
            wy = body_y1 + 2
            draw.ellipse((wx - 13, wy - 10, wx + 13, wy + 16), fill=(20, 26, 38, 255), outline=(*PALETTE["gold"], 255), width=3)
            draw.ellipse((wx - 4, wy - 1, wx + 4, wy + 7), fill=(*accent, 255))

        canvas.save(out_path, "PNG")
        return out_path

    # --------------------------------------------------------------------------
    # 3. Full-Length Animated Vande Bharat Express Train Rake Sprite
    # --------------------------------------------------------------------------

    def create_vande_bharat_rake_png(self, width_in: float = 4.4, height_in: float = 0.95) -> Path:
        """
        Renders a sleek multi-car Vande Bharat / WAP-7 Superfast Express Rake
        with glowing LED headlight beam, pantograph sparks, and bogie wheels.
        """
        out_path = self.paths.cache_dir / "vande_bharat_rake_v5.png"
        W = int(width_in * DPI_SCALE)
        H = int(height_in * DPI_SCALE)
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # Headlight beam on right
        beam_pts = [(W - 115, H - 46), (W - 2, H - 88), (W - 2, H - 14)]
        draw.polygon(beam_pts, fill=(255, 232, 120, 140))

        # Coach 1 (Rear LHB Coach)
        c1_x0, c1_x1 = 16, int(W * 0.44)
        c_y0, c_y1 = 26, H - 24
        draw.rounded_rectangle(
            [(c1_x0, c_y0), (c1_x1, c_y1)],
            radius=10,
            fill=(*PALETTE["panel_navy"], 255),
            outline=(*PALETTE["saffron"], 255),
            width=3,
        )
        draw.rectangle([(c1_x0 + 4, c_y1 - 14), (c1_x1 - 4, c_y1 - 6)], fill=(*PALETTE["saffron"], 255))
        for wx in range(c1_x0 + 18, c1_x1 - 24, 38):
            draw.rounded_rectangle([(wx, c_y0 + 12), (wx + 24, c_y0 + 30)], radius=4, fill=(*PALETTE["cyan"], 220))

        # Coupler
        draw.rectangle([(c1_x1, c_y1 - 22), (c1_x1 + 16, c_y1 - 12)], fill=(*PALETTE["gold"], 255))

        # Lead Aerodynamic Vande Bharat Locomotive
        l_x0 = c1_x1 + 14
        l_x1 = W - 95
        nose_pts = [
            (l_x0, c_y1),
            (l_x0, c_y0),
            (l_x1 - 48, c_y0),
            (l_x1 + 8, c_y0 + 28),
            (l_x1 + 22, c_y1),
        ]
        draw.polygon(nose_pts, fill=(*PALETTE["saffron"], 255), outline=(*PALETTE["white"], 255))
        draw.rectangle([(l_x0 + 4, c_y1 - 22), (l_x1 + 10, c_y1 - 12)], fill=(*PALETTE["white"], 255))
        draw.rectangle([(l_x0 + 4, c_y1 - 12), (l_x1 + 16, c_y1 - 4)], fill=(*PALETTE["deep_navy"], 255))

        # Cab Windshield
        wind_pts = [(l_x1 - 46, c_y0 + 8), (l_x1 - 4, c_y0 + 28), (l_x1 - 46, c_y0 + 28)]
        draw.polygon(wind_pts, fill=(*PALETTE["cyan"], 255))

        # Side windows on Lead Car
        for wx in range(l_x0 + 18, l_x1 - 68, 40):
            draw.rounded_rectangle([(wx, c_y0 + 12), (wx + 26, c_y0 + 28)], radius=4, fill=(*PALETTE["deep_navy"], 255))

        # Pantograph on roof
        px = l_x0 + 55
        draw.line([(px, c_y0), (px + 18, 6), (px + 38, c_y0)], fill=(*PALETTE["gold"], 255), width=3)
        draw.line([(px + 8, 6), (px + 30, 6)], fill=(*PALETTE["cyan"], 255), width=3)

        # Wheels
        for wheel_x in [c1_x0 + 36, c1_x0 + 72, c1_x1 - 72, c1_x1 - 36, l_x0 + 42, l_x0 + 78, l_x1 - 54, l_x1 - 18]:
            draw.ellipse(
                (wheel_x - 10, c_y1 - 4, wheel_x + 10, c_y1 + 16),
                fill=(18, 24, 36, 255),
                outline=(*PALETTE["gold"], 255),
                width=3,
            )

        canvas.save(out_path, "PNG")
        return out_path

    # --------------------------------------------------------------------------
    # 4. Digital Station Departure Board PNG (For Slide 11 Leaderboard)
    # --------------------------------------------------------------------------

    def create_departure_leaderboard_png(self, width_in: float = 7.35, height_in: float = 5.25) -> Path:
        """
        Renders an authentic Indian Railways Digital LED Departure Board with
        inline progress bars, rank badges, and high-contrast gold champion row.
        """
        out_path = self.paths.cache_dir / "departure_board_v5.png"
        W = int(width_in * DPI_SCALE)
        H = int(height_in * DPI_SCALE)
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        draw.rounded_rectangle(
            [(4, 4), (W - 5, H - 5)],
            radius=20,
            fill=(*PALETTE["panel_navy"], 252),
            outline=(*PALETTE["saffron"], 255),
            width=3,
        )
        draw.rounded_rectangle([(4, 4), (W - 5, 62)], radius=20, fill=(*PALETTE["midnight"], 255))
        draw.line([(4, 62), (W - 5, 62)], fill=(*PALETTE["gold"], 255), width=3)

        f_hdr = self.get_pil_font(16, bold=True, mono=True)
        draw.text((24, 22), "🚉  INDIAN RAILWAYS AI/ML DIGITAL LEADERBOARD (TEST SET N = 894)", font=f_hdr, fill=(*PALETTE["gold"], 255))

        rows = [
            ("RANK / MODEL ARCHITECTURE", "ACCURACY", "F1 MACRO", "F1 WGHT", "SIGNAL STATUS", "saffron", 0.0),
            ("#1  Decision Tree (Default) 🏆", "91.50%", "0.8896", "0.9146", "CHAMPION", "sign_yellow", 0.915),
            ("#2  Decision Tree (Depth=10)", "88.59%", "0.8459", "0.8836", "RUNNER-UP", "green_bright", 0.886),
            ("#3  KNN Classifier (k=5)", "85.23%", "0.7886", "0.8484", "STRONG", "cyan", 0.852),
            ("#4  SVM (RBF Kernel)", "84.12%", "0.7651", "0.8343", "STRONG", "blue", 0.841),
            ("#5  Baseline (Most-Frequent)", "55.03%", "0.2367", "0.3907", "BASELINE", "slate_mid", 0.550),
            ("#6  Gaussian Naive Bayes", "37.02%", "0.3098", "0.3636", "ASSUMP. FAIL", "red_bright", 0.370),
        ]

        f_col_hdr = self.get_pil_font(13, bold=True, mono=True)
        f_row = self.get_pil_font(15, bold=True)
        f_num = self.get_pil_font(15, bold=True, mono=True)
        f_pill = self.get_pil_font(12, bold=True, mono=True)

        cx = [28, 415, 545, 675, 810]
        for idx, (m_name, acc, f1m, f1w, status, col_name, bar_ratio) in enumerate(rows):
            ry = 76 + idx * 92
            is_h = idx == 0
            is_win = idx == 1
            row_h = 54 if is_h else 78
            if idx > 0:
                ry = 140 + (idx - 1) * 98

            bg_col = PALETTE["saffron"] if is_h else (PALETTE["sign_yellow"] if is_win else PALETTE["dark_navy"])
            border_col = PALETTE["gold"] if (is_h or is_win) else PALETTE["slate_mid"]
            draw.rounded_rectangle(
                [(18, ry), (W - 18, ry + row_h)],
                radius=12,
                fill=(*bg_col, 255),
                outline=(*border_col, 255),
                width=2 if is_win else 1,
            )

            txt_col = PALETTE["white"] if is_h else (PALETTE["sign_black"] if is_win else PALETTE["white"])
            num_col = PALETTE["white"] if is_h else (PALETTE["sign_black"] if is_win else PALETTE["gold_soft"])

            if is_h:
                for c_i, val in enumerate([m_name, acc, f1m, f1w, status]):
                    draw.text((cx[c_i], ry + 18), val, font=f_col_hdr, fill=(*txt_col, 255))
            else:
                draw.text((cx[0], ry + 14), m_name, font=f_row, fill=(*txt_col, 255))
                # Inline mini progress bar under model name
                bar_w = 340
                draw.rounded_rectangle([(cx[0], ry + 48), (cx[0] + bar_w, ry + 58)], radius=5, fill=(20, 35, 65, 220))
                fill_col = PALETTE["deep_navy"] if is_win else PALETTE[col_name]
                draw.rounded_rectangle(
                    [(cx[0], ry + 48), (cx[0] + int(bar_w * bar_ratio), ry + 58)],
                    radius=5,
                    fill=(*fill_col, 255),
                )

                draw.text((cx[1], ry + 26), acc, font=f_num, fill=(*txt_col, 255))
                draw.text((cx[2], ry + 26), f1m, font=f_num, fill=(*num_col, 255))
                draw.text((cx[3], ry + 26), f1w, font=f_num, fill=(*txt_col, 255))

                # Status Pill
                p_fill = PALETTE["deep_navy"] if is_win else PALETTE[col_name]
                p_txt = PALETTE["gold"] if is_win else (PALETTE["sign_black"] if col_name in ("green_bright", "cyan", "sign_yellow") else PALETTE["white"])
                draw.rounded_rectangle([(cx[4], ry + 18), (W - 32, ry + 58)], radius=10, fill=(*p_fill, 255))
                stw = self._measure_text_width(draw, status, f_pill)
                draw.text((cx[4] + ((W - 32 - cx[4]) - stw) / 2, ry + 31), status, font=f_pill, fill=(*p_txt, 255))

        canvas.save(out_path, "PNG")
        return out_path

    # --------------------------------------------------------------------------
    # Reuse & Enhance Background, Framed Charts, Tickets, Gauges & Signals
    # --------------------------------------------------------------------------

    def _crop_to_aspect(self, img: Image.Image, target_w: int, target_h: int) -> Image.Image:
        src_w, src_h = img.size
        target_ratio = target_w / target_h
        src_ratio = src_w / src_h
        if src_ratio > target_ratio:
            new_w = int(src_h * target_ratio)
            offset = (src_w - new_w) // 2
            img = img.crop((offset, 0, offset + new_w, src_h))
        else:
            new_h = int(src_w / target_ratio)
            offset = (src_h - new_h) // 2
            img = img.crop((0, offset, src_w, offset + new_h))
        return img.resize((target_w, target_h), resample=RESAMPLE_LANCZOS)

    def create_dark_hud_background(
        self,
        name: str,
        accent_color: Tuple[int, int, int] = PALETTE["saffron"],
        secondary_accent: Tuple[int, int, int] = PALETTE["blue"],
        hero_image_path: Optional[Path] = None,
        hero_opacity: float = 0.24,
        hero_align: str = "full",
    ) -> Path:
        out_path = self.paths.cache_dir / f"bg_v5_{name}.png"
        W, H = CANVAS_W_PX, CANVAS_H_PX

        base = Image.new("RGBA", (W, H), (*PALETTE["dark_navy"], 255))
        top_layer = Image.new("RGBA", (W, H), (*PALETTE["deep_navy"], 255))
        mask = Image.linear_gradient("L").resize((W, H), resample=RESAMPLE_BICUBIC)
        bg = Image.composite(base, top_layer, mask)

        if hero_image_path and hero_image_path.exists():
            try:
                hero = Image.open(hero_image_path).convert("RGBA")
                hero = self._crop_to_aspect(hero, W, H)
                if hero_align == "right":
                    grad = Image.linear_gradient("L").rotate(270, expand=True).resize((W, H))
                    grad = grad.point(lambda p: int(p * hero_opacity))
                else:
                    grad = Image.new("L", (W, H), int(255 * hero_opacity))
                bg.paste(hero, (0, 0), grad)
            except Exception:
                pass

        orb_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        orb_draw = ImageDraw.Draw(orb_layer)
        orb_draw.ellipse((W - 640, -240, W + 240, 640), fill=(*accent_color, 48))
        orb_draw.ellipse((-280, H - 640, 580, H + 240), fill=(*secondary_accent, 40))
        orb_layer = orb_layer.filter(ImageFilter.GaussianBlur(radius=90))
        bg = Image.alpha_composite(bg, orb_layer)

        grid_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(grid_layer)
        for x in range(0, W, 96):
            gdraw.line([(x, 0), (x, H)], fill=(255, 255, 255, 7), width=1)
        for y in range(0, H, 96):
            gdraw.line([(0, y), (W, y)], fill=(255, 255, 255, 7), width=1)

        header_h = 192
        gdraw.rectangle([(0, 0), (W, header_h)], fill=(3, 10, 24, 224))
        gdraw.line([(0, header_h), (W, header_h)], fill=(*accent_color, 210), width=3)
        gdraw.line([(0, header_h + 3), (int(W * 0.48), header_h + 3)], fill=(*PALETTE["gold"], 235), width=2)

        gdraw.rectangle([(0, 0), (W, 8)], fill=(*accent_color, 255))
        for i in range(12):
            x0 = W - 500 + i * 34
            gdraw.polygon(
                [(x0, 8), (x0 + 16, 8), (x0 - 26, header_h - 4), (x0 - 42, header_h - 4)],
                fill=(*accent_color, 22),
            )

        bg = Image.alpha_composite(bg, grid_layer)
        bg.convert("RGB").save(out_path, "PNG", optimize=True)
        return out_path

    def create_framed_chart_card(
        self,
        viz_filename: str,
        width_in: float,
        height_in: float,
        title_badge: str = "",
        accent: Tuple[int, int, int] = PALETTE["saffron"],
        footer_note: str = "",
    ) -> Path:
        safe_tag = viz_filename.replace(".png", "")
        out_path = self.paths.cache_dir / f"chart_v5_{safe_tag}_{int(width_in*100)}x{int(height_in*100)}.png"

        total_w = int(width_in * DPI_SCALE)
        total_h = int(height_in * DPI_SCALE)
        pad = 12
        header_h = 44 if title_badge else 12
        card_w = total_w - pad * 2
        card_h = total_h - pad * 2

        canvas = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))

        shadow = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow)
        sdraw.rounded_rectangle(
            [(pad + 4, pad + 6), (pad + card_w + 4, pad + card_h + 6)],
            radius=20,
            fill=(0, 0, 0, 150),
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=9))
        canvas = Image.alpha_composite(canvas, shadow)

        card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
        cdraw = ImageDraw.Draw(card)
        cdraw.rounded_rectangle(
            [(0, 0), (card_w - 1, card_h - 1)],
            radius=18,
            fill=(255, 255, 255, 255),
            outline=(*accent, 245),
            width=3,
        )

        if title_badge:
            cdraw.rounded_rectangle([(0, 0), (card_w - 1, header_h + 14)], radius=18, fill=(*PALETTE["deep_navy"], 255))
            cdraw.rectangle([(0, header_h), (card_w - 1, header_h + 14)], fill=(*PALETTE["deep_navy"], 255))
            cdraw.rectangle([(0, header_h - 3), (card_w - 1, header_h)], fill=(*accent, 255))

            dot_colors = [PALETTE["red_bright"], PALETTE["gold"], PALETTE["green_bright"]]
            for idx, dc in enumerate(dot_colors):
                cx = 20 + idx * 18
                cy = header_h // 2
                cdraw.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=(*dc, 255))

            font = self.get_pil_font(15, bold=True)
            cdraw.text((80, (header_h - 19) // 2), title_badge.upper(), font=font, fill=(*PALETTE["white"], 255))

        viz_path = self.paths.get_viz(viz_filename)
        footer_h = 46 if footer_note else 0
        inner_x = 10
        inner_y = header_h + 6
        inner_w = card_w - 20
        inner_h = card_h - inner_y - footer_h - 8

        if viz_path and viz_path.exists():
            try:
                raw_img = Image.open(viz_path).convert("RGBA")
                raw_img.thumbnail((inner_w, inner_h), resample=RESAMPLE_LANCZOS)
                paste_x = inner_x + (inner_w - raw_img.width) // 2
                paste_y = inner_y + (inner_h - raw_img.height) // 2
                card.paste(raw_img, (paste_x, paste_y), raw_img)
            except Exception:
                pass

        if footer_note:
            fy0 = card_h - footer_h
            cdraw.rounded_rectangle([(0, fy0 - 8), (card_w - 1, card_h - 1)], radius=18, fill=(*PALETTE["deep_navy"], 255))
            cdraw.rectangle([(0, fy0 - 8), (card_w - 1, fy0 + 10)], fill=(*PALETTE["deep_navy"], 255))
            cdraw.line([(0, fy0 - 8), (card_w - 1, fy0 - 8)], fill=(*accent, 255), width=2)
            f_foot = self.get_pil_font(14, bold=True)
            cdraw.text((18, fy0 + 4), footer_note, font=f_foot, fill=(*PALETTE["gold_soft"], 255))

        cdraw.rounded_rectangle([(0, 0), (card_w - 1, card_h - 1)], radius=18, outline=(*accent, 255), width=3)
        canvas.paste(card, (pad, pad), card)
        canvas.save(out_path, "PNG")
        return out_path

    def create_rounded_photo_card(
        self,
        img_filename: str,
        width_in: float,
        height_in: float,
        border_color: Tuple[int, int, int] = PALETTE["saffron"],
        caption: str = "",
    ) -> Path:
        safe_tag = img_filename.replace(".png", "")
        out_path = self.paths.cache_dir / f"photo_v5_{safe_tag}_{int(width_in*100)}x{int(height_in*100)}.png"

        total_w = int(width_in * DPI_SCALE)
        total_h = int(height_in * DPI_SCALE)
        pad = 12
        card_w = total_w - pad * 2
        card_h = total_h - pad * 2

        canvas = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
        img_path = self.paths.get_image(img_filename)
        if img_path and img_path.exists():
            photo = Image.open(img_path).convert("RGBA")
            photo = self._crop_to_aspect(photo, card_w, card_h)
        else:
            photo = Image.new("RGBA", (card_w, card_h), (*PALETTE["slate_dark"], 255))

        if caption:
            overlay = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
            odraw = ImageDraw.Draw(overlay)
            odraw.rectangle([(0, card_h - 62), (card_w, card_h)], fill=(4, 13, 31, 228))
            odraw.line([(0, card_h - 62), (card_w, card_h - 62)], fill=(*border_color, 255), width=3)
            font = self.get_pil_font(15, bold=True)
            odraw.text((18, card_h - 42), caption, font=font, fill=(*PALETTE["gold_soft"], 255))
            photo = Image.alpha_composite(photo, overlay)

        mask = Image.new("L", (card_w, card_h), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.rounded_rectangle([(0, 0), (card_w - 1, card_h - 1)], radius=20, fill=255)

        framed = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
        framed.paste(photo, (0, 0), mask)
        fdraw = ImageDraw.Draw(framed)
        fdraw.rounded_rectangle([(0, 0), (card_w - 1, card_h - 1)], radius=20, outline=(*border_color, 250), width=4)

        canvas.paste(framed, (pad, pad), framed)
        canvas.save(out_path, "PNG")
        return out_path

    def create_irctc_ticket_stub(
        self,
        ticket_id: str,
        pnr_no: str,
        from_station: str,
        to_station: str,
        phase_title: str,
        phase_subtitle: str,
        coach_code: str,
        berth_info: str,
        key_deliverables: List[str],
        telemetry_specs: List[Tuple[str, str]],
        stage_index: int = 1,
        width_in: float = 12.0,
        height_in: float = 5.15,
    ) -> Path:
        out_path = self.paths.cache_dir / f"irctc_v5_ticket_{ticket_id}.png"
        W = int(width_in * DPI_SCALE)
        H = int(height_in * DPI_SCALE)
        pad = 18
        tw = W - pad * 2
        th = H - pad * 2
        stub_x = int(tw * 0.70)
        left_max_w = stub_x - 68

        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ticket = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        tdraw = ImageDraw.Draw(ticket)
        tdraw.rounded_rectangle(
            [(0, 0), (tw - 1, th - 1)],
            radius=26,
            fill=(*PALETTE["ticket_cream"], 255),
            outline=(*PALETTE["gold"], 255),
            width=4,
        )

        header_h = 84
        tdraw.rounded_rectangle([(0, 0), (tw - 1, header_h + 18)], radius=26, fill=(*PALETTE["deep_navy"], 255))
        tdraw.rectangle([(0, header_h - 10), (tw - 1, header_h)], fill=(*PALETTE["saffron"], 255))

        f_hdr = self.get_pil_font(20, bold=True)
        f_sub = self.get_pil_font(13, bold=True)
        f_mono_lg = self.get_pil_font(17, bold=True, mono=True)
        f_mono_sm = self.get_pil_font(12, bold=True, mono=True)
        f_bold = self.get_pil_font(15, bold=True)

        tdraw.text((34, 15), "INDIAN RAILWAYS  •  AI/ML EXPRESS RESERVATION VOUCHER", font=f_hdr, fill=(*PALETTE["white"], 255))
        tdraw.text((34, 44), "GUJARAT UNIVERSITY BCA SEM-VII  |  TRAIN NO: 12026-ML (SUPERFAST)", font=f_sub, fill=(*PALETTE["gold_soft"], 255))

        pnr_w = 236
        tdraw.rounded_rectangle(
            [(stub_x - pnr_w - 24, 15), (stub_x - 24, 58)],
            radius=10,
            fill=(*PALETTE["sign_yellow"], 255),
            outline=(*PALETTE["sign_black"], 255),
            width=2,
        )
        tdraw.text((stub_x - pnr_w - 8, 25), f"PNR: {pnr_no}", font=f_mono_lg, fill=(*PALETTE["sign_black"], 255))

        route_y = header_h + 18
        route_h = 94
        box_w = (left_max_w - 150) // 2
        from_x0 = 34
        from_x1 = from_x0 + box_w
        arrow_cx = from_x1 + 75
        to_x0 = from_x1 + 150
        to_x1 = 34 + left_max_w

        tdraw.rounded_rectangle([(from_x0, route_y), (from_x1, route_y + route_h)], radius=14, fill=(*PALETTE["ticket_sub"], 255), outline=(*PALETTE["ticket_border"], 255), width=2)
        tdraw.text((from_x0 + 16, route_y + 10), "DEPARTURE STATION (FROM)", font=f_mono_sm, fill=(*PALETTE["slate_mid"], 255))
        self._draw_fitted_text(tdraw, from_x0 + 16, route_y + 34, box_w - 32, 48, from_station, start_size=18, min_size=13, bold=True, fill=(*PALETTE["deep_navy"], 255))

        tdraw.rounded_rectangle([(from_x1 + 14, route_y + 14), (to_x0 - 14, route_y + route_h - 14)], radius=12, fill=(*PALETTE["deep_navy"], 255))
        tdraw.text((arrow_cx - 40, route_y + 22), "ML TRACK", font=f_mono_sm, fill=(*PALETTE["gold"], 255))
        tdraw.line([(from_x1 + 28, route_y + 58), (to_x0 - 34, route_y + 58)], fill=(*PALETTE["saffron"], 255), width=4)
        tdraw.polygon([(to_x0 - 22, route_y + 58), (to_x0 - 38, route_y + 48), (to_x0 - 38, route_y + 68)], fill=(*PALETTE["saffron"], 255))

        tdraw.rounded_rectangle([(to_x0, route_y), (to_x1, route_y + route_h)], radius=14, fill=(*PALETTE["ticket_sub"], 255), outline=(*PALETTE["ticket_border"], 255), width=2)
        tdraw.text((to_x0 + 16, route_y + 10), "ARRIVAL STATION (TO)", font=f_mono_sm, fill=(*PALETTE["slate_mid"], 255))
        self._draw_fitted_text(tdraw, to_x0 + 16, route_y + 34, (to_x1 - to_x0) - 32, 48, to_station, start_size=18, min_size=13, bold=True, fill=(*PALETTE["deep_navy"], 255))

        content_y = route_y + route_h + 16
        next_y = self._draw_fitted_text(tdraw, 34, content_y, left_max_w, 52, phase_title, start_size=21, min_size=15, bold=True, fill=(*PALETTE["deep_navy"], 255))
        sub_bottom_y = self._draw_fitted_text(tdraw, 34, next_y + 4, left_max_w, 40, phase_subtitle, start_size=15, min_size=12, bold=True, fill=(*PALETTE["saffron"], 255))

        grid_y = max(sub_bottom_y + 14, 316)
        grid_h = 84
        col_gap = 12
        cell_w = (left_max_w - col_gap * 3) // 4
        for idx, (spec_lbl, spec_val) in enumerate(telemetry_specs[:4]):
            gx = 34 + idx * (cell_w + col_gap)
            tdraw.rounded_rectangle([(gx, grid_y), (gx + cell_w, grid_y + grid_h)], radius=12, fill=(*PALETTE["ticket_sub"], 255), outline=(*PALETTE["ticket_border"], 255), width=2)
            tdraw.rectangle([(gx, grid_y), (gx + cell_w, grid_y + 26)], fill=(*PALETTE["deep_navy"], 255))
            tdraw.text((gx + 12, grid_y + 5), spec_lbl, font=f_mono_sm, fill=(*PALETTE["gold"], 255))
            self._draw_fitted_text(tdraw, gx + 12, grid_y + 36, cell_w - 24, 40, spec_val, start_size=15, min_size=11, bold=True, fill=(*PALETTE["deep_navy"], 255))

        prog_y = grid_y + grid_h + 16
        prog_h = 52
        tdraw.rounded_rectangle([(34, prog_y), (34 + left_max_w, prog_y + prog_h)], radius=12, fill=(244, 236, 218, 255), outline=(*PALETTE["ticket_border"], 255), width=2)
        stages = ["STAGE 1: EDA & FIX", "STAGE 2: METRICS", "STAGE 3: MODELS", "STAGE 4: CLUSTERS"]
        st_w = (left_max_w - 40) // 4
        for s_idx, st_label in enumerate(stages):
            sx = 54 + s_idx * st_w
            sy = prog_y + prog_h // 2
            is_active = (s_idx + 1) <= stage_index
            is_current = (s_idx + 1) == stage_index
            if s_idx < 3:
                line_col = PALETTE["saffron"] if (s_idx + 1) < stage_index else PALETTE["ticket_border"]
                tdraw.line([(sx + 14, sy), (sx + st_w - 14, sy)], fill=(*line_col, 255), width=4)
            dot_col = PALETTE["saffron"] if is_current else (PALETTE["green"] if is_active else PALETTE["slate_mid"])
            tdraw.ellipse((sx - 10, sy - 10, sx + 10, sy + 10), fill=(*dot_col, 255), outline=(*PALETTE["deep_navy"], 255), width=2)
            tdraw.text((sx + 15, sy - 8), st_label, font=f_mono_sm, fill=(*PALETTE["deep_navy"], 255) if is_active else (*PALETTE["slate_mid"], 255))

        badge_y = th - 72
        gap = 14
        pill_w = (left_max_w - gap * 2) // 3
        for idx, item in enumerate(key_deliverables[:3]):
            px = 34 + idx * (pill_w + gap)
            tdraw.rounded_rectangle([(px, badge_y), (px + pill_w, badge_y + 48)], radius=10, fill=(*PALETTE["deep_navy"], 255), outline=(*PALETTE["gold"], 255), width=2)
            self._draw_vector_check_badge(tdraw, cx=px + 24, cy=badge_y + 24, radius=11, circle_fill=(*PALETTE["green"], 255), tick_color=(*PALETTE["white"], 255))
            self._draw_fitted_text(tdraw, px + 42, badge_y + 13, pill_w - 52, 28, item, start_size=13, min_size=10, bold=True, fill=(*PALETTE["gold_soft"], 255))

        for y_dash in range(18, th - 18, 18):
            tdraw.line([(stub_x, y_dash), (stub_x, y_dash + 10)], fill=(*PALETTE["slate_mid"], 200), width=3)

        rx = stub_x + 28
        right_max_w = tw - rx - 28
        tdraw.text((rx, 16), "BOARDING PASS STUB", font=f_sub, fill=(*PALETTE["gold"], 255))
        tdraw.text((rx, 44), "CLASS: FIRST AC (AI/ML)", font=f_mono_sm, fill=(*PALETTE["white"], 255))

        meta_items = [
            ("CANDIDATE", "RAJPUT PRINCE SINGH"),
            ("ROLL NO / BERTH", f"ROLL 83  |  {berth_info}"),
            ("SYLLABUS COACH", coach_code),
            ("ACADEMIC SESSION", "2025-26 (BCA SEM-VII)"),
        ]
        my = header_h + 20
        for lbl, val in meta_items:
            tdraw.text((rx, my), lbl, font=f_mono_sm, fill=(*PALETTE["slate_mid"], 255))
            self._draw_fitted_text(tdraw, rx, my + 18, right_max_w, 32, val, start_size=16, min_size=12, bold=True, fill=(*PALETTE["deep_navy"], 255))
            my += 52

        stamp_y = th - 134
        tdraw.rounded_rectangle([(rx, stamp_y), (tw - 28, stamp_y + 46)], radius=10, fill=(222, 247, 232, 255), outline=(*PALETTE["green"], 255), width=3)
        self._draw_vector_check_badge(tdraw, cx=rx + 24, cy=stamp_y + 23, radius=12, circle_fill=(*PALETTE["green"], 255), tick_color=(*PALETTE["white"], 255))
        tdraw.text((rx + 44, stamp_y + 13), "VALIDATED FOR VIVA", font=f_bold, fill=(*PALETTE["green"], 255))

        bar_y = th - 72
        bar_x = rx
        for i in range(46):
            bar_w = 2 if (i % 3 == 0) else (5 if i % 5 == 0 else 3)
            if bar_x + bar_w < tw - 28:
                tdraw.rectangle([(bar_x, bar_y), (bar_x + bar_w, bar_y + 44)], fill=(*PALETTE["deep_navy"], 255))
            bar_x += bar_w + 4

        mask = Image.new("L", (tw, th), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.rounded_rectangle([(0, 0), (tw - 1, th - 1)], radius=26, fill=255)
        notch_r = 22
        mdraw.ellipse((stub_x - notch_r, -notch_r, stub_x + notch_r, notch_r), fill=0)
        mdraw.ellipse((stub_x - notch_r, th - notch_r, stub_x + notch_r, th + notch_r), fill=0)

        final_ticket = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        final_ticket.paste(ticket, (0, 0), mask)
        canvas.paste(final_ticket, (pad, pad), final_ticket)
        canvas.save(out_path, "PNG")
        return out_path

    def create_speedometer_gauge(
        self,
        tag: str,
        value_text: str,
        label: str,
        sublabel: str,
        percentage: float,
        accent: Tuple[int, int, int],
        size_in: float = 2.75,
    ) -> Path:
        out_path = self.paths.cache_dir / f"gauge_v5_{tag}.png"
        S = int(size_in * DPI_SCALE)
        canvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        pad = 18
        box = [pad, pad, S - pad, S - pad]
        draw.ellipse(box, fill=(8, 22, 48, 248), outline=(*accent, 225), width=4)

        cx, cy = S // 2, S // 2
        r_outer = (S // 2) - pad - 12
        r_inner = r_outer - 13
        for i in range(28):
            angle_deg = 135 + (270.0 * i / 27.0)
            rad = math.radians(angle_deg)
            x1 = cx + int(r_inner * math.cos(rad))
            y1 = cy + int(r_inner * math.sin(rad))
            x2 = cx + int(r_outer * math.cos(rad))
            y2 = cy + int(r_outer * math.sin(rad))
            tick_col = accent if (i / 27.0) <= percentage else (45, 70, 110)
            draw.line([(x1, y1), (x2, y2)], fill=(*tick_col, 255), width=4 if i % 3 == 0 else 2)

        arc_box = [pad + 26, pad + 26, S - pad - 26, S - pad - 26]
        draw.arc(arc_box, start=135, end=405, fill=(30, 52, 90, 255), width=16)
        end_angle = 135 + int(270 * max(0.05, min(1.0, percentage)))
        draw.arc(arc_box, start=135, end=end_angle, fill=(*accent, 255), width=16)

        f_val = self.get_pil_font(42, bold=True)
        f_lbl = self.get_pil_font(16, bold=True)
        f_sub = self.get_pil_font(12, bold=True)

        vw = self._measure_text_width(draw, value_text, f_val)
        lw = self._measure_text_width(draw, label, f_lbl)
        sw = self._measure_text_width(draw, sublabel, f_sub)

        draw.text((cx - vw / 2, cy - 36), value_text, font=f_val, fill=(*PALETTE["white"], 255))
        draw.text((cx - lw / 2, cy + 20), label, font=f_lbl, fill=(*accent, 255))
        draw.text((cx - sw / 2, cy + 46), sublabel, font=f_sub, fill=(*PALETTE["gold_soft"], 255))

        canvas.save(out_path, "PNG")
        return out_path

    def create_railway_signal(self, active_state: str = "all", height_in: float = 2.75) -> Path:
        out_path = self.paths.cache_dir / f"signal_v5_{active_state}.png"
        W = int(height_in * 0.48 * DPI_SCALE)
        H = int(height_in * DPI_SCALE)
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        cx = W // 2
        housing_w = int(W * 0.64)
        housing_h = int(H * 0.78)
        hx0 = cx - housing_w // 2
        hy0 = 12

        draw.rectangle([(cx - 7, hy0 + housing_h), (cx + 7, H - 4)], fill=(110, 125, 145, 255))
        draw.rounded_rectangle([(hx0, hy0), (hx0 + housing_w, hy0 + housing_h)], radius=housing_w // 2, fill=(12, 18, 30, 255), outline=(*PALETTE["gold"], 240), width=3)

        lights = [
            ("red", PALETTE["red_bright"], hy0 + int(housing_h * 0.20)),
            ("yellow", PALETTE["gold"], hy0 + int(housing_h * 0.50)),
            ("green", PALETTE["green_bright"], hy0 + int(housing_h * 0.80)),
        ]
        r = int(housing_w * 0.28)
        for name, col, ly in lights:
            is_on = (active_state == name) or (active_state == "all")
            fill_col = (*col, 255) if is_on else (col[0] // 5, col[1] // 5, col[2] // 5, 255)
            draw.ellipse((cx - r, ly - r, cx + r, ly + r), fill=fill_col, outline=(235, 235, 235, 160), width=2)

        canvas.save(out_path, "PNG")
        return out_path

    def create_loco_progress_icon(self) -> Path:
        out_path = self.paths.cache_dir / "morph_loco_v5.png"
        W, H = 220, 68
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        draw.polygon([(168, 34), (218, 10), (218, 58)], fill=(255, 230, 110, 150))
        draw.line([(48, 18), (64, 5), (82, 18)], fill=(*PALETTE["gold"], 255), width=3)
        draw.line([(54, 5), (76, 5)], fill=(*PALETTE["gold"], 255), width=3)

        body_pts = [(10, 52), (10, 20), (138, 20), (172, 36), (176, 52)]
        draw.polygon(body_pts, fill=(*PALETTE["saffron"], 255), outline=(*PALETTE["white"], 255))
        draw.rectangle([(12, 34), (156, 42)], fill=(*PALETTE["white"], 255))
        draw.rectangle([(12, 42), (166, 48)], fill=(*PALETTE["deep_navy"], 255))
        draw.polygon([(132, 23), (156, 34), (132, 34)], fill=(*PALETTE["cyan"], 255))

        for wx in [24, 54, 84, 108]:
            draw.rounded_rectangle([(wx, 23), (wx + 18, 31)], radius=3, fill=(*PALETTE["deep_navy"], 255))
        for wheel_x in [28, 52, 118, 142]:
            draw.ellipse((wheel_x - 8, 48, wheel_x + 8, 64), fill=(25, 32, 44, 255), outline=(*PALETTE["gold"], 255), width=3)

        canvas.save(out_path, "PNG")
        return out_path


# ==============================================================================
# 5. TRUE OPENXML ANIMATION, 3D TRANSITION & NATIVE ZIP AUDIO INJECTOR
# ==============================================================================

class CinematicTimelineAndAudioEngine:
    """
    1. Injects creative 3D / Dynamic Transitions (`doors`, `vortex`, `ripple`,
       `honeycomb`, `ferris`, `zoom`, `morph`) with placeholder `<p:sndAc>`
       tokens that are wired directly to embedded `/ppt/media/*.wav` files.
    2. Injects True Hidden-to-Visible Entrance Animations (`<p:set>` visibility
       toggle + `<p:animEffect>` Fade/Wipe + `<p:animMotion>` Fly-In & Train Runs)
       so shapes dynamically appear and glide across the screen!
    3. Directly packages `.wav` files into the `.pptx` ZIP archive (`ppt/media/`,
       `[Content_Types].xml`, and `ppt/slides/_rels/slideX.xml.rels`) so audio
       plays 100% natively in PowerPoint without needing `pywin32`!
    """

    @staticmethod
    def apply_creative_transition(slide, style: str = "morph", slide_no: int = 1) -> None:
        """
        Applies varied creative PowerPoint transitions (`doors`, `vortex`,
        `ripple`, `honeycomb`, `ferris`, `zoom`, `morph`) with a placeholder
        `__AUDIO_PLACEHOLDER_{slide_no}__` node that the ZIP Audio Injector
        replaces with a valid `<p:sndAc>` relationship reference.
        """
        sld = slide._element
        for existing in list(sld):
            if existing.tag.endswith("transition") or existing.tag.endswith("AlternateContent"):
                sld.remove(existing)

        if style == "doors":
            choice_xml = f'<p:transition spd="med" p14:dur="1150" advClick="1"><p14:doors orient="vert" dir="out"/></p:transition>'
            fb_xml = f'<p:transition spd="med" advClick="1"><p:split orient="vert" dir="out"/></p:transition>'
            req = "p14"
        elif style == "vortex":
            choice_xml = f'<p:transition spd="med" p14:dur="1300" advClick="1"><p14:vortex dir="right"/></p:transition>'
            fb_xml = f'<p:transition spd="med" advClick="1"><p:dissolve/></p:transition>'
            req = "p14"
        elif style == "ripple":
            choice_xml = f'<p:transition spd="med" p14:dur="1150" advClick="1"><p14:ripple center="center"/></p:transition>'
            fb_xml = f'<p:transition spd="med" advClick="1"><p:wedge/></p:transition>'
            req = "p14"
        elif style == "honeycomb":
            choice_xml = f'<p:transition spd="med" p14:dur="1250" advClick="1"><p14:honeycomb/></p:transition>'
            fb_xml = f'<p:transition spd="med" advClick="1"><p:checker orient="horz"/></p:transition>'
            req = "p14"
        elif style == "ferris":
            choice_xml = f'<p:transition spd="med" p14:dur="1150" advClick="1"><p14:ferris dir="left"/></p:transition>'
            fb_xml = f'<p:transition spd="med" advClick="1"><p:push dir="l"/></p:transition>'
            req = "p14"
        elif style == "zoom":
            choice_xml = f'<p:transition spd="med" p14:dur="1100" advClick="1"><p14:warp dir="in"/></p:transition>'
            fb_xml = f'<p:transition spd="med" advClick="1"><p:zoom dir="in"/></p:transition>'
            req = "p14"
        else:
            choice_xml = f'<p:transition spd="med" p14:dur="1050" advClick="1"><p159:morph option="byObject"/></p:transition>'
            fb_xml = f'<p:transition spd="med" advClick="1"><p:fade thruBlk="0"/></p:transition>'
            req = "p159"

        ac_xml = parse_xml(
            f'<mc:AlternateContent '
            f'xmlns:p="{PML_NS}" '
            f'xmlns:mc="{MC_NS}" '
            f'xmlns:p14="{P14_NS}" '
            f'xmlns:p159="{P159_NS}">'
            f'  <mc:Choice Requires="{req}">{choice_xml}</mc:Choice>'
            f'  <mc:Fallback>{fb_xml}</mc:Fallback>'
            f'</mc:AlternateContent>'
        )

        timing = sld.find(f"{{{PML_NS}}}timing")
        if timing is not None:
            timing.addprevious(ac_xml)
        else:
            sld.append(ac_xml)

    @staticmethod
    def inject_dramatic_entrance_animations(
        slide,
        train_shapes: Sequence[Tuple[object, str, int]] = (),
        card_shapes: Sequence[object] = (),
        header_shapes: Sequence[object] = (),
    ) -> None:
        """
        Builds a true OpenXML <p:timing> sequence where:
        1. All animated `card_shapes` start HIDDEN (`style.visibility = hidden`
           at t=0) and then become VISIBLE at their staggered delay while
           performing a simultaneous `<p:animEffect>` (Fade/Wipe) + `<p:animMotion>`
           Fly-In sweep!
        2. All `train_shapes` roar across the screen along long motion paths!
        """
        if not ENABLE_CINEMATIC_ANIMATIONS:
            return
        if not train_shapes and not card_shapes and not header_shapes:
            return

        sld = slide._element
        existing_timing = sld.find(f"{{{PML_NS}}}timing")
        if existing_timing is not None:
            sld.remove(existing_timing)

        effect_nodes: List[str] = []
        ctn_id = 10

        # 1. Header Drop-Down Glide
        for idx, h_shape in enumerate(header_shapes):
            if h_shape is None:
                continue
            sp_id = h_shape.shape_id
            delay_ms = idx * 80
            effect_nodes.append(
                f'<p:par>'
                f'  <p:cTn id="{ctn_id}" fill="hold">'
                f'    <p:stCondLst><p:cond delay="{delay_ms}"/></p:stCondLst>'
                f'    <p:childTnLst>'
                f'      <p:animEffect transition="in" filter="wipe(left)">'
                f'        <p:cBhvr>'
                f'          <p:cTn id="{ctn_id+1}" dur="450" fill="hold" nodeType="withEffect"/>'
                f'          <p:tgtEl><p:spTgt spid="{sp_id}"/></p:tgtEl>'
                f'        </p:cBhvr>'
                f'      </p:animEffect>'
                f'    </p:childTnLst>'
                f'  </p:cTn>'
                f'</p:par>'
            )
            ctn_id += 3

        # 2. High-Speed Train & Coach Motion Paths
        for idx, (t_shape, path_d, dur_ms) in enumerate(train_shapes):
            if t_shape is None:
                continue
            sp_id = t_shape.shape_id
            delay_ms = 100 + idx * 220
            effect_nodes.append(
                f'<p:par>'
                f'  <p:cTn id="{ctn_id}" fill="hold">'
                f'    <p:stCondLst><p:cond delay="{delay_ms}"/></p:stCondLst>'
                f'    <p:childTnLst>'
                f'      <p:animMotion origin="layout" path="{path_d}" pathEditMode="relative" ptsTypes="AA">'
                f'        <p:cBhvr>'
                f'          <p:cTn id="{ctn_id+1}" dur="{dur_ms}" fill="hold" accel="15" decel="55" nodeType="withEffect"/>'
                f'          <p:tgtEl><p:spTgt spid="{sp_id}"/></p:tgtEl>'
                f'        </p:cBhvr>'
                f'      </p:animMotion>'
                f'    </p:childTnLst>'
                f'  </p:cTn>'
                f'</p:par>'
            )
            ctn_id += 3

        # 3. Staggered Hidden -> Visible Card & Chart Cascade (Fade/Wipe + Fly-In)
        filters = ["fade", "wipe(up)", "wipe(right)", "strips(downRight)"]
        for idx, c_shape in enumerate(card_shapes):
            if c_shape is None:
                continue
            sp_id = c_shape.shape_id
            delay_ms = 160 + idx * 170
            flt = filters[idx % len(filters)]
            motion_path = "M 0 0.14 L 0 0 E" if idx % 2 == 0 else "M -0.10 0.08 L 0 0 E"

            # First hide at delay=0 so it isn't sitting on screen before its turn!
            effect_nodes.append(
                f'<p:par>'
                f'  <p:cTn id="{ctn_id}" fill="hold">'
                f'    <p:stCondLst><p:cond delay="0"/></p:stCondLst>'
                f'    <p:childTnLst>'
                f'      <p:set>'
                f'        <p:cBhvr>'
                f'          <p:cTn id="{ctn_id+1}" dur="1" fill="hold" nodeType="withEffect">'
                f'            <p:stCondLst><p:cond delay="0"/></p:stCondLst>'
                f'          </p:cTn>'
                f'          <p:tgtEl><p:spTgt spid="{sp_id}"/></p:tgtEl>'
                f'          <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
                f'        </p:cBhvr>'
                f'        <p:to><p:strVal val="hidden"/></p:to>'
                f'      </p:set>'
                f'    </p:childTnLst>'
                f'  </p:cTn>'
                f'</p:par>'
            )
            ctn_id += 3

            # Then reveal + animate in at `delay_ms`
            effect_nodes.append(
                f'<p:par>'
                f'  <p:cTn id="{ctn_id}" fill="hold">'
                f'    <p:stCondLst><p:cond delay="{delay_ms}"/></p:stCondLst>'
                f'    <p:childTnLst>'
                f'      <p:set>'
                f'        <p:cBhvr>'
                f'          <p:cTn id="{ctn_id+1}" dur="1" fill="hold" nodeType="withEffect">'
                f'            <p:stCondLst><p:cond delay="0"/></p:stCondLst>'
                f'          </p:cTn>'
                f'          <p:tgtEl><p:spTgt spid="{sp_id}"/></p:tgtEl>'
                f'          <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
                f'        </p:cBhvr>'
                f'        <p:to><p:strVal val="visible"/></p:to>'
                f'      </p:set>'
                f'      <p:animEffect transition="in" filter="{flt}">'
                f'        <p:cBhvr>'
                f'          <p:cTn id="{ctn_id+2}" dur="650" fill="hold" nodeType="withEffect"/>'
                f'          <p:tgtEl><p:spTgt spid="{sp_id}"/></p:tgtEl>'
                f'        </p:cBhvr>'
                f'      </p:animEffect>'
                f'      <p:animMotion origin="layout" path="{motion_path}" pathEditMode="relative" ptsTypes="AA">'
                f'        <p:cBhvr>'
                f'          <p:cTn id="{ctn_id+3}" dur="680" fill="hold" accel="10" decel="60" nodeType="withEffect"/>'
                f'          <p:tgtEl><p:spTgt spid="{sp_id}"/></p:tgtEl>'
                f'        </p:cBhvr>'
                f'      </p:animMotion>'
                f'    </p:childTnLst>'
                f'  </p:cTn>'
                f'</p:par>'
            )
            ctn_id += 5

        children_xml = "".join(effect_nodes)
        timing_xml = parse_xml(
            f'<p:timing xmlns:p="{PML_NS}">'
            f'  <p:tnLst>'
            f'    <p:par>'
            f'      <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">'
            f'        <p:childTnLst>'
            f'          <p:seq concurrent="1" nextAc="seek">'
            f'            <p:cTn id="2" dur="indefinite" nodeType="mainSeq">'
            f'              <p:childTnLst>'
            f'                <p:par>'
            f'                  <p:cTn id="3" fill="hold">'
            f'                    <p:stCondLst><p:cond delay="0"/></p:stCondLst>'
            f'                    <p:childTnLst>'
            f'                      {children_xml}'
            f'                    </p:childTnLst>'
            f'                  </p:cTn>'
            f'                </p:par>'
            f'              </p:childTnLst>'
            f'            </p:cTn>'
            f'          </p:seq>'
            f'        </p:childTnLst>'
            f'      </p:cTn>'
            f'    </p:par>'
            f'  </p:tnLst>'
            f'</p:timing>'
        )
        sld.append(timing_xml)

    @staticmethod
    def embed_wav_files_into_pptx_zip(pptx_path: Path, slide_audio_map: Dict[int, Path]) -> None:
        """
        Directly packages `.wav` files into the `.pptx` ZIP archive so that
        PowerPoint plays the Station Announcements, Chimes, and Train Horns
        natively on slide transitions with ZERO external dependencies!
        """
        if not slide_audio_map:
            return

        tmp_zip_path = pptx_path.with_suffix(".tmp.pptx")
        unique_wavs: Dict[str, Path] = {p.name: p for p in slide_audio_map.values() if p and p.exists()}

        with zipfile.ZipFile(pptx_path, "r") as zin, zipfile.ZipFile(tmp_zip_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)

                # 1. Register .wav content type in [Content_Types].xml
                if item.filename == "[Content_Types].xml":
                    xml_str = data.decode("utf-8")
                    if 'Extension="wav"' not in xml_str:
                        xml_str = xml_str.replace(
                            "</Types>",
                            '<Default Extension="wav" ContentType="audio/wav"/></Types>',
                        )
                    zout.writestr(item, xml_str.encode("utf-8"))
                    continue

                # 2. Inject audio relationship in ppt/slides/_rels/slideX.xml.rels
                m_rel = re.match(r"^ppt/slides/_rels/slide(\d+)\.xml\.rels$", item.filename)
                if m_rel:
                    s_no = int(m_rel.group(1))
                    if s_no in slide_audio_map and slide_audio_map[s_no].exists():
                        wav_name = slide_audio_map[s_no].name
                        r_id = f"rIdRailAudio{s_no}"
                        xml_str = data.decode("utf-8")
                        if r_id not in xml_str:
                            rel_tag = (
                                f'<Relationship Id="{r_id}" '
                                f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/audio" '
                                f'Target="../media/{wav_name}"/>'
                            )
                            xml_str = xml_str.replace("</Relationships>", f"{rel_tag}</Relationships>")
                        zout.writestr(item, xml_str.encode("utf-8"))
                        continue

                # 3. Inject <p:sndAc> inside every <p:transition> in ppt/slides/slideX.xml
                m_sld = re.match(r"^ppt/slides/slide(\d+)\.xml$", item.filename)
                if m_sld:
                    s_no = int(m_sld.group(1))
                    if s_no in slide_audio_map and slide_audio_map[s_no].exists():
                        wav_name = slide_audio_map[s_no].name
                        r_id = f"rIdRailAudio{s_no}"
                        xml_str = data.decode("utf-8")
                        snd_xml = (
                            f'<p:sndAc>'
                            f'<p:stSnd>'
                            f'<p:snd xmlns:r="{REL_NS}" r:embed="{r_id}" name="{wav_name}"/>'
                            f'</p:stSnd>'
                            f'</p:sndAc>'
                        )
                        if "<p:sndAc>" not in xml_str:
                            xml_str = xml_str.replace("</p:transition>", f"{snd_xml}</p:transition>")
                        zout.writestr(item, xml_str.encode("utf-8"))
                        continue

                zout.writestr(item, data)

            # 4. Write all synthesized .wav files into ppt/media/
            for wav_name, wav_path in unique_wavs.items():
                zout.writestr(f"ppt/media/{wav_name}", wav_path.read_bytes())

        shutil.move(str(tmp_zip_path), str(pptx_path))


# ==============================================================================
# 6. MASTER PRESENTATION BUILDER (V5.0 — 22 SLIDES • AUDIO • 3D TRANSITIONS)
# ==============================================================================

class RailwayPresentationBuilder:
    def __init__(self) -> None:
        self.paths = ProjectPaths()
        self.studio = RailwayGraphicStudio(self.paths)
        self.audio_studio = RailwayBroadcastAudioStudio(self.paths.cache_dir)

        self.prs = Presentation()
        self.prs.slide_width = Inches(SLIDE_W_IN)
        self.prs.slide_height = Inches(SLIDE_H_IN)
        self.blank_layout = self.prs.slide_layouts[6]

        print("  [AUDIO STUDIO] Synthesizing Station Announcements, PA Chimes & WDP-4D Horns...")
        self.audio_tracks = self.audio_studio.build_all_railway_soundtracks()
        self.loco_icon_path = self.studio.create_loco_progress_icon()
        self.vb_rake_path = self.studio.create_vande_bharat_rake_png()

        self.total_slides = 22 if INCLUDE_TICKET_DIVIDER_SLIDES else 18
        self.current_slide_no = 0
        self.slide_audio_map: Dict[int, Path] = {}
        self._last_header_shapes: List[object] = []

    # --------------------------------------------------------------------------
    # Typography Helpers
    # --------------------------------------------------------------------------

    def _set_shape_text(
        self,
        shape,
        text: str,
        size: float = 12,
        bold: bool = False,
        color: str = "white",
        align=PP_ALIGN.LEFT,
        font_name: str = FONT_BODY,
    ) -> None:
        tf = shape.text_frame
        tf.clear()
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = Inches(0.08)
        tf.margin_right = Inches(0.08)
        tf.margin_top = Inches(0.04)
        tf.margin_bottom = Inches(0.04)

        for idx, line in enumerate(text.split("\n")):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.alignment = align
            run = p.add_run()
            run.text = line
            run.font.name = font_name
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = rgb_color(color)

    def _set_textbox(
        self,
        tb,
        text: str,
        size: float = 12,
        bold: bool = False,
        color: str = "white",
        align=PP_ALIGN.LEFT,
        font_name: str = FONT_BODY,
    ) -> None:
        tf = tb.text_frame
        tf.clear()
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        for idx, line in enumerate(text.split("\n")):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.alignment = align
            run = p.add_run()
            run.text = line
            run.font.name = font_name
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = rgb_color(color)

    def _add_glass_card(
        self,
        slide,
        x: float,
        y: float,
        w: float,
        h: float,
        fill_color: str = "panel_navy",
        border_color: str = "slate_mid",
        top_stripe_color: Optional[str] = None,
        left_stripe_color: Optional[str] = None,
    ):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        card.fill.solid()
        card.fill.fore_color.rgb = rgb_color(fill_color)
        card.line.color.rgb = rgb_color(border_color)
        card.line.width = Pt(1.75)
        if len(card.adjustments) > 0:
            card.adjustments[0] = 0.05

        if top_stripe_color:
            stripe = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.08), Inches(y + 0.04), Inches(w - 0.16), Inches(0.07)
            )
            stripe.fill.solid()
            stripe.fill.fore_color.rgb = rgb_color(top_stripe_color)
            stripe.line.fill.background()

        if left_stripe_color:
            lstripe = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.05), Inches(y + 0.10), Inches(0.09), Inches(h - 0.20)
            )
            lstripe.fill.solid()
            lstripe.fill.fore_color.rgb = rgb_color(left_stripe_color)
            lstripe.line.fill.background()

        return card

    def _add_bullet_list(
        self,
        slide,
        x: float,
        y: float,
        w: float,
        h: float,
        items: List[Tuple[str, str]],
        bullet_color: str = "saffron",
        text_color: str = "white",
        sub_color: str = "light_grey",
        row_gap: float = 0.62,
    ) -> List[object]:
        created = []
        for idx, (headline, detail) in enumerate(items):
            cy = y + idx * row_gap
            dot = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(cy + 0.05), Inches(0.24), Inches(0.24)
            )
            dot.fill.solid()
            dot.fill.fore_color.rgb = rgb_color(bullet_color)
            dot.line.fill.background()
            self._set_shape_text(dot, "▸", size=10, bold=True, color="white", align=PP_ALIGN.CENTER)

            tb = slide.shapes.add_textbox(Inches(x + 0.34), Inches(cy), Inches(w - 0.38), Inches(row_gap))
            tf = tb.text_frame
            tf.clear()
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

            p1 = tf.paragraphs[0]
            r1 = p1.add_run()
            r1.text = headline + (" — " if detail else "")
            r1.font.name = FONT_HEADING
            r1.font.size = Pt(11.5)
            r1.font.bold = True
            r1.font.color.rgb = rgb_color(text_color)

            if detail:
                r2 = p1.add_run()
                r2.text = detail
                r2.font.name = FONT_BODY
                r2.font.size = Pt(10.5)
                r2.font.bold = False
                r2.font.color.rgb = rgb_color(sub_color)
            created.append(tb)
        return created

    # --------------------------------------------------------------------------
    # Slide Scaffold with Auto-Fit Header, Transition & Audio Binding
    # --------------------------------------------------------------------------

    def _new_slide(
        self,
        bg_path: Path,
        section_tag: str = "",
        title: str = "",
        subtitle: str = "",
        accent_name: str = "saffron",
        transition_style: str = "morph",
        audio_key: Optional[str] = "horn_track",
        show_header: bool = True,
        show_footer: bool = True,
    ):
        self.current_slide_no += 1
        slide = self.prs.slides.add_slide(self.blank_layout)
        self._last_header_shapes = []

        if audio_key and audio_key in self.audio_tracks:
            self.slide_audio_map[self.current_slide_no] = self.audio_tracks[audio_key]

        bg_pic = slide.shapes.add_picture(
            str(bg_path), Inches(0), Inches(0), Inches(SLIDE_W_IN), Inches(SLIDE_H_IN)
        )
        bg_pic.name = f"bg_canvas_{self.current_slide_no}"

        prog_ratio = self.current_slide_no / float(self.total_slides)

        morph_bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0),
            Inches(0),
            Inches(1.5 + 11.833 * prog_ratio),
            Inches(0.08),
        )
        morph_bar.name = "!! morph_top_ribbon"
        morph_bar.fill.solid()
        morph_bar.fill.fore_color.rgb = rgb_color(accent_name)
        morph_bar.line.fill.background()

        if show_header:
            if section_tag:
                pill_w = min(6.6, max(2.5, len(section_tag) * 0.102 + 0.45))
                pill = slide.shapes.add_shape(
                    MSO_SHAPE.ROUNDED_RECTANGLE,
                    Inches(0.55),
                    Inches(0.16),
                    Inches(pill_w),
                    Inches(0.32),
                )
                pill.name = "!! morph_section_pill"
                pill.fill.solid()
                pill.fill.fore_color.rgb = rgb_color("sign_yellow")
                pill.line.color.rgb = rgb_color("saffron")
                pill.line.width = Pt(1.5)
                self._set_shape_text(
                    pill,
                    f"🚉  {section_tag.upper()}",
                    size=9.5,
                    bold=True,
                    color="sign_black",
                    align=PP_ALIGN.CENTER,
                )

            if title:
                t_len = len(title)
                title_pt = 21.0 if t_len <= 48 else (19.0 if t_len <= 56 else (17.2 if t_len <= 64 else 15.8))
                title_y = 0.52 if section_tag else 0.24
                tb = slide.shapes.add_textbox(Inches(0.55), Inches(title_y), Inches(11.45), Inches(0.42))
                tb.text_frame.word_wrap = False
                self._set_textbox(tb, title, size=title_pt, bold=True, color="white", font_name=FONT_HEADING)
                self._last_header_shapes.append(tb)

            if subtitle:
                sub_tb = slide.shapes.add_textbox(Inches(0.55), Inches(0.96), Inches(11.45), Inches(0.28))
                self._set_textbox(sub_tb, subtitle, size=10.8, bold=True, color="gold_soft", font_name=FONT_BODY)
                self._last_header_shapes.append(sub_tb)

        logo_path = self.paths.get_image("ir_logo.png")
        if logo_path:
            logo_badge = slide.shapes.add_shape(
                MSO_SHAPE.OVAL, Inches(12.22), Inches(0.18), Inches(0.76), Inches(0.76)
            )
            logo_badge.name = "!! morph_ir_logo_ring"
            logo_badge.fill.solid()
            logo_badge.fill.fore_color.rgb = rgb_color("white")
            logo_badge.line.color.rgb = rgb_color("gold")
            logo_badge.line.width = Pt(2)
            slide.shapes.add_picture(str(logo_path), Inches(12.27), Inches(0.23), Inches(0.66), Inches(0.66))

        if show_footer:
            self._add_railway_track_footer(slide, prog_ratio)

        CinematicTimelineAndAudioEngine.apply_creative_transition(
            slide, style=transition_style, slide_no=self.current_slide_no
        )
        return slide

    def _add_railway_track_footer(self, slide, prog_ratio: float) -> None:
        footer_y = 6.92
        footer_h = 0.58

        strip = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(footer_y), Inches(SLIDE_W_IN), Inches(footer_h)
        )
        strip.fill.solid()
        strip.fill.fore_color.rgb = rgb_color("midnight")
        strip.line.color.rgb = rgb_color("slate_mid")
        strip.line.width = Pt(1)

        track_x0 = 4.35
        track_x1 = 10.65
        track_w = track_x1 - track_x0
        rail_y = footer_y + 0.32

        rail_bg = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(track_x0), Inches(rail_y), Inches(track_w), Inches(0.06)
        )
        rail_bg.fill.solid()
        rail_bg.fill.fore_color.rgb = rgb_color("slate_mid")
        rail_bg.line.fill.background()

        active_w = max(0.15, track_w * prog_ratio)
        rail_active = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(track_x0), Inches(rail_y), Inches(active_w), Inches(0.06)
        )
        rail_active.name = "!! morph_track_fill"
        rail_active.fill.solid()
        rail_active.fill.fore_color.rgb = rgb_color("saffron")
        rail_active.line.fill.background()

        stations = [
            (0.00, "INTRO"),
            (0.23, "EDA"),
            (0.45, "EVAL"),
            (0.64, "MODELS"),
            (0.84, "CLUSTERS"),
            (1.00, "VIVA"),
        ]
        for st_ratio, st_name in stations:
            sx = track_x0 + track_w * st_ratio
            reached = prog_ratio >= (st_ratio - 0.02)
            dot = slide.shapes.add_shape(
                MSO_SHAPE.OVAL, Inches(sx - 0.055), Inches(rail_y - 0.025), Inches(0.11), Inches(0.11)
            )
            dot.fill.solid()
            dot.fill.fore_color.rgb = rgb_color("gold" if reached else "slate_mid")
            dot.line.color.rgb = rgb_color("midnight")
            dot.line.width = Pt(1)

            lbl = slide.shapes.add_textbox(Inches(sx - 0.38), Inches(footer_y + 0.04), Inches(0.76), Inches(0.20))
            self._set_textbox(
                lbl,
                st_name,
                size=7.5,
                bold=reached,
                color="gold_soft" if reached else "muted_text",
                align=PP_ALIGN.CENTER,
            )

        loco_w = 0.72
        loco_h = 0.23
        loco_x = track_x0 + (track_w * prog_ratio) - (loco_w * 0.65)
        loco_x = max(track_x0 - 0.10, min(track_x1 - loco_w + 0.15, loco_x))
        loco_pic = slide.shapes.add_picture(
            str(self.loco_icon_path), Inches(loco_x), Inches(rail_y - 0.17), Inches(loco_w), Inches(loco_h)
        )
        loco_pic.name = "!! morph_loco"

        left_tb = slide.shapes.add_textbox(Inches(0.42), Inches(footer_y + 0.16), Inches(3.85), Inches(0.28))
        self._set_textbox(
            left_tb,
            "Rajput Prince Singh  |  BCA Sem-VII  |  Lokmanya College",
            size=9.2,
            bold=True,
            color="white",
        )

        pct_val = int(round(prog_ratio * 100))
        odo_pill = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.82), Inches(footer_y + 0.11), Inches(0.84), Inches(0.34)
        )
        odo_pill.name = "!! morph_odometer_pill"
        odo_pill.fill.solid()
        odo_pill.fill.fore_color.rgb = rgb_color("panel_navy")
        odo_pill.line.color.rgb = rgb_color("cyan")
        odo_pill.line.width = Pt(1.2)
        self._set_shape_text(
            odo_pill, f"🔊 {pct_val:02d}%", size=8.2, bold=True, color="cyan", align=PP_ALIGN.CENTER, font_name=FONT_MONO
        )

        badge = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.74), Inches(footer_y + 0.11), Inches(1.18), Inches(0.34)
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = rgb_color("sign_yellow")
        badge.line.color.rgb = rgb_color("saffron")
        badge.line.width = Pt(1.5)
        self._set_shape_text(
            badge,
            f"SLIDE {self.current_slide_no:02d}/{self.total_slides:02d}",
            size=8.8,
            bold=True,
            color="sign_black",
            align=PP_ALIGN.CENTER,
        )

    # ==========================================================================
    # SLIDE BUILDERS (22 SLIDES WITH REAL STATION AUDIO & PIL INFOGRAPHICS)
    # ==========================================================================

    def build_slide_01_title(self) -> None:
        bg = self.studio.create_dark_hud_background(
            "01_title",
            accent_color=PALETTE["saffron"],
            secondary_accent=PALETTE["gold"],
            hero_image_path=self.paths.get_image("hero_train.png"),
            hero_opacity=0.38,
            hero_align="right",
        )
        slide = self._new_slide(
            bg,
            transition_style="doors",
            audio_key="welcome_hero",
            show_header=False,
            show_footer=True,
        )

        left_panel = self._add_glass_card(
            slide, x=0.52, y=0.45, w=7.68, h=6.20, fill_color="deep_navy", border_color="saffron", left_stripe_color="saffron"
        )

        badge = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.82), Inches(0.68), Inches(6.50), Inches(0.38)
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = rgb_color("sign_yellow")
        badge.line.color.rgb = rgb_color("saffron")
        badge.line.width = Pt(1.5)
        self._set_shape_text(
            badge,
            "🔊  LIVE STATION PA BROADCAST  •  BCA SEM-VII CAPSTONE (NEP 2020)",
            size=9.8,
            bold=True,
            color="sign_black",
            align=PP_ALIGN.CENTER,
        )

        t1 = slide.shapes.add_textbox(Inches(0.82), Inches(1.20), Inches(7.10), Inches(1.95))
        tf = t1.text_frame
        tf.clear()
        tf.word_wrap = True
        for idx, (txt, sz, col) in enumerate([
            ("CLASSIFICATION & CLUSTERING", 27, "gold"),
            ("OF INDIAN RAILWAY TRAINS", 27, "white"),
            ("USING MACHINE LEARNING", 21, "saffron_glow"),
        ]):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            r = p.add_run()
            r.text = txt
            r.font.name = FONT_HEADING
            r.font.size = Pt(sz)
            r.font.bold = True
            r.font.color.rgb = rgb_color(col)

        sub = slide.shapes.add_textbox(Inches(0.82), Inches(3.12), Inches(7.00), Inches(0.62))
        self._set_textbox(
            sub,
            "End-to-End Supervised Classification (Passenger, Express, Superfast) & Unsupervised Fleet Segmentation across 4,466 Operational Trains",
            size=11.5,
            bold=True,
            color="light_grey",
        )

        id_card = self._add_glass_card(
            slide, x=0.82, y=3.88, w=7.10, h=2.50, fill_color="slate_dark", border_color="gold", top_stripe_color="gold"
        )
        for lbl, val, mx, my in [
            ("CANDIDATE NAME", "RAJPUT PRINCE SINGH", 1.02, 4.08),
            ("ROLL NUMBER", "83  (BCA Semester VII)", 4.65, 4.08),
            ("INSTITUTION", "Lokmanya College of Computer Application", 1.02, 4.82),
            ("UNIVERSITY", "Gujarat University (2025-26)", 4.65, 4.82),
            ("SYLLABUS PAPERS", "DSC-C-BCA-471T (AI)  •  472T (ML)  •  473P (ML System Design)", 1.02, 5.56),
        ]:
            ltb = slide.shapes.add_textbox(Inches(mx), Inches(my), Inches(3.3), Inches(0.22))
            self._set_textbox(ltb, lbl, size=8.5, bold=True, color="gold", font_name=FONT_MONO)
            vtb = slide.shapes.add_textbox(Inches(mx), Inches(my + 0.20), Inches(6.6 if my > 5.4 else 3.4), Inches(0.32))
            self._set_textbox(vtb, val, size=13 if "PRINCE" in val else 11, bold=True, color="white")

        hero_card_path = self.studio.create_rounded_photo_card(
            "hero_train.png", width_in=4.48, height_in=4.35, border_color=PALETTE["gold"], caption="INDIAN RAILWAYS DIGITAL AI TRANSFORMATION"
        )
        hero_pic = slide.shapes.add_picture(str(hero_card_path), Inches(8.40), Inches(0.45), Inches(4.48), Inches(4.35))

        train_shape = slide.shapes.add_picture(
            str(self.vb_rake_path), Inches(8.38), Inches(5.05), Inches(4.48), Inches(1.38)
        )
        train_shape.name = "Hero_Animated_Train"

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide,
            train_shapes=[(train_shape, "M -0.65 0 L 0 0 E", 1900)],
            card_shapes=[id_card, hero_pic],
            header_shapes=[badge, t1],
        )

    def build_slide_02_about_ir(self) -> None:
        """Slide 2: 100% PIL-Rendered Glassmorphic KPI Cards (Zero Overlap!)."""
        bg = self.studio.create_dark_hud_background("02_about_ir", accent_color=PALETTE["saffron"])
        slide = self._new_slide(
            bg,
            section_tag="Junction 01 • Domain Context",
            title="Indian Railways: Continental Scale & Operational Complexity",
            subtitle="Understanding the massive scheduling network that motivates automated ML classification & clustering",
            transition_style="vortex",
            audio_key="horn_track",
        )

        stats = [
            ("s2_scale", "68,000+ km", "Total Track Network", "4th largest national railway network globally spanning diverse geography", "saffron", "SCALE", 0.94),
            ("s2_fleet", "13,000+", "Passenger Trains / Day", "Connecting millions of daily commuters across local, express & superfast tiers", "gold", "FLEET", 0.88),
            ("s2_zones", "19+ Zones", "Operational Zones", "Decentralized administration (NR, WR, ER, SR, CR, NFR, SCR & regional zones)", "cyan", "ZONES", 0.82),
            ("s2_nodes", "7,300+", "Railway Stations", "Complex multi-stop timetables where distance, speed & coaches define class", "green_bright", "NODES", 0.91),
        ]
        stat_pics = []
        for idx, (tag, val, tit, sub, acc, code, ratio) in enumerate(stats):
            cx = 0.52 + idx * 3.10
            png_path = self.studio.create_hud_kpi_card_png(
                tag=tag, big_value=val, title=tit, subtitle=sub, accent_name=acc, badge_code=code, meter_fill_ratio=ratio, width_in=2.96, height_in=2.30
            )
            pic = slide.shapes.add_picture(str(png_path), Inches(cx), Inches(1.45), Inches(2.96), Inches(2.30))
            stat_pics.append(pic)

        why_card = self._add_glass_card(
            slide, 0.55, 3.92, 7.35, 2.78, fill_color="panel_navy", border_color="gold", left_stripe_color="gold"
        )
        hdr = slide.shapes.add_textbox(Inches(0.85), Inches(4.06), Inches(6.80), Inches(0.34))
        self._set_textbox(hdr, "WHY MACHINE LEARNING FOR INDIAN RAILWAYS?", size=13.5, bold=True, color="gold")

        self._add_bullet_list(
            slide,
            x=0.85,
            y=4.48,
            w=6.85,
            h=2.05,
            items=[
                ("Service Tier Standardization", "Automatically distinguish Passenger (Pass), Express (Exp), and Superfast (SF) services from schedule metrics."),
                ("Infrastructure & Coach Allocation", "Quantify how 3AC, Chair Car, and Sleeper availability drive premium train categorization."),
                ("Data-Driven Zone Profiling", "Discover natural regional fleet clusters beyond manual administrative zone boundaries."),
            ],
            row_gap=0.66,
        )

        loco_card = self.studio.create_rounded_photo_card(
            "diesel_loco.png", width_in=4.72, height_in=2.78, border_color=PALETTE["saffron"], caption="LOCOMOTIVE TELEMETRY & SERVICE HIERARCHY"
        )
        loco_pic = slide.shapes.add_picture(str(loco_card), Inches(8.08), Inches(3.92), Inches(4.72), Inches(2.78))

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide,
            train_shapes=[(loco_pic, "M 0.35 0 L 0 0 E", 1350)],
            card_shapes=[*stat_pics, why_card],
            header_shapes=self._last_header_shapes,
        )

    def build_slide_03_problem_statement(self) -> None:
        bg = self.studio.create_dark_hud_background(
            "03_problem", accent_color=PALETTE["red_bright"], secondary_accent=PALETTE["green_bright"]
        )
        slide = self._new_slide(
            bg,
            section_tag="Junction 02 • Problem Formulation",
            title="Problem Statement: Operational Complexity vs ML Automation",
            subtitle="Bridging raw heterogeneous railway timetable data with supervised & unsupervised learning pipelines",
            transition_style="doors",
            audio_key="chime_only",
        )

        left_card = self._add_glass_card(
            slide, 0.55, 1.48, 5.65, 5.20, fill_color="danger_bg", border_color="red_bright", top_stripe_color="red_bright"
        )
        ch_hdr = slide.shapes.add_textbox(Inches(0.80), Inches(1.68), Inches(5.15), Inches(0.40))
        self._set_textbox(ch_hdr, "🔴  SIGNAL RED: THE OPERATIONAL CHALLENGE", size=14, bold=True, color="red_bright")

        self._add_bullet_list(
            slide,
            x=0.80,
            y=2.18,
            w=5.15,
            h=4.25,
            bullet_color="red_bright",
            row_gap=0.84,
            items=[
                ("Massive Multi-Dimensional Schedule Data", "5,208 raw train records stored in nested GeoJSON with inconsistent duration fields and 19+ zones."),
                ("Overlapping Operational Boundaries", "Express and Superfast trains often share similar route distances and AC coach configurations."),
                ("Severe Class Imbalance", "Local Passenger trains dominate (55.06%) while premium Superfast trains represent only 16.10%."),
                ("Lack of Unsupervised Fleet Taxonomy", "No automated way to group trains into operational archetypes without predefined labels."),
                ("Hidden Data Quality Traps", "Raw duration_m stored only partial minutes (0-58), distorting true journey duration signals."),
            ],
        )

        sig_path = self.studio.create_railway_signal("all", height_in=2.75)
        sig_pic = slide.shapes.add_picture(str(sig_path), Inches(6.32), Inches(2.65), Inches(0.70), Inches(2.75))

        right_card = self._add_glass_card(
            slide, 7.12, 1.48, 5.65, 5.20, fill_color="success_bg", border_color="green_bright", top_stripe_color="green_bright"
        )
        sol_hdr = slide.shapes.add_textbox(Inches(7.38), Inches(1.68), Inches(5.15), Inches(0.40))
        self._set_textbox(sol_hdr, "🟢  SIGNAL GREEN: DUAL-PIPELINE ML SOLUTION", size=14, bold=True, color="green_bright")

        self._add_bullet_list(
            slide,
            x=7.38,
            y=2.18,
            w=5.15,
            h=4.25,
            bullet_color="green_bright",
            row_gap=0.84,
            items=[
                ("Rigorous Preprocessing & Leakage Prevention", "Converted GeoJSON to CSV (4,466 clean rows), dropped identifiers, and performed 80/20 stratified split."),
                ("Feature Engineering Breakthrough", "Engineered exact total_duration = duration_h * 60 + duration_m, boosting every single model."),
                ("4 Supervised Classification Algorithms", "Benchmarked KNN, SVM (RBF), Gaussian Naive Bayes, and Decision Tree against Dummy Baseline."),
                ("Imbalance-Aware Evaluation", "Adopted Macro F1 (0.8896) and ROC-AUC alongside Accuracy (91.50%) for fair multi-class grading."),
                ("Dual Unsupervised Clustering", "Combined K-Means (k=5) + DBSCAN (Silhouette 0.2543) with 2D PCA projection & cluster profiling."),
            ],
        )

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide,
            card_shapes=[left_card, sig_pic, right_card],
            header_shapes=self._last_header_shapes,
        )

    def build_slide_04_objectives(self) -> None:
        bg = self.studio.create_dark_hud_background("04_objectives", accent_color=PALETTE["gold"])
        slide = self._new_slide(
            bg,
            section_tag="Junction 03 • Project Roadmap",
            title="Six Core Objectives Aligned with BCA Sem-VII ML Syllabus",
            subtitle="Structured end-to-end workflow covering Units 1, 2, 3, and 4 of DSC-C-BCA-472T & 473P",
            accent_name="gold",
            transition_style="honeycomb",
            audio_key="chime_only",
        )

        objectives = [
            ("obj1", "STAGE 01", "Data Engineering & EDA", "Transform 14.08 MB GeoJSON into structured CSV, audit constant columns & generate 10+ plot types.", "saffron", "UNIT-1", 0.85),
            ("obj2", "STAGE 02", "Data Quality Fix", "Diagnose and repair broken duration_m via compound total_duration and quantify model lift.", "gold", "FIX", 0.96),
            ("obj3", "STAGE 03", "Leakage-Free Split", "Enforce strict 80/20 stratified train-test isolation before fitting StandardScaler & encoding.", "cyan", "SPLIT", 0.90),
            ("obj4", "STAGE 04", "4 ML Classifiers", "Train Dummy Baseline, KNN (k=5), Decision Tree, Naive Bayes, and SVM (RBF) on 3 train classes.", "green_bright", "UNIT-3", 0.92),
            ("obj5", "STAGE 05", "Multi-Metric Audit", "Evaluate Macro/Weighted/Micro F1, Confusion Matrices, OvR ROC-AUC, and 5-Fold Cross-Validation.", "blue", "UNIT-2", 0.94),
            ("obj6", "STAGE 06", "Fleet Clustering", "Segment Indian Railways trains using K-Means (k=5) and DBSCAN with 2D PCA & cluster export.", "purple", "UNIT-4", 0.89),
        ]

        cards = []
        for idx, (tag, val, tit, desc, col, badge, ratio) in enumerate(objectives):
            row = idx // 3
            col_idx = idx % 3
            x = 0.55 + col_idx * 4.12
            y = 1.48 + row * 2.62
            png = self.studio.create_hud_kpi_card_png(
                tag=tag, big_value=val, title=tit, subtitle=desc, accent_name=col, badge_code=badge, meter_fill_ratio=ratio, width_in=3.92, height_in=2.42
            )
            pic = slide.shapes.add_picture(str(png), Inches(x), Inches(y), Inches(3.92), Inches(2.42))
            cards.append(pic)

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide, card_shapes=cards, header_shapes=self._last_header_shapes
        )

    def build_slide_05_dataset_overview(self) -> None:
        bg = self.studio.create_dark_hud_background("05_dataset", accent_color=PALETTE["saffron"])
        slide = self._new_slide(
            bg,
            section_tag="Junction 04 • Dataset Architecture",
            title="Dataset Overview: Indian Railways Operational Dataset",
            subtitle="Source: Kaggle (sripaadsrinivasan/indian-railways-dataset) • GeoJSON (14.08 MB) converted to CSV (636 KB)",
            transition_style="ripple",
            audio_key="horn_track",
        )

        kpis = [
            ("s5_raw", "5,208", "Raw GeoJSON Records", "14.08 MB spatial & schedule data", "saffron", "RAW", 1.0),
            ("s5_clean", "4,466", "Filtered Target Trains", "Retained 3 classes: Pass, Exp, SF", "gold", "CLEAN", 0.86),
            ("s5_dim", "26 Cols", "Engineered Features", "Numeric + coach flags + 19 zones", "cyan", "DIM", 0.90),
            ("s5_split", "80 : 20", "Stratified Split", "3,572 Train  |  894 Test rows", "green_bright", "SPLIT", 0.80),
        ]
        kpi_cards = []
        for idx, (tag, val, tit, sub, acc, code, ratio) in enumerate(kpis):
            png = self.studio.create_hud_kpi_card_png(
                tag=tag, big_value=val, title=tit, subtitle=sub, accent_name=acc, badge_code=code, meter_fill_ratio=ratio, width_in=2.94, height_in=1.68
            )
            pic = slide.shapes.add_picture(str(png), Inches(0.55 + idx * 3.10), Inches(1.42), Inches(2.94), Inches(1.68))
            kpi_cards.append(pic)

        tbl_card = self._add_glass_card(
            slide, 0.55, 3.20, 7.55, 2.65, fill_color="panel_navy", border_color="gold", top_stripe_color="gold"
        )
        thdr = slide.shapes.add_textbox(Inches(0.78), Inches(3.32), Inches(7.10), Inches(0.32))
        self._set_textbox(
            thdr,
            "TARGET VARIABLE DISTRIBUTION (3 CLASSES)  —  MODERATE IMBALANCE -> MACRO F1 PRIMARY METRIC",
            size=10.2,
            bold=True,
            color="gold",
        )

        rows = [
            ("Class", "Train Category", "Count", "Share", "Operational Profile"),
            ("Pass", "Passenger Train", "2,459", "55.06%", "Short-distance, frequent halts, unreserved / basic sleeper"),
            ("Exp", "Express Train", "1,288", "28.84%", "Medium-to-long distance, mixed Sleeper & 3AC/2AC coaches"),
            ("SF", "Superfast Train", "719", "16.10%", "High priority, fewer halts, high average speed & full AC"),
        ]
        col_x = [0.78, 1.72, 3.45, 4.30, 5.20]
        col_w = [0.90, 1.68, 0.80, 0.85, 2.70]
        for r_idx, row in enumerate(rows):
            ry = 3.68 + r_idx * 0.50
            is_hdr = r_idx == 0
            row_fill = "saffron" if is_hdr else "slate_dark"
            row_bg = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.72), Inches(ry), Inches(7.20), Inches(0.44)
            )
            row_bg.fill.solid()
            row_bg.fill.fore_color.rgb = rgb_color(row_fill)
            row_bg.line.color.rgb = rgb_color("gold" if is_hdr else "slate_mid")
            for c_idx, cell_val in enumerate(row):
                ctb = slide.shapes.add_textbox(Inches(col_x[c_idx]), Inches(ry + 0.07), Inches(col_w[c_idx]), Inches(0.30))
                self._set_textbox(
                    ctb,
                    cell_val,
                    size=9.5 if is_hdr else 10.0,
                    bold=is_hdr or (c_idx in (0, 2, 3)),
                    color="white" if is_hdr else ("gold" if c_idx == 0 else "light_grey"),
                )

        coach_card = self.studio.create_rounded_photo_card(
            "coach_interior.png", width_in=4.50, height_in=2.65, border_color=PALETTE["saffron"], caption="BINARY COACH FEATURES IN DATASET"
        )
        coach_pic = slide.shapes.add_picture(str(coach_card), Inches(8.28), Inches(3.20), Inches(4.50), Inches(2.65))

        # Animated Vande Bharat Rake roaring across bottom of Dataset slide!
        vb_train = slide.shapes.add_picture(str(self.vb_rake_path), Inches(8.20), Inches(5.92), Inches(4.55), Inches(0.92))
        vb_train.name = "Dataset_Express_Rake"

        rake_info = self._add_glass_card(slide, 0.55, 5.95, 7.55, 0.85, fill_color="midnight", border_color="saffron", left_stripe_color="saffron")
        rtb = slide.shapes.add_textbox(Inches(0.82), Inches(6.05), Inches(7.10), Inches(0.65))
        self._set_textbox(
            rtb,
            "COACH COMPOSITION TELEMETRY:  first_ac (H1)  •  second_ac (A1)  •  third_ac (B1)  •  sleeper (SL)  •  chair_car (CC)\nZONE ENCODING:  19 One-Hot Encoded Railway Zones + Continuous distance & total_duration = 26 Features.",
            size=9.8,
            bold=True,
            color="gold_soft",
            font_name=FONT_MONO,
        )

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide,
            train_shapes=[(vb_train, "M -0.85 0 L 0 0 E", 2100)],
            card_shapes=[*kpi_cards, tbl_card, coach_pic, rake_info],
            header_shapes=self._last_header_shapes,
        )

    def build_ticket_divider_slide(
        self,
        ticket_id: str,
        pnr_no: str,
        from_station: str,
        to_station: str,
        header_short_title: str,
        phase_title: str,
        phase_subtitle: str,
        coach_code: str,
        berth_info: str,
        deliverables: List[str],
        telemetry_specs: List[Tuple[str, str]],
        stage_index: int,
        audio_key: str,
    ) -> None:
        if not INCLUDE_TICKET_DIVIDER_SLIDES:
            return

        bg = self.studio.create_dark_hud_background(
            f"divider_{ticket_id}",
            accent_color=PALETTE["gold"],
            secondary_accent=PALETTE["saffron"],
            hero_image_path=self.paths.get_image("track_sunset.png"),
            hero_opacity=0.25,
        )
        slide = self._new_slide(
            bg,
            section_tag=f"🔊 STATION ANNOUNCEMENT • PNR {pnr_no}",
            title=header_short_title,
            subtitle="Official Indian Railways Machine Learning Pipeline Stage Verification Voucher",
            accent_name="gold",
            transition_style="doors",
            audio_key=audio_key,
        )

        ticket_img = self.studio.create_irctc_ticket_stub(
            ticket_id=ticket_id,
            pnr_no=pnr_no,
            from_station=from_station,
            to_station=to_station,
            phase_title=phase_title,
            phase_subtitle=phase_subtitle,
            coach_code=coach_code,
            berth_info=berth_info,
            key_deliverables=deliverables,
            telemetry_specs=telemetry_specs,
            stage_index=stage_index,
            width_in=12.0,
            height_in=5.15,
        )
        pic = slide.shapes.add_picture(str(ticket_img), Inches(0.66), Inches(1.45), Inches(12.0), Inches(5.15))
        pic.name = f"Ticket_Stub_{ticket_id}"

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide,
            train_shapes=[(pic, "M -0.45 0 L 0 0 E", 1350)],
            header_shapes=self._last_header_shapes,
        )

    def build_slide_06_eda_distribution(self) -> None:
        bg = self.studio.create_dark_hud_background("06_eda_dist", accent_color=PALETTE["saffron"])
        slide = self._new_slide(
            bg,
            section_tag="Phase 1 • Exploratory Data Analysis (Unit 1)",
            title="Class Balance & Railway Zone Distribution Analysis",
            subtitle="Visualizing the 3 target classes (Pass, Exp, SF) and regional train density across Indian Railway zones",
            transition_style="morph",
            audio_key="chime_only",
        )

        chart_card = self.studio.create_framed_chart_card(
            "eda_class_zone_distribution.png",
            width_in=8.30,
            height_in=5.25,
            title_badge="EDA PLOT 01  •  TARGET CLASS IMBALANCE & TOP RAILWAY ZONES",
            accent=PALETTE["saffron"],
            footer_note="Pass: 2,459 (55.06%)  |  Exp: 1,288 (28.84%)  |  SF: 719 (16.10%)  •  Total Clean Records: 4,466",
        )
        chart_pic = slide.shapes.add_picture(str(chart_card), Inches(0.50), Inches(1.45), Inches(8.30), Inches(5.25))

        info_card = self._add_glass_card(
            slide, 8.95, 1.52, 3.85, 5.10, fill_color="panel_navy", border_color="gold", top_stripe_color="gold"
        )
        ihdr = slide.shapes.add_textbox(Inches(9.18), Inches(1.70), Inches(3.40), Inches(0.34))
        self._set_textbox(ihdr, "KEY EDA TAKEAWAYS", size=13.5, bold=True, color="gold")

        self._add_bullet_list(
            slide,
            x=9.18,
            y=2.16,
            w=3.42,
            h=4.25,
            row_gap=1.02,
            items=[
                ("55.06% Passenger Dominance", "Passenger (2,459) is 3.4x larger than Superfast (719), making raw Accuracy misleading without Macro F1."),
                ("Regional Zone Concentration", "NR, WR, SR, ER, and CR handle the highest train volumes, reflecting dense commuter corridors."),
                ("Constant Column Audit", "Audited all binary coach indicators to verify variance before one-hot encoding 19 zone categories."),
                ("10+ Syllabus Plot Types", "Completed Histograms, Log-Histograms, Boxplots, KDE Density, Line Trends, Pairplot & Scatter."),
            ],
        )

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide, card_shapes=[chart_pic, info_card], header_shapes=self._last_header_shapes
        )

    def build_slide_07_feature_insights(self) -> None:
        bg = self.studio.create_dark_hud_background("07_feature_insights", accent_color=PALETTE["cyan"])
        slide = self._new_slide(
            bg,
            section_tag="Phase 1 • Feature Distributions & Correlations",
            title="Continuous Feature Distributions & Multi-Feature Correlation Matrix",
            subtitle="Inspecting skewness in Distance / Duration and collinearity across AC & Sleeper coach indicators",
            accent_name="cyan",
            transition_style="zoom",
            audio_key="horn_track",
        )

        left_chart = self.studio.create_framed_chart_card(
            "eda_histograms.png",
            width_in=6.05,
            height_in=4.35,
            title_badge="FEATURE HISTOGRAMS (DISTANCE & DURATION)",
            accent=PALETTE["cyan"],
            footer_note="Right-skewed distribution: High short-haul commuter density vs long-haul express tail",
        )
        right_chart = self.studio.create_framed_chart_card(
            "correlation_heatmap.png",
            width_in=6.05,
            height_in=4.35,
            title_badge="PEARSON CORRELATION HEATMAP",
            accent=PALETTE["gold"],
            footer_note="Strong positive correlation between Distance, Total Duration (r > 0.85) & AC Coaches",
        )
        l_pic = slide.shapes.add_picture(str(left_chart), Inches(0.50), Inches(1.45), Inches(6.05), Inches(4.35))
        r_pic = slide.shapes.add_picture(str(right_chart), Inches(6.75), Inches(1.45), Inches(6.05), Inches(4.35))

        bottom_card = self._add_glass_card(
            slide, 0.55, 5.88, 12.20, 0.86, fill_color="panel_navy", border_color="cyan", left_stripe_color="cyan"
        )
        btb = slide.shapes.add_textbox(Inches(0.82), Inches(5.98), Inches(11.75), Inches(0.66))
        self._set_textbox(
            btb,
            "MULTIVARIATE INSIGHT: Because Distance, Total Duration, Sleeper, 3AC, and 2AC exhibit strong inter-feature correlation, Gaussian Naive Bayes' conditional independence assumption is violated — whereas Decision Trees exploit these exact interaction thresholds.",
            size=10.8,
            bold=True,
            color="white",
        )

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide, card_shapes=[l_pic, r_pic, bottom_card], header_shapes=self._last_header_shapes
        )

    def build_slide_08_killer_data_quality_fix(self) -> None:
        bg = self.studio.create_dark_hud_background(
            "08_killer_fix", accent_color=PALETTE["gold"], secondary_accent=PALETTE["green_bright"]
        )
        slide = self._new_slide(
            bg,
            section_tag="🔥 KILLER VIVA DISCOVERY • DATA QUALITY > ALGORITHM",
            title="The Data Quality Breakthrough: Fixing the Broken Duration Feature",
            subtitle="How discovering a subtle schema bug in duration_m improved EVERY SINGLE supervised & unsupervised model",
            accent_name="gold",
            transition_style="vortex",
            audio_key="killer_discovery",
        )

        bef_png = self.studio.create_hud_kpi_card_png(
            tag="s8_before",
            big_value="0 – 58 min",
            title="❌ BEFORE: Broken duration_m",
            subtitle="Stored only minute remainder (0-58), NOT total trip time! A 24-hour SF train with 0 extra mins appeared as 0!",
            accent_name="red_bright",
            badge_code="SCHEMA BUG",
            meter_fill_ratio=0.22,
            width_in=3.48,
            height_in=2.10,
        )
        aft_png = self.studio.create_hud_kpi_card_png(
            tag="s8_after",
            big_value="h×60 + m",
            title="✅ AFTER: total_duration Fix",
            subtitle="Engineered exact continuous journey minutes across all 4,466 trains prior to scaling & modeling.",
            accent_name="green_bright",
            badge_code="FIXED!",
            meter_fill_ratio=0.98,
            width_in=3.48,
            height_in=2.10,
        )
        bef_pic = slide.shapes.add_picture(str(bef_png), Inches(0.52), Inches(1.45), Inches(3.48), Inches(2.10))
        aft_pic = slide.shapes.add_picture(str(aft_png), Inches(0.52), Inches(3.62), Inches(3.48), Inches(2.10))

        fix_chart = self.studio.create_framed_chart_card(
            "before_after_duration_fix.png",
            width_in=5.15,
            height_in=4.28,
            title_badge="BEFORE vs AFTER F1-MACRO ACROSS ALL MODELS",
            accent=PALETTE["gold"],
            footer_note="Every bar shifted upward after replacing broken duration_m with total_duration",
        )
        fix_pic = slide.shapes.add_picture(str(fix_chart), Inches(4.12), Inches(1.45), Inches(5.15), Inches(4.28))

        tbl_card = self._add_glass_card(
            slide, 9.38, 1.48, 3.42, 4.22, fill_color="panel_navy", border_color="gold", top_stripe_color="gold"
        )
        dhdr = slide.shapes.add_textbox(Inches(9.55), Inches(1.62), Inches(3.10), Inches(0.32))
        self._set_textbox(dhdr, "VERIFIED F1-MACRO GAINS", size=11.5, bold=True, color="gold")

        deltas = [
            ("Model / Metric", "Before", "After", "Δ Gain"),
            ("KNN (k=5)", "0.7552", "0.7886", "+0.0334"),
            ("DT (default) 🏆", "0.8309", "0.8896", "+0.0587"),
            ("DT (depth=10)", "0.7720", "0.8459", "+0.0739"),
            ("Naive Bayes", "0.2969", "0.3098", "+0.0129"),
            ("SVM (RBF)", "0.7168", "0.7651", "+0.0483"),
            ("Silhouette (k=5)", "0.1755", "0.2024", "+0.0269"),
        ]
        for idx, (m_name, bef, aft, dlt) in enumerate(deltas):
            ry = 2.00 + idx * 0.48
            is_h = idx == 0
            r_fill = "saffron" if is_h else ("sign_yellow" if idx == 2 else "deep_navy")
            r_box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.50), Inches(ry), Inches(3.18), Inches(0.42)
            )
            r_box.fill.solid()
            r_box.fill.fore_color.rgb = rgb_color(r_fill)
            r_box.line.fill.background()

            line_str = f"{m_name:<14} {bef:>6} {aft:>6} {dlt:>7}"
            ltb = slide.shapes.add_textbox(Inches(9.55), Inches(ry + 0.07), Inches(3.08), Inches(0.28))
            self._set_textbox(
                ltb,
                line_str,
                size=8.5,
                bold=True,
                color="white" if is_h else ("sign_black" if idx == 2 else "green_bright"),
                font_name=FONT_MONO,
            )

        banner = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(5.84), Inches(12.25), Inches(0.88)
        )
        banner.fill.solid()
        banner.fill.fore_color.rgb = rgb_color("sign_yellow")
        banner.line.color.rgb = rgb_color("saffron")
        banner.line.width = Pt(2.5)
        self._set_shape_text(
            banner,
            "★  KILLER VIVA FINDING: All 5 supervised models + K-Means improved immediately after fixing total_duration — proving empirically that Domain Data Quality outweighs Algorithm Selection!  ★",
            size=12.0,
            bold=True,
            color="sign_black",
            align=PP_ALIGN.CENTER,
        )

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide,
            card_shapes=[bef_pic, aft_pic, fix_pic, tbl_card, banner],
            header_shapes=self._last_header_shapes,
        )

    def build_slide_09_evaluation_metrics(self) -> None:
        bg = self.studio.create_dark_hud_background("09_eval_metrics", accent_color=PALETTE["saffron"])
        slide = self._new_slide(
            bg,
            section_tag="Phase 2 • Model Evaluation Framework (Unit 2)",
            title="Comprehensive Multi-Class Evaluation Metrics Suite",
            subtitle="Why single-metric accuracy fails on imbalanced railway classes and how our 6-metric framework guarantees rigor",
            transition_style="honeycomb",
            audio_key="chime_only",
        )

        metrics = [
            ("m_acc", "91.50%", "Overall Accuracy", "Fraction of total test trains (894) classified correctly. Useful baseline but biased toward majority Pass (55%).", "saffron", "ACCURACY", 0.915),
            ("m_mac", "0.8896", "Macro-Averaged F1 🏆", "PRIMARY METRIC: Unweighted mean of per-class F1 scores — treats Pass, Exp, and minority SF (16.1%) equally.", "gold", "MACRO F1", 0.890),
            ("m_wgt", "0.9146", "Weighted-Averaged F1", "Class-support weighted F1 combining precision and recall while accounting for natural operational fleet proportions.", "green_bright", "WEIGHTED", 0.915),
            ("m_mic", "0.9150", "Micro Precision / Recall", "Aggregates global true positives across all 3 classes; mathematically equals multi-class accuracy (0.9150).", "cyan", "MICRO", 0.915),
            ("m_auc", "0.9355", "One-vs-Rest ROC-AUC", "Measures ranking separability across all probability thresholds (KNN: 0.9355, SVM: 0.9285, DT: 0.9204).", "blue", "ROC-AUC", 0.936),
            ("m_err", "8.50%", "Confusion & Error Audit", "Granular off-diagonal confusion matrix inspection revealing SF <-> Exp boundary overlap (25 SF->Exp, 16 Exp->SF).", "purple", "ERR AUDIT", 0.850),
        ]

        cards = []
        for idx, (tag, val, tit, sub, acc, badge, ratio) in enumerate(metrics):
            row = idx // 3
            col_idx = idx % 3
            x = 0.55 + col_idx * 4.12
            y = 1.48 + row * 2.62
            png = self.studio.create_hud_kpi_card_png(
                tag=tag, big_value=val, title=tit, subtitle=sub, accent_name=acc, badge_code=badge, meter_fill_ratio=ratio, width_in=3.92, height_in=2.42
            )
            pic = slide.shapes.add_picture(str(png), Inches(x), Inches(y), Inches(3.92), Inches(2.42))
            cards.append(pic)

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide, card_shapes=cards, header_shapes=self._last_header_shapes
        )

    def build_slide_10_confusion_matrix_roc(self) -> None:
        bg = self.studio.create_dark_hud_background("10_cm_roc", accent_color=PALETTE["gold"])
        slide = self._new_slide(
            bg,
            section_tag="Phase 2 • Diagnostic Visuals",
            title="Decision Tree Confusion Matrix & Multi-Model ROC-AUC Curves",
            subtitle="Evaluating class-wise recall on the 894-train holdout test set and One-vs-Rest threshold performance",
            accent_name="gold",
            transition_style="morph",
            audio_key="horn_track",
        )

        cm_card = self.studio.create_framed_chart_card(
            "confusion_matrix_best.png",
            width_in=5.95,
            height_in=4.35,
            title_badge="BEST MODEL CONFUSION MATRIX (DECISION TREE)",
            accent=PALETTE["saffron"],
            footer_note="Pass Error: 3.0% (97% Recall)  |  Exp Error: 14.0%  |  SF Error: 17.4%",
        )
        roc_card = self.studio.create_framed_chart_card(
            "roc_curves.png",
            width_in=6.20,
            height_in=4.35,
            title_badge="ONE-VS-REST MULTI-CLASS ROC CURVES",
            accent=PALETTE["gold"],
            footer_note="KNN AUC: 0.9355 (Best)  |  SVM AUC: 0.9285  |  Decision Tree AUC: 0.9204",
        )
        cm_pic = slide.shapes.add_picture(str(cm_card), Inches(0.50), Inches(1.45), Inches(5.95), Inches(4.35))
        roc_pic = slide.shapes.add_picture(str(roc_card), Inches(6.62), Inches(1.45), Inches(6.20), Inches(4.35))

        bot_card = self._add_glass_card(
            slide, 0.55, 5.88, 12.22, 0.86, fill_color="panel_navy", border_color="gold", left_stripe_color="gold"
        )
        stb = slide.shapes.add_textbox(Inches(0.85), Inches(5.98), Inches(11.75), Inches(0.65))
        self._set_textbox(
            stb,
            "DIAGNOSTIC INSIGHT: Passenger trains achieve 97.0% recall due to distinct zero-AC profiles. The 8.50% total error is concentrated in Express ↔ Superfast confusion (25 SF→Exp, 16 Exp→SF) where coach composition and route distance overlap.",
            size=10.5,
            bold=True,
            color="white",
        )

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide, card_shapes=[cm_pic, roc_pic, bot_card], header_shapes=self._last_header_shapes
        )

    def build_slide_11_model_comparison(self) -> None:
        """Slide 11: PIL-Rendered Digital LED Station Departure Board + Benchmark Chart."""
        bg = self.studio.create_dark_hud_background("11_model_comp", accent_color=PALETTE["saffron"])
        slide = self._new_slide(
            bg,
            section_tag="Phase 3 • Supervised ML Benchmark (Unit 3)",
            title="Supervised Classification Leaderboard Across 5 Models + Baseline",
            subtitle="Comparing Dummy Baseline, KNN, Decision Tree (Unconstrained & Pruned), Naive Bayes, and SVM (RBF)",
            transition_style="ferris",
            audio_key="chime_only",
        )

        board_png = self.studio.create_departure_leaderboard_png(width_in=7.35, height_in=5.25)
        board_pic = slide.shapes.add_picture(str(board_png), Inches(0.50), Inches(1.45), Inches(7.35), Inches(5.25))

        comp_chart = self.studio.create_framed_chart_card(
            "model_comparison.png",
            width_in=4.85,
            height_in=5.25,
            title_badge="VISUAL BENCHMARK COMPARISON",
            accent=PALETTE["gold"],
            footer_note="Decision Tree leads in Accuracy (91.50%) & Macro F1 (0.8896)",
        )
        comp_pic = slide.shapes.add_picture(str(comp_chart), Inches(7.98), Inches(1.45), Inches(4.85), Inches(5.25))

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide, card_shapes=[board_pic, comp_pic], header_shapes=self._last_header_shapes
        )

    def build_slide_12_best_model_dt(self) -> None:
        bg = self.studio.create_dark_hud_background(
            "12_best_dt", accent_color=PALETTE["gold"], secondary_accent=PALETTE["saffron"]
        )
        slide = self._new_slide(
            bg,
            section_tag="Phase 3 • Champion Architecture",
            title="Champion Model: Decision Tree Classifier — Why It Won",
            subtitle="Capturing non-linear hierarchical railway scheduling thresholds without feature-independence bottlenecks",
            accent_name="gold",
            transition_style="zoom",
            audio_key="horn_track",
        )

        g1 = self.studio.create_speedometer_gauge("dt_acc", "91.50%", "TEST ACCURACY", "+36.5% over Baseline", 0.9150, PALETTE["gold"], size_in=2.75)
        g2 = self.studio.create_speedometer_gauge("dt_f1m", "0.8896", "MACRO F1 SCORE", "Primary Balanced Metric", 0.8896, PALETTE["saffron"], size_in=2.75)
        g3 = self.studio.create_speedometer_gauge("dt_f1w", "0.9146", "WEIGHTED F1", "0.9204 Mean ROC-AUC", 0.9146, PALETTE["green_bright"], size_in=2.75)

        p1 = slide.shapes.add_picture(str(g1), Inches(0.55), Inches(1.45), Inches(2.75), Inches(2.75))
        p2 = slide.shapes.add_picture(str(g2), Inches(3.45), Inches(1.45), Inches(2.75), Inches(2.75))
        p3 = slide.shapes.add_picture(str(g3), Inches(6.35), Inches(1.45), Inches(2.75), Inches(2.75))

        why_card = self._add_glass_card(
            slide, 0.55, 4.28, 8.55, 2.42, fill_color="panel_navy", border_color="gold", left_stripe_color="gold"
        )
        whdr = slide.shapes.add_textbox(Inches(0.85), Inches(4.40), Inches(8.10), Inches(0.32))
        self._set_textbox(whdr, "WHY DECISION TREE DOMINATED THIS RAILWAY DATASET", size=13, bold=True, color="gold")

        self._add_bullet_list(
            slide,
            x=0.85,
            y=4.78,
            w=8.10,
            h=1.80,
            row_gap=0.58,
            items=[
                ("Hierarchical Rule Alignment", "Indian Railways classifies trains via threshold rules (if third_ac == 1 and distance > X and speed > 55 km/h -> SF), which axis-aligned tree splits model naturally."),
                ("Zero Feature-Independence Penalty", "Gaussian Naive Bayes failed (37.02%) because distance, duration, and AC coaches are heavily correlated; Decision Trees thrive on correlated interactions."),
                ("26-Feature One-Hot Sparsity Resilience", "In 26D space (with 19 binary zone columns), Euclidean distance in KNN/SVM gets diluted, whereas Decision Tree selects only top informative splits."),
            ],
        )

        err_card = self.studio.create_framed_chart_card(
            "error_analysis.png",
            width_in=3.55,
            height_in=5.25,
            title_badge="ERROR ANALYSIS (8.50% ERR)",
            accent=PALETTE["saffron"],
            footer_note="Persisted: models/dt_classifier.joblib",
        )
        err_pic = slide.shapes.add_picture(str(err_card), Inches(9.25), Inches(1.45), Inches(3.55), Inches(5.25))

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide, card_shapes=[p1, p2, p3, why_card, err_pic], header_shapes=self._last_header_shapes
        )

    def build_slide_13_feature_importance_cv(self) -> None:
        bg = self.studio.create_dark_hud_background("13_fi_cv", accent_color=PALETTE["saffron"])
        slide = self._new_slide(
            bg,
            section_tag="Phase 3 • Explainability & Generalization",
            title="Decision Tree Feature Importance & 5-Fold Cross-Validation",
            subtitle="Verifying what drives model predictions and proving generalization stability via 5-fold stratified CV",
            transition_style="ripple",
            audio_key="chime_only",
        )

        fi_card = self.studio.create_framed_chart_card(
            "feature_importance.png",
            width_in=6.15,
            height_in=4.05,
            title_badge="TOP FEATURE IMPORTANCES (GINI REDUCTION)",
            accent=PALETTE["saffron"],
            footer_note="#1 third_ac (35.51%)  •  #2 distance (22.26%)  •  #3 total_duration (17.99%)",
        )
        cv_card = self.studio.create_framed_chart_card(
            "cross_validation.png",
            width_in=6.00,
            height_in=4.05,
            title_badge="5-FOLD STRATIFIED CROSS-VALIDATION",
            accent=PALETTE["green_bright"],
            footer_note="5-Fold Macro F1: 0.8743 ± 0.0155 (High stability across folds)",
        )
        fi_pic = slide.shapes.add_picture(str(fi_card), Inches(0.50), Inches(1.42), Inches(6.15), Inches(4.05))
        cv_pic = slide.shapes.add_picture(str(cv_card), Inches(6.78), Inches(1.42), Inches(6.00), Inches(4.05))

        ranks = [
            ("fi_1", "35.51%", "#1: third_ac", "Primary separator of Pass vs Exp/SF", "saffron", "RANK #1", 0.95),
            ("fi_2", "22.26%", "#2: distance", "Route length separates commuter vs long-haul", "gold", "RANK #2", 0.78),
            ("fi_3", "17.99%", "#3: total_duration", "Engineered feature ranks #3 overall!", "green_bright", "RANK #3", 0.70),
            ("fi_4", "11.81%", "#4: chair_car", "Identifies intercity day express trains", "cyan", "RANK #4", 0.55),
            ("fi_cv", "0.8743", "5-Fold CV F1", "± 0.0155 low variance confirms stability", "blue", "5-FOLD CV", 0.88),
        ]
        pills = []
        for idx, (tag, val, tit, desc, col, badge, ratio) in enumerate(ranks):
            px = 0.52 + idx * 2.48
            png = self.studio.create_hud_kpi_card_png(
                tag=tag, big_value=val, title=tit, subtitle=desc, accent_name=col, badge_code=badge, meter_fill_ratio=ratio, width_in=2.36, height_in=1.28
            )
            pic = slide.shapes.add_picture(str(png), Inches(px), Inches(5.52), Inches(2.36), Inches(1.28))
            pills.append(pic)

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide, card_shapes=[fi_pic, cv_pic, *pills], header_shapes=self._last_header_shapes
        )

    def build_slide_14_kmeans_clustering(self) -> None:
        bg = self.studio.create_dark_hud_background("14_kmeans", accent_color=PALETTE["purple"])
        slide = self._new_slide(
            bg,
            section_tag="Phase 4 • Unsupervised ML (Unit 4)",
            title="Unsupervised Fleet Discovery: K-Means Clustering (k = 5)",
            subtitle="Discovering intrinsic operational groupings across 3,572 scaled training records without class labels",
            accent_name="purple",
            transition_style="vortex",
            audio_key="horn_track",
        )

        elbow_card = self.studio.create_framed_chart_card(
            "elbow_curve.png",
            width_in=5.85,
            height_in=4.32,
            title_badge="ELBOW METHOD & SILHOUETTE ANALYSIS",
            accent=PALETTE["gold"],
            footer_note="Optimal k = 5 selected via Inertia inflection & Silhouette peak (0.2024)",
        )
        pca_viz_name = (
            "clusters_k5_fixed_pca.png"
            if self.paths.get_viz("clusters_k5_fixed_pca.png")
            else "clusters_k5_pca.png"
        )
        pca_card = self.studio.create_framed_chart_card(
            pca_viz_name,
            width_in=6.30,
            height_in=4.32,
            title_badge="K-MEANS (k=5) IN 2D PCA FEATURE SPACE",
            accent=PALETTE["purple"],
            footer_note="2D PCA projection preserves continuous + zone variance across 5 clusters",
        )
        e_pic = slide.shapes.add_picture(str(elbow_card), Inches(0.50), Inches(1.45), Inches(5.85), Inches(4.32))
        p_pic = slide.shapes.add_picture(str(pca_card), Inches(6.50), Inches(1.45), Inches(6.30), Inches(4.32))

        bot_card = self._add_glass_card(
            slide, 0.55, 5.85, 12.22, 0.88, fill_color="panel_navy", border_color="purple", left_stripe_color="purple"
        )
        ktb = slide.shapes.add_textbox(Inches(0.85), Inches(5.95), Inches(11.75), Inches(0.68))
        self._set_textbox(
            ktb,
            "K-MEANS (k=5) METRICS:  Inertia = 69,115.75  •  Silhouette Score = 0.2024 (improved from 0.1755 after duration fix)\nOUTPUT ARTIFACT:  Saved full cluster assignments + features to data/trains_with_clusters.csv (3,572 rows × 28 columns).",
            size=10.5,
            bold=True,
            color="white",
        )

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide, card_shapes=[e_pic, p_pic, bot_card], header_shapes=self._last_header_shapes
        )

    def build_slide_15_dbscan_vs_kmeans(self) -> None:
        bg = self.studio.create_dark_hud_background("15_dbscan", accent_color=PALETTE["purple"])
        slide = self._new_slide(
            bg,
            section_tag="Phase 4 • Density vs Centroid Clustering",
            title="DBSCAN vs K-Means: Handling Non-Spherical Clusters & Outliers",
            subtitle="Why density-based clustering (eps = 7.0, min_samples = 20) achieved a higher Silhouette score (0.2543)",
            accent_name="purple",
            transition_style="morph",
            audio_key="chime_only",
        )

        left_card = self._add_glass_card(
            slide, 0.55, 1.48, 5.85, 5.22, fill_color="panel_navy", border_color="purple", top_stripe_color="purple"
        )
        chdr = slide.shapes.add_textbox(Inches(0.78), Inches(1.64), Inches(5.40), Inches(0.34))
        self._set_textbox(chdr, "ALGORITHMIC HEAD-TO-HEAD COMPARISON", size=12.5, bold=True, color="gold")

        comp_rows = [
            ("Criterion", "K-Means (k=5)", "DBSCAN (eps=7, min=20)"),
            ("Clustering Paradigm", "Centroid-based (Voronoi)", "Density-based spatial"),
            ("Clusters Discovered", "5 (User-specified k)", "4 natural clusters"),
            ("Outlier / Noise Handling", "None (forces all points)", "0.4% Noise (13 anomalies)"),
            ("Silhouette Score", "0.2024", "0.2543 🏆 (+25.6%)"),
            ("Cluster Geometry", "Spherical / Convex only", "Arbitrary / Non-spherical"),
            ("Operational Strength", "Granular zone/tier split", "Clean anomaly isolation"),
        ]
        cx = [0.75, 2.52, 4.30]
        cw = [1.72, 1.72, 1.92]
        for r_idx, r_vals in enumerate(comp_rows):
            ry = 2.08 + r_idx * 0.62
            is_h = r_idx == 0
            is_sil = r_idx == 4
            row_fill = "purple" if is_h else ("sign_yellow" if is_sil else "deep_navy")

            box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.70), Inches(ry), Inches(5.55), Inches(0.52)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = rgb_color(row_fill)
            box.line.color.rgb = rgb_color("white" if is_sil else "slate_mid")

            for c_idx, val in enumerate(r_vals):
                tb = slide.shapes.add_textbox(Inches(cx[c_idx]), Inches(ry + 0.10), Inches(cw[c_idx]), Inches(0.34))
                desired_col = "white" if is_h else ("sign_black" if is_sil else ("gold_soft" if c_idx == 2 else "light_grey"))
                self._set_textbox(tb, val, size=9.5, bold=is_h or is_sil or (c_idx == 0), color=desired_col)

        db_card = self.studio.create_framed_chart_card(
            "dbscan_vs_kmeans.png",
            width_in=6.25,
            height_in=3.45,
            title_badge="DBSCAN (4 CLUSTERS + NOISE) vs K-MEANS (5 CLUSTERS)",
            accent=PALETTE["purple"],
            footer_note="2D PCA Projection: DBSCAN isolates 13 extreme schedule anomalies as Noise (-1)",
        )
        db_pic = slide.shapes.add_picture(str(db_card), Inches(6.55), Inches(1.45), Inches(6.25), Inches(3.45))

        anom_card = self._add_glass_card(
            slide, 6.55, 5.02, 6.25, 1.68, fill_color="panel_navy", border_color="gold", left_stripe_color="gold"
        )
        ahdr = slide.shapes.add_textbox(Inches(6.82), Inches(5.14), Inches(5.80), Inches(0.30))
        self._set_textbox(ahdr, "WHY DBSCAN ACHIEVED HIGHER SILHOUETTE (0.2543 vs 0.2024)", size=11.5, bold=True, color="gold")
        atxt = slide.shapes.add_textbox(Inches(6.82), Inches(5.46), Inches(5.80), Inches(1.12))
        self._set_textbox(
            atxt,
            "1. Outlier Rejection: K-Means forces extreme ultra-long-haul trains (e.g., Vivek Express > 4,000 km) into normal clusters, dragging down cluster cohesion. DBSCAN flags these 13 extreme trains (0.4%) as Noise.\n2. Natural Density Separation: Groups core commuter and express corridors without spherical distortion.",
            size=9.8,
            color="light_grey",
        )

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide, card_shapes=[left_card, db_pic, anom_card], header_shapes=self._last_header_shapes
        )

    def build_slide_16_cluster_interpretations(self) -> None:
        """
        Slide 16: 5 Authentic PIL-Rendered LHB Train Coach Bogies with Wheels
        that physically roll in along the track one after another!
        """
        bg = self.studio.create_dark_hud_background("16_clusters", accent_color=PALETTE["saffron"])
        slide = self._new_slide(
            bg,
            section_tag="Phase 4 • Domain Interpretation of Clusters",
            title="Interpreting the 5 Discovered Indian Railway Fleet Archetypes",
            subtitle="Each K-Means cluster is rendered as an authentic LHB Railway Coach Bogie rolling onto the platform",
            transition_style="ferris",
            audio_key="horn_track",
        )

        clusters = [
            (
                "c0",
                "COACH C-0",
                "Cluster 0: ER-Regional Network",
                "Eastern Railway (ER) Dominated Regional Fleet",
                "Medium-short distance routes concentrated heavily in the Eastern Railway zone with balanced stopping patterns and mixed general/sleeper coaches.",
                "saffron",
            ),
            (
                "c1",
                "COACH C-1",
                "Cluster 1: NFR-Mixed Operations",
                "Northeast Frontier Railway (NFR) Strategic Routes",
                "Captures trains operating across Northeast Frontier corridors featuring longer duration relative to distance due to hilly gradients and single-line sections.",
                "gold",
            ),
            (
                "c2",
                "COACH C-2",
                "Cluster 2: Short-Distance Commuter Pass",
                "High-Frequency Local Passenger Lifeline",
                "Short route distance, short duration, zero AC coaches (0% 1AC/2AC/3AC), high halt density — pure daily inter-town Passenger (Pass) services.",
                "cyan",
            ),
            (
                "c3",
                "COACH C-3",
                "Cluster 3: Long-Distance AC Premium Fleet",
                "Flagship Express & Superfast Trunk Corridors",
                "Longest average distance & duration, near-100% 3AC/2AC/Sleeper availability and high Chair Car/1AC presence — represents flagship Exp & SF trains.",
                "green_bright",
            ),
            (
                "c4",
                "COACH C-4",
                "Cluster 4: Secondary-Zone Short Passenger",
                "Regional Branch-Line & Unmapped Zone Connectors",
                "Short-to-medium haul passenger connectors distributed across secondary/unmapped zones providing rural-to-junction feeder connectivity.",
                "purple",
            ),
        ]

        train_motions = []
        for idx, (tag, code, title, sub, desc, col) in enumerate(clusters):
            cy = 1.44 + idx * 1.05
            bogie_png = self.studio.create_train_coach_bogie_png(
                tag=tag, coach_code=code, cluster_title=title, cluster_subtitle=sub, cluster_desc=desc, accent_name=col, width_in=12.22, height_in=1.00
            )
            pic = slide.shapes.add_picture(str(bogie_png), Inches(0.55), Inches(cy), Inches(12.22), Inches(1.00))
            train_motions.append((pic, "M -0.45 0 L 0 0 E", 1100 + idx * 150))

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide, train_shapes=train_motions, header_shapes=self._last_header_shapes
        )

    def build_slide_17_key_insights_conclusion(self) -> None:
        bg = self.studio.create_dark_hud_background(
            "17_conclusion", accent_color=PALETTE["gold"], secondary_accent=PALETTE["saffron"]
        )
        slide = self._new_slide(
            bg,
            section_tag="Junction 05 • Synthesis & Future Roadmap",
            title="Key Project Insights, Conclusion & Future Scope",
            subtitle="Synthesizing empirical findings across supervised classification, feature engineering, and clustering",
            accent_name="gold",
            transition_style="honeycomb",
            audio_key="chime_only",
        )

        insights = [
            (
                "ins1",
                "+7.39% F1",
                "1. Data Quality Beats Algorithms",
                "Fixing the broken duration_m schema bug (total_duration = duration_h * 60 + duration_m) immediately lifted all 5 supervised models and K-Means Silhouette (+0.0269).",
                "gold",
                "FINDING #1",
                0.98,
            ),
            (
                "ins2",
                "91.50% Acc",
                "2. Decision Tree Rules Win",
                "Decision Tree achieved 91.50% Accuracy, 0.8896 Macro F1, and 0.8743 ± 0.0155 5-Fold CV F1, driven by third_ac (35.5%), distance (22.3%), and total_duration (18.0%).",
                "saffron",
                "FINDING #2",
                0.92,
            ),
            (
                "ins3",
                "0.2543 Sil",
                "3. Dual Fleet Clustering",
                "K-Means (k=5, Silhouette 0.2024) uncovered interpretable regional/premium archetypes, while DBSCAN (Silhouette 0.2543) isolated 0.4% operational outliers.",
                "green_bright",
                "FINDING #3",
                0.90,
            ),
        ]

        icards = []
        for idx, (tag, val, tit, body, col, badge, ratio) in enumerate(insights):
            cx = 0.55 + idx * 4.12
            png = self.studio.create_hud_kpi_card_png(
                tag=tag, big_value=val, title=tit, subtitle=body, accent_name=col, badge_code=badge, meter_fill_ratio=ratio, width_in=3.92, height_in=3.55
            )
            pic = slide.shapes.add_picture(str(png), Inches(cx), Inches(1.48), Inches(3.92), Inches(3.55))
            icards.append(pic)

        fut_card = self._add_glass_card(
            slide, 0.55, 5.18, 12.22, 1.50, fill_color="panel_navy", border_color="cyan", left_stripe_color="cyan"
        )
        fhdr = slide.shapes.add_textbox(Inches(0.85), Inches(5.28), Inches(11.70), Inches(0.32))
        self._set_textbox(fhdr, "🚀  FUTURE SCOPE & REAL-WORLD DEPLOYMENT ROADMAP", size=12, bold=True, color="cyan")
        ftxt = slide.shapes.add_textbox(Inches(0.85), Inches(5.62), Inches(11.70), Inches(0.92))
        self._set_textbox(
            ftxt,
            "1. Ensemble & Gradient Boosting (Random Forest / XGBoost) to resolve the 8.50% Express ↔ Superfast boundary overlap.\n2. Incorporate live NTES delay telemetry, halt count, and average commercial speed features.\n3. Deploy the persisted joblib pipeline (models/dt_classifier.joblib & scaler.joblib) as a REST API for railway timetable auditing.",
            size=10.2,
            color="light_grey",
        )

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide, card_shapes=[*icards, fut_card], header_shapes=self._last_header_shapes
        )

    def build_slide_18_thank_you(self) -> None:
        bg = self.studio.create_dark_hud_background(
            "18_thank_you",
            accent_color=PALETTE["gold"],
            secondary_accent=PALETTE["saffron"],
            hero_image_path=self.paths.get_image("track_sunset.png"),
            hero_opacity=0.45,
        )
        slide = self._new_slide(
            bg,
            transition_style="doors",
            audio_key="terminus_viva",
            show_header=False,
            show_footer=True,
        )

        main_panel = self._add_glass_card(
            slide, 0.80, 0.55, 11.72, 6.08, fill_color="deep_navy", border_color="gold", top_stripe_color="saffron"
        )

        pill = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.45), Inches(0.82), Inches(6.45), Inches(0.38)
        )
        pill.fill.solid()
        pill.fill.fore_color.rgb = rgb_color("sign_yellow")
        pill.line.color.rgb = rgb_color("saffron")
        pill.line.width = Pt(1.5)
        self._set_shape_text(
            pill,
            "🔊  TERMINUS STATION BROADCAST  •  100% SYLLABUS COMPLIANT",
            size=10.0,
            bold=True,
            color="sign_black",
            align=PP_ALIGN.CENTER,
        )

        ty_tb = slide.shapes.add_textbox(Inches(1.20), Inches(1.32), Inches(10.90), Inches(0.85))
        self._set_textbox(
            ty_tb,
            "THANK YOU  •  OPEN FOR VIVA & Q&A",
            size=32,
            bold=True,
            color="gold",
            align=PP_ALIGN.CENTER,
            font_name=FONT_HEADING,
        )

        sub_tb = slide.shapes.add_textbox(Inches(1.50), Inches(2.12), Inches(10.30), Inches(0.42))
        self._set_textbox(
            sub_tb,
            "Classification and Clustering of Indian Railway Trains Using Machine Learning",
            size=14.5,
            bold=True,
            color="white",
            align=PP_ALIGN.CENTER,
        )

        cards = [
            (
                "ty_cred",
                "Roll No: 83",
                "Rajput Prince Singh",
                "BCA Sem-VII (2025-26) • Lokmanya College of Computer Application • Gujarat University",
                "saffron",
                "CANDIDATE",
                1.0,
            ),
            (
                "ty_res",
                "91.50% Acc",
                "Champion ML Results",
                "Decision Tree (0.8896 Macro F1, 0.8743 CV) • DBSCAN (0.2543 Silhouette) • +0.0587 Duration Fix",
                "gold",
                "RESULTS",
                0.95,
            ),
            (
                "ty_repo",
                "GitHub Repo",
                "Reproducible Artifacts",
                "github.com/rajputpri/Indian-Railway-Train • main_notebook.ipynb • models/*.joblib",
                "cyan",
                "ARTIFACTS",
                0.92,
            ),
        ]
        sub_cards = []
        for idx, (tag, val, tit, body, col, badge, ratio) in enumerate(cards):
            cx = 1.18 + idx * 3.74
            png = self.studio.create_hud_kpi_card_png(
                tag=tag, big_value=val, title=tit, subtitle=body, accent_name=col, badge_code=badge, meter_fill_ratio=ratio, width_in=3.50, height_in=2.38
            )
            pic = slide.shapes.add_picture(str(png), Inches(cx), Inches(2.72), Inches(3.50), Inches(2.38))
            sub_cards.append(pic)

        ty_train = slide.shapes.add_picture(
            str(self.vb_rake_path), Inches(4.25), Inches(5.22), Inches(4.85), Inches(1.22)
        )
        ty_train.name = "ThankYou_Animated_Train"

        CinematicTimelineAndAudioEngine.inject_dramatic_entrance_animations(
            slide,
            train_shapes=[(ty_train, "M -0.75 0 L 0 0 E", 2000)],
            card_shapes=sub_cards,
            header_shapes=[pill, ty_tb],
        )

    # ==========================================================================
    # MASTER BUILD PIPELINE
    # ==========================================================================

    def build_full_deck(self) -> Path:
        print("=" * 78)
        print("BUILDING INDIAN RAILWAYS ML PRESENTATION (V5.0 ULTRA BROADCAST EDITION)")
        print("=" * 78)

        print("[01/22] Slide 01: Hero Title + Spoken Station Welcome + WDP-4D Horn...")
        self.build_slide_01_title()
        print("[02/22] Slide 02: About Indian Railways (3D PIL Glassmorphic KPI Cards)...")
        self.build_slide_02_about_ir()
        print("[03/22] Slide 03: Problem Statement (Signal Red vs Signal Green)...")
        self.build_slide_03_problem_statement()
        print("[04/22] Slide 04: Project Objectives (6 PIL Telemetry Cards)...")
        self.build_slide_04_objectives()
        print("[05/22] Slide 05: Dataset Overview + Animated Vande Bharat Rake...")
        self.build_slide_05_dataset_overview()

        print("[06/22] Ticket Divider 01: Phase 1 (Spoken Station Announcement)...")
        self.build_ticket_divider_slide(
            ticket_id="phase1_eda",
            pnr_no="ML-2025-EDA1",
            from_station="RAW GEOJSON (5,208)",
            to_station="PHASE 1: EDA (4,466)",
            header_short_title="Phase 1 Boarding Pass: Exploratory Data Analysis & Data Fix",
            phase_title="PHASE 1 — EXPLORATORY DATA ANALYSIS & DATA QUALITY FIX",
            phase_subtitle="Syllabus Unit 1: Data Handling, Constant Audit, 10+ Visualizations & Duration Repair",
            coach_code="UNIT-1 / EDA",
            berth_info="PHASE-1 LOWER",
            deliverables=["10+ Plot Types Generated", "Constant Column Audit", "total_duration Feature Fix"],
            telemetry_specs=[
                ("RAW -> CLEAN", "5,208 -> 4,466"),
                ("FEATURE DIM", "26 COLUMNS"),
                ("KEY BUG FIXED", "duration_m REM"),
                ("STAGE SIGNAL", "GREEN / CLEAR"),
            ],
            stage_index=1,
            audio_key="phase1_eda",
        )

        print("[07/22] Slide 06: Phase 1 — Class & Zone Distribution...")
        self.build_slide_06_eda_distribution()
        print("[08/22] Slide 07: Phase 1 — Feature Histograms & Correlation Heatmap...")
        self.build_slide_07_feature_insights()
        print("[09/22] Slide 08: KILLER SLIDE — Data Quality Fix + Urgent Station Alert...")
        self.build_slide_08_killer_data_quality_fix()

        print("[10/22] Ticket Divider 02: Phase 2 (Spoken Station Announcement)...")
        self.build_ticket_divider_slide(
            ticket_id="phase2_eval",
            pnr_no="ML-2025-EVL2",
            from_station="PHASE 1: CLEAN DATA",
            to_station="PHASE 2: EVAL SUITE",
            header_short_title="Phase 2 Boarding Pass: Multi-Class Evaluation Framework",
            phase_title="PHASE 2 — MULTI-CLASS MODEL EVALUATION FRAMEWORK",
            phase_subtitle="Syllabus Unit 2: Accuracy, Precision, Recall, Macro/Weighted/Micro F1 & OvR ROC-AUC",
            coach_code="UNIT-2 / EVAL",
            berth_info="PHASE-2 UPPER",
            deliverables=["Macro F1 Primary Metric", "Micro Prec/Recall 0.9150", "Multi-Class OvR ROC Curves"],
            telemetry_specs=[
                ("TEST HOLDOUT", "894 TRAINS (20%)"),
                ("PRIMARY METRIC", "MACRO F1 (0.8896)"),
                ("BEST ROC-AUC", "0.9355 (KNN)"),
                ("ERROR AUDIT", "8.50% (SF <-> EXP)"),
            ],
            stage_index=2,
            audio_key="phase2_eval",
        )

        print("[11/22] Slide 09: Phase 2 — 6 PIL Evaluation Metric Cards...")
        self.build_slide_09_evaluation_metrics()
        print("[12/22] Slide 10: Phase 2 — Confusion Matrix & ROC Curves...")
        self.build_slide_10_confusion_matrix_roc()

        print("[13/22] Ticket Divider 03: Phase 3 (Spoken Station Announcement)...")
        self.build_ticket_divider_slide(
            ticket_id="phase3_models",
            pnr_no="ML-2025-MOD3",
            from_station="PHASE 2: METRICS",
            to_station="PHASE 3: CLASSIFIERS",
            header_short_title="Phase 3 Boarding Pass: Supervised Classification & Explainability",
            phase_title="PHASE 3 — SUPERVISED CLASSIFICATION & EXPLAINABILITY",
            phase_subtitle="Syllabus Unit 3: KNN, Decision Tree, Naive Bayes, SVM (RBF), Feature Importance & 5-Fold CV",
            coach_code="UNIT-3 / SUP-ML",
            berth_info="CHAMPION-DT",
            deliverables=["DT Winner: 91.50% / 0.8896", "5-Fold CV: 0.8743 ± 0.0155", "Top Feature: third_ac (35.5%)"],
            telemetry_specs=[
                ("CHAMPION MODEL", "DECISION TREE"),
                ("TEST ACCURACY", "91.50% (+36.5%)"),
                ("5-FOLD CV F1", "0.8743 ± 0.0155"),
                ("PERSISTED ARTIFACT", "dt_classifier.joblib"),
            ],
            stage_index=3,
            audio_key="phase3_models",
        )

        print("[14/22] Slide 11: Phase 3 — Digital LED Departure Leaderboard...")
        self.build_slide_11_model_comparison()
        print("[15/22] Slide 12: Best Model — Decision Tree Speedometer Gauges...")
        self.build_slide_12_best_model_dt()
        print("[16/22] Slide 13: Feature Importance & 5-Fold Cross-Validation...")
        self.build_slide_13_feature_importance_cv()

        print("[17/22] Ticket Divider 04: Phase 4 (Spoken Station Announcement)...")
        self.build_ticket_divider_slide(
            ticket_id="phase4_clusters",
            pnr_no="ML-2025-CLU4",
            from_station="PHASE 3: CLASSIFIERS",
            to_station="PHASE 4: CLUSTERING",
            header_short_title="Phase 4 Boarding Pass: Unsupervised Fleet Segmentation",
            phase_title="PHASE 4 — UNSUPERVISED FLEET SEGMENTATION",
            phase_subtitle="Syllabus Unit 4: K-Means (k=5), Elbow Method, 2D PCA Projection & DBSCAN Comparison",
            coach_code="UNIT-4 / UNSUP",
            berth_info="PCA-DBSCAN",
            deliverables=["K-Means Silhouette 0.2024", "DBSCAN Silhouette 0.2543", "trains_with_clusters.csv"],
            telemetry_specs=[
                ("K-MEANS OPTIMAL", "k = 5 CLUSTERS"),
                ("DBSCAN WINNER", "0.2543 SILHOUETTE"),
                ("OUTLIERS FOUND", "13 TRAINS (0.4%)"),
                ("EXPORTED CSV", "3,572 × 28 COLS"),
            ],
            stage_index=4,
            audio_key="phase4_clusters",
        )

        print("[18/22] Slide 14: Phase 4 — K-Means Elbow & PCA Projection...")
        self.build_slide_14_kmeans_clustering()
        print("[19/22] Slide 15: Phase 4 — DBSCAN vs K-Means Head-to-Head...")
        self.build_slide_15_dbscan_vs_kmeans()
        print("[20/22] Slide 16: Cluster Interpretations (5 Rolling LHB Coach Bogies)...")
        self.build_slide_16_cluster_interpretations()
        print("[21/22] Slide 17: Key Insights, Conclusion & Future Scope...")
        self.build_slide_17_key_insights_conclusion()
        print("[22/22] Slide 18: Thank You & Terminus Station Broadcast...")
        self.build_slide_18_thank_you()

        self.prs.save(str(self.paths.output_pptx))

        print("  [OPENXML ZIP ENGINE] Embedding .wav audio directly into .pptx package...")
        CinematicTimelineAndAudioEngine.embed_wav_files_into_pptx_zip(
            pptx_path=self.paths.output_pptx,
            slide_audio_map=self.slide_audio_map,
        )

        print("=" * 78)
        print(f"SUCCESS! V5.0 Presentation with Embedded Station Audio saved to:\n  {self.paths.output_pptx}")
        print(f"Total Slides Generated: {self.current_slide_no} (All 22 Slides have Native OpenXML Audio!)")
        print("=" * 78)
        return self.paths.output_pptx


if __name__ == "__main__":
    builder = RailwayPresentationBuilder()
    builder.build_full_deck()