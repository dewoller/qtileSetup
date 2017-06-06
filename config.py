# pylint: skip-file
# coding: utf-8
from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
import os
#import pynotify
from pprint import pformat
import copy

numScreen = int(os.popen(r"xrandr | grep '\*' | wc -l").read().rstrip("\n"))
network = "wlp1s0"
nscreen_left = 0
nscreen_middle = 0
nscreen_right = 0
if numScreen == 2:
    nscreen_left = 0
    nscreen_middle = 1
    nscreen_right = 1
    network = "enp0s31f6"
elif numScreen == 3:
    nscreen_left = 0
    nscreen_middle = 2
    nscreen_right = 1
    network = "enp0s31f6"


def init_colors():
    return [["#7cfcff", "#00afff"], # cyan gradiant
            ["#323335", "#525355"], # grey gradiant
            ["#040404", "#111113"]] # darker grey gradiant


def init_widgets_defaults():
    
    # global font options
   return dict(
        font = 'FontAwesome',
        fontsize = 16,
        padding = 3,
    )


def init_screens():
    widgetSets=[]
    screens=[]

    for i in range(0, numScreen ):
        widgetSets.append( [ 
                    widget.CurrentScreen(),
                    widget.GroupBox(highlight_method="block",urgent_alert_method='text'),
                    widget.CurrentLayout(),
                    widget.Notify(audiofile= "/usr/share/skype/sounds/ChatOutgoing.wav",
                                foreground_urgent="EE0000", 
                                foreground_low="dddddd",
                                default_timeout=60,
                                foreground="FF0000", 
                                fontsize=18, 
                                font="Ubuntu"),
                    widget.Clock(format='%Y-%m-%d %a %H:%M %p', foreground='00FF7F'),
                    widget.TextBox(text="Dim:"),
                    widget.Backlight(brightness_file='/sys/class/backlight/intel_backlight/brightness',  max_brightness_file='/sys/class/backlight/intel_backlight/max_brightness',  ),
                    widget.TextBox(text="Bat:"),
                    widget.Battery(),
                    widget.BatteryIcon(),
                    widget.TextBox(text="Vol:"),
                    widget.Volume(),
                    widget.TextBox(text="C"),
                    widget.CPUGraph(samples=100, width=200),
                    widget.TextBox(text="D"),
                    widget.NetGraph(samples=100, width=200, interface=network),
                    widget.TextBox(text="U"),
                    widget.NetGraph(samples=100, width=200, interface=network, bandwidth_type="up"),
                    widget.TextBox(text="M"),
                    widget.MemoryGraph(samples=100, width=200),
                ])

    # truncate the last widget, and add on the systray, if we 
    #widgetSets[ numScreen - 1 ] = widgetSets[ numScreen - 1 ][0:3]
    widgetSets[ numScreen - 1 ].insert( 0, widget.Systray() )

    for i in range(0, numScreen ):
        screens.append( Screen(top = bar.Bar( widgetSets[ i ] , 30)) )
    

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
        #Key(["control", "shift"], "q",  lazy.spawn("echo 'restart' | qsh")),
    Key(
        ["control", "shift"], "q",
        lazy.spawn("/home/dewoller/.config/qtile/scripts/doCmd restart")
    ),
    Key(
        [mod], "Tab",
        lazy.group.next_window()),
     Key(
        [mod, "shift"], "k",
        lazy.layout.shuffle_up(),         # Stack, xmonad-tall
       ),
    Key(
        [mod, "shift"], "j",
        lazy.layout.shuffle_down(),       # Stack, xmonad-tall
       ),
    Key(
        [mod, "control"], "l",
        lazy.layout.add(),                # Stack
        lazy.layout.increase_ratio(),     # Tile
        lazy.layout.maximize(),           # xmonad-tall
       ),
    Key(
        [mod, "control"], "h",
        lazy.layout.shrink(),             # xmonad-tall
        lazy.layout.decrease_nmaster(),   # Tile
       ),
    Key(
        [mod, "control"], "j",
        lazy.layout.grow(),               # xmonad-tall
        lazy.layout.increase_nmaster(),   # Tile
       ),
    Key(
        [mod, "control"], "k",
        lazy.layout.delete(),             # Stack
        lazy.layout.decrease_ratio(),     # Tile
        lazy.layout.normalize(),          # xmonad-tall
       ),
   # this is usefull when floating windows get buried
        Key([mod], "m",              lazy.layout.maximize()),
        Key([mod], "n",              lazy.layout.normalize()),
        Key([mod], "l",              lazy.layout.toggle_split()),
        Key([mod], "j",              lazy.screen.togglegroup()),
        Key([mod], "space",         lazy.spawn("/home/dewoller/.config/qtile/scripts/doCmd next_layout ")),
        Key([mod, "shift"], "space",         lazy.spawn("/home/dewoller/.config/qtile/scripts/doCmd prev_layout ")),
        Key([mod], "q",             lazy.to_screen(nscreen_left)),
        Key([mod], "w",             lazy.to_screen(nscreen_middle)),
        Key([mod], "e",             lazy.to_screen(nscreen_right)),
        Key([mod, "shift", "control"], "p",    lazy.spawn("/home/dewoller/bin/playOneMacro.sh")),
        Key([mod, "shift", "control"], "q",    lazy.window.to_screen(nscreen_left)),
        Key([mod, "shift", "control"], "w",    lazy.window.to_screen(nscreen_middle)),
        Key([mod, "shift", "control"], "e",    lazy.window.to_screen(nscreen_right)),
        Key([mod, "shift"], "q",    lazy.spawn("/home/dewoller/.config/qtile/scripts/moveToVacant.py %i " % nscreen_left)),
        Key([mod, "shift"], "w",    lazy.spawn("/home/dewoller/.config/qtile/scripts/moveToVacant.py %i " % nscreen_middle)),
        Key([mod, "shift"], "e",    lazy.spawn("/home/dewoller/.config/qtile/scripts/moveToVacant.py %i " % nscreen_right)),
        Key([mod, "shift"], "c",    lazy.window.kill()),
        Key([mod, "shift"], "t",    lazy.window.disable_floating()),
        Key([mod, "shift"], "x",    lazy.spawn("/home/dewoller/.config/qtile/scripts/fixExcel.py" )), 
        Key([], "XF86MonBrightnessDown",    lazy.spawn("/home/dewoller/.config/qtile/scripts/backlightDown" )), 
        Key([], "XF86MonBrightnessUp",    lazy.spawn("/home/dewoller/.config/qtile/scripts/backlightUp" )), 
        

        # interact with prompts
        Key([mod], "r",              lazy.spawn("/home/dewoller/.config/qtile/torun1.sh")),
        Key([mod, "shift"], "r",              lazy.spawn("/home/dewoller/.config/qtile/torun2.sh")),
        Key([mod], "p",              lazy.spawn("rofi -show run")),
        Key([mod], "o",              lazy.spawn("python /home/dewoller/.config/qtile/scripts/chooseMenu.py")),
        Key([mod], "b",              lazy.spawn("gnome-control-center bluetooth")),
        Key([mod, "control"], "e",   lazy.spawn("/usr/bin/nautilus --no-desktop")),
        Key([mod], "XF86AudioMute",  lazy.spawn("/usr/bin/pavucontrol")),
        Key([mod], "F7",             lazy.spawn("/home/dewoller/bin/proxy")),
        Key([mod], "F8",             lazy.spawn("setupMonitors")),
        Key([mod], "F1",             lazy.spawn("/home/dewoller/bin/gosleep")),
        Key([mod], "Escape",         lazy.spawn("setxkbmap -option caps:escape")),
        #Key([mod], "h", lazy.layout.left()),
        #Key([mod], "l", lazy.layout.right()),
        Key([mod], "k", lazy.layout.up()),
        Key([mod, "shift"], "h", lazy.layout.swap_left()),
        Key([mod, "shift"], "l", lazy.layout.swap_right()),
