import pygame
import numpy as np


SAMPLE_RATE = 44100


class SoundError(Exception):
    pass


def _make_sound(samples):
    samples = np.clip(samples * 0.3, -32767, 32767).astype(np.int16)
    stereo = np.zeros((len(samples), 2), dtype=np.int16)
    stereo[:, 0] = samples
    stereo[:, 1] = samples
    return pygame.sndarray.make_sound(stereo)


def _sine(freq, duration, sr=SAMPLE_RATE):
    t = np.linspace(0, duration, int(sr * duration), False)
    return np.sin(2 * np.pi * freq * t)


def _envelope(samples, attack=0.005, decay=0.1):
    n = len(samples)
    a = int(n * attack / (attack + decay + 0.001))
    d = int(n * decay / (attack + decay + 0.001))
    env = np.ones(n)
    env[:a] = np.linspace(0, 1, a)
    env[a:a+d] = np.linspace(1, 0, d)
    env[a+d:] = 0
    return samples * env


def _noise(duration, sr=SAMPLE_RATE):
    n = int(sr * duration)
    return np.random.uniform(-1, 1, n)


def _click():
    t = np.linspace(0, 0.02, int(SAMPLE_RATE * 0.02), False)
    s = np.sin(2 * np.pi * 800 * t) * (1 - t / 0.02)
    return _make_sound(s)


def _blip(freq=600, duration=0.08):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    s = np.sin(2 * np.pi * freq * t) * np.exp(-t * 30)
    return _make_sound(s)


class SoundManager:
    def __init__(self):
        try:
            pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2)
            self.enabled = True
        except Exception:
            self.enabled = False
        self.sounds = {}
        self.music_playing = False
        if self.enabled:
            self._generate_all()

    def _generate_all(self):
        self.sounds["paddle_hit"] = _blip(440, 0.1)
        self.sounds["brick_hit"] = _blip(660, 0.06)
        self.sounds["brick_break"] = self._gen_brick_break()
        self.sounds["powerup"] = self._gen_powerup()
        self.sounds["powerup_spawn"] = _blip(1200, 0.15)
        self.sounds["laser"] = self._gen_laser()
        self.sounds["ball_lost"] = self._gen_ball_lost()
        self.sounds["level_up"] = self._gen_level_up()
        self.sounds["game_over"] = self._gen_game_over()
        self.sounds["menu_move"] = _click()
        self.sounds["menu_select"] = self._gen_menu_select()
        self.sounds["combo"] = self._gen_combo()

    def _gen_brick_break(self):
        n = int(SAMPLE_RATE * 0.15)
        noise = np.random.uniform(-1, 1, n)
        tone = np.sin(2 * np.pi * 300 * np.linspace(0, 0.15, n))
        s = (noise * 0.5 + tone * 0.5) * np.exp(-np.linspace(0, 0.15, n) * 25)
        return _make_sound(s)

    def _gen_powerup(self):
        t = np.linspace(0, 0.3, int(SAMPLE_RATE * 0.3), False)
        freq = 400 + 1200 * (t / 0.3)
        s = np.sin(2 * np.pi * freq * t) * np.exp(-t * 8)
        return _make_sound(s)

    def _gen_laser(self):
        n = int(SAMPLE_RATE * 0.12)
        t = np.linspace(0, 0.12, n, False)
        freq = 2000 - 1500 * (t / 0.12)
        s = np.sin(2 * np.pi * freq * t) * (1 - t / 0.12)
        s += np.random.uniform(-0.3, 0.3, n) * (1 - t / 0.12)
        return _make_sound(s)

    def _gen_ball_lost(self):
        t = np.linspace(0, 0.4, int(SAMPLE_RATE * 0.4), False)
        freq = 500 - 400 * (t / 0.4)
        s = np.sin(2 * np.pi * freq * t) * np.exp(-t * 5)
        return _make_sound(s)

    def _gen_level_up(self):
        t = np.linspace(0, 0.6, int(SAMPLE_RATE * 0.6), False)
        notes = [523, 659, 784, 1047]
        s = np.zeros_like(t)
        seg = len(t) // 4
        for i, f in enumerate(notes):
            st = i * seg
            en = (i + 1) * seg
            seg_t = t[st:en] - t[st]
            s[st:en] = np.sin(2 * np.pi * f * seg_t) * np.exp(-seg_t * 5)
        return _make_sound(s)

    def _gen_game_over(self):
        t = np.linspace(0, 0.8, int(SAMPLE_RATE * 0.8), False)
        freq = 400 - 300 * (t / 0.8)
        s = np.sin(2 * np.pi * freq * t) * np.exp(-t * 3)
        s += np.random.uniform(-0.2, 0.2, len(t)) * np.exp(-t * 3)
        return _make_sound(s)

    def _gen_menu_select(self):
        t = np.linspace(0, 0.2, int(SAMPLE_RATE * 0.2), False)
        s = np.sin(2 * np.pi * 800 * t) * np.exp(-t * 15)
        s += np.sin(2 * np.pi * 1200 * t) * np.exp(-t * 12) * 0.5
        return _make_sound(s)

    def _gen_combo(self):
        t = np.linspace(0, 0.3, int(SAMPLE_RATE * 0.3), False)
        freq = 800 + 600 * (t / 0.3)
        s = np.sin(2 * np.pi * freq * t) * np.exp(-t * 6)
        s += np.sin(2 * np.pi * freq * 1.5 * t) * np.exp(-t * 8) * 0.4
        return _make_sound(s)

    def play(self, name):
        if not self.enabled:
            return
        if name in self.sounds:
            self.sounds[name].play()

    def set_volume(self, vol):
        if not self.enabled:
            return
        for s in self.sounds.values():
            s.set_volume(vol)
