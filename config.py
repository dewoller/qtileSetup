# coding: utf-8
from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy, Client
from libqtile import layout, bar, widget, hook
from libqtile.dgroups import simple_key_binder
import subprocess, re, sys, os

# TODO:
#  2. multi screen switching
#  3. better hotkeys for dgroups?

# Number of screens on machines I use regularly. I wish there was a good way to
# query this from qtile...

num_screens = os.popen("xrandr | grep '\*' | wc -l").read()


# If we're running in debug mode, it's for development. Make sure the
# hotkeys don't clash, only start one window, etc.
if '-l' in sys.argv:
    hostname = 'xephyr'
    mod = "mod4"

def init_colors():
    return [["#7cfcff", "#00afff"], # cyan gradiant
            ["#323335", "#525355"], # grey gradiant
            ["#040404", "#111113"]] # darker grey gradiant


def init_widgets_defaults():
    
    # global font options
   return dict(
        font = 'FontAwesome',
        fontsize = 18,
        padding = 3,
    )


def init_screens():
    screens = [
            Screen(top = bar.Bar([
                widget.GroupBox(highlight_method="block",urgent_alert_method='text'),
                widget.Notify(foreground="FF0000", fontsize=18, font="Anonymous Pro"),
                #                widget.GoogleCalendar(update_interval=600, foreground='FFFF33', format=' {next_event} '),
                widget.Clock('%Y-%m-%d %a %H:%M %p', foreground='00FF7F'),
                widget.Systray(),
                ], 30,),
                )
            ]
    if num_screens >1:
        screens.append(
                Screen(top = bar.Bar([
                    widget.GroupBox(highlight_method="block",urgent_alert_method='text'),
                    widget.TextBox(text="C"),
                    widget.CPUGraph(samples=600, width=200),
                    widget.TextBox(text="D"),
                    widget.NetGraph(samples=600, width=200, interface="wlan0"),
                    widget.TextBox(text="U"),
                    widget.NetGraph(samples=600, width=200, interface="wlan0", bandwidth_type="up"),
                    ], 30,),
                    )
                )
    if num_screens > 2:
        screens.append(
                Screen(top = bar.Bar([
                    widget.GroupBox(highlight_method="block",urgent_alert_method='text'),
                    #widget.Clipboard(),
                    #widget.Spacer(),
                    #widget.Clipboard(selection="PRIMARY"),
                    widget.YahooWeather(woeid='1103816', foreground='FBCEB1', metric=True, format='Rise:{astronomy_sunrise} Set:{astronomy_sunset}  '),
                    widget.YahooWeather(woeid='1103816', foreground='FFFF33', metric=True, format='{condition_text} {condition_temp}° Hum={atmosphere_humidity}% Wind={wind_speed}{units_speed}@{wind_direction}°'),
                    widget.Volume(),
                    ], 30,),
                    ),
                )
    return(screens)


def app_or_group(group, app):
    """ Go to specified group if it exists. Otherwise, run the specified app.
    When used in conjunction with dgroups to auto-assign apps to specific
    groups, this can be used as a way to go to an app if it is already
    running. """
    def f(qtile):
        try:
            qtile.groupMap[group].cmd_toscreen()
        except KeyError:
            qtile.cmd_spawn(app)
    return f

def init_mouse():
    # Drag floating layouts.
    return [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
    ]

