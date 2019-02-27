# -*- coding: utf-8 -*-


import wx
import webbrowser
from ..core import BaseControl
from .. import dialog as Di
from .. import abstract as Ab
from .. import utility as Ut
from .scrolled import ListCtrl

__all__ = [
    "Button",
    "ButtonMixinToggle", "ButtonMixinBundle", "Bundled",
    "ButtonNormal", "ButtonToggle", "ButtonBundle",
    "ToolNormal", "ToolToggle", "ToolBundle", "ToolTypes",
    "PickerColor", "PickerDirection", "PickerFont", "PickerNumber", "PickerValue",
    "Hider", "Sash", "Slider", "HyperLink",
]

# ======================================================= Button =======================================================
BTN_STATE_IDLE = 1 << 0
BTN_STATE_HOVER = 1 << 1
BTN_STATE_CLICK = 1 << 2
BTN_CHANGE_REVERSE = 0b1000
BTN_CHANGE_IDLE_HOVER = BTN_STATE_IDLE | BTN_STATE_HOVER
BTN_CHANGE_HOVER_IDLE = BTN_STATE_IDLE | BTN_STATE_HOVER | BTN_CHANGE_REVERSE
BTN_CHANGE_IDLE_CLICK = BTN_STATE_IDLE | BTN_STATE_CLICK
BTN_CHANGE_CLICK_IDLE = BTN_STATE_IDLE | BTN_STATE_CLICK | BTN_CHANGE_REVERSE
BTN_CHANGE_HOVER_CLICK = BTN_STATE_HOVER | BTN_STATE_CLICK
BTN_CHANGE_CLICK_HOVER = BTN_STATE_HOVER | BTN_STATE_CLICK | BTN_CHANGE_REVERSE


