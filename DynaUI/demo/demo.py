# -*- coding: utf-8 -*-

import os
import wx
from DynaUI import *

SF_000A4 = wx.SizerFlags().Border(wx.ALL, 4)
SF_110A4 = wx.SizerFlags().Expand().Border(wx.ALL, 4).Proportion(1)
SF_410A4 = wx.SizerFlags().Expand().Border(wx.ALL, 4).Proportion(4)
SF_010A4 = wx.SizerFlags().Expand().Border(wx.ALL, 4)
SF_001A4 = wx.SizerFlags().Center().Border(wx.ALL, 4)
SF_010A2 = wx.SizerFlags().Expand().Border(wx.ALL, 2)

SIZE_NORMAL = wx.Size(48, 30)
SIZE_LONG = wx.Size(80, 30)
SIZE_SQUARE = wx.Size(24, 24)


# ===================================================== Showcase ======================================================
class ExampleUI(wx.Frame):
    def __init__(self, r, s, l):
        self.R = r
        self.S = s
        self.L = l
        super().__init__(parent=None, title="DynaUI", pos=wx.DefaultPosition, size=wx.Size(1280, 800))
        self.SetIcon(wx.Icon(self.R["__DynaUI__"]))
        self.SetFont(self.R["FONT_N"])
        self.SetDoubleBuffered(True)

        self.Tool = Tool(self, edge=("", "B"))
        self.VTool = Tool(self, edge=("T", "RB"), orientation=wx.VERTICAL)
        self.Info = Info(self, edge=("T", ""))
        self.Info.AddItems((wx.StaticText(self.Info, label="status"), 0))
        items = (
            ("N", "TOOL_SETTING", self.ShowDialog), "|",
            ("N", "TOOL_SETTING", (self.Tool.SetItemSize, wx.Size(64, 64))),
            ("N", "TOOL_SETTING", (self.Tool.SetItemSize, wx.Size(32, 32))), "|",
            ("T", "TOOL_SETTING", None, {"toggle": 1, "res": "R"}), "|",
            ("B", "TOOL_SETTING", None, {"toggle": 1, "group": "whatever", "res": "X"}),
            ("B", "TOOL_SETTING", None, {"toggle": 0, "group": "whatever", "res": "Y"}),
            ("B", "TOOL_SETTING", None, {"toggle": 0, "group": "whatever", "res": "Z"}),)
        self.Tool.AddItems(*items)
        self.VTool.AddItems(*items)

        self.Main = BaseControl(self)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.Main.SetSizer(MainSizer)

        # ==================================================
        MainSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, tag="---- Various Buttons | Resource/Border Style ----"), SF_010A4)
        Sizer = wx.WrapSizer()
        Sizer.Add(ButtonToggle(self.Main, size=SIZE_NORMAL, tag="Off", tag2="On", toggle=True), SF_000A4)
        self.AddSeparator(Sizer)
        Sizer.Add(ButtonBundle(self.Main, size=SIZE_NORMAL, tag="1/3", group="whatever"), SF_000A4)
        Sizer.Add(ButtonBundle(self.Main, size=SIZE_NORMAL, tag="2/3", group="whatever", toggle=True), SF_000A4)
        Sizer.Add(ButtonBundle(self.Main, size=SIZE_NORMAL, tag="3/3", group="whatever"), SF_000A4)
        self.AddSeparator(Sizer)
        Sizer.Add(Button(self.Main, size=SIZE_NORMAL, tag="X", res="X"), SF_000A4)
        Sizer.Add(Button(self.Main, size=SIZE_NORMAL, tag="Y", res="Y"), SF_000A4)
        Sizer.Add(Button(self.Main, size=SIZE_NORMAL, tag="Z", res="Z"), SF_000A4)
        self.AddSeparator(Sizer)
        Sizer.Add(PickerColor(self.Main, size=SIZE_NORMAL), SF_000A4)
        Sizer.Add(PickerFont(self.Main, size=SIZE_NORMAL), SF_000A4)
        Sizer.Add(PickerDirection(self.Main, size=SIZE_NORMAL), SF_000A4)
        Sizer.Add(PickerNumber(self.Main, size=SIZE_NORMAL), SF_000A4)
        Sizer.Add(PickerValue(self.Main, size=SIZE_NORMAL, selected=-1, choices=[str(i) for i in range(40)]), SF_000A4)
        self.AddSeparator(Sizer)
        b1 = Button(self.Main, size=SIZE_NORMAL, tag=("Click", "B", 0, -2), pic=(self.R["UI_IMAGE2"], "T", 0, 2), func=lambda: (b2.Enable(not b2.IsEnabled()), b2.ReDraw()))
        b2 = Button(self.Main, size=SIZE_NORMAL, tag=("Click", "LT", 2, 2), pic=(self.R["UI_IMAGE2"], "RB", -2, -2), func=lambda: (b1.Enable(not b1.IsEnabled()), b1.ReDraw()))
        Sizer.Add(b1, SF_000A4)
        Sizer.Add(b2, SF_000A4)
        Sizer.Add(Slider(self.Main, size=(212, 30)), SF_010A4)
        Sizer.Add(HyperLink(self.Main, size=SIZE_LONG, tag=("GitHub", "L", 24), pics=(self.R["AP_ARROW_U"], "L", 4), url="github.com/yadizhou/DynaUI"), SF_110A4)

        MainSizer.Add(Sizer)
        Sizer = wx.WrapSizer()
        for res in ("D", "L", "B"):
            for edge in (None, "D", "L", "EM", "BE", "H", "V"):
                Sizer.Add(Button(self.Main, size=SIZE_NORMAL, tag="%s\n%s" % (res, edge), res=res, edge=edge), SF_000A4)
            if res != "B":
                self.AddSeparator(Sizer)
        MainSizer.Add(Sizer)

        # ==================================================
        MainSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, tag="---- Position: Tag & Image | Miscellaneous ----"), SF_010A4)
        Sizer = wx.BoxSizer(wx.HORIZONTAL)
        GridSizer = wx.GridSizer(3, 0, 0)
        for pos in ("LT", "T", "RT", "L", "C", "R", "LB", "B", "RB"):
            GridSizer.Add(Button(self.Main, size=SIZE_SQUARE, tag=(pos, pos), res="L", edge="EM"))
        for _ in range(3):
            GridSizer.Add(4, 4)
        for pos in ("LT", "T", "RT", "L", "C", "R", "LB", "B", "RB"):
            GridSizer.Add(ButtonBundle(self.Main, size=SIZE_SQUARE, pic=(self.R["UI_IMAGE2"], pos), group="whatever", res="L", edge="BE"))
        Sizer.Add(GridSizer, SF_000A4)
        self.AddSeparator(Sizer)

        SubSizer = wx.BoxSizer(wx.VERTICAL)
        SubSizer.Add(SwitchingText(self.Main, size=wx.Size(80, 20), values=("Switching", "Text", "Example"), bg="D"), SF_001A4)
        SubSizer.Add(StaticBitmap(self.Main, bitmap=self.R["UI_IMAGE3"]))
        SubSizer.Add(TextWithHint(self.Main, hint="TextWithHint", style=wx.BORDER_SIMPLE | wx.TE_MULTILINE), SF_110A4)
        Sizer.Add(SubSizer, SF_010A4)
        self.AddSeparator(Sizer)

        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, tag=("Z", "T"), shape="R"), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, tag="Z", shape="C"), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, tag=("Z", "B"), shape="L"), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, tag="Z", shape="R"), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, tag=("Z", "T"), shape="B", zOrder=1), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, tag="Z", shape="R", zOrder=1), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, tag=("Z", "B"), shape="C", zOrder=1), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, tag="Z", shape="L", zOrder=1), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, tag=("Z", "T"), shape="R", zOrder=1), SF_010A2)
        SubSizer = wx.BoxSizer(wx.VERTICAL)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, tag=" TWO ARROW  ", shape="B"), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, tag=" RECTANGLE  ", shape="S"), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, tag=" TWO CORNER ", shape="C"), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, tag=" LEFT ARROW ", shape="L"), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, tag=" RIGHT ARROW", shape="R"), SF_010A2)
        Sizer.Add(SubSizer, 1)
        SubSizer = wx.BoxSizer(wx.VERTICAL)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, tag=" TWO ARROW  ", shape="B", zOrder=1), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, tag=" RECTANGLE  ", shape="S", zOrder=1), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, tag=" TWO CORNER ", shape="C", zOrder=1), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, tag=" LEFT ARROW ", shape="L", zOrder=1), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, tag=" RIGHT ARROW", shape="R", zOrder=1), SF_010A2)
        Sizer.Add(SubSizer, 1)
        MainSizer.Add(Sizer, 0, wx.EXPAND)

        # ==================================================
        MainSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, tag="------- Scrolled --------"), SF_010A4)
        Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Sizer.Add(ListCtrl(self.Main, (("ListBox",), ("is",), ("one",), ("column",), ("ListCtrl",)) * 100, (-1,)), SF_110A4)
        Sizer.Add(ListCtrl(self.Main, [("A%s" % i, "B%s" % i, "C%s" % i) for i in range(200)], (-2, -2, -2)), SF_110A4)
        iv = ImageViewer(self.Main, self.R["UI_IMAGE4"])
        Sizer.Add(Hider(self.Main, targets=(iv,), edge=None), SF_010A2)
        Sizer.Add(iv, SF_410A4)
        MainSizer.Add(Sizer, 1, wx.EXPAND)

        MainSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, tag="------- ArtProvider --------"), SF_010A4)
        Sizer = wx.WrapSizer()
        for key in self.R:
            if key.startswith("AP_"):
                t = ToolNormal(self.Main, size=SIZE_SQUARE, pics=self.R[key], edge="D")
                t.SetTip(self.Info.SetStatus, key)
                Sizer.Add(t, SF_000A4)
        MainSizer.Add(Sizer, 0, wx.EXPAND)

        # ==================================================
        MiddleSizer = wx.BoxSizer(wx.HORIZONTAL)
        MiddleSizer.Add(self.VTool, 0, wx.EXPAND)
        MiddleSizer.Add(self.Main, 1, wx.EXPAND)
        FrameSizer = wx.BoxSizer(wx.VERTICAL)
        FrameSizer.Add(self.Tool, 0, wx.EXPAND)
        FrameSizer.Add(MiddleSizer, 1, wx.EXPAND)
        FrameSizer.Add(self.Info, 0, wx.EXPAND)
        self.SetSizer(FrameSizer)
        self.Layout()
        self.Center(wx.BOTH)

    def ShowDialog(self):
        d = BaseDialog(self, "Dialog", main=Dialog)
        d.SetSize(d.GetEffectiveMinSize())
        d.Center()
        d.Play("FADEIN")

    def AddSeparator(self, Sizer):
        Sizer.Add(Separator(self.Main, orientation=wx.VERTICAL), SF_010A4)


