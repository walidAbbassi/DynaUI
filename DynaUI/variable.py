# -*- coding: utf-8 -*-


import wx
from . import images as Img
from .abstract import BaseDict
from .utility import AlphaBlend, GetBitmaps
from .pixelate import BitmapFontList

__all__ = ["SETTINGS", "Locale", "Setting", "Resource"]

# Global UI settings # TODO put more params here to globally control the look
SETTINGS = {
    "SCROLL_DIAMETER"  : 16,
    "SCROLL_UNIT"      : 3,
    "SCROLL_MULTIPLIER": 10,
    "DLG_HEAD"         : 24,
    "DLG_HEAD_BTN"     : wx.Size(18, 18),
    "DLG_MAIN_MARGIN"  : 4,
    "DLG_MAIN_LABEL_W" : 80,
    "DLG_MAIN_LINE_H"  : 24,
    "DLG_MAIN_BUTTON_W": 80,
}


class Locale(BaseDict):
    DEFAULT = {}

    def __init__(self, fp=None):
        super().__init__()
        self.dict = self.DEFAULT
        if fp is not None:
            self.Load(fp)


class Setting(BaseDict):
    DEFAULT = {}

    def __init__(self, fp=None):
        super().__init__()
        self.dict = self.DEFAULT
        if fp is not None:
            self.Load(fp)


