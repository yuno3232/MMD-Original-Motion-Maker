# -*- coding: utf-8 -*-
"""
MMD Original Motion Maker - simple procedural VMD generator
Python 3.x / Windows. Uses only the Python standard library (Tkinter).
Creates basic, editable dance motions as .vmd files.
"""
import math
import struct
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

VMD_HEADER = b"Vocaloid Motion Data 0002"

def sjis_fixed(text, size):
    data = text.encode("shift_jis", errors="replace")
    return data[:size].ljust(size, b"\x00")

def quat_from_euler(rx, ry, rz):
    # Euler angles in radians; XYZ composition, output x,y,z,w.
    cx, sx = math.cos(rx/2), math.sin(rx/2)
    cy, sy = math.cos(ry/2), math.sin(ry/2)
    cz, sz = math.cos(rz/2), math.sin(rz/2)
    # q = qz * qy * qx
    w = cz*cy*cx + sz*sy*sx
    x = cz*cy*sx - sz*sy*cx
    y = cz*sy*cx + sz*cy*sx
    z = sz*cy*cx - cz*sy*sx
    return (x, y, z, w)

def curve_interp():
    # 4 curves x 16 bytes; usable smooth-ish default interpolation.
    one = bytes([20, 20, 107, 107] + [0]*12)
    return one * 4

def pack_bone_key(name, frame, pos, rot):
    return (
        sjis_fixed(name, 15) +
        struct.pack("<I", int(frame)) +
        struct.pack("<3f", *pos) +
        struct.pack("<4f", *rot) +
        curve_interp()
    )

def smooth_wave(phase):
    return math.sin(phase)

