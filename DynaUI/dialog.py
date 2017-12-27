# -*- coding: utf-8 -*-


import wx
from .core import BaseControl, Animation
from . import abstract as Ab
from . import variable as Va
from . import utility as Ut
from . import controls as UI

__all__ = ["BaseMain", "BaseHead", "BaseGrip", "BaseDialog", "BaseMiniDialog"]


# ====================================================== BaseMain ======================================================
class BaseMain(BaseControl):
    MARGIN = Va.SETTINGS["DLG_MAIN_MARGIN"]
    LABEL_WIDTH = Va.SETTINGS["DLG_MAIN_LABEL_W"]
    LINE_HEIGHT = Va.SETTINGS["DLG_MAIN_LINE_H"]
    BUTTON_WIDTH = Va.SETTINGS["DLG_MAIN_BUTTON_W"]

    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, **kwargs):
        super().__init__(parent=parent, pos=pos, size=size, style=style, **kwargs)
        self.Frame = parent
        self.SetDoubleBuffered(True)

    def _AddLabel(self, sizer, label):
        name = wx.StaticText(self, label=label, size=wx.Size(self.LABEL_WIDTH, -1), style=wx.ST_ELLIPSIZE_END)
        sizer.Add(name, self.LABEL_WIDTH == -1, wx.ALIGN_CENTER)
        sizer.Add(self.MARGIN * 2, self.MARGIN)
        return name

    def _AddSubSizer(self, sizer, orientation=wx.HORIZONTAL, w=0, h=0):
        subSizer = wx.BoxSizer(orientation)
        if sizer.GetOrientation() == wx.VERTICAL:
            sizer.Add(subSizer, h == -1, (w == -1 and wx.EXPAND) | wx.ALL, self.MARGIN)
        else:
            sizer.Add(subSizer, w == -1, (h == -1 and wx.EXPAND) | wx.ALL, self.MARGIN)
        return subSizer

    # --------------------------------------
    def AddSeparator(self, sizer):
        sizer.Add(UI.Separator(self, orientation=(wx.VERTICAL | wx.HORIZONTAL) ^ sizer.GetOrientation()), 0, wx.EXPAND | wx.ALL, self.MARGIN)

    def AddSectionHead(self, sizer, tag="", **kwargs):
        sizer.Add(UI.SectionHead(self, orientation=(wx.VERTICAL | wx.HORIZONTAL) ^ sizer.GetOrientation(), label=tag, **kwargs), 0, wx.EXPAND | wx.ALL, self.MARGIN)

    # --------------------------
    def AddButton(self, sizer, label="", tag="", width=None, onClick=None, **kwargs):
        width = width or self.BUTTON_WIDTH
        subSizer = self._AddSubSizer(sizer, orientation=wx.HORIZONTAL, w=width)
        if label:
            self._AddLabel(subSizer, label)
        button = UI.ButtonNormal(self, size=wx.Size(width, self.LINE_HEIGHT), tag=tag, func=onClick, edge="L", **kwargs)
        subSizer.Add(button, width == -1)
        return button

    def AddButtonToggle(self, sizer, label="", tags=(), width=None, toggle=False, onClick=None, **kwargs):
        width = width or self.BUTTON_WIDTH
        subSizer = self._AddSubSizer(sizer, orientation=wx.HORIZONTAL, w=width)
        if label:
            self._AddLabel(subSizer, label)
        button = UI.ButtonToggle(self, size=wx.Size(width, self.LINE_HEIGHT), tag=tags[0], tag2=tags[1], func=onClick, edge="L", toggle=toggle, **kwargs)
        subSizer.Add(button, width == -1)
        return button

    def AddButtonBundle(self, sizer, label="", tags=(), width=None, rows=1, toggled=0, group="", onClick=None, **kwargs):
        width = width or self.BUTTON_WIDTH
        bPerRow = (len(tags) + rows - 1) // rows
        subSizers = [wx.BoxSizer(wx.HORIZONTAL) for i in range(rows)]
        if label:
            self._AddLabel(subSizers[0], label)
            for s in subSizers[1:]:
                s.Add(self.LABEL_WIDTH, -1, 0, wx.ALIGN_CENTER)
                s.Add(self.MARGIN * 2, self.MARGIN)
        buttons = []
        for index, tag in enumerate(tags):
            button = UI.ButtonBundle(self, size=wx.Size(width, self.LINE_HEIGHT), tag=tag, func=onClick, edge="L", toggle=index == toggled, group=group, **kwargs)
            subSizers[index // bPerRow].Add(button, width == -1)
            buttons.append(button)
        subSizer = self._AddSubSizer(sizer, orientation=wx.VERTICAL, w=width)
        for s in subSizers:
            subSizer.Add(s, 1, wx.EXPAND)
        return UI.Bundled(buttons)

    def AddPickerValue(self, sizer, label="", choices=(), selected=-1, width=None, **kwargs):
        width = width or self.BUTTON_WIDTH
        subSizer = self._AddSubSizer(sizer, orientation=wx.HORIZONTAL, w=width)
        if label:
            self._AddLabel(subSizer, label)
        picker = UI.PickerValue(self, size=wx.Size(width, self.LINE_HEIGHT), choices=choices, selected=selected, edge="L", **kwargs)
        subSizer.Add(picker, width == -1)
        return picker

    # --------------------------
    def AddStaticText(self, sizer, label="", value="", width=-1):
        subSizer = self._AddSubSizer(sizer, orientation=wx.HORIZONTAL, w=width)
        if label:
            self._AddLabel(subSizer, label)
        text = wx.StaticText(self, label=value, size=wx.Size(width, -1), style=wx.ST_ELLIPSIZE_END)
        subSizer.SetMinSize(-1, self.LINE_HEIGHT)
        subSizer.Add(text, 1, wx.ALIGN_CENTER)
        return text

    def AddStaticBitmap(self, sizer, label="", width=-1, height=-1, inline=True, bitmap=wx.NullBitmap, **kwargs):
        pic = UI.StaticBitmap(self, size=wx.Size(width, height), bitmap=bitmap, **kwargs)
        if label:
            name = wx.StaticText(self, label=label, size=wx.Size(self.LABEL_WIDTH, -1 if inline else self.LINE_HEIGHT), style=wx.ST_ELLIPSIZE_END)
        else:
            name = None
        if inline:
            subSizer = self._AddSubSizer(sizer, orientation=wx.HORIZONTAL, w=width, h=height)
            if name:
                subSizer.Add(name, self.LABEL_WIDTH == -1, wx.ALIGN_CENTER)
                subSizer.Add(self.MARGIN * 2, self.MARGIN)
            subSizer.Add(pic, width == -1, wx.EXPAND)
        else:
            subSizer = self._AddSubSizer(sizer, orientation=wx.VERTICAL, w=width, h=height)
            if name:
                subSizer.Add(name, self.LABEL_WIDTH == -1, wx.EXPAND)
            subSizer.Add(pic, height == -1, wx.EXPAND)
        return pic

    def AddLineCtrl(self, sizer, label="", value="", width=-1, style=0, onInput=None, hint="", font=None, blend=False):
        subSizer = self._AddSubSizer(sizer, orientation=wx.HORIZONTAL, w=width)
        border = wx.BORDER_NONE if blend else wx.BORDER_SIMPLE
        if hint:
            text = UI.TextWithHint(self, hint=hint, value=value, size=wx.Size(width, self.LINE_HEIGHT), style=style | border)
        else:
            text = UI.Text(self, value=value, size=wx.Size(width, self.LINE_HEIGHT), style=style | border)
        if font is not None:
            text.SetFont(self.R["FONT_" + font] if isinstance(font, str) else font)
        if blend:
            text.SetBackgroundColour(self.R["COLOR_BG_L"])
        if label:
            name = self._AddLabel(subSizer, label)
            name.Bind(wx.EVT_LEFT_DOWN, lambda evt: (text.SetFocus(), text.SelectAll()))
        if onInput:
            text.Bind(wx.EVT_TEXT, onInput)
        subSizer.Add(text, width == -1)
        return text

    def AddTextCtrl(self, sizer, label="", value="", width=-1, height=-1, style=0, inline=True, onInput=None, hint="", font=None):
        if hint:
            text = UI.TextWithHint(self, hint=hint, value=value, size=wx.Size(width, height), style=style | wx.TE_MULTILINE | wx.BORDER_SIMPLE)
        else:
            text = UI.Text(self, value=value, size=wx.Size(width, height), style=style | wx.TE_MULTILINE | wx.BORDER_SIMPLE)
        if font is not None:
            text.SetFont(self.R["FONT_" + font] if isinstance(font, str) else font)
        if onInput:
            text.Bind(wx.EVT_TEXT, onInput)
        if label:
            name = wx.StaticText(self, label=label, size=wx.Size(self.LABEL_WIDTH, -1 if inline else self.LINE_HEIGHT), style=wx.ST_ELLIPSIZE_END)
            name.Bind(wx.EVT_LEFT_DOWN, lambda evt: (text.SetFocus(), text.SelectAll()))
        else:
            name = None
        if inline:
            subSizer = self._AddSubSizer(sizer, orientation=wx.HORIZONTAL, w=width, h=height)
            if name:
                subSizer.Add(name, self.LABEL_WIDTH == -1, wx.ALIGN_CENTER)
                subSizer.Add(self.MARGIN * 2, self.MARGIN)
            subSizer.Add(text, width == -1, wx.EXPAND)
        else:
            subSizer = self._AddSubSizer(sizer, orientation=wx.VERTICAL, w=width, h=height)
            if name:
                subSizer.Add(name, self.LABEL_WIDTH == -1, wx.EXPAND)
            subSizer.Add(text, height == -1, wx.EXPAND)
        return text

    # --------------------------
    def AddListBox(self, sizer, label="", choices=(), selected=-1, width=-1, height=-1, onClick=None, onDClick=None, inline=True):
        if label:
            name = wx.StaticText(self, label=label, size=wx.Size(self.LABEL_WIDTH, -1 if inline else self.LINE_HEIGHT), style=wx.ST_ELLIPSIZE_END)
        else:
            name = None
        listbox = UI.ListCtrl(self, data=[(i,) for i in choices], size=wx.Size(width, height), width=(-1,), edge="L")
        listbox.SetSelection(selected)
        listbox.OnSelection = onClick or Ab.DoNothing
        listbox.OnActivation = onDClick or Ab.DoNothing
        if inline:
            subSizer = self._AddSubSizer(sizer, orientation=wx.HORIZONTAL, w=width, h=height)
            if name:
                subSizer.Add(name, self.LABEL_WIDTH == -1, wx.ALIGN_CENTER)
                subSizer.Add(self.MARGIN * 2, self.MARGIN)
            subSizer.Add(listbox, width == -1, wx.EXPAND)
        else:
            subSizer = self._AddSubSizer(sizer, orientation=wx.VERTICAL, w=width, h=height)
            if name:
                subSizer.Add(name, self.LABEL_WIDTH == -1, wx.EXPAND)
            subSizer.Add(listbox, height == -1, wx.EXPAND)
        return listbox

    # --------------------------
    def AddPickerFile(self, sizer, label="", value="", width=-1, width2=None, mode="L", wildcard="All files (*.*)|*.*", hint="", style=0, onSelect=None):
        width2 = width2 or self.BUTTON_WIDTH
        onSelect = onSelect or Ab.DoNothing
        if hint:
            text = UI.TextWithHint(self, hint=hint, value=value, size=wx.Size(width, self.LINE_HEIGHT), style=style | wx.BORDER_SIMPLE)
        else:
            text = UI.Text(self, value=value, size=wx.Size(width, self.LINE_HEIGHT), style=style | wx.BORDER_SIMPLE)
        if mode == "L":
            func = lambda: text.SetValue(Ut.ShowOpenFileDialog(self, self.L.Get("GENERAL_HEAD_LOAD"), wildcard) or "")
        else:
            func = lambda: text.SetValue(Ut.ShowSaveFileDialog(self, self.L.Get("GENERAL_HEAD_SAVE"), wildcard) or "")
        button = UI.Button(self, size=wx.Size(width2, self.LINE_HEIGHT), tag="...", edge="L", func=((self.GetGrandParent().Disable,), func, onSelect, self.GetGrandParent().Enable))
        subSizer = self._AddSubSizer(sizer, orientation=wx.HORIZONTAL, w=width)
        if label:
            name = self._AddLabel(subSizer, label)
            name.Bind(wx.EVT_LEFT_DOWN, lambda evt: (text.SetFocus(), text.SelectAll()))
        subSizer.Add(text, width == -1)
        subSizer.Add(button, width2 == -1)
        return text

    # --------------------------
    def AddStdButton(self, sizer, size=wx.Size(40, 20), onOK=None, onCancel=None, onApply=None):
        if onOK is not None:
            self[1] = UI.ToolNormal(self, size=size, pics=self.R["AP_CHECK"], edge="D", func=onOK)
        if onCancel is not None:
            self[0] = UI.ToolNormal(self, size=size, pics=self.R["AP_CROSS"], edge="D", func=onCancel)
        if onApply is not None:
            self[2] = UI.ToolNormal(self, size=size, pics=self.R["AP_APPLY"], edge="D", func=onApply)
        subSizer = sizer if sizer.GetOrientation() == wx.HORIZONTAL else wx.BoxSizer(wx.HORIZONTAL)
        for i in (1, 0, 2):
            if i in self:
                subSizer.Add(self[i], 0, wx.ALL, self.MARGIN)
        if subSizer is not sizer:
            sizer.Add(subSizer, 0, wx.ALIGN_RIGHT | wx.ALL, 0)


# ====================================================== BaseHead ======================================================
class BaseHead(UI.Button):
    def __init__(self, parent, buttons=True, **kwargs):
        super().__init__(parent, size=wx.Size(-1, Va.SETTINGS["DLG_HEAD"]), tag=(parent.GetTitle(), "L", 7, 0), fg=parent.R["COLOR_DLG_HEAD_FG"]["00"], **kwargs)
        self.Frame = parent
        self.NewAnimation("ENTER", 10, self.SetResource, ("FF", "C0", "80", "40", "00"), False, onStop=(self.SetButtonResources, "BRUSH_DLG_SET_I"))
        self.NewAnimation("LEAVE", 10, self.SetResource, ("00", "40", "80", "C0", "FF"), False, onStart=(self.SetButtonResources, "BRUSH_DLG_SET_O"))
        self.lastMousePos = None
        self.lastFramePos = None
        self.SizerFlags = wx.SizerFlags().Center()
        Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Sizer.Add(0, 0, 1)
        if buttons:
            Sizer.Add(UI.ToolNormal(self, size=Va.SETTINGS["DLG_HEAD_BTN"], pics=self.R["AP_MINI"], func=self.Frame.OnMinimize), self.SizerFlags)
            Sizer.Add(UI.ToolNormal(self, size=Va.SETTINGS["DLG_HEAD_BTN"], pics=self.R["AP_MAXI"], func=self.Frame.OnMaximize), self.SizerFlags)
        Sizer.Add(UI.ToolNormal(self, size=Va.SETTINGS["DLG_HEAD_BTN"], pics=self.R["AP_EXIT"], func=self.Frame.OnClose, res="R"), self.SizerFlags)
        Sizer.Add(3, 0)
        self.SetSizer(Sizer)

    def SetResource(self, r):
        self.Brush = self.R["BRUSH_DLG_HEAD_BG"][r]
        self.SetForegroundColour(self.R["COLOR_DLG_HEAD_FG"][r])
        for i in self.GetChildren():
            i.Brush = self.Brush

    def SetButtonResources(self, res):
        for i in self.GetChildren():
            if i.Params["RES"] == "R":
                i.Resources = self.R[res + "_R"]
            else:
                i.Resources = self.R[res]
            i.Prepare()

    def OnMouse(self, evt):
        evtType = evt.GetEventType()
        evtPos = evt.GetPosition()
        if evtType == wx.wxEVT_LEFT_DOWN:
            if not self.HasCapture(): self.CaptureMouse()
            self.lastMousePos = self.Frame.ClientToScreen(evtPos)
            self.lastFramePos = self.Frame.GetPosition()
        elif evtType == wx.wxEVT_LEFT_UP:
            if self.HasCapture(): self.ReleaseMouse()
            self.lastMousePos = None
            self.lastFramePos = None
        elif evtType == wx.wxEVT_MOTION and self.lastMousePos:
            self.Frame.SetPosition(self.lastFramePos - self.lastMousePos + self.Frame.ClientToScreen(evtPos))
        elif evtType == wx.wxEVT_MIDDLE_DOWN:
            self.Frame.OnMinimize()
        elif evtType == wx.wxEVT_LEFT_DCLICK:
            self.Frame.OnMaximize()
        elif evtType == wx.wxEVT_RIGHT_DCLICK:
            self.Frame.OnClose()

    def OnCaptureLost(self, evt):
        self.lastMousePos = None
        self.lastFramePos = None


# ====================================================== BaseGrip ======================================================
class BaseGrip(BaseControl):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, size=wx.Size(8, 8), **kwargs)
        self.Frame = parent
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
        self.leftDown = False
        self.lastMousePos = None
        self.lastFrameSize = None
        self.sizeRect = None
        self.NewAnimation("FADEIN", 16, self.SetRectAlpha, range(10, 81, 10), False)
        self.NewAnimation("FADEOUT", 16, self.SetRectAlpha, range(80, 9, -10), False, onStop=self.CloseRect)

    def CloseRect(self):
        if self.sizeRect is not None:
            self.sizeRect.Destroy()
            self.sizeRect = None

    def SetRectAlpha(self, t):
        if self.sizeRect is not None:
            self.sizeRect.SetTransparent(t)

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        dc.SetPen(self.R["PEN_EDGE_L"])
        dc.SetBrush(self.R["BRUSH_EDGE_L"])
        dc.DrawPolygon(((6, 0), (6, 6), (0, 6)))
        dc.SetPen(self.R["PEN_EDGE_D"])
        dc.DrawLines(((7, 0), (7, 7), (-1, 7)))

    def OnMouse(self, evt):
        evtType = evt.GetEventType()
        evtPos = evt.GetPosition()
        if evtType == wx.wxEVT_LEFT_DOWN:
            if not self.HasCapture(): self.CaptureMouse()
            self.leftDown = True
            self.lastMousePos = self.ClientToScreen(evtPos)
            self.lastFrameSize = self.Frame.GetSize()
        elif evtType == wx.wxEVT_LEFT_UP:
            if self.HasCapture(): self.ReleaseMouse()
            if self.sizeRect:
                self.Frame.SetSize(self.sizeRect.GetSize())
                self.Frame.Refresh()
                self.Play("FADEOUT")
            self.leftDown = False
            self.lastMousePos = None
            self.lastFrameSize = None
        elif evtType == wx.wxEVT_MOTION and self.leftDown:
            if not self.sizeRect:
                self.sizeRect = wx.Frame(self, pos=self.Frame.GetPosition(), size=self.lastFrameSize, style=wx.BORDER_NONE | wx.FRAME_NO_TASKBAR | wx.FRAME_FLOAT_ON_PARENT)
                self.sizeRect.SetBackgroundColour(self.R["COLOR_SIZING"])
                self.sizeRect.SetTransparent(0)
                self.sizeRect.Show()
                self.Play("FADEIN")
            x, y = self.ClientToScreen(evtPos) - self.lastMousePos + self.lastFrameSize
            self.sizeRect.SetSize((max(x, 120), max(y, Va.SETTINGS["DLG_HEAD"] + 10)))
        elif evtType == wx.wxEVT_ENTER_WINDOW:
            self.SetCursor(self.R["CURSOR_SIZING"])
        elif evtType == wx.wxEVT_LEAVE_WINDOW:
            self.SetCursor(self.R["CURSOR_NORMAL"])
        evt.Skip()

    def OnCaptureLost(self, evt):
        self.leftDown = False
        self.lastMousePos = None
        self.lastFrameSize = None
        self.CloseRect()


