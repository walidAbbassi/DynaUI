# -*- coding: utf-8 -*-


import wx
from ..core import BaseControl
from .. import abstract as Ab
from .. import variable as Va
from .. import utility as Ut

__all__ = ["Scrolled", "ImageViewer", "ListCtrl"]


# ================================================== Scrolled Window ===================================================
# TODO this whole file need a rework

class ScrollBar(object):
    def __init__(self, parent, orientation):
        self.W = parent
        self.A = wx.Rect()  # Scrollbar Area
        self.R = wx.Rect()  # ScrollBar Rect
        self.O = {wx.VERTICAL: 1, wx.HORIZONTAL: 0}[orientation]
        self.HasFocus = False
        self.Activate = False
        self.Show = True
        self.LeftPos = None
        self.LastOffset = None
        (self.A.SetHeight, self.A.SetWidth)[self.O](Va.SETTINGS["SCROLL_DIAMETER"])
        (self.R.SetHeight, self.R.SetWidth)[self.O](Va.SETTINGS["SCROLL_DIAMETER"])
        self._PositionA = (self.A.SetY, self.A.SetX)[self.O]
        self._PositionR = (self.R.SetY, self.R.SetX)[self.O]
        self._LengthA = (self.A.SetWidth, self.A.SetHeight)[self.O]
        self._LengthR = (self.R.SetWidth, self.R.SetHeight)[self.O]
        self._Distance = (self.R.SetX, self.R.SetY)[self.O]

    def Draw(self, dc):
        if self.Activate:
            dc.SetBrush(self.W.R["BRUSH_SET_D"]["80"])
        elif self.HasFocus:
            dc.SetBrush(self.W.R["BRUSH_SET_D"]["FF"])
        else:
            dc.SetBrush(self.W.R["BRUSH_SET_D"]["00"])
        dc.DrawRectangle(self.R)

    def Update(self):
        # Update XY
        position = self.W.GetSize()[1 - self.O] - Va.SETTINGS["SCROLL_DIAMETER"]
        self._PositionA(position)
        self._PositionR(position)
        # Update WH
        self._LengthA(self.W.VSize[self.O] + 2)
        # Update wh
        self._LengthR(max(self.A.GetSize()[self.O] * self.W.VSize[self.O] // self.W.ASize[self.O], Va.SETTINGS["SCROLL_DIAMETER"]))  # DIVISION
        # Update xy
        self.Updatexy()

    def Updatexy(self):
        self._Distance(max(min(self.W.GetViewPoint()[self.O] * self.A.GetSize()[self.O] // self.W.ASize[self.O], self.A.GetSize()[self.O] - self.R.GetSize()[self.O]), 0))  # DIVISION

    def HandleMouse(self, evtType, evtPos):
        if evtType == wx.wxEVT_LEFT_DOWN:
            if not self.W.HasCapture():
                self.W.CaptureMouse()
            self.Activate = True
            if not self.R.Contains(evtPos):
                delta = (evtPos[self.O] - (self.R.GetSize()[self.O] >> 1) - self.R.GetPosition()[self.O]) * self.W.ASize[self.O] // (self.A.GetSize()[self.O] * self.W.Step[self.O])  # DIVISION
                if delta:
                    self.W.SetOffset(self.O, self.W.Offset[self.O] + delta)
                    self.Updatexy()
            self.LeftPos = evtPos
            self.LastOffset = [i for i in self.W.Offset]
        elif evtType == wx.wxEVT_LEFT_UP:
            if self.W.HasCapture():
                self.W.ReleaseMouse()
            self.Activate = False
        elif evtType == wx.wxEVT_MOTION and self.Activate:
            delta = (evtPos[self.O] - self.LeftPos[self.O]) * self.W.ASize[self.O] // (self.A.GetSize()[self.O] * self.W.Step[self.O])  # DIVISION
            if delta:
                self.W.SetOffset(self.O, self.LastOffset[self.O] + delta)
                self.Updatexy()


class Scrolled(BaseControl):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 font=None, res=None, bg="L", fg="L", edge="D", async=False, fpsLimit=120):
        super().__init__(parent, pos=pos, size=size, style=style | wx.BORDER_NONE | wx.WANTS_CHARS, font=font, res=res, bg=bg, fg=fg, edge=edge, async=async, fpsLimit=fpsLimit)
        self.Unbind(wx.EVT_PAINT)
        self.Bind(wx.EVT_PAINT, self.DoPaint)
        self.Bind(wx.EVT_SIZE, self.SetWindowSize)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnWheel)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.HandleMouse)
        self.ASize = [20, 20]  # Actual
        self.VSize = [20, 20]  # Visible
        self.VRect = wx.Rect(1, 1, 20, 20)
        self.Offset = [0, 0]  # In steps
        self.Step = [0, 0]  # In pixels
        self.ScrollBar = [None, None]
        self.MaxOffset = [0, 0]
        self.SetStep = self.AddScrollBar
        self.ScrollBarEdge = "L" if self.Edge[3] else "D"

    def AddScrollBar(self, step):
        self.Step = max(step[0], 0), max(step[1], 0)
        self.ScrollBar[0] = ScrollBar(self, wx.HORIZONTAL) if self.Step[0] > 0 else None
        self.ScrollBar[1] = ScrollBar(self, wx.VERTICAL) if self.Step[1] > 0 else None
        self.SetMaxOffset()

    def DoPaint(self, evt):
        w, h = self.GetSize()
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        dc.SetPen(self.R["PEN_EDGE_L"])
        if self.Edge[0]: dc.DrawLine(0, 0, 0, h)
        if self.Edge[1]: dc.DrawLine(0, 0, w, 0)
        if self.Edge[2]: dc.DrawLine(w - 1, 0, w - 1, h)
        if self.Edge[3]: dc.DrawLine(0, h - 1, w, h - 1)
        if self.ScrollBarEdge == "L":
            for sb in self.ScrollBar:
                if sb and sb.Show: sb.Draw(dc)
        dc.SetPen(self.R["PEN_EDGE_D"])
        if self.Edge[4]: dc.DrawLine(0, 0, 0, h)
        if self.Edge[5]: dc.DrawLine(0, 0, w, 0)
        if self.Edge[6]: dc.DrawLine(w - 1, 0, w - 1, h)
        if self.Edge[7]: dc.DrawLine(0, h - 1, w, h - 1)
        if self.ScrollBarEdge == "D":
            for sb in self.ScrollBar:
                if sb and sb.Show: sb.Draw(dc)
        dc.SetClippingRegion(self.VRect)
        self.OnPaint(dc)

    def GetActualSize(self):
        return self.ASize

    def GetVisibleSize(self):
        return self.VSize

    def GetViewPoint(self):  # In pixels
        return self.Offset[0] * self.Step[0], self.Offset[1] * self.Step[1]

    def GetMaxOffset(self):
        return self.MaxOffset

    def SetMaxOffset(self):
        for d in (0, 1):
            self.MaxOffset[d] = (max(self.ASize[d] - self.VSize[d] + self.Step[d] - 1, 0) // self.Step[d]) if self.Step[d] else 0  # DIVISION

    def SetOffset(self, d, value):
        old = self.Offset[d]
        new = min(max(value, 0), self.MaxOffset[d])
        if old != new:
            self.Offset[d] = new
            self.ReDraw()

    def Scroll(self, d, delta):
        if not delta: return
        self.SetOffset(d, self.Offset[d] + delta)
        self.ScrollBar[d].Updatexy()

    def SetActualSize(self):
        w, h = self.CalculateActualSize()
        self.ASize = [max(w, 4), max(h, 4)]
        self.EvaluateScrollBarVisibility()
        self.SetMaxOffset()
        self.SetOffset(0, self.Offset[0])
        self.SetOffset(1, self.Offset[1])
        for sb in self.ScrollBar:
            if sb: sb.Update()

    def SetWindowSize(self, evt):
        self.EvaluateScrollBarVisibility()
        self.SetMaxOffset()
        self.SetOffset(0, self.Offset[0])
        self.SetOffset(1, self.Offset[1])
        for sb in self.ScrollBar:
            if sb: sb.Update()
        self.OnSize()
        evt.Skip()

    def SetVisibleSize(self):
        self.VSize = self.GetSize() - (1, 1) - (Va.SETTINGS["SCROLL_DIAMETER"] if self.ScrollBar[1] and self.ScrollBar[1].Show else 1, Va.SETTINGS["SCROLL_DIAMETER"] if self.ScrollBar[0] and self.ScrollBar[0].Show else 1)
        self.VRect.SetSize(self.VSize)

    def EvaluateScrollBarVisibility(self):
        if self.ScrollBar[0]:
            self.ScrollBar[0].Show = self.ASize[0] > self.GetSize()[0] - 2
        if self.ScrollBar[1]:
            self.ScrollBar[1].Show = self.ASize[1] > self.GetSize()[1] - 2
        self.SetVisibleSize()
        newVisibility = (self.ScrollBar[0].Show if self.ScrollBar[0] else None, self.ScrollBar[1].Show if self.ScrollBar[1] else None)
        if newVisibility == (False, True):
            self.ScrollBar[0].Show = self.ASize[0] > self.VSize[0]
            if self.ScrollBar[0].Show:
                self.SetVisibleSize()
        elif newVisibility == (True, False):
            self.ScrollBar[1].Show = self.ASize[1] > self.VSize[1]
            if self.ScrollBar[1].Show:
                self.SetVisibleSize()

    def OnWheel(self, evt):
        if self.ScrollBar[0] is None and self.ScrollBar[1] is None: return
        if self.ScrollBar[0] is None:
            d = 1
        elif self.ScrollBar[1] is None:
            d = 0
        else:
            d = (1, 0)[evt.ControlDown()]
        self.Scroll(d, (-1, 1)[evt.GetWheelRotation() < 0] * Va.SETTINGS["SCROLL_UNIT"] * (Va.SETTINGS["SCROLL_MULTIPLIER"] if evt.ShiftDown() else 1))

    def HandleMouse(self, evt):
        evtType = evt.GetEventType()
        evtPos = evt.GetPosition()
        handled = False
        for sb in self.ScrollBar:
            if sb and sb.Show:
                if sb.HasFocus != sb.R.Contains(evtPos):
                    sb.HasFocus = not sb.HasFocus
                    if not sb.Activate:
                        self.ReDraw()
                if sb.Activate or (sb.A.Contains(evtPos) and evtType == wx.wxEVT_LEFT_DOWN):
                    sb.HandleMouse(evtType, evtPos)
                    handled = True
                    self.ReDraw()
        if not handled:
            self.OnMouse(evt)
        evt.Skip()  # wheel

    def CalculateActualSize(self):  # Re-implemented by subclass
        raise NotImplementedError

    def OnSize(self):  # Re-implemented by subclass
        pass

    def OnPaint(self, dc):  # Re-implemented by subclass
        pass

    def OnMouse(self, evt):  # Re-implemented by subclass
        pass


# ======================================================================================================================
class ImageViewer(Scrolled):
    def __init__(self, parent, bmp=None, size=wx.DefaultSize):
        super().__init__(parent, size=size)
        self.Bmp = bmp if bmp else wx.Bitmap(0, 0)
        self.SetActualSize()
        self.AddScrollBar((1, 1))
        self.LeftDown = False
        self.LastPos = None
        self.LastOffset = None
        self.CurrentPos = None
        self.NewTimer("Slide", self.OnSlide)

    def CalculateActualSize(self):
        return self.Bmp.GetSize()

    def OnPaint(self, dc):
        x, y = self.GetViewPoint()
        dc.DrawBitmap(self.Bmp, 1 - x, 1 - y)

    def OnMouse(self, evt):
        evtType = evt.GetEventType()
        evtPos = evt.GetPosition()
        if evtType == wx.wxEVT_LEFT_DOWN:
            self.SetFocus()
            self.LeftDown = True
            self.LastPos = self.ClientToScreen(evtPos)
            self.LastOffset = [i for i in self.Offset]
            self.SetCursor(self.R["CURSOR_MOVING"])
            if not self.HasCapture():
                self.CaptureMouse()
        elif evtType == wx.wxEVT_LEFT_UP:
            self.LeftDown = False
            self.SetCursor(self.R["CURSOR_NORMAL"])
            if self.HasCapture():
                self.ReleaseMouse()
        elif evtType == wx.wxEVT_MIDDLE_DOWN:
            self.SetCursor(self.R["CURSOR_MOVING"])
            self.LastPos = self.ClientToScreen(evtPos)
            self.LastOffset = [i for i in self.Offset]
            self.StartTimer("Slide", 16, wx.TIMER_CONTINUOUS)
            if not self.HasCapture():
                self.CaptureMouse()
        elif evtType == wx.wxEVT_MIDDLE_UP:
            self.SetCursor(self.R["CURSOR_NORMAL"])
            self.StopTimer("Slide")
            if self.HasCapture():
                self.ReleaseMouse()
        elif evtType == wx.wxEVT_MOTION:
            self.CurrentPos = self.ClientToScreen(evtPos)
            if self.LeftDown:
                dx, dy = self.LastPos - self.CurrentPos
                self.SetOffset(0, self.LastOffset[0] + 1.0 * dx / self.Step[0])
                self.SetOffset(1, self.LastOffset[1] + 1.0 * dy / self.Step[1])
                self.ScrollBar[0].Updatexy()
                self.ScrollBar[1].Updatexy()

    def OnSlide(self):
        dx, dy = self.CurrentPos - self.LastPos
        self.SetOffset(0, self.Offset[0] + 1.0 * dx / self.Step[0])
        self.SetOffset(1, self.Offset[1] + 1.0 * dy / self.Step[1])
        self.ScrollBar[0].Updatexy()
        self.ScrollBar[1].Updatexy()

    def OnCaptureLost(self, evt):
        self.SetCursor(self.R["CURSOR_NORMAL"])
        self.LeftDown = False
        self.LastPos = None
        self.LastOffset = None
        self.CurrentPos = None


# ======================================================================================================================
# ListCtrl, ListBox (ListBox is just ListCtrl with one column)
# width: positive for fixed width, negative for weight for auto adjust
# Subclass and implement OnSelection and OnActivation
# TODO H Scroll
class ListCtrl(Scrolled):
    def __init__(self, parent, data, width, order=None, drawColumn=True,
                 pos=wx.DefaultPosition, size=wx.DefaultSize, font=None, bg="D", fg="L", edge="D"):
        super().__init__(parent, pos=pos, size=size, font=font, bg=bg, fg=fg, edge=edge)
        self.LastVSize = [0, 0]
        self.CoordsX = []
        self.CoordsY = []
        self.Coords = []
        self.Selection = -1
        self.Input = ""
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.NewTimer("Typing", self.OnTyping)

        self.SetWidth(width)
        self.SetOrder(order)
        self.SetLineHeight(auto=False)
        self.SetData(data)

        self.drawColumn = drawColumn

    def SetData(self, data):
        self.data = data
        self.Selection = -1
        self.SetActualSize()

    def SetWidth(self, width):
        self.width = width
        self.widthTotal = sum([i for i in width if i < 0])
        self.widthFixed = sum([i for i in width if i > 0])
        self.ColumnRect = [wx.Rect(0, 0, 20, 20) for _ in width]

    def SetOrder(self, order):
        self.order = range(len(self.width)) if order is None else order

    def SetLineHeight(self, lineheight=None, auto=True):  # Call SetActualSize immediately after this
        if lineheight is None:
            self.LineHeight = max(self.GetFont().GetPixelSize()[1], Ut.GetFontHeight(self)) + 4
        else:
            self.LineHeight = lineheight
        self.AddScrollBar((0, self.LineHeight))  # step == lineheight
        self.CoordsY = []
        for i in range((wx.DisplaySize()[1] + self.LineHeight - 1) // self.LineHeight):
            self.CoordsY.append(i * self.LineHeight + 1)
        self.UpdateCoords()
        if auto:
            self.SetActualSize()

    def UpdateCoords(self):
        self.Coords = []
        for x in self.CoordsX:
            self.Coords.append([(x + 3, y + 2) for y in self.CoordsY])  # 1 for border, 2 for margin

    def CalculateActualSize(self):
        return max(self.VSize[0], self.widthFixed), len(self.data) * self.LineHeight

    def OnSize(self):
        if self.LastVSize[0] != self.VSize[0]:
            self.LastVSize[0] = self.VSize[0]
            flexible = max(0, self.VSize[0] - self.widthFixed)
            offsetX = -self.GetViewPoint()[0]
            self.CoordsX = []
            for index, width in enumerate(self.width):
                w = int(flexible * width / self.widthTotal if width < 0 else width)
                self.CoordsX.append(offsetX)
                self.ColumnRect[index].SetX(offsetX)
                self.ColumnRect[index].SetWidth(w)
                offsetX += w
            self.UpdateCoords()
        if self.LastVSize[1] < self.VSize[1]:
            self.LastVSize[1] = self.VSize[1]
            for index in range(len(self.ColumnRect)):
                self.ColumnRect[index].SetHeight(self.VSize[1])

    def OnPaint(self, dc):
        if not self.data: return
        data = self.data[self.Offset[1]:self.Offset[1] + len(self.CoordsY)]
        for index, order in enumerate(self.order):
            d = [line[order] for line in data]
            dc.SetClippingRegion(self.ColumnRect[index])
            dc.DrawTextList(d, self.Coords[index][:len(d)])
            if self.drawColumn:
                if index:
                    dc.SetPen(self.R["PEN_EDGE_L"])
                    dc.DrawLine(self.ColumnRect[index].x, 0, self.ColumnRect[index].x, self.VSize[1] + 1)
                if index != len(self.order) - 1:
                    dc.SetPen(self.R["PEN_EDGE_D"])
                    dc.DrawLine(self.ColumnRect[index].right, 0, self.ColumnRect[index].right, self.VSize[1] + 1)
            dc.DestroyClippingRegion()
            dc.SetClippingRegion(self.VRect)
        if self.HasSelection():
            row = self.Selection - self.Offset[1]
            if 0 <= row < len(self.CoordsY):
                dc.SetPen(wx.TRANSPARENT_PEN)
                dc.SetBrush(self.R["BRUSH_SET_D"]["FF"])
                dc.DrawRectangle(1, self.Selection * self.LineHeight - self.GetViewPoint()[1] + 1, self.VSize[0], self.LineHeight)
                dc.DrawTextList([self.data[self.Selection][i] for i in self.order], [coord[row] for coord in self.Coords])

    def OnMouse(self, evt):
        evtType = evt.GetEventType()
        evtPos = evt.GetPosition()
        if evtType == wx.wxEVT_LEFT_DOWN:
            self.SetSelection((self.GetViewPoint()[1] + evtPos[1]) // self.LineHeight)
            for column in range(len(self.CoordsX) - 1, -1, -1):
                if self.CoordsX[column] <= evtPos[0]:
                    getattr(self, "OnColumn%s" % column, Ab.DoNothing)()
                    break
            self.Refresh()
        if evtType == wx.wxEVT_LEFT_DCLICK:
            if self.Selection != -1:
                Ab.Do(self.OnActivation)

    # Selection related ====================================
    def SetSelection(self, s):  # -1 = no selection
        self.Selection = min(max(s, -1), len(self.data) - 1)
        if self.Selection != -1: Ab.Do(self.OnSelection)

    def GetSelection(self):
        return self.Selection

    def HasSelection(self):
        return self.Selection != -1

    def SetStringSelection(self, s, column=0):
        for index, c in enumerate(self.data):
            if c[column] == s:
                self.Selection = index
                return True
        return False

    def GetStringSelection(self, column=0):
        return self.data[self.Selection][column] if self.HasSelection() else False

    def EnsureVisible(self, index=None):
        if index is None: index = self.Selection
        if index > self.Offset[1]:
            self.SetOffset(1, index - self.VSize[1] // self.LineHeight + 1)
        elif index < self.Offset[1]:
            self.SetOffset(1, index)
        self.ScrollBar[1].Updatexy()

    def OnChar(self, evt):
        key = evt.GetKeyCode()
        if key in (wx.WXK_UP, wx.WXK_DOWN):
            self.SetSelection(max(self.Selection + (-1, 1)[key == wx.WXK_DOWN] * (Va.SETTINGS["SCROLL_MULTIPLIER"] if evt.ShiftDown() else 1), 0))
            y = self.Selection * self.LineHeight - self.GetViewPoint()[1]
            if y < 0 or y > self.VSize[1]:
                self.EnsureVisible(self.Selection)
            elif y < self.VSize[1] * 0.5 and key == wx.WXK_UP:
                self.Scroll(1, -1)
            elif y > self.VSize[1] * 0.5 and key == wx.WXK_DOWN:
                self.Scroll(1, 1)
        elif key == wx.WXK_RETURN:
            if self.GetSelection():
                Ab.Do(self.OnActivation)
        elif 32 <= key <= 126:
            self.Input += chr(key)
            for index, c in enumerate(self.data):
                if c[0].startswith(self.Input):
                    self.SetSelection(index)
                    self.EnsureVisible(self.Selection)
                    break
        self.StartTimer("Typing", 2000)
        self.Refresh()

    def OnTyping(self):
        self.Input = ""

    # Implemented by subclass ========================
    def OnSelection(self):
        pass

    def OnActivation(self):
        pass
