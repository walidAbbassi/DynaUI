# -*- coding: utf-8 -*-


import wx
from wx import stc
from ..core import BaseControl, DynaUIMixin
from .. import utility as Ut

__all__ = [
    "Text",
    "TextWithHint",
    "StyledTextCtrl",
    "StaticText",
    "StaticBitmap",
    "Separator",
    "Line",
    "SectionHead",
    "SwitchingText",
]


# =================================================== Miscellaneous ====================================================
class Text(wx.TextCtrl, DynaUIMixin):
    def __init__(self, parent, value="", font=None, bg="D", fg="L", edge=True, style=0, *args, **kwargs):
        style |= (wx.BORDER_SIMPLE if edge else wx.BORDER_NONE)
        wx.TextCtrl.__init__(self, parent, value=value, style=style, *args, **kwargs)
        DynaUIMixin.__init__(self, parent, font=font, bg=bg, fg=fg)


# =================================================== Miscellaneous ====================================================
class TextWithHint(wx.TextCtrl, DynaUIMixin):  # Only GetValue/SetValue/AppendText/Clear are reimplemented!
    def __init__(self, parent, value="", hint="", font=None, bg="D", fg="L", edge=True, style=0, *args, **kwargs):
        style |= (wx.BORDER_SIMPLE if edge else wx.BORDER_NONE)
        wx.TextCtrl.__init__(self, parent, value=value, style=style, *args, **kwargs)
        DynaUIMixin.__init__(self, parent, font=font, bg=bg, fg=fg)
        self.fg = fg
        self.hint = hint
        self.Bind(wx.EVT_TEXT, self.OnText)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnLeave)
        self.Bind(wx.EVT_SET_FOCUS, self.OnEnter)
        if self.IsEmpty():
            self.showMessage = True
            self.SetFG("D")
            self.ChangeValue(self.hint)
        else:
            self.showMessage = False
            self.SetFG(self.fg)

    def Clear(self):
        if not self.showMessage:
            super().Clear()
            if self.IsEmpty():
                self.showMessage = True
                self.ChangeValue(self.hint)
                self.SetFG("D")

    def AppendText(self, text):
        if self.showMessage:
            self.SetFG(self.fg)
        super().AppendText(text)

    def SetValue(self, value):
        if self.showMessage:
            self.SetFG(self.fg)
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
            self.SetFG("D")
        evt.Skip()

    def OnEnter(self, evt):
        if self.showMessage:
            self.ChangeValue("")
            self.SetFG(self.fg)
        evt.Skip()


# =================================================== Miscellaneous ====================================================
class StyledTextCtrl(stc.StyledTextCtrl, DynaUIMixin):
    def __init__(self, parent, value="", font=None, bg="D", fg="L", edge=False, hideScrollBar=False, style=0, *args, **kwargs):
        stc.StyledTextCtrl.__init__(self, parent, style=style | (wx.BORDER_SIMPLE if edge else wx.BORDER_NONE), *args, **kwargs)
        DynaUIMixin.__init__(self, parent, font=font, bg=bg, fg=fg)
        if hideScrollBar:
            self.SetUseVerticalScrollBar(False)
            self.SetUseHorizontalScrollBar(False)
        self.SetCaretWidth(2)
        self.SetCaretForeground(self.ForegroundColour)
        self.SetMarginLeft(4)
        self.SetMarginRight(4)
        self.SetMarginWidth(1, 0)
        self.SetEOLMode(stc.STC_EOL_LF)
        self.SetLexer(stc.STC_LEX_NULL)
        self.SetIndent(4)
        self.SetUseTabs(False)
        self.SetTabWidth(4)
        self.SetScrollWidth(self.GetSize()[0])
        self.SetScrollWidthTracking(True)
        self.SetSelBackground(True, self.R["COLOR_BG_B"])
        self.StyleSetBackground(stc.STC_STYLE_DEFAULT, self.BackgroundColour)
        self.StyleSetForeground(stc.STC_STYLE_DEFAULT, self.ForegroundColour)
        self.StyleSetFont(stc.STC_STYLE_DEFAULT, self.Font)
        self.StyleClearAll()
        self.SetValue(value)