# ===================================================== BaseDialog =====================================================
class BaseDialog(wx.Frame):
    def __init__(self,
                 parent=None, title="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 invoker=None,
                 font="N", bg="L", fg="L",
                 main=BaseMain,
                 head=BaseHead,
                 grip=BaseGrip):
        invoker = parent or invoker
        super().__init__(parent=parent, title=invoker.L.Get(title), pos=pos, size=size, style=wx.BORDER_NONE | wx.FRAME_FLOAT_ON_PARENT | style)
        self.R = invoker.R
        self.S = invoker.S
        self.L = invoker.L
        self.SetFont(self.R["FONT_" + font] if isinstance(font, str) else font)
        self.SetBackgroundColour(self.R["COLOR_BG_" + bg] if isinstance(bg, str) else bg)
        self.SetForegroundColour(self.R["COLOR_FG_" + fg] if isinstance(fg, str) else fg)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        self.Bind(wx.EVT_TIMER, lambda evt: Ab.Do(evt.GetTimer().func))
        self.Timers = {}
        self.Animations = {}
        self.NewAnimation("FADEIN", 16, self.SetTransparent, range(55, 256, 50), False, onStart=self.Show, onStop=(self.Bind, wx.EVT_ACTIVATE, self.OnActivation))
        self.NewAnimation("FADEOUT", 16, self.SetTransparent, range(200, -1, -50), False, onStart=(self.Unbind, wx.EVT_ACTIVATE), onStop=self.Destroy)
        self.SetTransparent(5)

        self.minimized = False
        self.maximized = False
        self.Main = main[0](self, **main[1]) if isinstance(main, (tuple, list)) else (BaseMain(self, **main) if isinstance(main, dict) else main(self))
        self.Head = head[0](self, **head[1]) if isinstance(head, (tuple, list)) else (BaseHead(self, **head) if isinstance(head, dict) else head(self))
        self.Grip = grip[0](self, **grip[1]) if isinstance(grip, (tuple, list)) else (BaseGrip(self, **grip) if isinstance(grip, dict) else grip(self))
        FrameSizer = wx.BoxSizer(wx.VERTICAL)
        FrameSizer.Add(self.Head, 0, wx.EXPAND)
        FrameSizer.Add(self.Main, 1, wx.EXPAND | wx.ALL ^ wx.BOTTOM, 4)
        FrameSizer.Add(self.Grip, 0, wx.ALIGN_RIGHT)
        self.SetSizer(FrameSizer)
        self.Layout()
        self.GetBorderPoints()
        self.Main.SetFocus()
        Ut.DropShadow(self)

    # --------------------------------------
    def OnDestroy(self, evt):
        self.MakeModal(False)
        for timer in self.Timers:
            self.Timers[timer].Stop()
        evt.Skip()

    def OnSize(self, evt):
        evt.Skip()
        self.Layout()
        self.GetBorderPoints()
        Ut.DropShadow(self)

    def GetBorderPoints(self):
        w, h = self.GetSize()
        self._pointsI = (1, Va.SETTINGS["DLG_HEAD"]), (1, h - 2), (w - 2, h - 2), (w - 2, Va.SETTINGS["DLG_HEAD"]), (1, Va.SETTINGS["DLG_HEAD"])
        self._pointsO = (0, Va.SETTINGS["DLG_HEAD"]), (0, h - 1), (w - 1, h - 1), (w - 1, Va.SETTINGS["DLG_HEAD"] - 1)

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        dc.SetPen(self.R["PEN_EDGE_L"])
        dc.DrawLines(self._pointsI)
        dc.SetPen(self.R["PEN_EDGE_D"])
        dc.DrawLines(self._pointsO)

    def OnActivation(self, evt):
        if self:
            self.Head.Play("ENTER" if evt.GetActive() else "LEAVE")

    # --------------------------------------
    def NewAnimation(self, name, interval, variable, sequence=None, resource=True, repeat=0, onUpdate=None, onStart=None, onStop=None, onRepeat=None):
        self.Timers[name] = wx.Timer(self)
        self.Animations[name] = Animation(self, self.Timers[name], interval, variable, sequence, resource, repeat, self.Refresh if onUpdate is None else onUpdate, onStart, onStop, onRepeat)
        self.Timers[name].func = self.Animations[name].Update

    def Play(self, name, sequence=None, repeat=None):
        for a in self.Animations:
            self.Animations[a].Stop()
        self.Animations[name].Play(sequence, repeat)

    # --------------------------------------
    def MakeModal(self, modal=True):
        if modal and not hasattr(self, "_disabler"):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, "_disabler"):
            del self._disabler

    def OnMinimize(self):
        if self.maximized:
            self.OnMaximize()
        if self.minimized:
            self.SetSize((-1, self.minimized))
            self.Main.Show()
            self.Grip.Show()
            self.minimized = False
        else:
            self.minimized = self.GetSize()[1]
            self.Main.Hide()
            self.Grip.Hide()
            self.SetSize((-1, Va.SETTINGS["DLG_HEAD"]))
        self.Layout()

    def OnMaximize(self):
        if self.minimized:
            self.OnMinimize()
        if self.maximized:
            self.maximized = False
            self.Restore()
        else:
            self.maximized = True
            self.Maximize()
        self.Layout()
        self.Refresh()

    def OnClose(self):
        self.Play("FADEOUT")


