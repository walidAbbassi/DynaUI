# -*- coding: utf-8 -*-


import wx
from ..core import BaseControl
from .. import utility as Ut

__all__ = [
    "Text",
    "TextWithHint",
    "Separator",
    "SectionHead",
    "StaticBitmap",

    "Label",
    "SwitchingText",
]


# =================================================== Miscellaneous ====================================================
class Text(wx.TextCtrl):
    def __init__(self, parent, style=wx.BORDER_SIMPLE, *args, **kwargs):
        super().__init__(parent, *args, **kwargs, style=style)
        self.R = parent.R
        self.S = parent.S
        self.L = parent.L
        self.SetBackgroundColour(self.R["COLOR_BG_D"])
        self.SetForegroundColour(self.R["COLOR_FG_L"])


# =================================================== Miscellaneous ====================================================
class TextWithHint(wx.TextCtrl):  # Only GetValue/SetValue/AppendText are reimplemented!
    def __init__(self, parent, hint="", style=wx.BORDER_SIMPLE, *args, **kwargs):
        super().__init__(parent, *args, **kwargs, style=style)
        self.hint = hint
        self.R = parent.R
        self.S = parent.S
        self.L = parent.L
        self.SetBackgroundColour(self.R["COLOR_BG_D"])
        self.Bind(wx.EVT_TEXT, self.OnText)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnLeave)
        self.Bind(wx.EVT_SET_FOCUS, self.OnEnter)
        if self.IsEmpty():
            self.showMessage = True
            self.SetForegroundColour(self.R["COLOR_FG_D"])
            self.ChangeValue(self.hint)
        else:
            self.showMessage = False
            self.SetForegroundColour(self.R["COLOR_FG_L"])

    def AppendText(self, text):
        if self.showMessage:
            self.SetForegroundColour(self.R["COLOR_FG_L"])
        super().AppendText(text)

    def SetValue(self, value):
        if self.showMessage:
            self.SetForegroundColour(self.R["COLOR_FG_L"])
        super().SetValue(value)

    def GetValue(self):
        if self.showMessage:
            return ""
        else:
            return super().GetValue()

    def OnText(self, evt):
        if self.showMessage:
            self.showMessage = False
        evt.Skip()

    def OnLeave(self, evt):
        if self.IsEmpty():
            self.showMessage = True
            self.ChangeValue(self.hint)
            self.SetForegroundColour(self.R["COLOR_FG_D"])
        evt.Skip()

    def OnEnter(self, evt):
        if self.showMessage:
            self.ChangeValue("")
            self.SetForegroundColour(self.R["COLOR_FG_L"])
        evt.Skip()


# =================================================== Miscellaneous ====================================================
class Separator(BaseControl):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.Size(2, 2), orientation=wx.VERTICAL, bg="L"):
        super().__init__(parent, pos=pos, size=size, bg=bg)
        self.Bind(wx.EVT_PAINT, self.OnPaintV if orientation == wx.VERTICAL else self.OnPaintH)

    def OnPaintV(self, evt):
        w, h = self.GetSize()
        w2, h2 = w >> 1, h >> 1
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(self.R["PEN_EDGE_D"])
        dc.DrawLine(w2 - 1, 0, w2 - 1, h)
        dc.SetPen(self.R["PEN_EDGE_L"])
        dc.DrawLine(w2, 0, w2, h)

    def OnPaintH(self, evt):
        w, h = self.GetSize()
        w2, h2 = w >> 1, h >> 1
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(self.R["PEN_EDGE_D"])
        dc.DrawLine(0, h2 - 1, w, h2 - 1)
        dc.SetPen(self.R["PEN_EDGE_L"])
        dc.DrawLine(0, h2, w, h2)