# =================================================== Miscellaneous ====================================================
class StaticText(wx.StaticText, DynaUIMixin):
    def __init__(self, parent, value="", font=None, bg="L", fg="L", style=0, *args, **kwargs):
        wx.StaticText.__init__(self, parent, label=value, style=style | wx.BORDER_NONE, *args, **kwargs)
        DynaUIMixin.__init__(self, parent, font=font, bg=bg, fg=fg)

    def SetValue(self, value):
        self.SetLabel(value)

    def GetValue(self):
        self.GetLabel()


# =================================================== Miscellaneous ====================================================
class StaticBitmap(BaseControl):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, bitmap=wx.NullBitmap, bg="L"):
        super().__init__(parent, pos=pos, size=size, bg=bg)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
        self.NullBitmap = wx.Bitmap(0, 0)
        self.Bitmap = bitmap or self.NullBitmap
        if size is wx.DefaultSize:
            self.SetInitialSize(self.Bitmap.GetSize())
        self.leftDown = False
        self.leftPos = None
        self.offset = (0, 0)
        self.lastOffset = (0, 0)

    def SetBitmap(self, bitmap):
        self.Bitmap = bitmap
        self.ReDraw()

    def SetNullBitmap(self):
        self.Bitmap = self.NullBitmap
        self.ReDraw()

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self.Bitmap, *self.offset, 1)

    def OnSize(self, evt):
        evt.Skip()
        self.SetOffset(self.offset)

    def OnMouse(self, evt):
        evtType = evt.GetEventType()
        evtPos = evt.GetPosition()
        if evtType == wx.wxEVT_LEFT_DOWN or evtType == wx.wxEVT_LEFT_DCLICK:
            if not self.HasCapture(): self.CaptureMouse()
            self.leftDown = True
            self.leftPos = evtPos
        elif evtType == wx.wxEVT_LEFT_UP:
            if self.HasCapture(): self.ReleaseMouse()
            self.leftDown = False
            self.leftPos = None
            self.lastOffset = self.offset
        elif evtType == wx.wxEVT_MOTION and self.leftDown:
            self.SetOffset(evtPos - self.leftPos + self.lastOffset)
            self.ReDraw()
        evt.Skip()

    def OnCaptureLost(self, evt):
        self.leftDown = False
        self.leftPos = None
        self.lastOffset = self.offset

    def SetOffset(self, offset):
        x, y = offset
        w, h = self.GetSize()
        bw, bh = self.Bitmap.GetSize()
        self.offset = (min(max(x, w - bw), 0), min(max(y, h - bh), 0))


# =================================================== Miscellaneous ====================================================
class Separator(BaseControl):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.Size(2, 2), orientation=wx.VERTICAL):
        super().__init__(parent, pos=pos, size=size)
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
class Line(BaseControl):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.Size(1, 1), orientation=wx.HORIZONTAL, bg="L", fg="L"):
        super().__init__(parent, pos=pos, size=size, bg=bg, fg=fg)
        self.Bind(wx.EVT_PAINT, self.OnPaintV if orientation == wx.VERTICAL else self.OnPaintH)

    def OnPaintV(self, evt):
        w, h = self.GetSize()
        h2 = h >> 1
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.GradientFillLinear(wx.Rect(0, 0, w, h2), self.BackgroundColour, self.ForegroundColour, wx.BOTTOM)
        dc.GradientFillLinear(wx.Rect(0, h2, w, h2), self.BackgroundColour, self.ForegroundColour, wx.UP)

    def OnPaintH(self, evt):
        w, h = self.GetSize()
        w2 = w >> 1
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.GradientFillLinear(wx.Rect(0, 0, w2, h), self.BackgroundColour, self.ForegroundColour, wx.RIGHT)
        dc.GradientFillLinear(wx.Rect(w2, 0, w2, h), self.BackgroundColour, self.ForegroundColour, wx.LEFT)


# =================================================== Miscellaneous ====================================================
class SectionHead(BaseControl):  # TODO rework
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, orientation=wx.HORIZONTAL, tag=("", "C"), shape="B", zOrder=0, font=None, bg="L", bg2="D", fg="B"):
        super().__init__(parent, pos=pos, size=size, font=font, bg=bg, fg=fg)
        self.Bg2 = self.R["BRUSH_BG_" + bg2] if isinstance(bg2, str) else bg2
        self.Orientation = orientation
        if isinstance(tag, (tuple, list)):
            self.SetLabel(tag[0])
            self.SetTagPos(tag[1])
        else:
            self.SetLabel(tag)
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
class SwitchingText(BaseControl):  # TODO doesn't work on non MSW
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
