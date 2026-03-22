# Вы можете расположить сценарий своей игры в этом файле.

label splashscreen:
    python:
        music_vol = _preferences.volumes.get("music", 0.0)
        sfx_vol = _preferences.volumes.get("sfx", 0.0)
        voice_vol = _preferences.volumes.get("voice", 0.0)

        # Восстанавливаем громкость, если все микшеры оказались выключены.
        if music_vol <= 0.0 and sfx_vol <= 0.0 and voice_vol <= 0.0:
            _preferences.volumes["music"] = 0.7
            _preferences.volumes["sfx"] = 0.8
            _preferences.volumes["voice"] = 1.0

    scene black
    pause 0.5
    $ renpy.movie_cutscene("video/di.webm")
    return


# Обработчик загрузки сохранения
label after_load:
    $ restore_player_music()
    return
   

screen start_game_icon():
    default bag_hover = False
    
    text _("что мне делать сейчас?"):
        xalign 0.5
        yalign 0.12
        size 52
        color "#ffffff"
        outlines [(2, "#000000", 0, 0)]

    imagebutton:
        idle "images/obj/obj bag.png"
        hover "images/obj/obj bag hover.png"
        focus_mask True
        xpos 1250
        ypos 490
        hovered SetScreenVariable("bag_hover", True)
        unhovered SetScreenVariable("bag_hover", False)
        action Return()

    if bag_hover:
        text _("поиграть? а потом и собрать сумку"):
            xalign 0.5
            ypos 430
            size 44
            color "#ffe9a8"
            outlines [(2, "#000000", 0, 0)]

# Игра начинается здесь:

# флаг, чтобы меню с мини‑игрой показывалось только один раз
default have_played_nes = False

label start:
    $ progress = 1
    $ lock_music_change()
    $ story_stop_music(fadeout=1.0)
    $ story_play_music(audio.mystic, fadein=3.0, volume=0.35)
    scene bg night
    $ persistent.cg_1 = True
    show gg backa:
        xalign 0.4
        yalign 0.1
    with eyes_blink

    gg backa "Эмм... Где я? Что это за место?"

    play sound wings
    scene bg black with eyes_blink
    n "Вжух Вжух"
    scene bg 1
    $ persistent.cg_2 = True
    gg scared baga "ЧТО ЗА ЧЁРТ?!"
    an "Ты должен сделать выбор, Лиам."
    gg "Кто ты?!"
    stop sound fadeout 2.0
    scene bg black with eyes_blink
    n "Толчок"

    scene bg falling
    $ persistent.cg_3 = True
    gg scared baga "AAAAAAAA!!!"

    scene bg black with eyes_blink
    play sound alarm
    n "Звук будильника"
    scene bg room with fade
    stop sound 
    play audio click
    gg emberasseda "Фуф... Это был всего лишь сон. Но он был таким реалистичным..."
    $ story_stop_music(fadeout=2.0)
    $ unlock_music_change()
    gg "Не стоило кушать лапшу перед сном"
    gg "Ладно уж. Пора вставать"
    
    scene bg room table

    call screen start_game_icon
    $ persistent.cg_4 = True
    $ persistent.cg_5 = True
    # call the minigame menu; when it returns the story continues below
    call nes_start from _call_nes_start

    gg "Пора в школу."
    $ story_play_music(audio.normal, fadein=3.0, volume=0.35)
    jump street

label play_hiddenfolks:
    # настройка (копия из HiddenFolks_test)
    $ hf_init("bg room table", 5,
        ("beer", 1013, 705, _("Мишка")),
        ("elf", 111, 560, _("Эльф")),
        ("flowers", 700, 615, _("Букет")),
        ("skull", 1813, 161, _("Череп")),
        ("sprite", 355, 240, _("Дотти-чан")),
        mouse=True,
        inventory=False,
        hint=True,
        hover=brightness(.05),
        w=200,
        h=200
    )

    # показываем фон и игровое поле
    $ hf_bg()
    with dissolve

    centered "{size=+24}Нужно собрать все предметы за 5 секунд.\nНачинаем!"

    # запускаем саму мини‑игру
    $ hf_start()

    # пауза перед выводом результатов
    $ renpy.pause(1, hard=True)

    if hf_return == 0:
        centered "{size=+24}Ура! Все предметы собраны!"
    else:
        centered "{size=+24}GAME OVER\nНе собрано предметов: [hf_return]."

    $ hf_hide()
    with dissolve
    return