class Button(BaseControl):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 tag=None, pic=None, func=None,
                 font=None, res="D", bg="D", fg="L", edge="L", sync=True, fpsLimit=0):
        super().__init__(parent=parent, pos=pos, size=size, style=style, font=font, res=res, bg=bg, fg=fg, edge=edge, sync=sync, fpsLimit=fpsLimit)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
        self.Func = func
        self.SetTip(Ab.DoNothing)

        self._toDrawList = []
        self.InitTag(*tag if isinstance(tag, (tuple, list)) else (tag,))
        self.InitPic(*pic if isinstance(pic, (tuple, list)) else (pic,))
        self.Positioning()

        self.Brush = self.Resources["00"]
        self.NewAnimation("ENTER", 25, "Brush", ("80", "FF"))
        self.NewAnimation("LEAVE", 25, "Brush", ("C0", "80", "40", "00"))
        self.NewAnimation("LEAVE_WHEN_CLICKED", 25, "Brush", ("40", "00"))
        self.NewAnimation("ENTER_THEN_LEAVE", 25, "Brush", ("FF", "FF", "FF", "FF", "FF", "C0", "80", "40", "00"))

        self.state = BTN_STATE_IDLE
        self.leftDown = False

    def OnMouse(self, evt):
        evtType = evt.GetEventType()
        evtPos = evt.GetPosition()
        if evtType == wx.wxEVT_LEFT_DOWN or evtType == wx.wxEVT_LEFT_DCLICK:
            self.CaptureMouse()
            self.SetState(BTN_STATE_CLICK)
            self.leftDown = True
        elif evtType == wx.wxEVT_LEFT_UP:
            self.ReleaseMouse()
            if self.leftDown:
                self.OnClick()
                self.leftDown = False
            if wx.Rect(0, 0, *self.GetSize()).Contains(evtPos):
                self.SetState(BTN_STATE_HOVER)
            else:
                self.SetState(BTN_STATE_IDLE)
        elif evtType == wx.wxEVT_ENTER_WINDOW:
            if not self.leftDown:
                self.SetState(BTN_STATE_HOVER)
            self.TipFunc(self.TipText or self.Tag)
        elif evtType == wx.wxEVT_LEAVE_WINDOW and not self.leftDown:
            if not self.leftDown:
                self.SetState(BTN_STATE_IDLE)
            self.TipFunc("")
        evt.Skip()

    def OnCaptureLost(self, evt):
        self.leftDown = False

    def OnClick(self):
        Ab.Do(self.Func)

    def Click(self, evt=None):
        self.Play("ENTER_THEN_LEAVE")
        Ab.Do(self.Func)

    # --------------------------------------
    def InitTag(self, tag, pos="C", x=0, y=0):
        self.SetTag(tag, False)
        self.SetTagPos(pos)
        self.SetTagOffset(x, y)
        self.TagXY = (0, 0)
        if tag is not None:
            self._toDrawList.append(self.DrawTag)

    def InitPic(self, pic, pos="C", x=0, y=0):
        self.SetPic(pic, False)
        self.SetPicPos(pos)
        self.SetPicOffset(x, y)
        self.PicXY = (0, 0)
        if pic is not None:
            self._toDrawList.append(self.DrawPic)

    def SetTag(self, tag, reposition=True):
        self.Tag = tag
        if reposition:
            self.Positioning()

    def SetPic(self, pic, reposition=True):
        self.Pic = pic
        if reposition:
            self.Positioning()

    def SetTagPos(self, pos):
        self.TagPos = pos

    def SetPicPos(self, pos):
        self.PicPos = pos

    def SetTagOffset(self, x, y):
        self.TagOffset = x, y

    def SetPicOffset(self, x, y):
        self.PicOffset = x, y

    def ShowTag(self, show):
        if not show and self.DrawTag in self._toDrawList:
            self._toDrawList.remove(self.DrawTag)
        elif show and self.DrawTag not in self._toDrawList:
            self._toDrawList.append(self.DrawTag)

    def ShowPic(self, show):
        if not show and self.DrawPic in self._toDrawList:
            self._toDrawList.remove(self.DrawPic)
        elif show and self.DrawPic not in self._toDrawList:
            self._toDrawList.append(self.DrawPic)

    def Positioning(self):
        w, h = self.GetSize()
        if self.Tag is not None:
            tw, th = Ut.GetMultiLineTextExtent(self, self.Tag)
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
            self.TagXY = (x + self.TagOffset[0], y + self.TagOffset[1])
        if self.Pic is not None:
            bw, bh = self.Pic.GetSize()
            if "L" in self.PicPos:
                x = 0
            elif "R" in self.PicPos:
                x = w - bw
            else:
                x = (w - bw) >> 1
            if "T" in self.PicPos:
                y = 0
            elif "B" in self.PicPos:
                y = h - bh
            else:
                y = (h - bh) >> 1
            self.PicXY = (x + self.PicOffset[0], y + self.PicOffset[1])

    # --------------------------------------
    def SetTip(self, func, text=""):
        self.TipFunc = func
        self.TipText = text

    def SetState(self, state):
        transition = self.state | state | [BTN_CHANGE_REVERSE, 0][self.state < state]
        self.state = state
        if transition == BTN_CHANGE_IDLE_HOVER:
            self.Play("ENTER")
        elif transition == BTN_CHANGE_HOVER_IDLE:
            self.Play("LEAVE")
        elif transition == BTN_CHANGE_CLICK_IDLE:
            self.Play("LEAVE_WHEN_CLICKED")
        elif transition == BTN_CHANGE_IDLE_CLICK:  # When a submenu item is clicked and mouse switch to another submenu item
            self.Brush = self.Resources["80"]
            self.ReDraw()
        elif transition == BTN_CHANGE_HOVER_CLICK:
            self.Brush = self.Resources["80"]
            self.ReDraw()
        elif transition == BTN_CHANGE_CLICK_HOVER:
            self.Brush = self.Resources["FF"]
            self.ReDraw()

    def DrawTag(self, dc, w=0, h=0):
        dc.DrawText(self.Tag, self.TagXY[0], self.TagXY[1])

    def DrawPic(self, dc, w=0, h=0):
        dc.DrawBitmap(self.Pic, self.PicXY[0], self.PicXY[1], 1)

    def OnPaint(self, evt):
        w, h = self.GetSize()
        dc = wx.BufferedPaintDC(self)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(self.Brush)
        dc.DrawRectangle(0, 0, w, h)
        for draw in self._toDrawList:
            draw(dc, w, h)
        if not self.IsEnabled():
            gc = wx.GraphicsContext.Create(dc)
            gc.SetBrush(self.R["BRUSH_DISABLED"])
            gc.DrawRectangle(0, 0, w, h)
        if self.state == BTN_STATE_IDLE:
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

    def OnSize(self, evt):
        self.Positioning()
        evt.Skip()


