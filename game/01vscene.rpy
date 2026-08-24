#
#
# Creator-defined statement:
#        vscene filename [fullscreen]
# Starts a new scene, showing the image or video in the given file
#
#

transform master:
    align (720,405)
    anchor (0.5,0.5)
    maxsize (1440,810)

transform big_master:
    align (960,540)
    anchor (0.5,0.5)
    maxsize (1920,1080)

#image big_movie = Movie(channel='movie', size=(1920,1080), align=(0.5,0.5))
image big_movie = Movie(channel='movie', size=(1440,810), align=(720,405))
image small_movie = Movie(channel='movie', size=(500,500), yalign=0.4)

python early:
    class SceneRuntimeState(object):
        def __init__(self):
            self.picture = ""
            self.text = ""
            self.location_text = ""
            self.movie = False
            self.fullscreen = False
            self.controller_from_timer = False


default scene_runtime = SceneRuntimeState()

python early:

    VSCENE_MOVIE_EXTENSIONS = (".webm", ".mkv", ".ogv", ".ogg", ".avi", ".mp4", ".m4v", ".mpg", ".mpeg")

    def vscene_parse(lex):
        expression = lex.simple_expression()
        fullscreen = lex.keyword("fullscreen")
        return (expression, fullscreen)


    def vscene_execute(obj):
        expression, fullscreen = obj

        renpy.scene()
        # Keep full viewport consistently black around the media viewport.
        renpy.show("_layout_black_bg", what=renpy.easy.displayable("#000"), layer="master")

        if scene_runtime.fullscreen:
            renpy.hide_screen("controller")
            #renpy.show_screen("status")
        if scene_runtime.movie:
            renpy.music.stop("movie")

        if (not expression):
            scene_runtime.picture = ""
            return

        filename = renpy.python.py_eval(expression)
        scene_runtime.picture = str(filename or "")
        movie = str(filename or "").lower().endswith(VSCENE_MOVIE_EXTENSIONS)

        if (movie):
            renpy.music.set_volume(0.0 if preferences.mute['music'] else preferences.volumes['music'], channel="movie")
            if (fullscreen):
                #renpy.show("big_movie", at_list=[big_master], layer='master')
                renpy.show("big_movie", at_list=[master], layer='master')
                renpy.music.play(filename, channel="movie", loop=False)
                #renpy.hide_screen("status")
                renpy.show_screen("controller")
            else:
                renpy.show("small_movie", at_list=[master], layer='master')
                renpy.music.play(filename, channel="movie", loop=True)
        else:
            image = renpy.easy.displayable(filename)
            renpy.show(filename, at_list=[master], layer='master', what=image)

        scene_runtime.movie = movie
        scene_runtime.fullscreen = fullscreen


    def vscene_predict(obj):
        expression, fullscreen = obj
        filename = renpy.python.py_eval(expression)
        if str(filename or "").lower().endswith(VSCENE_MOVIE_EXTENSIONS):
            return []
        image = renpy.easy.displayable(filename)
        return [image]


    def vscene_lint(obj):
        expression, fullscreen = obj
        source = str(expression or "").strip()
        if len(source) < 2 or source[0] not in ("'", '"') or source[-1] != source[0]:
            return
        try:
            filename = renpy.python.py_eval(source)
            if filename and not renpy.loadable(filename):
                renpy.error("Unable to find %s" % filename)
        except Exception:
            return


    renpy.register_statement("vscene", parse=vscene_parse,
                            execute=vscene_execute,
                            predict=vscene_predict,
                            lint=vscene_lint)


screen controller():
    bar adjustment vcAdjustor:
        yalign 1.0
    on "show" action Function(vcUpdateBar)
    timer 0.1 action Function(vcUpdateBar) repeat True

init python:
    def vcSetPosition(val):
        if scene_runtime.controller_from_timer:
            scene_runtime.controller_from_timer = False
            return
        duration = renpy.music.get_duration("movie")
        filename = renpy.music.get_playing("movie")
        if (filename):
            filename = re.sub(r"<.*?>", "", filename)
            filename = "<from %d>%s" % (duration*val//1000, filename)
            renpy.play(filename, channel="movie")

    def vcUpdateBar():
        duration = renpy.music.get_duration("movie")
        duration = duration if duration else 1.0
        pos = renpy.music.get_pos("movie")
        pos = pos if pos else 0.0
        scene_runtime.controller_from_timer = True
        vcAdjustor.change(1000*pos//duration)
        return

    vcAdjustor = ui.adjustment(range=1000, value=0, adjustable=True,
                                                    changed=vcSetPosition)