def init_keys_and_groups():
    # Next, we specify group names, and use the group name list to generate an appropriate
    # set of bindings for group switching.

    keys = [
        # Log out; note that this doesn't use mod3: that's intentional in case mod3
        # gets hosed (which happens if you unplug and replug your usb keyboard
        # sometimes, or on ubuntu upgrades). This way you can still log back out
        # and in gracefully.
        Key(["shift", "mod1"], "q",  lazy.shutdown()),
        Key([mod, "shift"], "q",     lazy.spawn("python ~/.config/qtile/config.py && echo 'restart' | qsh")),

        Key([mod], "l",              lazy.layout.toggle_split()),
        Key([mod], "j",              lazy.screen.togglegroup()),
        Key([mod], "Tab",            lazy.layout.next()),
        Key([mod, "shift"], "Tab",  lazy.layout.previous()),
        Key([mod], "space",         lazy.nextlayout()),
        Key([mod], "q",             lazy.to_screen(0)),
        Key([mod], "w",             lazy.to_screen(2)),
        Key([mod], "e",             lazy.to_screen(1)),
        Key([mod, "shift", "control"], "q",    lazy.window.to_screen(0)),
        Key([mod, "shift", "control"], "w",    lazy.window.to_screen(2)),
        Key([mod, "shift", "control"], "e",    lazy.window.to_screen(1)),
        Key([mod, "shift"], "q",    lazy.spawn("~/.config/qtile/scripts/moveToVacant.py %i " % 0)),
        Key([mod, "shift"], "w",    lazy.spawn("~/.config/qtile/scripts/moveToVacant.py %i " % 2)),
        Key([mod, "shift"], "e",    lazy.spawn("~/.config/qtile/scripts/moveToVacant.py %i " % 1)),
        Key([mod, "shift"], "c",    lazy.window.kill()),

        # interact with prompts
        Key([mod], "p",              lazy.spawn("synapse")),
        Key([mod], "b",              lazy.spawn("gnome-control-center bluetooth")),
        Key([mod, "control"], "e",   lazy.spawn("/usr/bin/nautilus")),
        Key([mod], "XF86AudioMute",  lazy.spawn("/usr/bin/pavucontrol")),
        Key([mod], "F7",             lazy.spawn("~/bin/proxy")),
        Key([mod], "F8",             lazy.spawn("setupMonitors")),
        Key([mod], "F1",             lazy.spawn("~/bin/gosleep")),
        Key([mod], "Escape",         lazy.spawn("setxkbmap -option caps:swapescape")),

#-- Screenshots 
        Key([], "Print",             lazy.spawn("shutter")),
        Key([mod], "Print",          lazy.spawn("scrot '/tmp/screenshot-%Y%m%d%H%M%S-$wx$h.png'")),
 
        # Control the notify widget
        Key([mod], "y",              lazy.widget['notify'].toggle()),
        Key([mod, "mod1"], "y",         lazy.widget['notify'].prev()),
        Key([mod, "mod1"], "u",         lazy.widget['notify'].next()),

        Key([mod, "control"], "leftarrow",         lazy.layout.decrease_ratio()),
        Key([mod, "control"], "rightarrow",         lazy.layout.increase_ratio()),

        # start specific apps
        Key([mod, "shift"], "Return", lazy.spawn("gnome-terminal")),
        Key([mod], "Return",          lazy.layout.rotate()),

            # Change the volume if our keyboard has keys
            Key(
                [], "XF86AudioRaiseVolume",
                lazy.spawn("amixer -c 0 -q set Master 2dB+")
                ),
            Key(
                [], "XF86AudioLowerVolume",
                lazy.spawn("amixer -c 0 -q set Master 2dB-")
                ),
            Key(
                [], "XF86AudioMute",
                lazy.spawn("amixer -q set Master toggle")
                ),

            # also allow changing volume the old fashioned way
            Key([mod], "asterisk", lazy.spawn("amixer -q set Master 2dB+")),
            Key([mod], "minus", lazy.spawn("amixer -q set Master 2dB-")),

            ]

    groups = []

    for i in "1234567689":
        if i == '1':
            gn=''
            groups.append(
                    Group(gn, layout='stack', persist=False, init=True, 
                        spawn='gnome-terminal',
                        ))
        elif i == '2':
            gn=''
            groups.append(
                    Group(gn, persist=False, layout='max',
                        spawn='thunderbird',
                        matches=[Match(wm_class=['Thunderbird'])])
                    )
        elif i == '3':
            gn=''
            groups.append(
                    Group(gn, persist=False, layout='max', init=True,
                        spawn='/usr/local/bin/xsc',
                        matches=[Match(wm_class=['google-chrome', 'Google-chrome', 'Chromium-browser'])]),
                    )
        elif i == '4':
            gn='' 
            groups.append(
                    Group(gn, layout='max', persist=False, init=True,
                        spawn='firefox',
                        matches=[Match(wm_class=['Firefox', 'TorBrowser'])]),
                    )
        else:
            gn=i
            groups.append(Group(i, layout='treetab'))

        keys.append(
            Key([mod], i, lazy.group[gn].toscreen())
        )
        keys.append(
            Key([mod, "shift"], i, lazy.window.togroup(gn))
        )

    gn=''
    groups.append(
            Group(gn, layout='treetab', persist=False, init=True,
                spawn='/usr/bin/pavucontrol',
                matches=[Match(wm_class=['Pavucontrol', 'Banshee', 'Skype'])]),
            )
    keys.append(
        Key([mod], 'KP_Add', lazy.group[gn].toscreen())
    )
    keys.append(
        Key([mod, "shift"],  'KP_Add', lazy.window.togroup(gn))
    )


    gn=''
    groups.append(
            Group(gn, layout='treetab', persist=False, init=True,
                spawn='/usr/bin/keepassx',
                matches=[Match(wm_class=['Keepassx'])]),
            )
    keys.append(
        Key([mod], 'KP_Enter', lazy.group[gn].toscreen())
    )
    keys.append(
        Key([mod, "shift"],  'KP_Enter', lazy.window.togroup(gn))
    )
    return((keys, groups))