# ---- Mix-ins ----
class ButtonMixinToggle(object):
    def __init__(self, toggle, tag2=None, pic2=None):
        self.Toggle = toggle
        self.Tag2 = self.Tag if tag2 is None else tag2
        self.Pic2 = self.Pic if pic2 is None else pic2
        if toggle:
            self.Tag, self.Tag2 = self.Tag2, self.Tag
            self.Pic, self.Pic2 = self.Pic2, self.Pic
            self.Brush = self.Resources["FF"]

    def T(self):
        self.Toggle = not self.Toggle
        self.Tag, self.Tag2 = self.Tag2, self.Tag
        self.Pic, self.Pic2 = self.Pic2, self.Pic
        self.Positioning()

    def OnClick(self):
        self.T()
        Ab.Do(self.Func)

    def Click(self, evt=None):
        self.T()
        self.Play("ENTER" if self.Toggle else "LEAVE")
        Ab.Do(self.Func)

    def SetToggle(self, toggle):
        if self.IsToggled() != toggle:
            self.Click()

    def IsToggled(self):
        return self.Toggle

    def SetState(self, state):
        transition = self.state | state | [BTN_CHANGE_REVERSE, 0][self.state < state]
        self.state = state
        if self.Toggle:
            if transition == BTN_CHANGE_CLICK_IDLE:
                self.Brush = self.Resources["FF"]
                self.ReDraw()
        else:
            if transition == BTN_CHANGE_IDLE_HOVER:
                self.Play("ENTER")
            elif transition == BTN_CHANGE_HOVER_IDLE:
                self.Play("LEAVE")
            elif transition == BTN_CHANGE_CLICK_IDLE:
                self.Play("LEAVE_WHEN_CLICKED")
        if state == BTN_STATE_CLICK:
            self.Brush = self.Resources["80"]
            self.ReDraw()
        elif transition == BTN_CHANGE_CLICK_HOVER:
            self.Brush = self.Resources["FF"]
            self.ReDraw()


class ButtonMixinBundle(object):
    def __init__(self, toggle, group):
        self.Toggle = toggle
        self.Group = group
        if toggle:
            self.Brush = self.Resources["FF"]
        if group not in self.GetParent().Groups:
            self.GetParent().Groups[group] = []
        self.GetParent().Groups[group].append(self)

    def OnClick(self):
        if not self.Toggle:
            self.Toggle = True
            for tool in self.GetParent().Groups[self.Group]:
                if tool != self and tool.Toggle:
                    tool.Toggle = False
                    tool.Play("LEAVE")
        Ab.Do(self.Func)

    def Click(self, evt=None):
        if not self.Toggle:
            self.Toggle = True
            self.Play("ENTER")
            for tool in self.GetParent().Groups[self.Group]:
                if tool != self and tool.Toggle:
                    tool.Toggle = False
                    tool.Play("LEAVE")
        Ab.Do(self.Func)

    def IsToggled(self):
        return self.Toggle

    def SetState(self, state):
        transition = self.state | state | [BTN_CHANGE_REVERSE, 0][self.state < state]
        self.state = state
        if self.Toggle:
            if transition == BTN_CHANGE_CLICK_IDLE:
                self.Brush = self.Resources["FF"]
                self.ReDraw()
        else:
            if transition == BTN_CHANGE_IDLE_HOVER:
                self.Play("ENTER")
            elif transition == BTN_CHANGE_HOVER_IDLE:
                self.Play("LEAVE")
            elif transition == BTN_CHANGE_CLICK_IDLE:
                self.Play("LEAVE_WHEN_CLICKED")
        if state == BTN_STATE_CLICK:
            self.Brush = self.Resources["80"]
            self.ReDraw()
        elif transition == BTN_CHANGE_CLICK_HOVER:
            self.Brush = self.Resources["FF"]
            self.ReDraw()


# ---- Basic buttons ----
ButtonNormal = Button


class ButtonToggle(ButtonMixinToggle, Button):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 toggle=False, tag=None, pic=None, tag2=None, pic2=None, func=None,
                 font=None, res="D", bg="D", fg="L", edge="L", sync=True, fpsLimit=0):
        Button.__init__(self, parent=parent, pos=pos, size=size, style=style, tag=tag, pic=pic, func=func, font=font, res=res, bg=bg, fg=fg, edge=edge, sync=sync, fpsLimit=fpsLimit)
        ButtonMixinToggle.__init__(self, toggle, tag2, pic2)


