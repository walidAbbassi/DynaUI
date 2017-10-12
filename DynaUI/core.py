# -*- coding: utf-8 -*-


import wx
from . import abstract as Ab

__all__ = ["BaseControl"]

MAPPING_EDGE = {
    None: ("", ""),
    "D" : ("", "LTRB"),
    "L" : ("LTRB", ""),
    "EM": ("LT", "RB"),
    "BE": ("RB", "LT"),
    "H" : ("T", "B"),
    "V" : ("L", "R"),
}


# ======================================================== Base ========================================================
class BaseControl(wx.Control):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 font=None, res=None, bg="L", fg="L", edge=None, async=False, fpsLimit=0):
        super().__init__(parent, pos=pos, size=size, style=wx.BORDER_NONE | style)
        self.R = parent.R
        self.S = parent.S
        self.L = parent.L
        if font is not None:  # Font inherit by default
            self.SetFont(self.R["FONT_" + font] if isinstance(font, str) else font)
        self.res = res
        self.Resources = self.R["BRUSH_SET_" + res] if isinstance(res, str) else res
        self.SetBackgroundColour(self.R["COLOR_BG_" + bg] if isinstance(bg, str) else bg)
        self.SetForegroundColour(self.R["COLOR_FG_" + fg] if isinstance(fg, str) else fg)
        self.BackgroundBrush = self.R["BRUSH_BG_" + bg] if isinstance(bg, str) else bg
        self.ForegroundBrush = self.R["BRUSH_FG_" + fg] if isinstance(fg, str) else fg
        if isinstance(edge, str) or edge is None:
            edge = MAPPING_EDGE[edge]
        self.Edge = ["L" in edge[0], "T" in edge[0], "R" in edge[0], "B" in edge[0], "L" in edge[1], "T" in edge[1], "R" in edge[1], "B" in edge[1]]
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.OnCaptureLost)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)  # Is there a better way to clean up the timer?
        self.Bind(wx.EVT_TIMER, lambda evt: Ab.Do(evt.GetTimer().func))
        self._async = async
        self._fpsLimit = fpsLimit
        self.Timers = {}
        self.Animations = {}
        if fpsLimit:
            self.Interval = 1000 // min(fpsLimit, 240)
            self.NewTimer("_", self.DoRefresh)
            self._needReDraw = False
        else:
            self.ReDraw = self.Refresh
        self._Controls = {}
        self.Groups = {}

    def __getitem__(self, item):
        return self._Controls[item]

    def __setitem__(self, key, value):
        self._Controls[key] = value

    def __contains__(self, item):
        return self._Controls.__contains__(item)

    def OnDestroy(self, evt):
        for timer in self.Timers:
            self.Timers[timer].Stop()
        evt.Skip()

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        w, h = self.GetSize()
        dc.SetPen(self.R["PEN_EDGE_L"])
        if self.Edge[0]: dc.DrawLine(0, 0, 0, h)
        if self.Edge[1]: dc.DrawLine(0, 0, w, 0)
        if self.Edge[2]: dc.DrawLine(w - 1, 0, w - 1, h)
        if self.Edge[3]: dc.DrawLine(0, h - 1, w, h - 1)
        dc.SetPen(self.R["PEN_EDGE_D"])
        if self.Edge[4]: dc.DrawLine(0, 0, 0, h)
        if self.Edge[5]: dc.DrawLine(0, 0, w, 0)
        if self.Edge[6]: dc.DrawLine(w - 1, 0, w - 1, h)
        if self.Edge[7]: dc.DrawLine(0, h - 1, w, h - 1)

    def OnCaptureLost(self, evt):
        pass

    # Timer
    def NewTimer(self, name, func=None):
        self.Timers[name] = wx.Timer(self)
        self.Timers[name].func = func

    def StartTimer(self, name, interval, mode=wx.TIMER_ONE_SHOT):
        if self.Timers[name].IsRunning():
            self.Timers[name].Stop()
        self.Timers[name].Start(interval, mode)

    def StopTimer(self, name):
        self.Timers[name].Stop()

    # Animation control
    def NewAnimation(self, name, interval, variable, sequence=None, resource=True, repeat=0, onUpdate=None, onStart=None, onStop=None, onRepeat=None):
        self.NewTimer(name)
        self.Animations[name] = Animation(self, self.Timers[name], interval, variable, sequence, resource, repeat, self.ReDraw if onUpdate is None else onUpdate, onStart, onStop, onRepeat)
        self.Timers[name].func = self.Animations[name].Update

    def Play(self, name, sequence=None, repeat=None):
        if not self._async:
            self.Stop()
        self.Animations[name].Play(sequence, repeat)

    def Pause(self, name, frames=-1):
        self.Animations[name].Pause(frames)

    def Stop(self, name=None):
        if name is None:
            for a in self.Animations:
                self.Animations[a].Stop()
        else:
            self.Animations[name].Stop()

    def Prepare(self, name=None):
        if name is None:
            for a in self.Animations:
                self.Animations[a].Prepare()
        else:
            self.Animations[name].Prepare()

    def ChangeResources(self, res):
        self.res = res
        self.Resources = self.R["BRUSH_SET_" + res] if isinstance(res, str) else res
        self.Prepare()

    # Refresh with limited fps
    def ReDraw(self):
        if self.Timers["_"].IsRunning():
            self._needReDraw = True
        else:
            self.Refresh()
            self._needReDraw = False
            self.Timers["_"].Start(self.Interval, wx.TIMER_ONE_SHOT)

    def DoRefresh(self):
        if self._needReDraw:
            self.Refresh()
            self._needReDraw = False