label nes_start:
    # не показывать меню повторно
    if have_played_nes:
        return

    $ run_hiddenfolks_after_nes = False

    menu:
        with dissolve

        "{size=22}!!!Игру нельзя перезапустить. Нельзя загрузить другую игру, если одна уже запущена."
        "{size=22}!!!Нельзя сменить игру. Q – выход."

        "{size=22}Z- прыжок/стрелять"

        "Марио":
            call screen NES("Super Mario Bros 1 rus")
            $ run_hiddenfolks_after_nes = True

        "Танки":
            call screen NES("Battle City")
            $ run_hiddenfolks_after_nes = True

        "Марио ТВ":
            call screen NES("Super Mario Bros 1 rus", False)
            $ run_hiddenfolks_after_nes = True

        "Выход":
            $ run_hiddenfolks_after_nes = True

    if run_hiddenfolks_after_nes:
        call play_hiddenfolks from _call_play_hiddenfolks

    # запомнить, что меню уже использовано
    $ have_played_nes = True

    return

label street:
    
    scene bg street with moveinright
    
    show gg static baga:
        xalign 0.1
        yalign 0.1
    with fade    
    with Pause(0.5) 
    gg "Наверное стоит подготовиться к экзамену"
    gg opening baga "Ну-ка"

    scene bg fe
    play sound wings
    gg shocked baga"....чего? перья?"
    scene bg black with eyes_blink
    scene bg first meet
    $ persistent.cg_meet = True
    with eyes_blink
    pause 1.0
    scene bg black with eyes_blink
    scene bg roof
    $ persistent.cg_6 = True
    pause 1.0
    show an roofa:
        xpos 0.65
        ypos 0.3
    with fade
    stop sound fadeout 1.0
    pause 0.5
    gg scared baga"Что за чёрт..."
    an "Не чёрт, а Ангел"
    n "Ангел плавно встал"
    show an roof:
        xalign 0.9
        yalign 0.001
    an angrya "Ты выглядишь разочаровывающе."
    
    show gg emberasseda:
        xpos 0.1
        ypos 1
    gg """Эмм...
    
    Я тоже рад встрече?"""

    n "..."

    gg """Ну так... Эмм...
    
    У вас какое-то собрание косплейщиков?"""

    an """ Нет. Я ангел. Не люблю повторять."""
    gg """Ага, конечно. Слушай, чувак, я так понимаю это какой-то пранк и т.п.?"""
    n "Вздыхает. Раскрывает одежду. Появляются крылья."
    scene bg angel with dissolve
    $ persistent.cg_angel = True
    pause 1.0
    gg shocked baga "..."
    pause 1.0
    gg  """Ты… ты действительно не придумывал…"""
    pause 1.0

    scene bg roof with fade

    show an angrya:
        xalign 0.9
        yalign 0.001
        
    show gg emberasseda:
        xpos 0.1
        ypos 1

    an """Повторяю в последний раз. Я ангел. Зовут Рафаэль.
    """
    gg "Ага… а я… я Лиам."
    an smirka "Знаю"
    gg "Что?"
    an "Ты единственный кто может меня видеть."
    an smilea "Это не случайно. Ты избран, поздравляю."
    gg "Ого. Ну, круто. А приз — хотя бы бесплатный обед в столовой?"
    an angrya "…"
    play sound "sounds/meme_spiderman.mp3" volume 0.5
    an angrya "Ты будешь решать судьбы людей"
    gg argue baga """Ч-чего?!
    А нельзя сразу отказаться?"""
    stop sound fadeout 1.0
    an "Нет."
    jump school

label school:
    window hide
    nvl clear
    scene school tree
    with fade
    pause 0.5
    with dissolve
    sc "Он ходит с ним на уроки."
    scene bg classroom with dissolve
    pause 1.0
    $ persistent.cg_7 = True
    sc "Во время занятий Рафаэль сидит у окна, на полу — да вообще на любой плоской поверхности — и наблюдает."
    scene school pink with Pause(0.5)
    
    sc "В раздевалке он без стеснения разглядывает парней."
    scene bg f fire with dissolve
    $ persistent.cg_8 = True
    pause 1.0
    nvl clear
    sc "На улице Лиаму пришлось 'мягко' объяснить ему концепцию личного пространства."
    nvl hide
    pause 1.0

    scene bg hill with fade
    show an hilla:
        xpos 1470
        ypos 350
    $ persistent.cg_hill = True

    show gg hilla:
        xpos 1595
        ypos 690

    pause 1.5
    gg "Слушай, а как это всё работает? Что это за судьбы?"
    an """У каждого человека есть своя судьба. Свой путь. 

    Но постепенно тьма поглощает человека, и эта судьба попросту ломается. 

    Ангелы всегда стараются поддержать эту душу, но бывают моменты, когда это невозможно. 

    Вот почему я тут. Я не могу вмешиваться в их жизни, но ты можешь. 
    
    Ты должен помочь, Лиам."""
    
    jump zephir