class ButtonBundle(ButtonMixinBundle, Button):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 toggle=False, group="", tag=None, pic=None, func=None,
                 font=None, res="D", bg="D", fg="L", edge="L", sync=True, fpsLimit=0):
        Button.__init__(self, parent=parent, pos=pos, size=size, style=style, tag=tag, pic=pic, func=func, font=font, res=res, bg=bg, fg=fg, edge=edge, sync=sync, fpsLimit=fpsLimit)
        ButtonMixinBundle.__init__(self, toggle, group)


class Bundled(object):
    def __init__(self, buttons):
        self.buttons = buttons

    def __getitem__(self, item):
        return self.buttons[item]

    def GetSelection(self):
        for index, b in enumerate(self.buttons):
            if b.IsToggled():
                return index
        return -1

    def SetSelection(self, index):
        if self.GetSelection() != index:
            self.buttons[index].Click()


ButtonTypes = {"N": ButtonNormal, "T": ButtonToggle, "B": ButtonBundle}


# ---- Tool Buttons ----
class ToolNormal(Button):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 pics=(), tag=None, func=None, showTag=False,
                 font=None, res="D", bg="D", fg="L", edge=None, sync=True, fpsLimit=0):
        if isinstance(pics[0], (tuple, list)):
            pics, *other = pics
        else:
            other = ()
        super().__init__(parent=parent, pos=pos, size=size, style=style, tag=tag, pic=(pics[0], *other), func=func, font=font, res=res, bg=bg, fg=fg, edge=edge, sync=sync, fpsLimit=fpsLimit)
        self.Pics = pics
        self.NewAnimation("ENTER", 25, self.SetResource, ((0, "40"), (1, "80"), (2, "C0"), (3, "FF")), False)
        self.NewAnimation("LEAVE", 25, self.SetResource, ((2, "80"), (1, "80"), (0, "00")), False)
        self.NewAnimation("LEAVE_WHEN_CLICKED", 25, self.SetResource, ((2, "80"), (1, "80"), (0, "00")), False)
        self.ShowTag(showTag)

    def SetResource(self, r):
        self.Pic = self.Pics[r[0]]
        self.Brush = self.Resources[r[1]]


class ToolToggle(ButtonMixinToggle, ToolNormal):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 toggle=False, pics=(), tag=None, tag2=None, func=None, showTag=False,
                 font=None, res="D", bg="D", fg="L", edge=None, sync=True, fpsLimit=0):
        ToolNormal.__init__(self, parent=parent, pos=pos, size=size, style=style, pics=pics, tag=tag, func=func, showTag=showTag, font=font, res=res, bg=bg, fg=fg, edge=edge, sync=sync, fpsLimit=fpsLimit)
        ButtonMixinToggle.__init__(self, toggle, tag2, pic2=None)
        if self.Toggle:
            self.Pic = self.Pics[3]

    def T(self):
        self.Toggle = not self.Toggle
        self.Tag, self.Tag2 = self.Tag2, self.Tag
        self.Positioning()


class ToolBundle(ButtonMixinBundle, ToolNormal):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 toggle=False, group="", pics=(), tag=None, func=None, showTag=False,
                 font=None, res="D", bg="D", fg="L", edge=None, sync=True, fpsLimit=0):
        ToolNormal.__init__(self, parent=parent, pos=pos, size=size, style=style, pics=pics, tag=tag, func=func, showTag=showTag, font=font, res=res, bg=bg, fg=fg, edge=edge, sync=sync, fpsLimit=fpsLimit)
        ButtonMixinBundle.__init__(self, toggle, group)
        if self.Toggle:
            self.Pic = self.Pics[3]


ToolTypes = {"N": ToolNormal, "T": ToolToggle, "B": ToolBundle}


# ---- Pickers ----
# When a value is picked, they pass it to the associated function (if provided)
class PickerColor(Button):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 associate=None, value="#000000",
                 tag="", pic=None,
                 font=None, res="D", bg="D", fg="L", edge=None):
        super().__init__(parent=parent, pos=pos, size=size, style=style, tag=tag, pic=pic, func=self.OnButton, font=font, res=res, bg=bg, fg=fg, edge=edge)
        self.Associate = associate
        self.AutoLabel = self.Tag == ""
        self._toDrawList.insert(0, self.DrawColor)
        self.SetValue(value)

    def DrawColor(self, dc, w, h):
        dc.SetBrush(self.ColorBrush)
        dc.DrawRectangle(1, 1, w - 2, h - 2)

    def OnButton(self):
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            self.SetValue(Ut.C2S(wx.Colour(*dlg.GetColourData().GetColour().Get())))
            if self.Associate:
                self.Associate(self.Value)
        dlg.Destroy()

    def GetValue(self):
        return self.Value

    def SetValue(self, value):
        self.Value = value
        self.ColorBrush = wx.Brush(value)
        self.SetForegroundColour((wx.BLACK, wx.WHITE)[Ut.GetBrightness(value) < 127.5])
        if self.AutoLabel:
            self.SetTag(value)
        self.ReDraw()


