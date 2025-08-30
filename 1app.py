# v21.5 Ultra Hybrid Tabbed (Super Full Hybrid) - FULL (auto switch Colab / Local)
# ---------------------------------------------------------------------
# Copy-paste ke Colab / Jupyter, jalankan sel. Script auto-install gradio jika belum ada.

import os, json, time, random, textwrap, pathlib
from typing import Dict, List, Any

# Optional auto-install gradio
try:
    import gradio as gr
except Exception:
    import sys, subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "gradio>=4.44.0"])
    import gradio as gr

# -------------------------
# CONFIG: RUN MODE
# -------------------------
# Options: "auto" (detect colab), "colab" (share=True), "local" (localhost)
RUN_MODE = os.getenv("ULTRA_RUN_MODE", "auto")

def detect_colab() -> bool:
    try:
        import google.colab  # type: ignore
        return True
    except Exception:
        return False

if RUN_MODE == "auto":
    RUN_MODE = "colab" if detect_colab() else "local"

# -------------------------
# PROJECT STATE
# -------------------------
VERSION = "v21.5 Ultra Hybrid Tabbed (Super Full Hybrid)"

def now_ts():
    return int(time.time())

PROJECT: Dict[str, Any] = {
    "meta": {
        "version": VERSION,
        "created": now_ts(),
        "last_saved": None,
        "notes": "v21.5 full: edit + dropdown dinamis + JSON output + local/colab switch"
    },
    "characters": {},    # name -> {role, traits, voice, mood_base, skills}
    "scenes": {},        # name -> {bg, lighting, weather, time_of_day, location}
    "dialogs": {},       # id -> {speaker, text, emotion_hint, pace}
    "transforms": {},
    "physical": {},
    "cameras": {},
    "event_triggers": {},
    "reka_adegan_ultra": []
}

# -------------------------
# Util
# -------------------------
def safe_name(s: str) -> str:
    return (s or "").strip().replace("\n", " ")

def list_choices(d: Dict[str, Any]) -> List[str]:
    return sorted(list(d.keys())) if d else []

# -------------------------
# Core CRUD
# -------------------------
def add_character(name: str, role: str, traits: str, voice: str, mood_base: str, skills: str) -> str:
    name = safe_name(name)
    if not name:
        return "Nama karakter wajib diisi."
    PROJECT["characters"][name] = {
        "role": role or "",
        "traits": traits or "",
        "voice": voice or "",
        "mood_base": mood_base or "neutral",
        "skills": [s.strip() for s in (skills or "").split(',') if s.strip()]
    }
    return f"✔ Karakter '{name}' disimpan."

def remove_character(name: str) -> str:
    name = safe_name(name)
    if name in PROJECT["characters"]:
        del PROJECT["characters"][name]
        return f"✔ Karakter '{name}' dihapus."
    return "Karakter tidak ditemukan."

def add_scene(name: str, bg: str, lighting: str, weather: str, time_of_day: str, location: str) -> str:
    name = safe_name(name)
    if not name:
        return "Nama scene wajib diisi."
    PROJECT["scenes"][name] = {
        "bg": bg or "",
        "lighting": lighting or "soft",
        "weather": weather or "clear",
        "time_of_day": time_of_day or "day",
        "location": location or ""
    }
    return f"✔ Scene '{name}' disimpan."

def remove_scene(name: str) -> str:
    name = safe_name(name)
    if name in PROJECT["scenes"]:
        del PROJECT["scenes"][name]
        return f"✔ Scene '{name}' dihapus."
    return "Scene tidak ditemukan."

def add_dialog(dialog_id: str, speaker: str, text: str, emotion_hint: str, pace: float) -> str:
    dialog_id = safe_name(dialog_id)
    if not dialog_id:
        return "ID dialog wajib diisi."
    if speaker and speaker not in PROJECT["characters"]:
        return f"Speaker '{speaker}' belum terdaftar di Characters."
    PROJECT["dialogs"][dialog_id] = {
        "speaker": speaker or "",
        "text": text or "",
        "emotion_hint": emotion_hint or "auto",
        "pace": max(0.25, min(3.0, float(pace or 1.0)))
    }
    return f"✔ Dialog '{dialog_id}' disimpan."

def remove_dialog(dialog_id: str) -> str:
    dialog_id = safe_name(dialog_id)
    if dialog_id in PROJECT["dialogs"]:
        del PROJECT["dialogs"][dialog_id]
        return f"✔ Dialog '{dialog_id}' dihapus."
    return "Dialog tidak ditemukan."

