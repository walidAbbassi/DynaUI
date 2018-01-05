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

    # --------------------------------------
    def _AddCtrl(self, sizer, label, ctrl, stretchX, stretchY, inline):
        if label:
            name = wx.StaticText(self, label=label, size=wx.Size(self.LABEL_WIDTH, -1), style=wx.ST_ELLIPSIZE_END)
            ctrl.label = name
            if inline:
                if sizer.GetOrientation() == wx.HORIZONTAL:
                    subSizer = sizer
                else:
                    subSizer = self.AddPerpendicularSizer(sizer, stretchY, (stretchX or self.LABEL_WIDTH == -1) and wx.EXPAND)
                subSizer.Add(name, self.LABEL_WIDTH == -1, wx.ALIGN_CENTER | wx.ALL, self.MARGIN)
                subSizer.Add(ctrl, stretchX, (stretchY and wx.EXPAND) | wx.ALL, self.MARGIN)
            else:
                if sizer.GetOrientation() == wx.HORIZONTAL:
                    subSizer = self.AddPerpendicularSizer(sizer, stretchX or self.LABEL_WIDTH == -1, stretchY and wx.EXPAND)
                else:
                    subSizer = sizer
                subSizer.Add(name, 0, (self.LABEL_WIDTH == -1 and wx.EXPAND) | wx.ALL, self.MARGIN)
                subSizer.Add(ctrl, stretchY, (stretchX and wx.EXPAND) | wx.ALL, self.MARGIN)
        else:
            ctrl.label = None
            if sizer.GetOrientation() == wx.HORIZONTAL:
                sizer.Add(ctrl, stretchX, (stretchY and wx.EXPAND) | wx.ALL, self.MARGIN)
            else:
                sizer.Add(ctrl, stretchY, (stretchX and wx.EXPAND) | wx.ALL, self.MARGIN)

    # --------------------------------------
    def AddPerpendicularSizer(self, sizer, *args, **kwargs):
        subSizer = wx.BoxSizer((wx.VERTICAL | wx.HORIZONTAL) ^ sizer.GetOrientation())
        sizer.Add(subSizer, *args, **kwargs)
        return subSizer

    # --------------------------------------
    def AddSeparator(self, sizer, **kwargs):
        edge = UI.Separator(self, orientation=(wx.VERTICAL | wx.HORIZONTAL) ^ sizer.GetOrientation(), **kwargs)
        sizer.Add(edge, 0, wx.EXPAND | wx.ALL, self.MARGIN)
        return edge

    def AddLine(self, sizer, **kwargs):
        line = UI.Line(self, orientation=(wx.VERTICAL | wx.HORIZONTAL) ^ sizer.GetOrientation(), **kwargs)
        sizer.Add(line, 0, wx.EXPAND | wx.ALL, self.MARGIN)
        return line

    def AddSectionHead(self, sizer, tag="", **kwargs):
        head = UI.SectionHead(self, orientation=(wx.VERTICAL | wx.HORIZONTAL) ^ sizer.GetOrientation(), tag=tag, **kwargs)
        sizer.Add(head, 0, wx.EXPAND | wx.ALL, self.MARGIN)
        return head

    # -------------------------------------- # Stretch only on X and not by default
    def AddButton(self, sizer, label="", width=None, height=None, tag="", onClick=None, **kwargs):
        width = width or self.BUTTON_WIDTH
        height = height or self.LINE_HEIGHT
        btn = (UI.ToolNormal if "pics" in kwargs else UI.ButtonNormal)(self, size=wx.Size(width, height), tag=tag, func=onClick, **kwargs)
        self._AddCtrl(sizer, label, btn, width == -1, False, True)
        return btn

    def AddButtonToggle(self, sizer, label="", width=None, height=None, tags=(), toggle=False, onClick=None, **kwargs):
        width = width or self.BUTTON_WIDTH
        height = height or self.LINE_HEIGHT
        btn = (UI.ToolToggle if "pics" in kwargs else UI.ButtonToggle)(self, size=wx.Size(width, height), tag=tags[0], tag2=tags[1], func=onClick, toggle=toggle, **kwargs)
        self._AddCtrl(sizer, label, btn, width == -1, False, True)
        return btn

    def AddButtonBundle(self, sizer, label="", width=None, height=None, rows=1, choices=(), selected=-1, group=None, onClick=None, **kwargs):
        width = width or self.BUTTON_WIDTH
        height = height or self.LINE_HEIGHT
        ctrl = (UI.ToolBundle if "pics" in kwargs else UI.ButtonBundle)
        group = group or Ut.GetRandomName(exclude=self.Groups.keys())
        autoEdge = "edge" not in kwargs
        cols = (len(choices) + rows - 1) // rows
        rows = (len(choices) + cols - 1) // cols
        btns = []
        gridSizer = wx.GridSizer(rows, cols, 0, 0)
        for index, tag in enumerate(choices):
            if autoEdge:
                kwargs["edge"] = ("RB" + ("L" if not index % cols else "") + ("T" if index < cols else ""), "")
            btn = ctrl(self, size=wx.Size(width, height), tag=tag, func=onClick, toggle=index == selected, group=group, **kwargs)
            gridSizer.Add(btn, width == -1)
            btns.append(btn)
        self._AddCtrl(sizer, label, gridSizer, width == -1, False, True)
        bundled = UI.Bundled(btns)
        bundled.label = gridSizer.label
        return bundled

    def AddPickerValue(self, sizer, label="", width=None, height=None, choices=(), selected=-1, **kwargs):
        width = width or self.BUTTON_WIDTH
        height = height or self.LINE_HEIGHT
        btn = UI.PickerValue(self, size=wx.Size(width, height), choices=choices, selected=selected, **kwargs)
        self._AddCtrl(sizer, label, btn, width == -1, False, True)
        return btn

    # -------------------------------------- # Stretch only on X and does it by default
    def AddStaticText(self, sizer, label="", width=-1, height=-1, value="", **kwargs):
        height = height or self.LINE_HEIGHT
        text = UI.StaticText(self, value=value, size=wx.Size(width, height), **kwargs)
        self._AddCtrl(sizer, label, text, width == -1, False, True)
        return text

    def AddLineCtrl(self, sizer, label="", width=-1, height=None, value="", onInput=None, **kwargs):
        height = height or self.LINE_HEIGHT
        text = (UI.TextWithHint if "hint" in kwargs else UI.Text)(self, value=value, size=wx.Size(width, height), **kwargs)
        if onInput:
            text.Bind(wx.EVT_TEXT, onInput)
        self._AddCtrl(sizer, label, text, width == -1, False, True)
        s = text.GetContainingSizer()
        if s.GetOrientation() == wx.HORIZONTAL:
            s.Detach(text)
            s.Add(text, width == -1, wx.ALIGN_CENTER | wx.ALL, self.MARGIN)
        return text

    # -------------------------------------- # Stretch on both X and Y and does it by default
    def AddStaticBitmap(self, sizer, label="", width=-1, height=-1, inline=True, bitmap=wx.NullBitmap, **kwargs):
        pic = UI.StaticBitmap(self, size=wx.Size(width, height), bitmap=bitmap, **kwargs)
        self._AddCtrl(sizer, label, pic, width == -1, height == -1, inline)
        return pic

    def AddTextCtrl(self, sizer, label="", width=-1, height=-1, inline=True, value="", onInput=None, **kwargs):
        kwargs["style"] = wx.TE_MULTILINE | kwargs.get("style", 0)
        text = (UI.TextWithHint if "hint" in kwargs else UI.Text)(self, value=value, size=wx.Size(width, height), **kwargs)
        if onInput:
            text.Bind(wx.EVT_TEXT, onInput)
        self._AddCtrl(sizer, label, text, width == -1, height == -1, inline)
        return text

    def AddStyledTextCtrl(self, sizer, label="", width=-1, height=-1, inline=True, value="", **kwargs):
        text = UI.StyledTextCtrl(self, size=wx.Size(width, height), value=value, **kwargs)
        self._AddCtrl(sizer, label, text, width == -1, height == -1, inline)
        return text

    def AddListBox(self, sizer, label="", width=-1, height=-1, inline=True, choices=(), selected=-1, **kwargs):
        lbox = UI.ListCtrl(self, size=wx.Size(width, height), **kwargs)
        lbox.SetChoices(choices)
        lbox.SetSelection(selected, False)
        self._AddCtrl(sizer, label, lbox, width == -1, height == -1, inline)
        return lbox

    # --------------------------------------
    def AddPickerFile(self, sizer, label="", width=-1, width2=None, height=None, value="", mode="L", wildcard="All files (*.*)|*.*", onSelect=None, **kwargs):
        width2 = width2 or self.LINE_HEIGHT
        height = height or self.LINE_HEIGHT
        text = (UI.TextWithHint if "hint" in kwargs else UI.Text)(self, value=value, size=wx.Size(width, height), **kwargs)
        btn = UI.Button(self, size=wx.Size(width2, height), tag="...", edge=("TRB", ""))
        if mode == "L":
            func = lambda: text.SetValue(Ut.ShowOpenFileDialog(self, self.L.Get("GENERAL_HEAD_LOAD"), wildcard) or text.GetValue())
        else:
            func = lambda: text.SetValue(Ut.ShowSaveFileDialog(self, self.L.Get("GENERAL_HEAD_SAVE"), wildcard) or text.GetValue())
        btn.Func = ((self.GetGrandParent().Disable,), func, onSelect, self.GetGrandParent().Enable, lambda: wx.PostEvent(btn, wx.MouseEvent(wx.wxEVT_LEAVE_WINDOW)))
        subSizer = wx.BoxSizer(wx.HORIZONTAL)
        subSizer.Add(text, width == -1)
        subSizer.Add(btn, width2 == -1)
        self._AddCtrl(sizer, label, subSizer, width == -1, False, True)
        text.label = subSizer.label
        return text

    # --------------------------------------
    def AddStdButton(self, sizer, size=None, onOK=None, onCancel=None, onApply=None):
        size = size or wx.Size(60, self.LINE_HEIGHT)
        if onOK is not None:
            self[1] = UI.ToolNormal(self, size=size, pics=self.R["AP_CHECK"], edge="D", func=onOK)
        if onCancel is not None:
            self[0] = UI.ToolNormal(self, size=size, pics=self.R["AP_CROSS"], edge="D", func=onCancel)
        if onApply is not None:
            self[2] = UI.ToolNormal(self, size=size, pics=self.R["AP_APPLY"], edge="D", func=onApply)
        if sizer.GetOrientation() == wx.HORIZONTAL:
            subSizer = sizer
            sizer.Add(4, 4, 1)
        else:
            subSizer = self.AddPerpendicularSizer(sizer, 0, wx.ALIGN_RIGHT)
        for i in (1, 0, 2):
            if i in self:
                subSizer.Add(self[i], 0, wx.ALL, self.MARGIN)