def init_layouts(): 
    return  [
        layout.Max(),
        layout.Stack(stacks=2, **border_args),
        layout.Tile(ratio=0.5, border_focus="#00afff"),
        layout.Zoomy(), 
        layout.Matrix(), 
        layout.TreeTab(),
        layout.MonadTall(), 
        layout.RatioTile(),
        ]


def init_floating_layout():
    # Automatically float these types. This overrides the default behavior (which
    # is to also float utility types), but the default behavior breaks our fancy
    # gimp slice layout specified later on.
    return layout.Floating(auto_float_types=[
    "notification",
    "toolbar",
    "splash",
    "dialog",
    ])

def is_running(process):
    s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(process, x):
            return True
    return False

def execute_once(process):
    if not is_running(process):
        return subprocess.Popen(process.split())

# start the applications at Qtile startup
@hook.subscribe.startup
def startup():
#    execute_once("parcellite")
    execute_once("nm-applet")
    execute_once("dropboxd")
#    execute_once("feh --bg-scale ~/Pictures/wallpapers.jpg")

@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    qtile.cmd_restart()



float_windows = set([
    "feh",
    "x11-ssh-askpass",
    "gimp-2.8",
    "synapse",
])


def should_be_floating(w):
    wm_class = w.get_wm_class()
    if isinstance(wm_class, tuple):
        for cls in wm_class:
            if cls.lower() in float_windows:
                return True
    else:
        if wm_class.lower() in float_windows:
            return True
    return w.get_wm_type() == 'dialog' or bool(w.get_wm_transient_for())


@hook.subscribe.client_new
def dialogs(window):
    if should_be_floating(window.window):
        window.floating = True



if __name__ in ["config", "__main__"]:
    mod = "mod4"
    lock = "i3lock -d -c000000"
    term = "gnome-terminal"


    border_args = dict(
        border_width=5,
    )

    colors = init_colors()
    (keys,groups) = init_keys_and_groups()
    mouse = init_mouse()
    floating_layout = init_floating_layout()
    layouts = init_layouts()
    screens = init_screens()
    widget_defaults = init_widgets_defaults()


# vim: tabstop=4 shiftwidth=4 expandtab