def add_transform(name: str, position: str, rotation: str, scale: str, fx: str) -> str:
    name = safe_name(name)
    if not name:
        return "Nama transform wajib diisi."
    PROJECT["transforms"][name] = {
        "position": position or "0,0,0",
        "rotation": rotation or "0,0,0",
        "scale": scale or "1,1,1",
        "fx": [s.strip() for s in (fx or "").split(',') if s.strip()]
    }
    return f"✔ Transform '{name}' disimpan."

def remove_transform(name: str) -> str:
    name = safe_name(name)
    if name in PROJECT["transforms"]:
        del PROJECT["transforms"][name]
        return f"✔ Transform '{name}' dihapus."
    return "Transform tidak ditemukan."

def add_physical(name: str, wind: float, particles: str, collision: bool, gravity: float) -> str:
    name = safe_name(name)
    if not name:
        return "Nama physical wajib diisi."
    PROJECT["physical"][name] = {
        "wind": float(wind or 0.0),
        "particles": [s.strip() for s in (particles or "").split(',') if s.strip()],
        "collision": bool(collision),
        "gravity": float(gravity or 9.8)
    }
    return f"✔ Physical '{name}' disimpan."

def remove_physical(name: str) -> str:
    name = safe_name(name)
    if name in PROJECT["physical"]:
        del PROJECT["physical"][name]
        return f"✔ Physical '{name}' dihapus."
    return "Physical tidak ditemukan."

def add_camera(name: str, cam_type: str, fov: float, dof: str, movement: str) -> str:
    name = safe_name(name)
    if not name:
        return "Nama kamera wajib diisi."
    PROJECT["cameras"][name] = {
        "type": cam_type or "perspective",
        "fov": max(10.0, min(140.0, float(fov or 50.0))),
        "dof": dof or "auto",
        "movement": movement or "static"
    }
    return f"✔ Kamera '{name}' disimpan."

def remove_camera(name: str) -> str:
    name = safe_name(name)
    if name in PROJECT["cameras"]:
        del PROJECT["cameras"][name]
        return f"✔ Kamera '{name}' dihapus."
    return "Kamera tidak ditemukan."

def add_event(name: str, when: str, action: str, params: str) -> str:
    name = safe_name(name)
    if not name:
        return "Nama event wajib diisi."
    PROJECT["event_triggers"][name] = {
        "when": when or "",
        "action": action or "",
        "params": params or ""
    }
    return f"✔ Event '{name}' disimpan."

def remove_event(name: str) -> str:
    name = safe_name(name)
    if name in PROJECT["event_triggers"]:
        del PROJECT["event_triggers"][name]
        return f"✔ Event '{name}' dihapus."
    return "Event tidak ditemukan."

# -------------------------
# Ultra engine (keperluan demo)
# -------------------------
EMOTION_MAP = {
    "happy": ["smile_soft", "smile_wide", "laugh"],
    "sad": ["frown_soft", "tear_up"],
    "angry": ["brow_down", "shout"],
    "fear": ["gasp", "tremble"],
    "love": ["soft_gaze", "blush"],
    "neutral": ["idle", "blink"],
    "auto": ["auto"]
}
CAM_PATTERNS = ["dolly_in_slow","dolly_out_slow","handheld_subtle","pan_left_slow","pan_right_slow","crane_up","crane_down","orbit_subject","static_center"]
WEATHER_AUDIO = {
    "rain": ["rain_light","rain_medium","thunder_far"],
    "clear": ["birds","soft_breeze"],
    "storm": ["thunder_close","heavy_wind"],
    "snow": ["wind_chill","footstep_snow"],
    "city": ["traffic_low","hum_crowd"],
}

def infer_emotion(text: str, hint: str) -> str:
    t = (text or "").lower()
    if hint and hint != "auto":
        return hint
    if any(k in t for k in ["marah","kesal","benci","angry"]):
        return "angry"
    if any(k in t for k in ["sedih","kecewa","menangis","sad"]):
        return "sad"
    if any(k in t for k in ["takut","cemas","fear","khawatir"]):
        return "fear"
    if any(k in t for k in ["cinta","sayang","love"]):
        return "love"
    if any(k in t for k in ["senang","gembira","bahagia","happy"]):
        return "happy"
    return "neutral"

def suggest_soundscape(scene: Dict[str, Any]) -> List[str]:
    weather = (scene.get("weather") or "clear").lower()
    base = WEATHER_AUDIO.get(weather, ["ambience_low"])
    tod = (scene.get("time_of_day") or "day").lower()
    if tod in ("night","dawn") and "birds" in base:
        base = [s for s in base if s != "birds"] + ["crickets"]
    return sorted(set(base))