# =================================================== Miscellaneous ====================================================
class SectionHead(BaseControl):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, orientation=wx.HORIZONTAL, label=("", "C"), shape="B", zOrder=0, font=None, bg="L", bg2="D", fg="B"):
        super().__init__(parent, pos=pos, size=size, font=font, bg=bg, fg=fg)
        self.Bg2 = self.R["BRUSH_BG_" + bg2] if isinstance(bg2, str) else bg2
        self.Orientation = orientation
        if isinstance(label, (tuple, list)):
            self.SetLabel(label[0])
            self.SetTagPos(label[1])
        else:
            self.SetLabel(label)
            self.SetTagPos("C")
        self.Render(shape, zOrder)
        if size is wx.DefaultSize:
            size = self.Buffer.GetSize()
            size[self.Orientation == wx.VERTICAL] = -1
            self.SetInitialSize(size)
        self.Bind(wx.EVT_PAINT, self.OnPaintV if orientation == wx.VERTICAL else self.OnPaintH)

    def SetTagPos(self, position):
        self.TagPos = position

    def OnPaintV(self, evt):
        w, h = self.GetSize()
        w2, h2 = w >> 1, h >> 1
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(self.R["PEN_EDGE_D"])
        dc.DrawLine(w2 - 1, 0, w2 - 1, h)
        dc.SetPen(self.R["PEN_EDGE_L"])
        dc.DrawLine(w2, 0, w2, h)
        self.DrawTitleX(dc)

    def OnPaintH(self, evt):
        w, h = self.GetSize()
        w2, h2 = w >> 1, h >> 1
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(self.R["PEN_EDGE_D"])
        dc.DrawLine(0, h2 - 1, w, h2 - 1)
        dc.SetPen(self.R["PEN_EDGE_L"])
        dc.DrawLine(0, h2, w, h2)
        self.DrawTitleX(dc)

    def DrawTitleX(self, dc):
        w, h = self.GetSize()
        tw, th = self.Buffer.GetSize()
        if "L" in self.TagPos:
            x = 0
        elif "R" in self.TagPos:
            x = w - tw
        else:
            x = (w - tw) >> 1
        if "T" in self.TagPos:
            y = 0
        elif "B" in self.TagPos:
            y = h - th
        else:
            y = (h - th) >> 1
        dc.DrawBitmap(self.Buffer, x, y)

    def Render(self, shape, zOrder):
        w, h = Ut.GetTextExtent(self, self.Label)
        h = h + (h & 1) + 8
        w = w + (w & 1) + h
        h2 = h >> 1
        self.Buffer = wx.Bitmap(w, h)
        mdc = wx.MemoryDC(self.Buffer)
        mdc.SetFont(self.GetFont())
        mdc.SetBackground(self.BackgroundBrush)
        mdc.SetTextForeground(self.GetForegroundColour())
        mdc.Clear()
        if shape == "S":
            pointsO = ((0, h2 - 1), (0, 0), (w - 1, 0), (w - 1, h2))
            pointsI = ((0, h2), (0, h - 1), (w - 1, h - 1), (w - 1, h2 - 1))
        elif shape == "C":
            pointsO = ((0, h2 - 1), (h2 - 1, 0), (w - 1, 0), (w - 1, h2))
            pointsI = ((0, h2), (0, h - 1), (w - h2, h - 1), (w, h2 - 1))
        elif shape == "L":
            pointsO = ((0, h2 - 1), (h2 - 1, 0), (w - 1, 0), (w - 1, h2))
            pointsI = ((0, h2), (h2 - 1, h - 1), (w - 1, h - 1), (w - 1, h2 - 1))
        elif shape == "R":
            pointsO = ((0, h2 - 1), (0, 0), (w - h2, 0), (w, h2))
            pointsI = ((0, h2), (0, h - 1), (w - h2, h - 1), (w, h2 - 1))
        else:
            pointsO = ((0, h2 - 1), (h2 - 1, 0), (w - h2, 0), (w, h2))
            pointsI = ((0, h2), (h2 - 1, h - 1), (w - h2, h - 1), (w, h2 - 1))
        if zOrder == 1:
            pointsO, pointsI = pointsI, pointsO
        mdc.SetPen(self.R["PEN_EDGE_D"])
        mdc.DrawLines(pointsO)
        mdc.SetPen(self.R["PEN_EDGE_L"])
        mdc.DrawLines(pointsI)
        mdc.SetBrush(self.Bg2)
        mdc.FloodFill(w // 2, h2, self.GetBackgroundColour())
        mdc.DrawText(self.Label, h2, 4)
        mdc.SelectObject(wx.NullBitmap)
        if self.Orientation == wx.VERTICAL:
            self.Buffer = self.Buffer.ConvertToImage().Rotate90().Rotate180().ConvertToBitmap()


# =================================================== Miscellaneous ====================================================
class StaticBitmap(BaseControl):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, bitmap=wx.NullBitmap, bg="L"):
        super().__init__(parent, pos=pos, size=size, bg=bg)
        self.SetBitmap(bitmap if bitmap else wx.Bitmap(0, 0))
        if size is wx.DefaultSize:
            self.SetInitialSize(self.Bitmap.GetSize())

    def SetBitmap(self, bitmap):
        self.Bitmap = bitmap

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self.Bitmap, 0, 0, 1)