# ====================================================== BaseHead ======================================================
class BaseHead(UI.Button):
    def __init__(self, parent, buttons=True, **kwargs):
        super().__init__(parent, size=wx.Size(-1, Va.SETTINGS["DLG_HEAD"]), tag=(parent.GetTitle(), "L", 7, 0), fg=parent.R["COLOR_DLG_HEAD_FG"]["00"], edge="D", **kwargs)
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
    def __init__(self, parent, minSize=wx.Size(120, 10), **kwargs):
        super().__init__(parent, size=wx.Size(8, 8), **kwargs)
        self.Frame = parent
        self.minSize = minSize
        self.leftDown = False
        self.lastMousePos = None
        self.lastFrameSize = None
        self.sizeRect = None
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
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
            self.sizeRect.SetSize((max(x, self.minSize[0]), max(y, Va.SETTINGS["DLG_HEAD"] + self.minSize[1])))
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
        self.SetBackgroundColour(self.R["COLOR_BG_" + bg] if isinstance(bg, str) and not bg.startswith("#") else bg)
        self.SetForegroundColour(self.R["COLOR_FG_" + fg] if isinstance(fg, str) and not fg.startswith("#") else fg)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        self.Bind(wx.EVT_TIMER, lambda evt: Ab.Do(evt.GetTimer().func))
        self.Timers = {}
        self.Animations = {}
        self.NewAnimation("FADEIN", 16, self.SetTransparent, range(55, 256, 50), False, onStart=self.Show, onStop=(self.Bind, wx.EVT_ACTIVATE, self.OnActivation))
        self.NewAnimation("FADEOUT", 16, self.SetTransparent, range(200, -1, -50), False, onStart=(self.Unbind, wx.EVT_ACTIVATE), onStop=self.DoDestroy)
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
    def DoDestroy(self):
        if self.GetCapture():
            self.GetCapture().ReleaseMouse()  # Why is this not a default behavior !?
        self.Destroy()

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
        if hasattr(self.Main, "OnClose"):
            self.Main.OnClose()
        else:
            self.Play("FADEOUT")


