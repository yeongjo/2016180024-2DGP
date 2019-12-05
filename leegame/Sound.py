import pico2d as pc


class Sound:
    sounds = {}

    @classmethod
    def load(cls, path, volume):
        if path not in cls.sounds:
            sound = pc.load_wav(path)
            sound.set_volume(volume)
            cls.sounds[path] = sound
        return cls.sounds[path]
