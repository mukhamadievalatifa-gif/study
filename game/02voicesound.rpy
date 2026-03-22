init python:
    # Dedicated channel so typewriter beeps don't cut off "sound" effects (e.g. alarm).
    try:
        renpy.music.register_channel("typewriter", "voice", loop=False, tight=True)
    except Exception:
        pass

    typewriter_beep_count = 5

    def typewriter_count_callback(text, **kwargs):
        # Fixed beep count per line.
        renpy.store.typewriter_beep_count = 5

    # Typewriter sound callback for dialogue text (single beep per line).
    def typewriter_sound_callback(event, interact=True, name=None, **kwargs):
        if event != "show":
            return

        if renpy.is_skipping() or renpy.in_rollback():
            return

        char = kwargs.get("who")
        char_id = kwargs.get("cb_name") or name or kwargs.get("name")
        if not char_id and char is not None:
            if hasattr(char, "image"):
                char_id = char.image
            elif hasattr(char, "name"):
                char_id = char.name
            else:
                char_id = str(char)
        if not char_id:
            char_id = getattr(renpy.store, "speaking_char", None) or getattr(renpy.store, "current_speaker", None)

        if char_id == "gg":
            sound = "sounds/gg.mp3"
        elif char_id == "d":
            sound = "sounds/d.mp3"
        elif char_id == "ld":
            sound = "sounds/ld.mp3"
        elif char_id == "x":
            sound = "sounds/X.mp3"
        else:
            sound = "sounds/X.mp3"

        channel = "typewriter"
        renpy.music.play(sound, channel=channel, loop=False)
        beep_count = getattr(renpy.store, "typewriter_beep_count", 4)
        for _i in range(beep_count - 1):
            renpy.music.queue(sound, channel=channel)
        renpy.store.typewriter_beep_count = 4

    def combined_callback(event, interact=True, name=None, **kwargs):
        try:
            name_callback(event, interact=interact, name=name, **kwargs)
        except Exception:
            pass
        typewriter_sound_callback(event, interact=interact, name=name, **kwargs)