class Resource(BaseDict):
    DEFAULT = {
        "COLOR_R"            : "#ff0000",
        "COLOR_X"            : "#ff8000",
        "COLOR_Y"            : "#0080ff",
        "COLOR_Z"            : "#ff0080",

        "COLOR_EDGE_D"       : "#141414",
        "COLOR_EDGE_L"       : "#5a5a5a",
        "COLOR_EDGE_B"       : "#808080",
        "COLOR_BG_D"         : "#343434",
        "COLOR_BG_L"         : "#404040",
        "COLOR_BG_B"         : "#606060",
        "COLOR_FG_D"         : "#808080",
        "COLOR_FG_L"         : "#c0c0c0",
        "COLOR_FG_B"         : "#ffffff",

        "COLOR_ACTIVE"       : "#2675b2",
        "COLOR_INACTIVE"     : "#80808080",

        "COLOR_SIZING"       : "#00c0ff",
        "COLOR_DLG_HEAD_FG_I": "#ffffff",
        "COLOR_DLG_HEAD_FG_O": "#202020",
        "COLOR_DLG_HEAD_BG_I": "#303030",
        "COLOR_DLG_HEAD_BG_O": "#808080",
    }

    def __init__(self, fp=None):
        super().__init__()
        self.dict = self.DEFAULT
        if fp is not None:
            self.Load(fp)
        self["__DynaUI__"] = Img.DynaUI.GetBitmap()
        # ---- Border ----
        self["PEN_EDGE_D"] = wx.Pen(self["COLOR_EDGE_D"])
        self["PEN_EDGE_L"] = wx.Pen(self["COLOR_EDGE_L"])
        self["PEN_EDGE_B"] = wx.Pen(self["COLOR_EDGE_B"])
        self["BRUSH_EDGE_D"] = wx.Brush(self["COLOR_EDGE_D"])
        self["BRUSH_EDGE_L"] = wx.Brush(self["COLOR_EDGE_L"])
        self["BRUSH_EDGE_B"] = wx.Brush(self["COLOR_EDGE_B"])
        # ---- Background ----
        self["BRUSH_BG_D"] = wx.Brush(self["COLOR_BG_D"])
        self["BRUSH_BG_L"] = wx.Brush(self["COLOR_BG_L"])
        self["BRUSH_BG_B"] = wx.Brush(self["COLOR_BG_B"])
        # ---- Foreground ----
        self["BRUSH_FG_D"] = wx.Brush(self["COLOR_FG_D"])
        self["BRUSH_FG_L"] = wx.Brush(self["COLOR_FG_L"])
        self["BRUSH_FG_B"] = wx.Brush(self["COLOR_FG_B"])
        # ---- Button ----
        self["BRUSH_SET__D"] = {i: self["BRUSH_BG_D"] for i in ("00", "40", "80", "C0", "FF")}
        self["BRUSH_SET__L"] = {i: self["BRUSH_BG_L"] for i in ("00", "40", "80", "C0", "FF")}
        self["BRUSH_SET__B"] = {i: self["BRUSH_BG_B"] for i in ("00", "40", "80", "C0", "FF")}
        self["BRUSH_SET_D"] = self.GetBrushSet(self["COLOR_BG_D"], self["COLOR_ACTIVE"])
        self["BRUSH_SET_L"] = self.GetBrushSet(self["COLOR_BG_L"], self["COLOR_ACTIVE"])
        self["BRUSH_SET_B"] = self.GetBrushSet(self["COLOR_BG_B"], self["COLOR_ACTIVE"])
        self["BRUSH_SET_R"] = self.GetBrushSet(self["COLOR_BG_D"], self["COLOR_R"])
        self["BRUSH_SET_X"] = self.GetBrushSet(self["COLOR_BG_D"], self["COLOR_X"])
        self["BRUSH_SET_Y"] = self.GetBrushSet(self["COLOR_BG_D"], self["COLOR_Y"])
        self["BRUSH_SET_Z"] = self.GetBrushSet(self["COLOR_BG_D"], self["COLOR_Z"])
        self["BRUSH_DISABLED"] = wx.Brush(self["COLOR_INACTIVE"])
        # ---- Cursor ----
        self["CURSOR_NORMAL"] = wx.Cursor(wx.CURSOR_DEFAULT)
        self["CURSOR_SIZING"] = wx.Cursor(wx.CURSOR_SIZENWSE)
        self["CURSOR_MOVING"] = wx.Cursor(wx.CURSOR_SIZING)
        self["CURSOR_SASH_H"] = wx.Cursor(wx.CURSOR_SIZEWE)
        self["CURSOR_SASH_V"] = wx.Cursor(wx.CURSOR_SIZENS)
        # ---- Image ----
        self["BITMAP_SLIDER"] = Img.Slider.GetBitmap()
        # ---- Image Set ----
        for key in (
                "AP_MINI", "AP_MAXI", "AP_EXIT", "AP_HELP",
                "AP_ARROW_L", "AP_ARROW_R", "AP_ARROW_U", "AP_ARROW_D",
                "AP_TRIANGLE_L", "AP_TRIANGLE_R", "AP_TRIANGLE_U", "AP_TRIANGLE_D",
                "AP_CROSS", "AP_CHECK",
                "AP_APPLY", "AP_RESET",
                "AP_BEGIN", "AP_PAUSE", "AP_ABORT",
                "AP_TRASH", "AP_LOCAL", "AP_CLOUD",
        ):
            self[key] = GetBitmaps(getattr(Img, key).GetBitmap(), 20, 20)
        self["AP_HIDER_V"] = [self["AP_MINI"][0].ConvertToImage().AdjustChannels(x, x, x).Rotate90().Mirror().ConvertToBitmap() for x in (0.55, 0.70, 0.85, 1)]
        self["AP_HIDER_H"] = [self["AP_MINI"][0].ConvertToImage().AdjustChannels(x, x, x).ConvertToBitmap() for x in (0.55, 0.70, 0.85, 1)]
        # ---- Dialog ----
        self["COLOR_DLG_HEAD_FG"] = self.GetColorSet(self["COLOR_DLG_HEAD_FG_I"], self["COLOR_DLG_HEAD_FG_O"])
        self["BRUSH_DLG_HEAD_BG"] = self.GetBrushSet(self["COLOR_DLG_HEAD_BG_I"], self["COLOR_DLG_HEAD_BG_O"])
        self["BRUSH_DLG_SET_O"] = self.GetBrushSet(self["COLOR_DLG_HEAD_BG_O"], self["COLOR_ACTIVE"])
        self["BRUSH_DLG_SET_I"] = self.GetBrushSet(self["COLOR_DLG_HEAD_BG_I"], self["COLOR_ACTIVE"])
        self["BRUSH_DLG_SET_O_R"] = self.GetBrushSet(self["COLOR_DLG_HEAD_BG_O"], self["COLOR_R"])
        self["BRUSH_DLG_SET_I_R"] = self.GetBrushSet(self["COLOR_DLG_HEAD_BG_I"], self["COLOR_R"])
        # ---- Font ----
        self.SetMainFont(8, wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT).GetFaceName())
        self.TheBitmapFontList = BitmapFontList()
        self.GetBitmapFont = self.TheBitmapFontList.FindOrCreateFont
        for font in self.TheBitmapFontList.FontPool:
            self["BITMAPFONT_%s" % font] = self.GetBitmapFont(font, "#ffffff")

    def SetMainFont(self, point, fontface):
        self["FONT_N"] = wx.Font(point, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, fontface)  # Normal
        self["FONT_I"] = wx.Font(point, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, fontface)  # Impact
        self["FONT_H"] = wx.Font(point, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, fontface)  # Handwritten
        self["FONT_J"] = wx.Font(point, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, fontface)  # H I J
        self["FONT_U"] = wx.Font(point, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True, fontface)  # Underline

    def GetColorSet(self, bg, fg):
        return {"00": AlphaBlend(bg, fg, 0),
                "40": AlphaBlend(bg, fg, 0.25),
                "80": AlphaBlend(bg, fg, 0.5),
                "C0": AlphaBlend(bg, fg, 0.75),
                "FF": AlphaBlend(bg, fg, 1)}

    def GetBrushSet(self, bg, fg):
        d = self.GetColorSet(bg, fg)
        for k in d:
            d[k] = wx.Brush(d[k])
        return d

    def GetPenSet(self, bg, fg):
        d = self.GetColorSet(bg, fg)
        for k in d:
            d[k] = wx.Pen(d[k])
        return d
