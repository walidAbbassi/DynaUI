# -*- coding: utf-8 -*-


import wx
from .utility import GetBrightness
from wx.lib.embeddedimage import PyEmbeddedImage

__all__ = ["BitmapFont", "BitmapFontList"]

CHARSET = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~…•\x00'


class BitmapFont(object):
    def __init__(self, color, bitmap, rect, w=None, h=None, mode=0, charset=CHARSET):
        offsetX, offsetY, charW, charH = rect
        self.w = w or charW
        self.h = h or charH
        self.color = color
        bitmap = bitmap.GetBitmap() if isinstance(bitmap, PyEmbeddedImage) else bitmap
        if color is not None:
            mdc = wx.MemoryDC(bitmap)
            mdc.SetPen(wx.TRANSPARENT_PEN)
            mdc.SetBrush(wx.Brush(self.color))
            mdc.SetLogicalFunction((wx.AND, wx.OR_REVERSE)[GetBrightness(self.color) < 127.5])
            mdc.DrawRectangle(0, 0, *bitmap.GetSize())
            mdc.SelectObject(wx.NullBitmap)
        self.characters = {}
        rect = wx.Rect(offsetX, offsetY, charW, charH)
        for c in charset:
            self.characters[c] = bitmap.GetSubBitmap(rect)
            rect.Offset(charW, 0)
        self.Draw = {0: self.DrawSkipUnknown, 1: self.DrawWarnUnknown, 2: self.DrawDrawUnknown}[mode]

    def DrawSkipUnknown(self, dc, text, x, y):
        for c in text:
            if c in self.characters:
                dc.DrawBitmap(self.characters[c], x, y, True)
            x += self.w

    def DrawWarnUnknown(self, dc, text, x, y):
        for c in text:
            dc.DrawBitmap(self.characters.get(c, self.characters["\x00"]), x, y, True)
            x += self.w

    def DrawDrawUnknown(self, dc, text, x, y):
        for c in text:
            if c in self.characters:
                dc.DrawBitmap(self.characters[c], x, y, True)
                x += self.w
            else:
                dc.DrawText(c, x, y)
                x += dc.GetTextExtent(c)[0]


class BitmapFontList(object):
    def __init__(self, pool=None):
        self.FontPool = pool or {}
        self.FontList = {}

    def FindOrCreateFont(self, font, color, mode=0):
        key = "%s-%s-%s" % (font, color, mode)
        if key in self.FontList:
            return self.FontList[key]
        elif font in self.FontPool:
            f = BitmapFont(color, *self.FontPool[font], mode=mode)
            self.FontList[key] = f
            return f
        else:
            raise Exception

    def AddFontPool(self, dic):
        for key in dic:
            self.FontPool[key] = dic[key]
