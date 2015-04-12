# coding: utf-8
from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
import os
import pynotify
from pprint import pformat

num_screens = int(os.popen("xrandr | grep '\*' | wc -l").read().rstrip("\n"))
network="wlan0"
nscreen_left = 0
nscreen_middle = 0
nscreen_right = 0
if num_screens == 2:
    #uni
    nscreen_left = 1
    nscreen_middle = 0
    nscreen_right = 0
    network="eth0"
elif num_screens == 3:
    nscreen_left = 0
    nscreen_middle = 1
    nscreen_right = 2
    network="wlan0"


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
                widget.Notify(foreground="FF0000", fontsize=18, font="Ubuntu"),
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
                    widget.NetGraph(samples=600, width=200, interface=network),
                    widget.TextBox(text="U"),
                    widget.NetGraph(samples=600, width=200, interface=network, bandwidth_type="up"),
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
        Key(["control", "shift"], "q",     lazy.spawn("python ~/.config/qtile/config.py && echo 'restart' | qsh")),

        Key([mod], "m",              lazy.layout.maximize()),
        Key([mod], "n",              lazy.layout.normalize()),
        Key([mod], "l",              lazy.layout.toggle_split()),
        Key([mod], "j",              lazy.screen.togglegroup()),
        Key([mod], "Tab",            lazy.layout.next()),
        Key([mod, "shift"], "Tab",  lazy.layout.previous()),
        Key([mod], "space",         lazy.nextlayout()),
        Key([mod], "q",             lazy.to_screen(nscreen_left)),
        Key([mod], "w",             lazy.to_screen(nscreen_middle)),
        Key([mod], "e",             lazy.to_screen(nscreen_right)),
        Key([mod, "shift", "control"], "q",    lazy.window.to_screen(nscreen_left)),
        Key([mod, "shift", "control"], "w",    lazy.window.to_screen(nscreen_middle)),
        Key([mod, "shift", "control"], "e",    lazy.window.to_screen(nscreen_right)),
        Key([mod, "shift"], "q",    lazy.spawn("~/.config/qtile/scripts/moveToVacant.py %i " % nscreen_left)),
        Key([mod, "shift"], "w",    lazy.spawn("~/.config/qtile/scripts/moveToVacant.py %i " % nscreen_middle)),
        Key([mod, "shift"], "e",    lazy.spawn("~/.config/qtile/scripts/moveToVacant.py %i " % nscreen_right)),
        Key([mod, "shift"], "c",    lazy.window.kill()),
        Key([mod, "shift"], "t",    lazy.window.disable_floating()),
        Key([mod], "t",    lazy.window.disable_floating()),
        Key([mod], "x",    lazy.spawn("~/.config/qtile/scripts/fixExcel.py" )), 
        

        # interact with prompts
        Key([mod], "p",              lazy.spawn("synapse")),
        Key([mod], "o",              lazy.spawn("~/.config/qtile/scripts/chooseMenu.py")),
        Key([mod], "b",              lazy.spawn("gnome-control-center bluetooth")),
        Key([mod, "control"], "e",   lazy.spawn("/usr/bin/nautilus --no-desktop")),
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

        Key([mod, "control"], "Left",         lazy.layout.decrease_ratio()),
        Key([mod, "control"], "Right",         lazy.layout.increase_ratio()),
        Key([mod], "Down",          lazy.spawn("xbacklight -dec 10 -time 1 -steps 1")) ,
        Key([mod], "Up",          lazy.spawn("xbacklight -inc 10 -time 1 -steps 1")) ,


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

    for i in "12345676890":
        gn=i
        if i == '1':
            gn=''
            groups.append(
                    Group(gn, layout='xmonad-tall', persist=True, init=True, 
                        spawn='gnome-terminal',
                        ))
        elif i == '2':
            gn=''
            groups.append(
                    Group(gn, persist=True, layout='max',
                        spawn='thunderbird',
                        matches=[Match(wm_class=['Thunderbird'])])
                    )
        elif i == '3':
            gn=''
            groups.append(
                    Group(gn, persist=True, layout='max', init=True,
                        spawn='/usr/local/bin/xsc',
                        matches=[Match(wm_class=['google-chrome', 'Google-chrome', 'Chromium-browser'])]),
                    )
        elif i == '4':
            gn='' 
            groups.append(
                    Group(gn, layout='max', persist=True, init=True,
                        spawn='firefox',
                        matches=[Match(wm_class=['Firefox', 'TorBrowser'])]),
                    )
        elif i == '0':
            groups.append(
                    Group(gn, layout='tile', persist=True, init=True,
                        matches=[Match(wm_class=["VirtualBox"])]),
                    )
        else:
            groups.append(Group(i, layout='xmonad-tall', persist=True, init=True))

        keys.append(
            Key([mod], i, lazy.group[gn].toscreen())
        )
        keys.append(
            Key([mod, "shift"], i, lazy.window.togroup(gn))
        )

    gn=''
    groups.append(
            Group(gn, layout='ratio-tile', persist=True, init=True,
                spawn='/usr/bin/pavucontrol',
                matches=[Match(wm_class=['Pavucontrol', 'Banshee', 'Skype','Empathy','Pidgin'])]),
            )
    keys.append(
        Key([mod], 'KP_Add', lazy.group[gn].toscreen())
    )
    keys.append(
        Key([mod, "shift"],  'KP_Add', lazy.window.togroup(gn))
    )

    gn='='
    groups.append(
            Group(gn, layout='ratio-tile', persist=True, init=True,
                matches=[Match(wm_class=['Desktop'])]),
            )
    keys.append(
        Key([mod], 'F10', lazy.group[gn].toscreen())
    )
    keys.append(
        Key([mod, "shift"],  'F10', lazy.window.togroup(gn))
    )

    gn=''
    groups.append(
            Group(gn, layout='xmonad-tall', persist=True, init=True,
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




def init_layouts(): return  [
        layout.Max(),
        layout.Tile(ratio=0.5, border_focus="#00afff", **border_args),
        layout.Matrix( **border_args), 
        #layout.Zoomy(), 
        # layout.xmonad-tall( **border_args),
        layout.MonadTall( name='xmonad-tall', **border_args), 
        layout.RatioTile( name='ratio-tile', **border_args),
        layout.Stack(stacks=2, **border_args)

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

def sendmessage(title, message):
    subprocess.Popen("sleep 1".split())
    os.popen('echo %s - %s >>' '/tmp/a.out' % (title, message))
    return

import subprocess, re, sys, os
def is_running(process):
    s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
    #sendmessage('checking',process)
    for x in s.stdout:
        if (re.search(process, x) and not re.search('<defunct>', x)) :
            #sendmessage('existing',x)
            return True
    #sendmessage('not existing', process)
    return False

def execute_once(process, args=" "):
    if not is_running(process):
        #sendmessage('running',process)
        return subprocess.Popen(" ".join((process, args)).split())

@hook.subscribe.startup
def startup():
    execute_once("dropbox","start")
    execute_once("fluxgui")
    execute_once("syncwall")
    execute_once("pidgin")
 #   execute_once("/usr/bin/gnome-keyring-daemon --start --components=gpg,pkcs11,secrets,ssh")
    execute_once("syndaemon")
    execute_once("synapse","-s")
    execute_once("indicator-cpufreq")
    execute_once("system-config-printer-applet")
    execute_once("parcellite")
    execute_once("nm-applet","--sm-disable")
    execute_once("bluetoothd")
#    execute_once("feh --bg-scale ~/Pictures/wallpapers.jpg")
    os.popen('export SSH_ASKPASS="/usr/bin/ssh-askpass"')
#    os.popen("cat /dev/null | ssh-add&")
    return
    os.popen("export GNOME_KEYRING_CONTROL GNOME_KEYRING_PID GPG_AGENT_INFO SSH_AUTH_SOCK")

@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    qtile.cmd_restart()


hide_windows = set([
    "scp-dbus-service.py",
    "desktop_window",

])
float_windows = set([
    "feh",
    "x11-ssh-askpass",
    "gimp-2.8",
    "gimp",
    "synapse",
    "mplayer",
    "guvcview",
    "gdesklets-daemon",
    "vncviewer",
    "vlc (xvideo output)",
    "vlc",
    "syncwall",

])
def should_be_hiding(w):
    wm_class = w.get_wm_class()
    if isinstance(wm_class, tuple):
        for cls in wm_class:
            if cls.lower() in hide_windows:
                return True
    else:
        if wm_class.lower() in hide_windows:
            return True
    return False

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
    if should_be_hiding(window.window):
        window.togroup("=")
        #window.hide = True



#@hook.subscribe.client_new
def windowInfo(window):
    with open("/tmp/test.txt", "a") as myfile:
        myfile.write("WINDOW\n")
        myfile.write(pformat( window.window.get_wm_class()))
        myfile.write("\n")
        myfile.write(pformat( window.cmd_inspect()))
        myfile.write("\n")
        myfile.write(pformat( window.window.get_wm_hints()))
        myfile.write("\n")
        myfile.write(pformat( window.window.get_wm_type()))
        myfile.write("\n")


@hook.subscribe.client_new
def excelHide(window):
#    with open("/tmp/test.txt", "a") as myfile:
#        myfile.write("\n>>CHECKING<<\n")
#        myfile.write(pformat( window.cmd_inspect()))
#        myfile.write("\n")
#        myfile.write(pformat( window.window.get_wm_hints()))
#        myfile.write("\n")
    winName = window.cmd_inspect()['name']
    initialState = window.window.get_wm_hints()['initial_state']
    winClass = window.window.get_wm_class()[0]
#    with open("/tmp/test.txt", "a") as myfile:
#        myfile.write("\n>>INSIDE<<\n")
#        myfile.write(pformat( winName))
#        myfile.write("\n")
#        myfile.write(pformat( winClass))
#        myfile.write("\n")
#        myfile.write(pformat( initialState ))
#        myfile.write("\n>>END CHECKING <<\n\n")
    if (winName == 'Microsoft Excel' and initialState == 1) or (winClass=="EXCEL.EXE" and initialState==3):
#        with open("/tmp/test.txt", "a") as myfile:
#            myfile.write("\n>>HIDING WINDOW<<\n")
        window.toggleminimize()
#        with open("/tmp/test.txt", "a") as myfile:
#            myfile.write("\n>>END HIDING WINDOW <<\n\n")