#        Key([mod, "shift"], "o", lazy.layout.maximize()),
#        Key([mod, "shift"], "space", lazy.layout.flip()),

#-- Screenshots 
        Key([], "Print",             lazy.spawn("shutter")),
 
        Key([mod, "control"], "Left",         lazy.layout.decrease_ratio()),
        Key([mod, "control"], "Right",         lazy.layout.increase_ratio()),
        Key([mod], "Down",    lazy.spawn("xbacklight -dec $(( $(xbacklight)/10));" )), 
        Key([mod], "Up",    lazy.spawn("xbacklight -inc $(( $(xbacklight)/10));" )), 


        # start specific apps
        Key([mod, "shift"], "Return", lazy.spawn("gnome-terminal")),
        Key([mod], "Return",          lazy.layout.rotate()),

            # Change the volume if our keyboard has keys
            Key(
                [], "XF86AudioRaiseVolume",
                lazy.spawn("amixer -D pulse sset Master 5%+")
                ),
            Key(
                [], "XF86AudioLowerVolume",
                lazy.spawn("amixer -D pulse sset Master 5%-")
                ),
            Key(
                [], "XF86AudioMute",
                lazy.spawn("amixer -D pulse sset Master toggle")
                ),

            # also allow changing volume the old fashioned way
            Key([mod], "asterisk", lazy.spawn("amixer -D pulse sset Master 5%+")),
            Key([mod], "minus", lazy.spawn("amixer -D pulse sset Master 5%-")),

            ]

    groups = []

    for i in "12345676890":
        gn=i
        if i == '1':
            gn='1'
            groups.append(
                    Group(gn, persist=True, init=True, 
                        ))
        elif i == '2':
            gn='2'
            groups.append(
                    Group(gn, persist=True,init=True,
                        spawn='thunderbird',
                        matches=[Match(wm_class=['Thunderbird'])])
                    )
        elif i == '3':
            gn='3'
            groups.append(
                    Group(gn, persist=True, init=True,
                        matches=[Match(wm_class=['google-chrome', 'Google-chrome', 'Chromium-browser', 'google-chrome-beta', 'Google-chrome-beta'])]),
                    )
        elif i == '4':
            gn='4' 
            groups.append(
                    Group(gn, persist=True, init=True,
                        spawn='firefox',
                        matches=[Match(wm_class=['Firefox', 'TorBrowser'])]),
                    )
        elif i == '5':
            gn='5' 
            groups.append(
                    Group(gn, persist=True, init=True,
                        matches=[Match(wm_class=['Eclipse'])]),
                    )
        elif i == '9':
            groups.append(
                    Group(gn, persist=True, init=True,
                        matches=[Match(wm_class=['VirtualBox']
                            )]),
                    )
        elif i == '8':
            groups.append(
                    Group(gn, persist=True, init=True,
                        matches=[Match(wm_class=['zoom']
                            )]),
                    )
        elif i == '0':
            groups.append(
                    Group(gn, persist=True, init=True,
                        matches=[Match(wm_class=[ "WINWORD.EXE", "POWERPNT.EXE"])]),
                    )
        else:
            groups.append(Group(i, persist=True, init=True))

        keys.append(
            Key([mod], i, lazy.group[gn].toscreen())
        )
        keys.append(
            Key([mod, "shift"], i, lazy.window.togroup(gn))
        )

    gn='Z'
    groups.append(
            Group(gn, persist=True, init=True,
                matches=[Match(wm_class=["Franz","franz"])]),
            )
    keys.append(
        Key([mod], 'grave', lazy.group[gn].toscreen())
    )
    keys.append(
        Key([mod, "shift"],  'grave', lazy.window.togroup(gn))
    )
    keys.append(
        Key([mod], 'z', lazy.group[gn].toscreen())
    )
    keys.append(
        Key([mod,"shift"],  'z', lazy.window.togroup(gn))
    )

    gn=''
    groups.append(
            Group(gn, persist=True, init=True,
                spawn='/usr/bin/pavucontrol',
                matches=[Match(wm_class=['Pavucontrol', 'Banshee', 'Skype', 'skypeforlinux', 'Empathy','Pidgin', 'Scudcloud'])]),
            )
    keys.append(
        Key([mod], 'KP_Subtract', lazy.group[gn].toscreen())
    )
    keys.append(
        Key([mod, "shift"],  'KP_Subtract', lazy.window.togroup(gn))
    )
    keys.append(
        Key([mod], 'minus', lazy.group[gn].toscreen())
    )
    keys.append(
        Key([mod,"shift"],  'minus', lazy.window.togroup(gn))
    )


    gn=''
    groups.append(
            Group(gn, persist=True, init=True,
                spawn='/usr/bin/keepassx',
                matches=[Match(wm_class=['Keepassx'])]),
            )
    keys.append(
        Key([mod], 'KP_Enter', lazy.group[gn].toscreen())
    )
    keys.append(
        Key([mod, "shift"],  'KP_Enter', lazy.window.togroup(gn))
    )
    keys.append(
        Key([mod], 'equal', lazy.group[gn].toscreen())
    )
    keys.append(
        Key([mod,"shift"],  'equal', lazy.window.togroup(gn))
    )

    gn='=' # junk window
    groups.append(
            Group(gn, persist=True, init=True,
                matches=[Match(wm_class=['Desktop'])]),
            )
    keys.append(
        Key([mod], "F10", lazy.group[gn].toscreen())
    )
    keys.append(
        Key([mod, "shift"],  "F10", lazy.window.togroup(gn))
    )


    return((keys, groups))