# ===================================================== Animation ======================================================
class Animation(object):
    def __init__(self, control, timer, interval, variable, sequence, resource, repeat, onUpdate, onStart, onStop, onRepeat):
        self.control = control
        self.timer = timer
        self.interval = interval
        self.variable = variable if callable(variable) else lambda r, v=variable: setattr(control, v, r)
        self.sequence = sequence
        self.resource = resource
        self.OnUpdate = onUpdate
        self.OnStart = onStart
        self.OnStop = onStop
        self.OnRepeat = onRepeat
        self.currentFrame = 0
        self.totalFrame = len(sequence)
        self.playing = False
        self.pausing = False
        self.pausingPast = 0
        self.pausingTotal = 0
        self.repeatLeft = repeat
        self.repeatTotal = repeat
        self.Prepare()

    def Prepare(self):  # Call it on resource change
        self._resource = [self.control.Resources[i] for i in self.sequence] if self.resource else self.sequence

    def Play(self, sequence=None, repeat=None):  # repeat=-1 : repeat infinitely until Stop is called
        self.Stop()
        if sequence is not None:
            self.sequence = sequence
            self.totalFrame = len(self.sequence)
            self.Prepare()
        if repeat is not None:
            self.repeatTotal = repeat
        Ab.Do(self.OnStart)
        self.currentFrame = 0
        self.playing = True
        self.repeatLeft = self.repeatTotal
        self.timer.Start(self.interval)

    def Stop(self):
        if self.playing:
            self.timer.Stop()
            self.playing = False
            self.pausing = False

    def Pause(self, frames=-1):  # frames=-1 : pause infinitely until Pause is called again
        if self.playing:
            if frames == -1:
                self.pausing = True
                self.pausingPast = 0
                self.pausingTotal = -1
            elif frames == 0:
                self.pausing = False
                self.pausingPast = 0
                self.pausingTotal = 0
            else:
                self.pausingTotal += frames

    def Update(self):
        if self.pausing:
            self.pausingPast += 1
            if self.pausingPast == self.pausingTotal:
                self.Pause(0)
            return
        self.variable(self._resource[self.currentFrame])
        Ab.Do(self.OnUpdate)
        self.currentFrame += 1
        if self.currentFrame == self.totalFrame:
            if self.repeatLeft == 0:
                self.timer.Stop()
                self.playing = False
                self.pausing = False
                Ab.Do(self.OnStop)
            else:
                self.currentFrame = 0
                self.repeatLeft -= self.repeatLeft > 0
                Ab.Do(self.OnRepeat)