def auto_camera(scene: Dict[str, Any], style: str) -> Dict[str, Any]:
    pattern = random.choice(CAM_PATTERNS)
    fov = 28.0 if "cinematic" in (style or "").lower() else round(random.uniform(35,75), 2)
    dof = "shallow" if fov < 35 else "auto"
    return {"type":"perspective","fov":round(fov,2),"dof":dof,"movement":pattern}

def background_adapt(scene: Dict[str, Any], style: str) -> Dict[str, Any]:
    bg = scene.get("bg") or "neutral_stage"
    lighting = scene.get("lighting") or "soft"
    if "noir" in (style or "").lower():
        lighting = "hard_contrast"
    return {"bg":bg,"lighting":lighting,"grade":style or "default"}

def npc_autonomy(char: Dict[str, Any], emotion: str) -> Dict[str, Any]:
    base = (char.get("traits") or "").lower()
    move = "idle_breath"
    if "energetic" in base or emotion == "happy":
        move = random.choice(["talk_hand","lean_forward","nod_fast"])
    elif emotion in ("sad","fear"):
        move = random.choice(["look_down","shiver","step_back"])
    elif emotion == "angry":
        move = random.choice(["point_finger","clench_fist","lean_in"])
    return {"behavior":move,"intensity":round(random.uniform(0.3,0.9),2)}

def ultra_generate(prompt: str, scene_name: str, dialog_ids: List[str], style: str, shots: int, seed: int = 42) -> Dict[str, Any]:
    random.seed(int(seed or 42))
    if not scene_name or scene_name not in PROJECT["scenes"]:
        return {"error":"Scene tidak valid."}
    scene = PROJECT["scenes"][scene_name]
    seq = []
    for i in range(max(1,int(shots or 3))):
        cam = auto_camera(scene, style)
        bgd = background_adapt(scene, style)
        dialog = None
        if dialog_ids:
            chosen = random.choice(dialog_ids)
            dialog = PROJECT["dialogs"].get(chosen)
        emo = infer_emotion((dialog or {}).get("text") or prompt, (dialog or {}).get("emotion_hint","auto"))
        expr = random.choice(EMOTION_MAP.get(emo, EMOTION_MAP["neutral"]))
        if PROJECT["characters"]:
            cname = random.choice(list(PROJECT["characters"].keys()))
            char = PROJECT["characters"][cname]
            npc = npc_autonomy(char, emo)
        else:
            cname = None
            npc = {"behavior":"idle_breath","intensity":0.4}
        sfx = suggest_soundscape(scene)
        seq.append({
            "shot_index": i,
            "prompt": prompt,
            "scene": scene_name,
            "camera": cam,
            "background": bgd,
            "speaker": (dialog or {}).get("speaker"),
            "text": (dialog or {}).get("text"),
            "emotion": emo,
            "expression": expr,
            "npc": {"character": cname, **npc},
            "soundscape": sfx,
            "duration": round(random.uniform(2.5,6.0),2)
        })
    pack = {"created": now_ts(), "style": style or "default", "seed": int(seed or 42), "shots": seq}
    PROJECT["reka_adegan_ultra"].append(pack)
    return {"ok": True, "pack": pack}

# Formatter (human readable + JSON)
def format_ultra_pack(pack: Dict[str, Any]) -> str:
    if not pack:
        return ""
    lines = [f"ULTRA PACK @ {pack.get('created')} | style={pack.get('style')} | seed={pack.get('seed')}"]
    for s in pack.get("shots", []):
        # Camera/background and npc are dicts: present them compactly but readable
        cam_str = json.dumps(s.get("camera", {}), ensure_ascii=False)
        bg_str = json.dumps(s.get("background", {}), ensure_ascii=False)
        npc_str = json.dumps(s.get("npc", {}), ensure_ascii=False)
        lines.append(textwrap.dedent(f"""
            — Shot {s['shot_index']} —
              Scene     : {s['scene']}
              Camera    : {cam_str}
              Background: {bg_str}
              Speaker   : {s.get('speaker')}
              Dialog    : {s.get('text')}
              Emotion   : {s['emotion']} | Expr: {s['expression']}
              NPC       : {npc_str}
              SFX       : {', '.join(s['soundscape'])}
              Duration  : {s['duration']}s
        """))
    return "\n".join(lines)

def format_ultra_json(pack: Dict[str, Any]) -> str:
    if not pack:
        return "{}"
    # Ensure all contained dicts/lists are JSON-serializable (they are)
    return json.dumps(pack, ensure_ascii=False, indent=2)