class PickerFont(Button):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 associate=None, value=None,
                 tag="", pic=None,
                 font=None, res="D", bg="D", fg="L", edge="L"):
        super().__init__(parent=parent, pos=pos, size=size, style=style, tag=tag, pic=pic, func=self.OnButton, font=font, res=res, bg=bg, fg=fg, edge=edge)
        self.Associate = associate
        self.AutoLabel = self.Tag == ""
        self.SetValue(value if value else self.GetFont())

    def OnButton(self):
        data = wx.FontData()
        data.EnableEffects(True)
        data.SetInitialFont(self.Value)
        dlg = wx.FontDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            self.SetValue(dlg.GetFontData().GetChosenFont())
            if self.Associate:
                self.Associate(self.Value)
        dlg.Destroy()

    def GetValue(self):
        return self.Value

    def SetValue(self, value):
        self.Value = value
        self.SetFont(value)
        self.SetToolTip("%s\n%s" % (self.Value.GetFaceName(), self.Value.GetPointSize()))
        if self.AutoLabel:
            self.SetTag(self.GetToolTipText())
        self.ReDraw()


class PickerDirection(Button):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 associate=None, value="CC",
                 tag="[+]", pic=None,
                 font=None, res="D", bg="D", fg="L", edge="L"):
        super().__init__(parent=parent, pos=pos, size=size, style=style, tag=tag, pic=pic, func=None, font=font, res=res, bg=bg, fg=fg, edge=edge)
        self.Associate = associate
        self.SetValue(value)

    def OnMouse(self, evt):
        super().OnMouse(evt)
        if evt.GetEventType() == wx.wxEVT_MOTION and self.leftDown:
            self.UpdateDirection(*evt.GetPosition())
        elif evt.GetEventType() == wx.wxEVT_RIGHT_DOWN:
            w, h = self.GetSize()
            self.UpdateDirection(w >> 1, h >> 1)

    def UpdateDirection(self, x, y):
        W, H = self.GetSize()
        if x < W * 0.35:
            h = "L"
        elif x > W * 0.65:
            h = "R"
        else:
            h = ""
        if y < H * 0.35:
            v = "T"
        elif y > H * 0.65:
            v = "B"
        else:
            v = ""
        d = h + v
        if d != self.Value:
            self.SetValue(d)
            if self.Associate:
                self.Associate(d)

    def GetValue(self):
        return self.Value

    def SetValue(self, value):
        self.Value = value
        self.SetTagPos(value)
        self.SetPicPos(value)
        self.Positioning()
        self.ReDraw()


