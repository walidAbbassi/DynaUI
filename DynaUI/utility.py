# -*- coding: utf-8 -*-


import sys
import wx
import win32gui
import win32api

__all__ = [
    "DropShadow",
    "AlphaBlend",
    "C2S", "S2C",
    "GetBrightness",
    "GetBitmaps",
    "GetFontHeight",
    "GetTextExtent",
    "GetMultiLineTextExtent",
    "EnsureWindowInScreen",
    "ShowSaveFileDialog",
    "ShowOpenFileDialog",
    "ShowSimpleMessageDialog",
]

# ----------------------------------------------------------
if sys.getwindowsversion().major > 6 or (sys.getwindowsversion().major == 6 and sys.getwindowsversion().minor > 1):
    _rounded = 0
else:
    _rounded = 2


def DropShadow(w, drop=True):
    if wx.Platform != "__WXMSW__":
        return
    hwnd = w.GetHandle()
    size = w.GetSize()
    rgn = win32gui.CreateRoundRectRgn(0, 0, size.x + 1, size.y + 1, _rounded, _rounded)
    win32gui.SetWindowRgn(hwnd, rgn, True)
    CS_DROPSHADOW = 0x00020000
    GCL_STYLE = -26
    cstyle = win32gui.GetClassLong(hwnd, GCL_STYLE)
    if drop:
        if cstyle & CS_DROPSHADOW == 0:
            win32api.SetClassLong(hwnd, GCL_STYLE, cstyle | CS_DROPSHADOW)
    else:
        win32api.SetClassLong(hwnd, GCL_STYLE, cstyle & ~ CS_DROPSHADOW)


# ----------------------------------------------------------
def AlphaBlend(bg, fg, opacity):
    r0, g0, b0 = int(bg[1:3], 16), int(bg[3:5], 16), int(bg[5:7], 16)
    r1, g1, b1 = int(fg[1:3], 16), int(fg[3:5], 16), int(fg[5:7], 16)
    transparency = 1 - opacity
    return wx.Colour(r0 * transparency + r1 * opacity, g0 * transparency + g1 * opacity, b0 * transparency + b1 * opacity)


def C2S(c, alpha=False):
    r = hex(c.red)[2:].rjust(2, "0")
    g = hex(c.green)[2:].rjust(2, "0")
    b = hex(c.blue)[2:].rjust(2, "0")
    a = hex(c.alpha)[2:].rjust(2, "0") if c.Alpha() != 255 or alpha else ""
    return "".join(("#", r, g, b, a))


def S2C(s):
    r, g, b = int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16)
    a = int(s[7:9], 16) if len(s) == 9 else 255
    return wx.Colour(r, g, b, a)


def GetBrightness(c):
    if isinstance(c, wx.Colour):
        return (299 * c.Red() + 587 * c.Green() + 114 * c.Blue()) / 1000.0
    else:
        return (299 * int(c[1:3], 16) + 587 * int(c[3:5], 16) + 114 * int(c[5:7], 16)) / 1000.0


def GetBitmaps(bitmap, w, h, dx=0, dy=0):
    W, H = bitmap.GetSize()
    bitmaps = []
    y = 0
    while y + h <= H:
        x = 0
        while x + w <= W:
            bitmaps.append(bitmap.GetSubBitmap((x, y, w, h)))
            x += dx + w
        y += dy + h
    return bitmaps


def GetFontHeight(window):
    dc = wx.ScreenDC()
    dc.SetFont(window.GetFont())
    return dc.GetTextExtent("bdfghjklpqyJQ^,`'")[1]


def GetTextExtent(window, text):
    dc = wx.ScreenDC()
    dc.SetFont(window.GetFont())
    return dc.GetTextExtent(text)


def GetMultiLineTextExtent(window, text):
    dc = wx.ScreenDC()
    dc.SetFont(window.GetFont())
    return dc.GetMultiLineTextExtent(text)


def EnsureWindowInScreen(pos, size, snap=0):
    sW, sH = wx.DisplaySize()
    if pos[1] + size[1] > sH - snap: pos[1] = sH - size[1]
    if pos[0] < snap: pos[0] = 0
    if pos[1] < snap: pos[1] = 0
    if pos[0] + size[0] > sW - snap: pos[0] = sW - size[0]
    return pos


# ----------------------------------------------------------
def ShowSaveFileDialog(parent, message, wildcard):
    dlg = wx.FileDialog(parent, message=message, wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    filename = dlg.GetPath() if dlg.ShowModal() == wx.ID_OK else None
    dlg.Destroy()
    return filename


def ShowOpenFileDialog(parent, message, wildcard, style=0):
    dlg = wx.FileDialog(parent, message=message, wildcard=wildcard, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_CHANGE_DIR | style)
    filename = dlg.GetPath() if dlg.ShowModal() == wx.ID_OK else None
    dlg.Destroy()
    return filename


def ShowSimpleMessageDialog(parent, message, caption):
    dlg = wx.MessageDialog(parent, message=message, caption=caption, style=wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()