# -------------------------
# Save / Load / Export
# -------------------------
def save_project(path: str) -> str:
    PROJECT["meta"]["last_saved"] = now_ts()
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(PROJECT, f, ensure_ascii=False, indent=2)
    return f"✔ Project disimpan ke: {p}"

def load_project(path: str) -> str:
    p = pathlib.Path(path)
    if not p.exists():
        return "File tidak ditemukan."
    global PROJECT
    with open(p, 'r', encoding='utf-8') as f:
        PROJECT = json.load(f)
    return f"✔ Project dimuat dari: {p}"

def export_storyboard_csv(path: str) -> str:
    lines = ["shot_index,scene,cam_type,fov,dof,movement,emotion,expression,duration,sfx"]
    packs = PROJECT.get("reka_adegan_ultra", [])
    for pack in packs:
        for s in pack.get("shots", []):
            sfx = ";".join(s.get("soundscape", []))
            cam = s.get("camera", {})
            lines.append(f"{s['shot_index']},{s['scene']},{cam.get('type')},{cam.get('fov')},{cam.get('dof')},{cam.get('movement')},{s.get('emotion')},{s.get('expression')},{s.get('duration')},{sfx}")
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    return f"✔ Storyboard CSV diekspor ke: {p}"

# -------------------------
# Demo seed
# -------------------------
def seed_demo():
    if not PROJECT["characters"]:
        add_character("Raka","protagonist","energetic, brave","tenor","neutral","parkour,leadership")
        add_character("Maya","deuteragonist","calm, analytic","alto","neutral","hacking,first_aid")
    if not PROJECT["scenes"]:
        add_scene("RooftopDawn","city_rooftop","soft","clear","dawn","Jakarta")
        add_scene("AlleyRain","narrow_alley","moody","rain","night","Jakarta")
    if not PROJECT["dialogs"]:
        add_dialog("D1","Raka","Kita harus bergerak sekarang sebelum mereka tiba.","auto",1.0)
        add_dialog("D2","Maya","Tunggu, aku butuh waktu beberapa detik lagi...","auto",1.0)

seed_demo()