def pose_at(t, style, intensity):
    # t is seconds; all angles are radians. Simple generic MMD bone names.
    beat = t * 2.0 * math.pi * 2.0  # 120 BPM = 2 beats/sec
    slow = t * 2.0 * math.pi * 0.5
    section = int(t // 16)  # rough phrase changes every 16 seconds
    chorus = (t % 48 >= 0 and (int(t // 24) % 2 == 1))
    amp = intensity / 100.0
    if style == "アイドル":
        arm_base = 0.30
        step_amp = 0.28
    elif style == "クール":
        arm_base = 0.20
        step_amp = 0.20
    else:
        arm_base = 0.26
        step_amp = 0.24

    # values are euler rotations (x,y,z) in radians
    pose = {}
    def add(name, rx=0, ry=0, rz=0, pos=(0,0,0)):
        pose[name] = (pos, quat_from_euler(rx*amp, ry*amp, rz*amp))

    # Body sway and center translation; all motions are intentionally modest.
    sway = math.sin(beat) * step_amp
    twist = math.sin(beat/2) * 0.12
    if style == "アイドル":
        shoulder = 0.18 + 0.08*math.sin(beat/2)
    elif style == "クール":
        shoulder = 0.10 + 0.06*math.sin(beat/2)
    else:
        shoulder = 0.14 + 0.08*math.sin(beat/2)

    # Chorus moments: larger arm opening; final pose settles at end.
    phrase = int(t // 4)
    phrase_mod = phrase % 8
    lift = [0.10, 0.28, 0.38, 0.18, 0.45, 0.25, 0.52, 0.08][phrase_mod]
    if style == "アイドル":
        wrist_wave = 0.24 * math.sin(beat*0.5)
    elif style == "クール":
        wrist_wave = 0.10 * math.sin(beat*0.5)
    else:
        wrist_wave = 0.18 * math.sin(beat*0.5)

    # Generic body bones
    add("センター", 0.02*math.sin(beat), 0.04*math.sin(beat/2), 0.04*math.sin(beat), (0.12*math.sin(beat/2)*amp, 0.02*(1+math.sin(beat*2))*amp, 0.06*math.cos(beat/2)*amp))
    add("上半身", 0.04*math.sin(beat), twist, sway*0.20)
    add("上半身2", 0.025*math.sin(beat+1), -twist*0.6, -sway*0.12)
    add("下半身", 0.015*math.sin(beat), -twist*0.5, -sway*0.10)
    add("首", 0.035*math.sin(beat/2), 0.04*math.sin(beat), 0.05*math.sin(beat/2))
    add("頭", 0.035*math.sin(beat/2+0.6), 0.07*math.sin(beat/2), 0.04*math.sin(beat+0.4))

    # Arms alternate and open outward on phrase changes.
    right_raise = arm_base + lift + 0.28*math.sin(beat/2)
    left_raise = arm_base + lift + 0.28*math.sin(beat/2 + math.pi)
    if style == "アイドル":
        add("右肩", 0, 0, -0.08*math.sin(beat))
        add("左肩", 0, 0, 0.08*math.sin(beat))
        add("右腕", 0.10*math.sin(beat), 0.08*math.sin(beat/2), -right_raise)
        add("左腕", 0.10*math.sin(beat+math.pi), -0.08*math.sin(beat/2), left_raise)
    elif style == "クール":
        add("右肩", 0, 0, -0.04*math.sin(beat))
        add("左肩", 0, 0, 0.04*math.sin(beat))
        add("右腕", 0.05*math.sin(beat), 0.05*math.sin(beat/2), -right_raise*0.8)
        add("左腕", 0.05*math.sin(beat+math.pi), -0.05*math.sin(beat/2), left_raise*0.8)
    else:
        add("右肩", 0, 0, -0.06*math.sin(beat))
        add("左肩", 0, 0, 0.06*math.sin(beat))
        add("右腕", 0.08*math.sin(beat), 0.06*math.sin(beat/2), -right_raise)
        add("左腕", 0.08*math.sin(beat+math.pi), -0.06*math.sin(beat/2), left_raise)

    add("右ひじ", 0.15 + 0.22*math.sin(beat+0.7), 0, 0.04*math.sin(beat))
    add("左ひじ", 0.15 + 0.22*math.sin(beat+math.pi+0.7), 0, -0.04*math.sin(beat))
    add("右手首", wrist_wave, 0, 0.12*math.sin(beat*0.5))
    add("左手首", -wrist_wave, 0, -0.12*math.sin(beat*0.5))

    # Legs alternate small step motions; not a full foot-IK solver.
    add("右足", step_amp*math.sin(beat), 0.02*math.sin(beat), 0.04*math.sin(beat))
    add("左足", step_amp*math.sin(beat+math.pi), -0.02*math.sin(beat), -0.04*math.sin(beat))
    add("右ひざ", 0.10 + 0.18*max(0, math.sin(beat)), 0, 0)
    add("左ひざ", 0.10 + 0.18*max(0, math.sin(beat+math.pi)), 0, 0)
    add("右足首", 0.04*math.sin(beat+0.5), 0, 0)
    add("左足首", 0.04*math.sin(beat+math.pi+0.5), 0, 0)
    return pose

def create_vmd(path, duration=120, bpm=120, style="アイドル", intensity=70):
    # MMD VMD motion file. Samples at each beat, plus start/end.
    fps = 30
    frames_per_beat = fps * 60.0 / float(bpm)
    total_frames = int(round(duration * fps))
    sample_frames = set([0, total_frames])
    frame = 0.0
    while frame < total_frames:
        sample_frames.add(int(round(frame)))
        frame += frames_per_beat
    # Add every 15 frames for smoother motion even when BPM changes.
    for f in range(0, total_frames + 1, 15):
        sample_frames.add(f)
    sample_frames = sorted(f for f in sample_frames if 0 <= f <= total_frames)

    keys = []
    for f in sample_frames:
        t = f / fps
        pose = pose_at(t, style, intensity)
        for name, (pos, rot) in pose.items():
            # For VMD, positions are model-local; keep center translation subtle.
            keys.append((name, f, pos, rot))
    # VMD parsers generally accept per-bone ordered keys; sort by name then frame.
    keys.sort(key=lambda k: (k[0].encode("shift_jis", errors="replace"), k[1]))

    with open(path, "wb") as fp:
        fp.write(VMD_HEADER.ljust(30, b"\x00"))
        fp.write(sjis_fixed("MMD Original Motion Maker", 20))
        fp.write(struct.pack("<I", len(keys)))
        for name, frame, pos, rot in keys:
            fp.write(pack_bone_key(name, frame, pos, rot))
        fp.write(struct.pack("<I", 0))  # morph count
        fp.write(struct.pack("<I", 0))  # camera count
        fp.write(struct.pack("<I", 0))  # light count
        fp.write(struct.pack("<I", 0))  # self-shadow count
        fp.write(struct.pack("<I", 0))  # IK/display count

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MMD Original Motion Maker")
        self.geometry("560x430")
        self.minsize(520, 400)
        root = ttk.Frame(self, padding=18)
        root.pack(fill="both", expand=True)
        ttk.Label(root, text="MMD Original Motion Maker", font=("Yu Gothic UI", 18, "bold")).pack(anchor="w")
        ttk.Label(root, text="基本的なダンスVMDを自動生成する試作ツール").pack(anchor="w", pady=(0, 14))

        grid = ttk.Frame(root)
        grid.pack(fill="x")
        ttk.Label(grid, text="曲の長さ（秒）").grid(row=0, column=0, sticky="w", pady=6)
        self.duration = tk.IntVar(value=120)
        ttk.Spinbox(grid, from_=4, to=600, textvariable=self.duration, width=12).grid(row=0, column=1, sticky="w", padx=12)
        ttk.Label(grid, text="BPM").grid(row=1, column=0, sticky="w", pady=6)
        self.bpm = tk.IntVar(value=120)
        ttk.Spinbox(grid, from_=40, to=240, textvariable=self.bpm, width=12).grid(row=1, column=1, sticky="w", padx=12)
        ttk.Label(grid, text="ダンスの雰囲気").grid(row=2, column=0, sticky="w", pady=6)
        self.style = tk.StringVar(value="アイドル")
        ttk.Combobox(grid, textvariable=self.style, values=["アイドル", "クール", "ポップ"], state="readonly", width=10).grid(row=2, column=1, sticky="w", padx=12)
        ttk.Label(grid, text="動きの大きさ").grid(row=3, column=0, sticky="w", pady=6)
        self.intensity = tk.IntVar(value=70)
        ttk.Scale(grid, from_=30, to=100, variable=self.intensity, orient="horizontal", length=180).grid(row=3, column=1, sticky="w", padx=12)
        self.intensity_label = ttk.Label(grid, text="70%")
        self.intensity_label.grid(row=3, column=2, sticky="w")
        self.intensity.trace_add("write", self.update_intensity)

        ttk.Separator(root).pack(fill="x", pady=14)
        ttk.Label(root, text="出力：VMD（モーションデータ）").pack(anchor="w")
        ttk.Label(root, text="MMDでモデルに読み込んで再生してください。モデルにないボーンは無視されます。", wraplength=510).pack(anchor="w", pady=(4, 12))
        ttk.Button(root, text="VMDを生成して保存", command=self.save).pack(anchor="w")
        self.status = ttk.Label(root, text="設定して「VMDを生成して保存」を押してください。", foreground="#287a58")
        self.status.pack(anchor="w", pady=(12, 0))

    def update_intensity(self, *_):
        self.intensity_label.config(text=f"{int(self.intensity.get())}%")

    def save(self):
        try:
            duration = int(self.duration.get())
            bpm = int(self.bpm.get())
            intensity = int(float(self.intensity.get()))
            if duration < 1 or not (40 <= bpm <= 240):
                raise ValueError("長さまたはBPMが範囲外です。")
            filename = filedialog.asksaveasfilename(
                title="VMDを保存",
                defaultextension=".vmd",
                filetypes=[("VMD motion", "*.vmd")],
                initialfile="original_dance.vmd")
            if not filename:
                return
            create_vmd(filename, duration, bpm, self.style.get(), intensity)
            size = Path(filename).stat().st_size
            self.status.config(text=f"生成完了：{filename}（{size:,} bytes）")
            messagebox.showinfo("完了", "VMDを生成しました。\nMMDでモデルに読み込んで確認してください。")
        except Exception as e:
            messagebox.showerror("エラー", str(e))

if __name__ == "__main__":
    App().mainloop()