# =================================================== BaseMiniDialog ===================================================
class BaseMiniDialog(wx.Frame):
    def __init__(self, parent=None, pos=wx.DefaultPosition, size=wx.DefaultSize, invoker=None, font="N", bg="L", fg="L", main=None, **kwargs):
        super().__init__(parent=parent, pos=pos, size=size, style=wx.BORDER_NONE | wx.FRAME_NO_TASKBAR | (wx.FRAME_FLOAT_ON_PARENT if parent else 0))
        invoker = parent or invoker
        self.R = invoker.R
        self.S = invoker.S
        self.L = invoker.L
        self.SetFont(self.R["FONT_" + font] if isinstance(font, str) else font)
        self.SetBackgroundColour(self.R["COLOR_BG_" + bg] if isinstance(bg, str) and not bg.startswith("#") else bg)
        self.SetForegroundColour(self.R["COLOR_FG_" + fg] if isinstance(fg, str) and not fg.startswith("#") else fg)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        self.Bind(wx.EVT_TIMER, lambda evt: Ab.Do(evt.GetTimer().func))
        self.Timers = {}
        self.Animations = {}
        self.NewAnimation("FADEIN", 16, self.SetTransparent, range(55, 256, 50), False, onStart=self.Show)
        self.NewAnimation("FADEOUT", 16, self.SetTransparent, range(200, -1, -50), False, onStop=self.DoDestroy)
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

    def DoDestroy(self):
        if self.GetCapture():
            self.GetCapture().ReleaseMouse()  # Why is this not a default behavior !?
        self.Destroy()

    def OnDestroy(self, evt):
        for timer in self.Timers:
            self.Timers[timer].Stop()
        evt.Skip()

    def OnSize(self, evt):
        evt.Skip()
        self.Layout()
        Ut.DropShadow(self)