label zephir:
    pause 0.5
    scene school tree with fade
    pause 0.5
    
    show an smilea:
        xpos 1200
        ypos 1
    with dissolve

    show gg gripping baga:
        xpos -100
        ypos 1
    with dissolve

    n """Новый день

    Лиам опять шёл по школе что-то обсуждая с Рафаэлем, когда вдруг послышался голос"""
    $ persistent.story_stage = 1
    ld "Лиам?"

    n "Они оборачиваются и видят Зефира-лучшего друга Лиама. Парень приятной мягкой внешности с улыбкой."
    
    show ld happya:
        xpos 500
        ypos 1
    with moveinleft
    pause 0.5
    gg smirking fold baga"Зефиииир. Привет, братан."
    ld "Дароваа~"
    n "Рафаэль смотрит на него с подозрением."
    window hide
    nvl clear
    sc """
    Лиам решил провести день с Зефиром, и оно проходит действительно хорошо. 
    Они болтают, смеются, гуляют после школы."""
    nvl clear
    scene bg room night
    sc "Уставший Лиам возвращается домой и почти сразу засыпает."
    $ lock_music_change()
    $ story_stop_music(fadeout=2.0)
    sc "Но ночью ему снится сон."
    $ story_play_music("music/firstdream.mp3", fadein=1.0)
    scene bg black with eyes_blink
    pause 1.0
    n "Темнота. Душно."
    pause 0.5
    scene bg zephir cry 1 with eyes_blink
    $ persistent.cg_9 = True
    gg shocked baga "Зефир?"
    scene bg zephir cry 2 with dissolve
    pause 1.5
    play sound "sounds/footsteps.mp3" fadein 1.0 volume 0.5
    ld scareda "Помоги. Я… я боюсь.."
    
    pause 1.0
    scene bg zephir cry 3 with dissolve
    $ persistent.cg_10 = True
    pause 1.0
    stop sound 
    scene bg room night with fade
    $ persistent.cg_roomnight = True
    n "Лиам резко просыпается, тяжело дыша."
    show gg static baga:
        xpos 100
        ypos 1
    with dissolve

    n "Рядом сидит Рафаэль."
    show an sittinga:
        xpos 1000
        ypos 1
    with dissolve

    an "Вижу, утро у тебя началось с бодрячком."
    gg "Ага. Конечно."
    an "Видел Зефира?"
    gg shocked baga "Откуда ты…?"
    an "Начинается…"
    gg argue baga """Харе говорить загадками, как какой-то загадочный мастер-кукловод.
    
    Причём тут Зефир? Я ничего не понимаю."""
    an "Он первая жертва"
    gg shocked baga '''….
    
    Зефир? Как? Нет… но….
    '''
    $ unlock_music_change()

    $ story_stop_music(fadeout=2.0)
    an "Постепенно ты всё узнаешь"
    
    scene school tree with dissolve
    
    $ story_play_music("music/Crescent-Moon(chosic.com).mp3", fadein=2.0)
    window hide
    nvl clear
    sc  '''В школе.

    В тот день Лиам начинает внимательнее наблюдать за Зефиром. 

    Каждая улыбка.

    Каждое вздрагивание.

    Каждый Шёпот.

    Каждая Дрожь в голосе. 
    '''
    nvl clear
    sc '''Он замечает одну странную закономерность.

    Зефир становится тише, когда рядом находится его дядя.
    Со стороны это не выглядит чем-то необычным для семейных отношений…
    но всё равно чувствуется —
    
    что-то не так.
    '''
    n "После урока."
    show gg static baga:
        xpos 900
        ypos 1
    with dissolve

    show ld statica:
        xpos 200
        ypos 1
    with dissolve
    gg emberasseda "Зефир"
    ld "Да?"
    gg "Я… не особо умею подбирать слова, но…"
    gg "Ты знаешь, что я твой друг. И ты всегда можешь рассказать мне всё."
    ld oa"Ты чего это вдруг?"
    gg "Просто. Хочу, чтобы ты знал — ты можешь доверять мне."
    n "Зефир колеблется."
    ld shya "Ли… Лиам… я…"
    n """Но вдруг на его плечо ложится рука.
    
    Это его дядя."""
    show un statica:
        xpos -200
        ypos 1
    with fade
    n "Зефир сразу напрягается и опускает голову."
    show ld cry 
    un "Ну что, ребята? О чём болтаете?"
    ld statica"Ничего, дядя."
    n "Дядя на секунду задерживает на нём непроницаемый взгляд, а потом снова улыбается."
    un "Тогда пойдём домой."
    un "Спасибо что присматриваешь за моим пацаном, Лиам"
    un "Передай привет своим родным"
    jump home_1