def init_layouts(): return  [
        layout.Max(),
        layout.Zoomy( **border_args),
        layout.MonadTall(ratio=0.65, **border_args),
        layout.Columns( **border_args),
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
    os.popen('/home/dewoller/.config/qtile/startup-hook')

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
    "tk",
    "Toplevel",

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
        window.toggleminimize()
        #window.hide = True
    if(window.window.get_wm_type() == 'dialog'
        or window.window.get_wm_transient_for()):
        window.floating = True
        window.toggleminimize()


#@hook.subscribe.client_new
def windowInfo(window):
    with open("/tmp/test.txt", "a") as myfile:
        myfile.write("WINDOW\n")
        myfile.write(pformat( window.window.get_wm_class()))
        myfile.write("\n")
        myfile.write(pformat( window.window.cmd_inspect()['name']))
        myfile.write("\n")
       # myfile.write(pformat( window.cmd_inspect()))
        myfile.write("\n")
       # myfile.write(pformat( window.window.get_wm_hints()))
        myfile.write("\n")
       # myfile.write(pformat( window.window.get_wm_type()))
        myfile.write("\n")


@hook.subscribe.client_new
def excelHide(window):
    winName = window.cmd_inspect()['name']
    winClass = window.window.get_wm_class()[0]
    if (winName == 'Microsoft Excel' and initialState == 1) or (winClass=="EXCEL.EXE" ):
        window.toggleminimize()
        window.togroup("=")



@hook.subscribe.client_new
def vue_tools(window):
    if((window.window.get_wm_class() == ('sun-awt-X11-XWindowPeer',
                                        'tufts-vue-VUE')
                and window.window.get_wm_hints()['window_group'] != 0)
                or (window.window.get_wm_class() == ('sun-awt-X11-XDialogPeer',
                                         'tufts-vue-VUE'))):
        window.floating = True

@hook.subscribe.client_new
def idle_dialogues(window):
    if((window.window.get_name() == 'Search Dialog') or
      (window.window.get_name() == 'Module') or
      (window.window.get_name() == 'Goto') or
      (window.window.get_name() == 'IDLE Preferences')):
        window.floating = True

@hook.subscribe.client_new
def libreoffice_dialogues(window):
    if((window.window.get_wm_class() == ('VCLSalFrame', 'libreoffice-calc')) or
    (window.window.get_wm_class() == ('VCLSalFrame', 'LibreOffice 3.4'))):
        window.floating = True

@hook.subscribe.client_new
def inkscape_dialogues(window):
   if window.window.get_name() == 'Sozi':
        window.floating = True