# =================================================== Miscellaneous ====================================================
class Label(BaseControl):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, label="", target=None):
        super().__init__(parent, pos=pos, size=size)
        self.SetLabel(label)
        self.Resources = self.R["BRUSH_SET_L"]
        self.Brush = self.Resources["00"]
        if target:
            self.Bind(wx.EVT_MOUSE_EVENTS, lambda evt: wx.PostEvent(target, evt))
            self.Bind(wx.EVT_ENTER_WINDOW, lambda evt: (self.Play("ENTER"), evt.Skip()))
            self.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: (self.Play("LEAVE"), evt.Skip()))
            self.NewAnimation("ENTER", 25, "Brush", ("80", "FF"), True)
            self.NewAnimation("LEAVE", 25, "Brush", ("C0", "80", "40", "00"), True)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        w, h = self.GetSize()
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(self.Brush)
        dc.DrawRectangle(0, 0, w, h)
        tw, th, lh = dc.GetFullMultiLineTextExtent(self.Label)
        dc.DrawText(self.GetLabel(), (w - tw) >> 1, (h - th) >> 1)


# =================================================== Miscellaneous ====================================================
class SwitchingText(BaseControl):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, values=(),
                 font=None, res=None, bg="L", fg="L", edge=None):
        super().__init__(parent, pos=pos, size=size, font=font, res=res, bg=bg, fg=fg, edge=edge)
        self.SetValues(values)
        self.Render()
        self.NewAnimation("SWITCH", 50, "CurrentFrame", range(21), False, repeat=-1, onUpdate=((self.Refresh,), self.Update), onRepeat=lambda: self.Values.append(self.Values.pop(0)))
        self.Bind(wx.EVT_ENTER_WINDOW, lambda evt: self.Pause("SWITCH", -1))
        self.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.Pause("SWITCH", 0))
        self.Play("SWITCH")

    def SetValues(self, values):
        self.Values = [(v, (0, 0)) for v in values]

    def Render(self):  # Call Render when values, color, font, or size is changed
        self.CurrentFrame = 0
        bg = Ut.C2S(self.GetBackgroundColour())
        fg = Ut.C2S(self.GetForegroundColour())
        self.Colors = [(Ut.AlphaBlend(bg, fg, 1 - alpha * 0.1), Ut.AlphaBlend(bg, fg, alpha * 0.1)) for alpha in range(11)]
        for i in range(10):
            self.Colors.append(self.Colors[-1])
        w, h = self.GetSize()
        for index in range(len(self.Values)):
            text = self.Values[index][0]
            tw, th = Ut.GetTextExtent(self, text)
            self.Values[index] = (text, ((w - tw) >> 1, (h - th) >> 1))

    def OnPaint(self, evt):
        w, h = self.GetSize()
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
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
        c1, c2 = self.Colors[self.CurrentFrame]
        x0, y0 = self.Values[0][1]
        x1, y1 = self.Values[1][1]
        if self.CurrentFrame > 5:
            dc.SetTextForeground(c1)
            dc.DrawText(self.Values[0][0], x0, y0)
            dc.SetTextForeground(c2)
            dc.DrawText(self.Values[1][0], x1, y1)
        else:
            dc.SetTextForeground(c2)
            dc.DrawText(self.Values[1][0], x1, y1)
            dc.SetTextForeground(c1)
            dc.DrawText(self.Values[0][0], x0, y0)