label home_1:
    scene bg room1
    n "Дома."
    show gg argue baga:
        xpos 200
        ypos 1
    with dissolve
    
    show an sidea:
        xpos 1000
        ypos 1
    with dissolve
    gg "Что это было??"
    an "ты наконец начал замечать."
    gg "Что именно? Давай опять без загадок"
    an "Ну если не хочешь мои «загадки» то сам со временем поймёшь."
    gg "Ты типа обиделся?"
    pause 1.0
    gg emberasseda "…."
    gg emberasseda"Ну прости."
    n "Рафаэль тихо усмехается."
    an smirka"Хех, какой же ты наивный."
    n "Больше Рафаэль ничего не сказал за тот день. "

    scene bg room night with fade
    n "Ночь."
    window hide
    nvl clear
    sc """Лиам долго не может уснуть.
    В итоге среди ночи он выпивает снотворное и ложится в кровать.
    Рафаэль всё это время наблюдает за ним.
    Он слегка взмахивает рукой.
    В воздухе появляются тихие искры света."""
    $ lock_music_change()
    $ story_stop_music(fadeout=1.0)
    sc "После этого он просто ждёт."

    $ progress = 2

    scene bg black with fade
    
    $ story_play_music("music/Demented-Nightmare-MP3(chosic.com).mp3", fadein=2.0, volume=0.5)
    n """Сон Лиама

    Опять душно.

    Но на этот раз в темноте постепенно появляется свет…
    """
    pause 1.0
    scene bg zep1 with fade
    pause 1.5
    _("Женский голос") "Знаешь, Лиам, почему машина никогда не спорит с папой?"
    n "Почему?"
    _("Женский голос") "Потому что папа всё равно всегда “рулит”"
    n "смех"
    window hide
    pause 1.5
    _("Мужской голос") "Ради таких моментов, я готов даже быть водителем всю жизнь"
    window hide
    pause 1.5
    scene bg black with eyes_blink
    pause 1.0
    scene bg zep2 with dissolve
    pause 2.5
    play sound "sounds/ambulance.mp3"
    scene bg black with eyes_blink
    pause 1.0
    scene bg zep3 with dissolve
    pause 0.5
    stop sound fadeout 1.0
    scene bg black with eyes_blink
    play sound "sounds/hosp.mp3" volume 1.5
    play audio "sounds/Heart-monitor-sound.mp3" volume 0.1 loop
    pause 1.0
    scene bg zep4 with dissolve
    pause 1.0
    show s1a:
        xpos 1000
        ypos 1
    with dissolve
    s1a "Эй, ты очнулся?"
    s1a "Не двигайся, ладно? Всё хорошо. Ты в больнице."
    n "А где мама? Папа?"
    s1a "..."
    pause 0.5
    s1a "Прости, парень. Они... они не выжили."
    pause 1.5
    n "А я... когда поеду домой?"
    n "*Следователь переглядывается с врачом, тяжело вздыхает и медленно садится на край стула.*"
    s1a "Послушай, "
    s1a "Пока… пока тебе не найдут опекуна, ты не сможешь вернуться домой."
    n "Что это значит? "
    s1a "Это значит, что ты поживёшь немного в одном доме, где живут дети, у которых тоже нет мамы и папы"
    s1a "Это называется приют. Там за тобой будут смотреть взрослые, ты будешь ходить в школу, а мы будем искать для тебя семью."
    n "*Слёзы*"
    window hide
    pause 1.5
    scene bg black with eyes_blink
    scene bg kinderg with fade
    n "*дети играются вокруг*"
    show s2sa:
        xpos 1200
        ypos 250
    s2sa "У новенького тоже нет мамы и папы?"
    hide s2sa
    show s2a:
        xpos 1200
        ypos 250
    s2a "Ой Ой. Тише. Тише. Так нельзя говорить. Мальчику сейчас итак грустно"
    scene bg kinderg with fade
    pause 1.5
    show s1a:
        xpos 1000
        ypos 1
    with dissolve
    s1a "Эй, малыш, как ты?"
    s1a "У нас хорошая новость"
    s1a "Мы нашли тебе опекуна!"
    s1a "И этот опекун твой родной дядя!"
    s1a ""
    s1a ""
    s1a ""
    
    

    
