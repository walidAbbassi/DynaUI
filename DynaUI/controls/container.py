# -*- coding: utf-8 -*-


import wx
from ..core import BaseControl
from .button import ToolTypes
from .miscellaneous import Separator

__all__ = ["Tool", "Info"]

DefaultFlags1 = wx.SizerFlags().Expand().Border(wx.ALL, 1)
DefaultFlags2 = wx.SizerFlags().Center().Border(wx.ALL, 1)
DefaultFlags3 = wx.SizerFlags().Center().Border(wx.ALL, 1).Proportion(1)


class Tool(BaseControl):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 orientation=wx.HORIZONTAL, itemSize=wx.Size(32, 32),
                 font=None, res=None, bg="D", fg="L", edge="V", async=False, fpsLimit=0):
        super().__init__(parent=parent, pos=pos, size=size, style=style, font=font, res=res, bg=bg, fg=fg, edge=edge, async=async, fpsLimit=fpsLimit)
        self.SetSizer(wx.BoxSizer(orientation))
        self.SizerFlags1 = DefaultFlags1
        self.SizerFlags2 = DefaultFlags2
        self.ItemSize = itemSize

    def AddItems(self, *items):
        frame = self.GetTopLevelParent()
        sizer = self.GetSizer()
        orientation = (wx.VERTICAL | wx.HORIZONTAL) ^ sizer.GetOrientation()
        for item in items:
            if item == "|":
                sizer.Add(Separator(self, orientation=orientation), self.SizerFlags1)
            elif isinstance(item, int):
                sizer.Add(item, item, item == -1)
            else:
                tType, key, func, *extra = item
                tool = ToolTypes[tType](self, size=self.ItemSize, tag=self.L[key], pics=self.R[key], func=func, **(extra[0] if extra else {}))
                tool.SetTip(frame.SetStatus)
                sizer.Add(tool, self.SizerFlags2)
                self[key] = tool

    def AddItemsWithHotKey(self, *items):
        frame = self.GetTopLevelParent()
        sizer = self.GetSizer()
        orientation = (wx.VERTICAL | wx.HORIZONTAL) ^ sizer.GetOrientation()
        for item in items:
            if item == "|":
                sizer.Add(Separator(self, orientation=orientation), self.SizerFlags1)
            elif isinstance(item, int):
                sizer.Add(item, item, item == -1)
            else:
                tType, key, func, flags, keyCode, *extra = item
                tool = ToolTypes[tType](self, size=self.ItemSize, tag=self.L[key], pics=self.R[key], func=func, **(extra[0] if extra else {}))
                tool.SetTip(frame.SetStatus)
                sizer.Add(tool, self.SizerFlags2)
                self[key] = tool
                cmd = wx.NewId()
                frame.Bind(wx.EVT_MENU, tool.Click, id=cmd)
                frame.AcceleratorEntries.append(wx.AcceleratorEntry(flags=flags, keyCode=keyCode, cmd=cmd))


class Info(BaseControl):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.Size(24, 24), style=0,
                 orientation=wx.HORIZONTAL, main=True,
                 font=None, res=None, bg="D", fg="L", edge="V", async=False, fpsLimit=0):
        super().__init__(parent=parent, pos=pos, size=size, style=style, font=font, res=res, bg=bg, fg=fg, edge=edge, async=async, fpsLimit=fpsLimit)
        self.SetSizer(wx.BoxSizer(orientation))
        self.SizerFlags1 = DefaultFlags1
        self.SizerFlags2 = DefaultFlags2
        self.SizerFlags3 = DefaultFlags3
        if main:
            self.GetTopLevelParent().SetStatus = self.SetStatus

    def SetStatus(self, msg, index=0, second=0):
        self[index].SetLabel(msg)
        if second:
            self.StartTimer(index, second * 1000, wx.TIMER_ONE_SHOT)
        elif self.Timers[index].IsRunning():
            self.Timers[index].Stop()

    def AddItems(self, *args):
        sizer = self.GetSizer()
        orientation = (wx.VERTICAL | wx.HORIZONTAL) ^ sizer.GetOrientation()
        last = len(args) - 1
        for index, arg in enumerate(args):
            sizer.Add(arg[0], self.SizerFlags3 if arg[1] else self.SizerFlags2)
            if index < last:
                sizer.Add(Separator(self, orientation=orientation), self.SizerFlags1)
            self[index] = arg[0]
            self.NewTimer(index, (arg[0].SetLabel, ""))
