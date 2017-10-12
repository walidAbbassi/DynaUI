# -*- coding: utf-8 -*-


import wx
from DynaUI import *

SF_000A4 = wx.SizerFlags().Border(wx.ALL, 4)
SF_110A4 = wx.SizerFlags().Expand().Border(wx.ALL, 4).Proportion(1)
SF_410A4 = wx.SizerFlags().Expand().Border(wx.ALL, 4).Proportion(4)
SF_010A4 = wx.SizerFlags().Expand().Border(wx.ALL, 4)
SF_001A4 = wx.SizerFlags().Center().Border(wx.ALL, 4)
SF_010A2 = wx.SizerFlags().Expand().Border(wx.ALL, 2)

SIZE_NORMAL = wx.Size(48, 30)
SIZE_SQUARE = wx.Size(24, 24)


# ===================================================== Showcase ======================================================
class ExampleUI(wx.Frame):
    def __init__(self, r, s, l):
        self.R = r
        self.S = s
        self.L = l
        super().__init__(parent=None, title="DynaUI", pos=wx.DefaultPosition, size=wx.Size(1280, 800))
        self.SetFont(self.R["FONT_N"])
        self.SetDoubleBuffered(True)

        self.Tool = Tool(self, edge=("", "B"))
        self.VTool = Tool(self, edge=("T", "RB"), orientation=wx.VERTICAL)
        self.Info = Info(self, edge=("T", ""))
        self.Info.AddItems((wx.StaticText(self.Info, label="status"), 0))
        items = (
            ("N", "TOOL_SETTING", self.ShowDialog), "|",
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
        MainSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, label="---- Various Buttons | Resource/Border Style ----"), SF_010A4)
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
        self.AddSeparator(Sizer)
        b1 = Button(self.Main, size=SIZE_NORMAL, tag=("Click", "B", 0, -2), pic=(self.R["UI_IMAGE2"], "T", 0, 2), func=lambda: (b2.Enable(not b2.IsEnabled()), b2.ReDraw()))
        b2 = Button(self.Main, size=SIZE_NORMAL, tag=("Click", "LT", 2, 2), pic=(self.R["UI_IMAGE2"], "RB", -2, -2), func=lambda: (b1.Enable(not b1.IsEnabled()), b1.ReDraw()))
        Sizer.Add(b1, SF_000A4)
        Sizer.Add(b2, SF_000A4)
        Sizer.Add(Slider(self.Main, size=(212, 30)), SF_010A4)
        Sizer.Add(TextWithHint(self.Main, hint="TextWithHint"))

        MainSizer.Add(Sizer)
        Sizer = wx.WrapSizer()
        for res in ("D", "L", "B"):
            for edge in (None, "D", "L", "EM", "BE", "H", "V"):
                Sizer.Add(Button(self.Main, size=SIZE_NORMAL, tag="%s\n%s" % (res, edge), res=res, edge=edge), SF_000A4)
            if res != "B":
                self.AddSeparator(Sizer)
        MainSizer.Add(Sizer)

        # ==================================================
        MainSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, label="---- Position: Tag & Image | Miscellaneous ----"), SF_010A4)
        Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Sizer1 = wx.GridSizer(3, 3, 0, 0)
        Sizer2 = wx.GridSizer(3, 3, 0, 0)
        for pos in ("LT", "T", "RT", "L", "C", "R", "LB", "B", "RB"):
            Sizer1.Add(Button(self.Main, size=SIZE_SQUARE, tag=(pos, pos), res="L", edge="EM"))
        for pos in ("LT", "T", "RT", "L", "C", "R", "LB", "B", "RB"):
            Sizer2.Add(Button(self.Main, size=SIZE_SQUARE, pic=(self.R["UI_IMAGE2"], pos), res="L", edge="BE"))
        Sizer.Add(Sizer1, SF_000A4)
        Sizer.Add(Sizer2, SF_000A4)
        self.AddSeparator(Sizer)
        pd = PickerDirection(self.Main, size=wx.Size(40, 40))
        Sizer.Add(Label(self.Main, size=wx.Size(120, 40), label="I redirect mouse\nevent to my target", target=pd), SF_001A4)
        Sizer.Add(pd, SF_001A4)
        self.AddSeparator(Sizer)
        Sizer.Add(SwitchingText(self.Main, size=wx.Size(80, 20), values=("Switching", "Text", "Example"), bg="D"), SF_001A4)
        Sizer.Add(StaticBitmap(self.Main, bitmap=self.R["UI_IMAGE3"]))

        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, label=("Z", "T"), shape="R"), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, label="Z", shape="C"), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, label=("Z", "B"), shape="L"), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, label="Z", shape="R"), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, label=("Z", "T"), shape="B", zOrder=1), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, label="Z", shape="R", zOrder=1), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, label=("Z", "B"), shape="C", zOrder=1), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, label="Z", shape="L", zOrder=1), SF_010A2)
        Sizer.Add(SectionHead(self.Main, orientation=wx.VERTICAL, label=("Z", "T"), shape="R", zOrder=1), SF_010A2)
        SubSizer = wx.BoxSizer(wx.VERTICAL)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, label=" TWO ARROW  ", shape="B"), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, label=" RECTANGLE  ", shape="R"), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, label=" TWO CORNER ", shape="C"), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, label=" LEFT ARROW ", shape="L"), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, label=" RIGHT ARROW", shape="R"), SF_010A2)
        Sizer.Add(SubSizer, 1)
        SubSizer = wx.BoxSizer(wx.VERTICAL)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, label=" TWO ARROW  ", shape="B", zOrder=1), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, label=" RECTANGLE  ", shape="R", zOrder=1), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, label=" TWO CORNER ", shape="C", zOrder=1), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, label=" LEFT ARROW ", shape="L", zOrder=1), SF_010A2)
        SubSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, label=" RIGHT ARROW", shape="R", zOrder=1), SF_010A2)
        Sizer.Add(SubSizer, 1)
        MainSizer.Add(Sizer, 0, wx.EXPAND)

        # ==================================================
        MainSizer.Add(SectionHead(self.Main, orientation=wx.HORIZONTAL, label="------- Scrolled --------"), SF_010A4)
        Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Sizer.Add(ListCtrl(self.Main, (("ListBox",), ("is",), ("one",), ("column",), ("ListCtrl",)) * 100, (-1,)), SF_110A4)
        Sizer.Add(ListCtrl(self.Main, [("A%s" % i, "B%s" % i, "C%s" % i) for i in range(200)], (-2, -2, -2)), SF_110A4)
        iv = ImageViewer(self.Main, self.R["UI_IMAGE4"])
        Sizer.Add(Hider(self.Main, targets=(iv,), size=(4, -1), edge=None), SF_010A2)
        Sizer.Add(iv, SF_410A4)
        MainSizer.Add(Sizer, 1, wx.EXPAND)

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
        Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(Sizer)

        Left = wx.BoxSizer(wx.VERTICAL)
        Middle = wx.BoxSizer(wx.VERTICAL)
        Right = wx.BoxSizer(wx.VERTICAL)
        self.AddButton(Left, label="", tag="Button", width=40)
        self.AddButton(Left, label="", tag="Button", width=-1)
        self.AddButton(Left, label="123", tag="Button", width=40)
        self.AddButton(Left, label="123", tag="Button", width=-1)
        self.AddSeparator(Left)
        self.AddButtonToggle(Left, label="", tags=("Button", "Nottub"), width=40)
        self.AddButtonToggle(Left, label="", tags=("Button", "Nottub"), width=-1)
        self.AddButtonToggle(Left, label="123", tags=("Button", "Nottub"), width=40)
        self.AddButtonToggle(Left, label="123", tags=("Button", "Nottub"), width=-1)
        self.AddSeparator(Left)
        self.AddButtonBundle(Left, label="", tags=("A", "B", "C"), width=20, toggled=0, group="1")
        self.AddButtonBundle(Left, label="", tags=("A", "B", "C"), width=-1, toggled=1, group="2")
        self.AddButtonBundle(Left, label="123", tags=("A", "B", "C"), width=20, toggled=2, group="3")
        self.AddButtonBundle(Left, label="123", tags=("A", "B", "C"), width=-1, toggled=0, group="4")

        self.AddStaticText(Middle, "STA", "ssss", width=-1)
        self.AddLineCtrl(Middle, "TEXT", width=100)
        self.AddLineCtrl(Middle, "TEXT", width=-1)
        self.AddSeparator(Middle)
        self.AddTextCtrl(Middle, "TEXT", inline=1, height=-1, width=-1)
        self.AddTextCtrl(Middle, "TEXT", inline=1, height=40, width=-1)
        self.AddTextCtrl(Middle, "TEXT", inline=1, height=-1, width=40)
        self.AddTextCtrl(Middle, "TEXT", inline=1, height=40, width=40)
        self.AddTextCtrl(Right, "TEXT", inline=0, height=-1, width=-1)
        self.AddTextCtrl(Right, "TEXT", inline=0, height=40, width=-1)
        self.AddTextCtrl(Right, "TEXT", inline=0, height=-1, width=40)
        self.AddTextCtrl(Right, "TEXT", inline=0, height=40, width=40)
        self.AddTextCtrl(Right, "", inline=0, height=-1, width=-1)
        self.AddTextCtrl(Right, "", inline=0, height=40, width=-1)
        self.AddTextCtrl(Right, "", inline=0, height=-1, width=40)
        self.AddTextCtrl(Right, "", inline=0, height=40, width=40)

        self.AddStdButton(Right)
        Sizer.Add(Left, 0, wx.EXPAND)
        self.AddSeparator(Sizer)
        Sizer.Add(Middle, 1, wx.EXPAND)
        self.AddSeparator(Sizer)
        Sizer.Add(Right, 1, wx.EXPAND)


if __name__ == "__main__":
    App = wx.App(redirect=0)

    Resource = Resource()
    Setting = Setting()
    Locale = Locale()

    Resource["TOOL_SETTING"] = GetBitmaps(wx.Bitmap("image1.png"), 20, 20)
    Resource["UI_IMAGE2"] = wx.Bitmap("image2.png")
    Resource["UI_IMAGE3"] = wx.Bitmap("image3.png")
    Resource["UI_IMAGE4"] = wx.Bitmap("image4.jpg")
    Locale["TOOL_SETTING"] = "Tool Buttons"

    Frame = ExampleUI(Resource, Setting, Locale)
    Frame.Show()
    App.MainLoop()