# -------------------------
# GRADIO UI (Tabbed)
# -------------------------
with gr.Blocks(title=VERSION, fill_height=True) as APP:
    gr.Markdown(f"# {VERSION}\nSuper Full Hybrid edition: semua tab + pilihan JSON + lokal/colab switch.")

    with gr.Tabs():
        # Project
        with gr.Tab("Project"):
            with gr.Row():
                save_path = gr.Textbox(value="/content/project_v21_5.json", label="Path Save Project (.json)")
                load_path = gr.Textbox(value="/content/project_v21_5.json", label="Path Load Project (.json)")
            with gr.Row():
                btn_save = gr.Button("💾 Save Project")
                btn_load = gr.Button("📂 Load Project")
                btn_export_csv = gr.Button("📤 Export Storyboard CSV")
            out_proj = gr.Textbox(label="Status", interactive=False)
            btn_save.click(save_project, inputs=[save_path], outputs=[out_proj])
            btn_load.click(load_project, inputs=[load_path], outputs=[out_proj])
            btn_export_csv.click(export_storyboard_csv, inputs=[save_path], outputs=[out_proj])

        # Characters
        with gr.Tab("Characters"):
            with gr.Row():
                ch_name = gr.Textbox(label="Name")
                ch_role = gr.Textbox(label="Role")
            ch_traits = gr.Textbox(label="Traits (comma separated)")
            with gr.Row():
                ch_voice = gr.Textbox(label="Voice")
                ch_mood = gr.Dropdown(["neutral","happy","sad","angry","fear","love"], value="neutral", label="Base Mood")
            ch_skills = gr.Textbox(label="Skills (comma separated)")
            with gr.Row():
                ch_add = gr.Button("➕ Add/Update")
                ch_edit_name = gr.Dropdown(choices=list_choices(PROJECT["characters"]), label="Edit Character")
                ch_remove_name = gr.Dropdown(choices=list_choices(PROJECT["characters"]), label="Remove Character")
                ch_remove = gr.Button("🗑 Remove")
            ch_out = gr.Textbox(label="Status", interactive=False)

            def refresh_char_choices():
                return gr.update(choices=list_choices(PROJECT["characters"]))

            def load_char_to_inputs(name):
                if not name or name not in PROJECT["characters"]:
                    return "", "", "", "", "neutral", ""
                c = PROJECT["characters"][name]
                return name, c.get("role",""), c.get("traits",""), c.get("voice",""), c.get("mood_base","neutral"), ",".join(c.get("skills",[]))

            ch_edit_name.change(load_char_to_inputs, inputs=[ch_edit_name], outputs=[ch_name, ch_role, ch_traits, ch_voice, ch_mood, ch_skills])

            ch_add.click(add_character, inputs=[ch_name, ch_role, ch_traits, ch_voice, ch_mood, ch_skills], outputs=[ch_out]).then(
                refresh_char_choices, outputs=[ch_edit_name]
            ).then(
                refresh_char_choices, outputs=[ch_remove_name]
            )
            ch_remove.click(remove_character, inputs=[ch_remove_name], outputs=[ch_out]).then(
                refresh_char_choices, outputs=[ch_edit_name]
            ).then(
                refresh_char_choices, outputs=[ch_remove_name]
            )

        # Scenes
        with gr.Tab("Scenes"):
            with gr.Row():
                sc_name = gr.Textbox(label="Scene Name")
                sc_bg = gr.Textbox(label="Background Key")
            with gr.Row():
                sc_light = gr.Dropdown(["soft","moody","hard","ambient"], value="soft", label="Lighting")
                sc_weather = gr.Dropdown(["clear","rain","storm","snow","city"], value="clear", label="Weather")
                sc_tod = gr.Dropdown(["dawn","day","dusk","night"], value="day", label="Time of Day")
            sc_loc = gr.Textbox(label="Location")
            with gr.Row():
                sc_add = gr.Button("➕ Add/Update")
                sc_edit_name = gr.Dropdown(choices=list_choices(PROJECT["scenes"]), label="Edit Scene")
                sc_rm_name = gr.Dropdown(choices=list_choices(PROJECT["scenes"]), label="Remove Scene")
                sc_remove = gr.Button("🗑 Remove")
            sc_out = gr.Textbox(label="Status", interactive=False)

            def refresh_scene_choices():
                return gr.update(choices=list_choices(PROJECT["scenes"]))

            def load_scene_to_inputs(name):
                if not name or name not in PROJECT["scenes"]:
                    return "", "", "soft", "clear", "day", ""
                s = PROJECT["scenes"][name]
                return name, s.get("bg",""), s.get("lighting","soft"), s.get("weather","clear"), s.get("time_of_day","day"), s.get("location","")

            sc_edit_name.change(load_scene_to_inputs, inputs=[sc_edit_name], outputs=[sc_name, sc_bg, sc_light, sc_weather, sc_tod, sc_loc])

            sc_add.click(add_scene, inputs=[sc_name, sc_bg, sc_light, sc_weather, sc_tod, sc_loc], outputs=[sc_out]).then(
                refresh_scene_choices, outputs=[sc_edit_name]
            ).then(
                refresh_scene_choices, outputs=[sc_rm_name]
            )

            sc_remove.click(remove_scene, inputs=[sc_rm_name], outputs=[sc_out]).then(
                refresh_scene_choices, outputs=[sc_edit_name]
            ).then(
                refresh_scene_choices, outputs=[sc_rm_name]
            )

        # Dialogs
        with gr.Tab("Dialogs"):
            with gr.Row():
                dl_id = gr.Textbox(label="Dialog ID")
                dl_speaker = gr.Dropdown(choices=list_choices(PROJECT["characters"]), label="Speaker (Character)")
            dl_text = gr.Textbox(label="Text", lines=3)
            with gr.Row():
                dl_emotion = gr.Dropdown(["auto","neutral","happy","sad","angry","fear","love"], value="auto", label="Emotion Hint")
                dl_pace = gr.Slider(0.25, 3.0, value=1.0, step=0.05, label="Pace (dialog delivery)")
            with gr.Row():
                dl_add = gr.Button("➕ Add/Update")
                dl_edit_id = gr.Dropdown(choices=list_choices(PROJECT["dialogs"]), label="Edit Dialog")
                dl_rm_id = gr.Dropdown(choices=list_choices(PROJECT["dialogs"]), label="Remove Dialog")
                dl_remove = gr.Button("🗑 Remove")
            dl_out = gr.Textbox(label="Status", interactive=False)

            def refresh_dialog_choices():
                return gr.update(choices=list_choices(PROJECT["dialogs"]))

            def refresh_speaker_choices():
                return gr.update(choices=list_choices(PROJECT["characters"]))

            def load_dialog_to_inputs(did):
                if not did:
                    return "", "", "", "auto", 1.0
                d = PROJECT["dialogs"].get(did)
                if not d:
                    return "", "", "", "auto", 1.0
                return did, d.get("speaker",""), d.get("text",""), d.get("emotion_hint","auto"), d.get("pace",1.0)

            dl_edit_id.change(load_dialog_to_inputs, inputs=[dl_edit_id], outputs=[dl_id, dl_speaker, dl_text, dl_emotion, dl_pace])

            dl_add.click(add_dialog, inputs=[dl_id, dl_speaker, dl_text, dl_emotion, dl_pace], outputs=[dl_out]).then(
                refresh_dialog_choices, outputs=[dl_edit_id]
            ).then(
                refresh_dialog_choices, outputs=[dl_rm_id]
            ).then(
                refresh_speaker_choices, outputs=[dl_speaker]
            )

            dl_remove.click(remove_dialog, inputs=[dl_rm_id], outputs=[dl_out]).then(
                refresh_dialog_choices, outputs=[dl_edit_id]
            ).then(
                refresh_dialog_choices, outputs=[dl_rm_id]
            )

        # Transforms
        with gr.Tab("Transforms"):
            with gr.Row():
                tr_name = gr.Textbox(label="Transform Name")
                tr_pos = gr.Textbox(value="0,0,0", label="Position (x,y,z)")
                tr_rot = gr.Textbox(value="0,0,0", label="Rotation (x,y,z)")
                tr_scale = gr.Textbox(value="1,1,1", label="Scale (x,y,z)")
            tr_fx = gr.Textbox(label="FX (comma separated)")
            with gr.Row():
                tr_add = gr.Button("➕ Add/Update")
                tr_edit = gr.Dropdown(choices=list_choices(PROJECT["transforms"]), label="Edit Transform")
                tr_rm = gr.Dropdown(choices=list_choices(PROJECT["transforms"]), label="Remove Transform")
                tr_remove = gr.Button("🗑 Remove")
            tr_out = gr.Textbox(label="Status", interactive=False)

            def refresh_tr_choices():
                return gr.update(choices=list_choices(PROJECT["transforms"]))

            def load_tr_to_inputs(name):
                if not name:
                    return "", "0,0,0", "0,0,0", "1,1,1", ""
                t = PROJECT["transforms"].get(name)
                if not t:
                    return "", "0,0,0", "0,0,0", "1,1,1", ""
                return name, t.get("position","0,0,0"), t.get("rotation","0,0,0"), t.get("scale","1,1,1"), ",".join(t.get("fx",[]))

            tr_edit.change(load_tr_to_inputs, inputs=[tr_edit], outputs=[tr_name, tr_pos, tr_rot, tr_scale, tr_fx])

            tr_add.click(add_transform, inputs=[tr_name, tr_pos, tr_rot, tr_scale, tr_fx], outputs=[tr_out]).then(
                refresh_tr_choices, outputs=[tr_edit]
            ).then(
                refresh_tr_choices, outputs=[tr_rm]
            )

            tr_remove.click(remove_transform, inputs=[tr_rm], outputs=[tr_out]).then(
                refresh_tr_choices, outputs=[tr_edit]
            ).then(
                refresh_tr_choices, outputs=[tr_rm]
            )

        # Physical
        with gr.Tab("Physical"):
            with gr.Row():
                ph_name = gr.Textbox(label="Physical Name")
                ph_wind = gr.Slider(0.0, 25.0, value=0.0, step=0.1, label="Wind (m/s)")
                ph_particles = gr.Textbox(label="Particles (comma separated)")
            with gr.Row():
                ph_collision = gr.Checkbox(label="Collision Enabled", value=True)
                ph_gravity = gr.Slider(0.0, 20.0, value=9.8, step=0.1, label="Gravity (m/s^2)")
            with gr.Row():
                ph_add = gr.Button("➕ Add/Update")
                ph_edit = gr.Dropdown(choices=list_choices(PROJECT["physical"]), label="Edit Physical")
                ph_rm = gr.Dropdown(choices=list_choices(PROJECT["physical"]), label="Remove Physical")
                ph_remove = gr.Button("🗑 Remove")
            ph_out = gr.Textbox(label="Status", interactive=False)

            def refresh_ph_choices():
                return gr.update(choices=list_choices(PROJECT["physical"]))

            def load_ph_to_inputs(name):
                if not name:
                    return "", 0.0, "", True, 9.8
                p = PROJECT["physical"].get(name)
                if not p:
                    return "", 0.0, "", True, 9.8
                return name, p.get("wind",0.0), ",".join(p.get("particles",[])), p.get("collision",True), p.get("gravity",9.8)

            ph_edit.change(load_ph_to_inputs, inputs=[ph_edit], outputs=[ph_name, ph_wind, ph_particles, ph_collision, ph_gravity])

            ph_add.click(add_physical, inputs=[ph_name, ph_wind, ph_particles, ph_collision, ph_gravity], outputs=[ph_out]).then(
                refresh_ph_choices, outputs=[ph_edit]
            ).then(
                refresh_ph_choices, outputs=[ph_rm]
            )
            ph_remove.click(remove_physical, inputs=[ph_rm], outputs=[ph_out]).then(
                refresh_ph_choices, outputs=[ph_edit]
            ).then(
                refresh_ph_choices, outputs=[ph_rm]
            )

        # Camera
        with gr.Tab("Camera"):
            with gr.Row():
                cm_name = gr.Textbox(label="Camera Name")
                cm_type = gr.Dropdown(["perspective","ortho"], value="perspective", label="Type")
                cm_fov = gr.Slider(10.0, 140.0, value=50.0, step=0.5, label="FOV")
            with gr.Row():
                cm_dof = gr.Dropdown(["auto","shallow","deep"], value="auto", label="DOF")
                cm_move = gr.Dropdown(["static","pan_left","pan_right","tilt_up","tilt_down","dolly_in","dolly_out","orbit"], value="static", label="Movement")
            with gr.Row():
                cm_add = gr.Button("➕ Add/Update")
                cm_edit = gr.Dropdown(choices=list_choices(PROJECT["cameras"]), label="Edit Camera")
                cm_rm = gr.Dropdown(choices=list_choices(PROJECT["cameras"]), label="Remove Camera")
                cm_remove = gr.Button("🗑 Remove")
            cm_out = gr.Textbox(label="Status", interactive=False)

            def refresh_cm_choices():
                return gr.update(choices=list_choices(PROJECT["cameras"]))

            def load_cm_to_inputs(name):
                if not name:
                    return "", "perspective", 50.0, "auto", "static"
                c = PROJECT["cameras"].get(name)
                if not c:
                    return "", "perspective", 50.0, "auto", "static"
                return name, c.get("type","perspective"), c.get("fov",50.0), c.get("dof","auto"), c.get("movement","static")

            cm_edit.change(load_cm_to_inputs, inputs=[cm_edit], outputs=[cm_name, cm_type, cm_fov, cm_dof, cm_move])

            cm_add.click(add_camera, inputs=[cm_name, cm_type, cm_fov, cm_dof, cm_move], outputs=[cm_out]).then(
                refresh_cm_choices, outputs=[cm_edit]
            ).then(
                refresh_cm_choices, outputs=[cm_rm]
            )

            cm_remove.click(remove_camera, inputs=[cm_rm], outputs=[cm_out]).then(
                refresh_cm_choices, outputs=[cm_edit]
            ).then(
                refresh_cm_choices, outputs=[cm_rm]
            )

        # Events
        with gr.Tab("Events"):
            with gr.Row():
                ev_name = gr.Textbox(label="Event Name")
                ev_when = gr.Textbox(label="When (e.g. t>3, on_dialog:D1)")
            with gr.Row():
                ev_action = gr.Textbox(label="Action (e.g. play_sfx, camera_shake)")
                ev_params = gr.Textbox(label="Params (json/plain)")
            with gr.Row():
                ev_add = gr.Button("➕ Add/Update")
                ev_edit = gr.Dropdown(choices=list_choices(PROJECT["event_triggers"]), label="Edit Event")
                ev_rm = gr.Dropdown(choices=list_choices(PROJECT["event_triggers"]), label="Remove Event")
                ev_remove = gr.Button("🗑 Remove")
            ev_out = gr.Textbox(label="Status", interactive=False)

            def refresh_ev_choices():
                return gr.update(choices=list_choices(PROJECT["event_triggers"]))

            def load_ev_to_inputs(name):
                if not name:
                    return "", "", "", ""
                e = PROJECT["event_triggers"].get(name)
                if not e:
                    return "", "", "", ""
                return name, e.get("when",""), e.get("action",""), e.get("params","")

            ev_edit.change(load_ev_to_inputs, inputs=[ev_edit], outputs=[ev_name, ev_when, ev_action, ev_params])

            ev_add.click(add_event, inputs=[ev_name, ev_when, ev_action, ev_params], outputs=[ev_out]).then(
                refresh_ev_choices, outputs=[ev_edit]
            ).then(
                refresh_ev_choices, outputs=[ev_rm]
            )

            ev_remove.click(remove_event, inputs=[ev_rm], outputs=[ev_out]).then(
                refresh_ev_choices, outputs=[ev_edit]
            ).then(
                refresh_ev_choices, outputs=[ev_rm]
            )

        # Ultra AI
        with gr.Tab("Ultra AI"):
            ultra_prompt = gr.Textbox(label="Prompt sinematik (narasi global)", lines=3, value="Kejar-kejaran di atap gedung saat fajar, nuansa tegang namun heroik.")
            with gr.Row():
                ultra_scene = gr.Dropdown(choices=list_choices(PROJECT["scenes"]), value=(list_choices(PROJECT["scenes"])[0] if PROJECT["scenes"] else None), label="Scene")
                ultra_dialogs = gr.CheckboxGroup(choices=list_choices(PROJECT["dialogs"]), label="Dialog IDs (opsional)")
            with gr.Row():
                ultra_style = gr.Dropdown(["default","cinematic","noir","documentary","handheld"], value="cinematic", label="Gaya")
                ultra_shots = gr.Slider(1, 12, value=4, step=1, label="Jumlah Shot")
                ultra_seed = gr.Number(value=42, label="Seed")
            with gr.Row():
                ultra_format = gr.Radio(["Human-readable","JSON"], value="Human-readable", label="Output Format")
                ultra_btn = gr.Button("⚡ Generate Ultra Pack")
            ultra_text = gr.Textbox(label="Output (ringkas / JSON)", lines=18)

            def do_ultra(prompt, scene, dlg_ids, style, shots, seed, fmt):
                if isinstance(dlg_ids, (list, tuple)):
                    dialog_ids = [d for d in dlg_ids if d in PROJECT["dialogs"]]
                else:
                    dialog_ids = []
                res = ultra_generate(prompt, scene, dialog_ids, style, int(shots or 3), int(seed or 42))
                if res.get("ok"):
                    if fmt == "JSON":
                        return format_ultra_json(res["pack"])
                    return format_ultra_pack(res["pack"])
                return f"Error: {res.get('error')}"

            ultra_btn.click(do_ultra, inputs=[ultra_prompt, ultra_scene, ultra_dialogs, ultra_style, ultra_shots, ultra_seed, ultra_format], outputs=[ultra_text])

            # --- REFRESH HELPERS for Ultra AI sync ---
            def refresh_ultra_scene():
                choices = list_choices(PROJECT["scenes"])
                val = choices[0] if choices else None
                return gr.update(choices=choices, value=val)

            def refresh_ultra_dialogs():
                return gr.update(choices=list_choices(PROJECT["dialogs"]))

            def refresh_ultra_speakers():
                return gr.update(choices=list_choices(PROJECT["characters"]))

            # Wire Scenes/Dialogs/Characters add/remove to Ultra AI components
            sc_add.click(refresh_ultra_scene, outputs=[ultra_scene])
            sc_remove.click(refresh_ultra_scene, outputs=[ultra_scene])
            dl_add.click(refresh_ultra_dialogs, outputs=[ultra_dialogs])
            dl_remove.click(refresh_ultra_dialogs, outputs=[ultra_dialogs])
            ch_add.click(refresh_ultra_speakers, outputs=[dl_speaker])
            ch_remove.click(refresh_ultra_speakers, outputs=[dl_speaker])

        # Inspect / JSON
        with gr.Tab("Inspect / JSON"):
            show_btn = gr.Button("👁 Tampilkan JSON Project")
            json_box = gr.Code(language="json", label="PROJECT JSON")
            def show_json():
                return json.dumps(PROJECT, ensure_ascii=False, indent=2)
            show_btn.click(show_json, outputs=[json_box])

    gr.Markdown("""
    **Tips Pakai Cepat**
    1. Buka tab Characters & Scenes untuk tambah minimal 1-2 data.
    2. Opsional: tambah Dialogs, Transforms, Physical, Camera, Events.
    3. Masuk tab Ultra AI, pilih Scene, lalu klik Generate (pilih format JSON bila mau dipakai LLM).
    4. Simpan project via tab Project → Save Project. Export storyboard ke CSV juga bisa.
    """)

# -------------------------
# -------------------------
# LAUNCH (Colab / Local auto switch)
# -------------------------
if RUN_MODE == "colab":
    # Mode Google Colab → otomatis link publik
    APP.launch(
        share=True,
        debug=False,
        show_error=True
    )
else:
    # Mode Localhost → otomatis cari port kosong kalau bentrok
    import socket

    def get_free_port(default_port=7860):
        port = default_port
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(("127.0.0.1", port)) != 0:
                    return port
            port += 1

    free_port = get_free_port(7860)

    APP.launch(
        server_name="127.0.0.1",
        server_port=free_port,
        share=False,
        debug=False,
        show_error=True
    )