class Dialog(BaseMain):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        Sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(Sizer)
        self.AddSectionHead(Sizer, tag="SectionHead", shape="C")
        self.AddButton(Sizer, label="Button", tag="Click me")
        self.AddButtonToggle(Sizer, label="ButtonToggle", tags=("No", "Yes"))
        self.AddButtonBundle(Sizer, label="ButtonBundle", choices=list("012345"), rows=2)
        self.AddStaticText(Sizer, label="StaticText", value="Dialog Example")
        self.AddLineCtrl(Sizer, label="LineCtrl")
        self.AddTextCtrl(Sizer, label="TextCtrl")
        self.AddListBox(Sizer, label="ListBox", choices=list("012345"), selected=3)
        self.AddPickerValue(Sizer, label="PickerValue", choices=list("012345"), selected=2)
        self.AddSeparator(Sizer)
        self.AddPickerFile(Sizer, label="PickerFile")

        # Sizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.SetSizer(Sizer)
        # Left = wx.BoxSizer(wx.VERTICAL)
        # Middle = wx.BoxSizer(wx.VERTICAL)
        # Right = wx.BoxSizer(wx.VERTICAL)
        # self.AddButton(Left, label="", tag="Button", width=40)
        # self.AddButton(Left, label="", tag="Button", width=-1)
        # self.AddButton(Left, label="123", tag="Button", width=40)
        # self.AddButton(Left, label="123", tag="Button", width=-1)
        # self.AddSeparator(Left)
        # self.AddButtonToggle(Left, label="", tags=("Button", "Nottub"), width=40)
        # self.AddButtonToggle(Left, label="", tags=("Button", "Nottub"), width=-1)
        # self.AddButtonToggle(Left, label="123", tags=("Button", "Nottub"), width=40)
        # self.AddButtonToggle(Left, label="123", tags=("Button", "Nottub"), width=-1)
        # self.AddSeparator(Left)
        # self.AddButtonBundle(Left, label="", tags=("A", "B", "C"), width=20, toggled=0, group="1")
        # self.AddButtonBundle(Left, label="", tags=("A", "B", "C"), width=-1, toggled=1, group="2")
        # self.AddButtonBundle(Left, label="123", tags=("A", "B", "C", "D", "E"), width=20, rows=2, toggled=2, group="3")
        # self.AddButtonBundle(Left, label="123", tags=("A", "B", "C", "D", "E", "F"), width=-1, rows=3, toggled=0, group="4")
        # self.AddPickerValue(Left, label="", choices=("A", "B", "C"), width=40)
        # self.AddPickerValue(Left, label="", choices=("A", "B", "C"), width=-1)
        # self.AddPickerValue(Left, label="123", choices=("A", "B", "C", "D", "E"), width=40)
        # self.AddPickerValue(Left, label="123", choices=("A", "B", "C", "D", "E", "F"), width=-1)
        # self.AddStaticText(Middle, "STA", "ssss", width=-1)
        # self.AddLineCtrl(Middle, "TEXT", width=100)
        # self.AddLineCtrl(Middle, "TEXT", width=-1)
        # self.AddSeparator(Middle)
        # self.AddTextCtrl(Middle, "TEXT", inline=1, height=-1, width=-1)
        # self.AddTextCtrl(Middle, "TEXT", inline=1, height=40, width=-1)
        # self.AddTextCtrl(Middle, "TEXT", inline=1, height=-1, width=40)
        # self.AddTextCtrl(Middle, "TEXT", inline=1, height=40, width=40)
        # self.AddTextCtrl(Right, "TEXT", inline=0, height=-1, width=-1)
        # self.AddTextCtrl(Right, "TEXT", inline=0, height=40, width=-1)
        # self.AddTextCtrl(Right, "TEXT", inline=0, height=-1, width=40)
        # self.AddTextCtrl(Right, "TEXT", inline=0, height=40, width=40)
        # self.AddTextCtrl(Right, "", inline=0, height=-1, width=-1)
        # self.AddTextCtrl(Right, "", inline=0, height=40, width=-1)
        # self.AddTextCtrl(Right, "", inline=0, height=-1, width=40)
        # self.AddTextCtrl(Right, "", inline=0, height=40, width=40)
        # self.AddStdButton(Right)
        # Sizer.Add(Left, 0, wx.EXPAND)
        # self.AddSeparator(Sizer)
        # Sizer.Add(Middle, 1, wx.EXPAND)
        # self.AddSeparator(Sizer)
        # Sizer.Add(Right, 1, wx.EXPAND)


if __name__ == "__main__":
    App = wx.App(redirect=0)

    Resource = Resource()
    Setting = Setting()
    Locale = Locale()

    MAIN_PATH = os.path.dirname(os.path.realpath(__file__))
    Here = lambda f="": os.path.join(MAIN_PATH, f)

    Resource["TOOL_SETTING"] = GetBitmaps(wx.Bitmap(Here("image1.png")), 20, 20)
    Resource["UI_IMAGE2"] = wx.Bitmap(Here("image2.png"))
    Resource["UI_IMAGE3"] = wx.Bitmap(Here("image3.png"))
    Resource["UI_IMAGE4"] = wx.Bitmap(Here("image4.jpg"))
    Locale["TOOL_SETTING"] = "Tool Buttons"

    Frame = ExampleUI(Resource, Setting, Locale)
    Frame.Show()
    App.MainLoop()