# =================================================== BaseMiniDialog ===================================================
class BaseMiniDialog(wx.Frame):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, font="N", bg="L", fg="L", main=None, **kwargs):
        super().__init__(parent=parent, pos=pos, size=size, style=wx.BORDER_NONE | wx.FRAME_NO_TASKBAR | wx.FRAME_FLOAT_ON_PARENT)
        self.R = parent.R
        self.S = parent.S
        self.L = parent.L
        self.SetFont(self.R["FONT_" + font] if isinstance(font, str) else font)
        self.SetBackgroundColour(self.R["COLOR_BG_" + bg] if isinstance(bg, str) else bg)
        self.SetForegroundColour(self.R["COLOR_FG_" + fg] if isinstance(fg, str) else fg)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        self.Bind(wx.EVT_TIMER, lambda evt: Ab.Do(evt.GetTimer().func))
        self.Timers = {}
        self.Animations = {}
        self.NewAnimation("FADEIN", 16, self.SetTransparent, range(55, 256, 50), False, onStart=self.Show)
        self.NewAnimation("FADEOUT", 16, self.SetTransparent, range(200, -1, -50), False, onStop=self.Destroy)
        self.SetTransparent(5)

        self.Main = main(self, **kwargs)
        FrameSizer = wx.BoxSizer(wx.VERTICAL)
        FrameSizer.Add(self.Main, 1, wx.EXPAND)
        self.SetSizer(FrameSizer)
        self.Layout()
        self.Main.SetFocus()
        Ut.DropShadow(self)

    def NewAnimation(self, name, interval, variable, sequence=None, resource=True, repeat=0, onUpdate=None, onStart=None, onStop=None, onRepeat=None):
        self.Timers[name] = wx.Timer(self)
        self.Animations[name] = Animation(self, self.Timers[name], interval, variable, sequence, resource, repeat, self.Refresh if onUpdate is None else onUpdate, onStart, onStop, onRepeat)
        self.Timers[name].func = self.Animations[name].Update

    def Play(self, name, sequence=None, repeat=None):
        for a in self.Animations:
            self.Animations[a].Stop()
        self.Animations[name].Play(sequence, repeat)

    def OnDestroy(self, evt):
        for timer in self.Timers:
            self.Timers[timer].Stop()
        evt.Skip()

    def OnSize(self, evt):
        evt.Skip()
        self.Layout()
        Ut.DropShadow(self)