class PickerNumber(Button):  # TODO Wheel
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 associate=None, value=0, vRange=(0, 5), baseRange=None,
                 tag="", pic=None,
                 font=None, res="D", bg="D", fg="L", edge="L"):
        super().__init__(parent=parent, pos=pos, size=size, style=style, tag=tag, pic=pic, func=None, font=font, res=res, bg=bg, fg=fg, edge=edge)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnWheel)
        self.Associate = associate
        self.Old = value
        self.Number = value
        self.IsInt = isinstance(value, int)
        self.Range = vRange
        self.Base = vRange[0] if baseRange is None else baseRange
        self.leftMotion = False
        self.StepX = int(wx.DisplaySize()[0] / max(self.Range[1] - self.Range[0], wx.DisplaySize()[0] / 100) / 1.5)
        self.StepY = wx.DisplaySize()[1] / 100
        self.SetTag("%s" % self.Number)
        self._toDrawList.insert(0, self.DrawGauge)

    def OnMouse(self, evt):
        super().OnMouse(evt)
        evtType = evt.GetEventType()
        if evtType == wx.wxEVT_LEFT_UP:
            if not self.leftMotion:
                self.SetValue(min(self.Number + 1, self.Range[1]))
            self.leftMotion = False
            self.Old = self.Number
            if self.Associate:
                self.Associate(self.Number)
        elif evtType == wx.wxEVT_MOTION and self.leftDown:
            self.leftMotion = True
            self.UpdateNumber(*evt.GetPosition())
        elif evtType == wx.wxEVT_RIGHT_DOWN or evtType == wx.wxEVT_RIGHT_DCLICK:
            self.SetState(BTN_STATE_CLICK)
        elif evtType == wx.wxEVT_RIGHT_UP:
            self.SetState(BTN_STATE_HOVER)
            self.SetValue(max(self.Number - 1, self.Range[0]))
            if self.Associate:
                self.Associate(self.Number)

    def OnWheel(self, evt):
        if evt.GetWheelRotation() > 0:
            self.SetValue(min(self.Number + 1, self.Range[1]))
        else:
            self.SetValue(max(self.Number - 1, self.Range[0]))

    def DrawGauge(self, dc, w, h):
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(self.ForegroundBrush)
        if self.Range[1] != self.Base:
            dc.DrawRectangle(1, h - 3, (w - 2) * (self.Number - self.Base) // (self.Range[1] - self.Base), 2)

    def UpdateNumber(self, x, y):
        if self.IsInt:
            new = max(min(int(self.Old + x // self.StepX), self.Range[1]), self.Range[0])
        else:
            new = max(min(int(self.Old + x // self.StepX) + y // self.StepY / 10, self.Range[1]), self.Range[0])
        if self.Number != new:
            self.SetValue(new)

    def GetValue(self):
        return self.Number

    def SetValue(self, value):
        self.Number = value
        self.SetTag(("%d" if self.IsInt else "%.1f") % value)
        self.ReDraw()


class PickerValue(ToolNormal):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 associate=None, selected=-1, choices=(),
                 tag="", pics=None,
                 font=None, res="D", bg="D", fg="L", edge="L"):
        super().__init__(parent=parent, pos=pos, size=size, style=style, showTag=True, tag=tag or ("", "L", 2), pics=pics or (parent.R["AP_TRIANGLE_D"], "R"), func=self.OnButton,
                         font=font, res=res, bg=bg, fg=fg, edge=edge)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnWheel)
        self.Associate = associate
        self.AutoLabel = self.Tag == ""
        self.selected = selected
        self.choices = choices
        self.choosing = None
        if selected != -1 and self.AutoLabel:
            self.SetTag(self.choices[self.selected])

    def SetChoices(self, choices):
        self.choices = choices
        if self.AutoLabel:
            self.SetTag("")
            self.ReDraw()

    def OnWheel(self, evt):
        if evt.GetWheelRotation() > 0:
            self.SetSelection(max(0, self.selected - 1))
        else:
            self.SetSelection(min(self.selected + 1, len(self.choices) - 1))

    def OnButton(self):
        if not self.choices or self.choosing:
            return
        size = wx.Size(self.GetSize()[0], min(400, (max(self.GetFont().GetPixelSize()[1], Ut.GetFontHeight(self)) + 4) * len(self.choices) + 2))
        d = Di.BaseMiniDialog(invoker=self, pos=self.GetScreenPosition() + (0, self.GetSize()[1] - 1), size=size, main=ListCtrl, data=[(i,) for i in self.choices], width=(-1,), edge=self.Params["EDGE"] or "D")
        d.Main.SetSelection(self.selected)
        d.Main.Bind(wx.EVT_KILL_FOCUS, lambda evt: (d.Play("FADEOUT"), self.SetFocus()))
        d.Main.OnSelection = lambda: (self.SetSelection(d.Main.GetSelection()), d.Play("FADEOUT"), self.SetFocus())
        d.Play("FADEIN")
        self.choosing = d

    def GetSelection(self):
        return self.selected

    def SetSelection(self, selected, send=True):
        self.selected = selected
        if send and self.Associate:
            self.Associate(self.selected)
        if self.AutoLabel:
            self.SetTag(self.choices[self.selected])
            self.ReDraw()

    def GetValue(self):
        return self.choices[self.selected]

    def SetValue(self, value):
        self.SetSelection(self.choices.index(value))


# ---- Misc Buttons ----
class Hider(ToolNormal):
    def __init__(self, parent, targets, orientation="V", func=Ab.DoNothing, font=None, res="L", bg="L", fg="D", edge=None):
        self.orientation = orientation
        if self.orientation == "V":
            size = wx.Size(4, -1)
            pics = parent.R["AP_HIDER_V"]
        else:
            size = wx.Size(-1, 4)
            pics = parent.R["AP_HIDER_H"]
        super().__init__(parent=parent, size=size, pics=pics, func=((self.OnHider,), func), font=font, res=res, bg=bg, fg=fg, edge=edge)
        self.Targets = targets
        self.show = True

    def OnHider(self):
        if self.show:
            for target in self.Targets:
                target.Hide()
        else:
            for target in self.Targets:
                target.Show()
        self.show = not self.show
        self.GetParent().Layout()


class Sash(ToolNormal):
    def __init__(self, parent, target, direction="L", vRange=(150, 600), func=None, font="I", res="L", bg="L", fg="D", edge=None):
        self.orientation = "H" if direction in "LR" else "V"
        if self.orientation == "H":
            size = wx.Size(4, -1)
            pics = parent.R["AP_HIDER_V"]
            self.dimension = 0
            self.cursor = parent.R["CURSOR_SASH_H"]
        else:
            size = wx.Size(-1, 4)
            pics = parent.R["AP_HIDER_H"]
            self.dimension = 1
            self.cursor = parent.R["CURSOR_SASH_V"]
        super().__init__(parent=parent, size=size, pics=pics, func=parent.Layout if func is None else func, font=font, res=res, bg=bg, fg=fg, edge=edge)
        self.Target = target
        self.multiplier = {"L": 1, "R": -1, "T": 1, "B": -1}[direction]
        self.leftPos = None
        self.sizeRect = None
        self.sizeNew = None
        clipMin = vRange[0] >= 0
        clipMax = vRange[1] >= 0

        def Clipped(raw):
            if clipMin:
                raw = max(vRange[0], raw)
            if clipMax:
                raw = min(vRange[1], raw)
            return raw

        self.Clipped = Clipped

    def CloseRect(self):
        if self.sizeRect is not None:
            self.sizeRect.Destroy()
            self.sizeRect = None

    def SetRectAlpha(self, t):
        if self.sizeRect is not None:
            self.sizeRect.SetTransparent(t)

    def OnMouse(self, evt):
        super().OnMouse(evt)
        evtType = evt.GetEventType()
        evtPos = evt.GetPosition()
        if evtType == wx.wxEVT_LEFT_DOWN or evtType == wx.wxEVT_LEFT_DCLICK:
            self.leftPos = evtPos[self.dimension]
        elif evtType == wx.wxEVT_LEFT_UP:
            self.leftPos = None
            self.SetCursor(self.R["CURSOR_NORMAL"])
            if self.sizeRect:
                self.Target.SetInitialSize(self.sizeNew)
                self.CloseRect()
                Ab.Do(self.Func)
            self.Brush = self.Resources["00"]
            self.ReDraw()
        elif evtType == wx.wxEVT_MOTION and self.leftDown:
            if not self.sizeRect:
                self.sizeRect = wx.Frame(self, pos=self.GetScreenPosition(), size=self.GetSize(), style=wx.BORDER_NONE | wx.FRAME_NO_TASKBAR | wx.FRAME_FLOAT_ON_PARENT)
                self.sizeRect.SetBackgroundColour(self.R["COLOR_SIZING"])
                self.sizeRect.SetTransparent(192)
                self.sizeRect.Show()
            length = self.Clipped(self.Target.GetSize()[self.dimension] + (evtPos[self.dimension] - self.leftPos) * self.multiplier)
            change = (length - self.Target.GetSize()[self.dimension]) * self.multiplier
            if self.orientation == "H":
                self.sizeNew = wx.Size(length, -1)
                self.sizeRect.SetPosition(self.GetScreenPosition() + [change, 0])
            else:
                self.sizeNew = wx.Size(-1, length)
                self.sizeRect.SetPosition(self.GetScreenPosition() + [0, change])
        elif evtType == wx.wxEVT_ENTER_WINDOW:
            self.SetCursor(self.cursor)
        elif evtType == wx.wxEVT_LEAVE_WINDOW and not self.leftDown:
            self.SetCursor(self.R["CURSOR_NORMAL"])

    def OnCaptureLost(self, evt):
        self.leftPos = None
        self.leftDown = False
        self.sizeNew = None
        self.CloseRect()
        self.SetCursor(self.R["CURSOR_NORMAL"])


class Slider(Button):  # TODO rework
    def __init__(self, parent, pos=wx.DefaultPosition, size=(112, -1), drawLabel=True,
                 associate=None, value=50, domain=(0, 100), step=1):
        super().__init__(parent=parent, pos=pos, size=wx.Size(size[0], (40 if drawLabel else 20) if size[1] == -1 else size[1]), res="B", bg="D", fg="D", edge="BE", fpsLimit=240)
        self.SetBackgroundColour(parent.GetBackgroundColour())
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnWheel)
        self.Associate = associate
        self.drawLabel = drawLabel
        self.value = value - domain[0]
        self.domain = domain
        self.length = max(domain[1] - domain[0], 1)
        self.step = min(max(step, 1), self.length)
        self.label1 = str(self.domain[0])
        self.label2 = str(self.domain[1])
        self.labelV = str(value)
        self.leftPos = None
        self.Render()

    def OnSize(self, evt):
        super().OnSize(evt)
        self.Render()

    def OnPaint(self, evt):
        l = self.leftPos if self.leftDown else self.barW * self.value / self.length
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self.Buffer, 4, self.offsetY)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(self.Brush)
        dc.DrawRectangle(5, self.offsetY + 1, l, 4)
        if self.drawLabel:
            r = self.GetSize()[0] - dc.GetTextExtent(self.label2)[0]
            tw, th = dc.GetTextExtent(self.labelV)
            dc.DrawText(self.label1, 0, self.offsetY + 7)
            dc.DrawText(self.label2, r, self.offsetY + 7)
            dc.DrawText(self.labelV, max(min(5 + l - tw // 2, r), 0), self.offsetY - th)
        dc.DrawBitmap(self.R["BITMAP_SLIDER"], l, self.offsetY - 2)

    def OnMouse(self, evt):
        super().OnMouse(evt)
        evtType = evt.GetEventType()
        x = max(min(evt.GetPosition()[0] - 4, self.barW), 0)
        if evtType == wx.wxEVT_LEFT_DOWN or evtType == wx.wxEVT_LEFT_DCLICK:
            self.leftPos = x
            self.UpdateValue(x)
        elif evtType == wx.wxEVT_LEFT_UP:
            self.leftPos = None
        elif evtType == wx.wxEVT_MOTION and self.leftDown:
            self.leftPos = x
            self.UpdateValue(x)
        self.ReDraw()

    def OnCaptureLost(self, evt):
        self.leftDown = False
        self.leftPos = None

    def OnWheel(self, evt):
        if evt.GetWheelRotation() < 0:
            self.NewValue(max(self.value - self.step, self.domain[0]))
        else:
            self.NewValue(min(self.value + self.step, self.domain[1]))
        self.ReDraw()

    def UpdateValue(self, x):
        self.NewValue(int((self.length * x / self.barW + self.step // 2) // self.step * self.step))

    def NewValue(self, value):
        self.value = value
        self.labelV = str(self.value + self.domain[0])
        if self.Associate:
            self.Associate(self.value + self.domain[0])

    def Render(self):
        wS, hS = self.GetSize()
        w = max(wS - 4 - 6, 6)
        h = 6
        self.barW = w - 2
        self.offsetY = hS // 2 - 3
        self.Buffer = wx.Bitmap(w, h)
        mdc = wx.MemoryDC(self.Buffer)
        mdc.SetBackground(self.BackgroundBrush)
        mdc.Clear()
        mdc.SetPen(self.R["PEN_EDGE_L"])
        mdc.DrawLine(w - 1, 0, w - 1, h)
        mdc.DrawLine(0, h - 1, w, h - 1)
        mdc.SetPen(self.R["PEN_EDGE_D"])
        mdc.DrawLine(0, 0, 0, h)
        mdc.DrawLine(0, 0, w, 0)
        mdc.SelectObject(wx.NullBitmap)


class HyperLink(ToolNormal):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 tag=None, pics=None, url="", showTag=True,
                 font="U", res="L", bg="D", fg="#40c0ff", edge=None):
        super().__init__(parent=parent, pos=pos, size=size, style=style, tag=tag, pics=pics, func=self.OnUrl, showTag=showTag, font=font, res=res, bg=bg, fg=fg, edge=edge)
        self.url = url

    def OnUrl(self):
        try:
            webbrowser.open(self.url)
        except Exception:
            pass
