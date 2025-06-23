# MenuTitle: Stem Tool

from mojo.roboFont import AllFonts
from mojo.subscriber import Subscriber
import ezui


class StemTool(Subscriber, ezui.WindowController):

    def build(self):
        content = """
        | Name         | StemSnapH     | StemSnapV     | @fontTable
        = HorizontalStack
        > Add H Stem
        > (+-) @HStemButton
        > Add V Stem
        > (+-) @VStemButton
        > (Clear values) @clearButton
        > (Save all) @saveButton
        """

        descriptionData = dict(
            fontTable=dict(
                items=[],
                height=200,
                columnDescriptions=[
                    dict(identifier="name", title="Name", width=130),
                    dict(identifier="stemSnapH", title="StemSnapH", width=150),
                    dict(identifier="stemSnapV", title="StemSnapV", width=150),
                ],
            )
        )

        self.w = ezui.EZPanel(
            title="Stem Tool",
            size=(500, "auto"),
            content=content,
            descriptionData=descriptionData,
            controller=self,
        )

    def started(self):
        self.refreshTable()
        self.w.open()

    def saveButtonCallback(self, sender):
        self.saveFonts()

    def refreshTable(self):
        items = []
        for font in AllFonts():
            name = font.info.familyName + " " + font.info.styleName or "Untitled"
            stemSnapH = getattr(font.info, "postscriptStemSnapH", None)
            stemSnapV = getattr(font.info, "postscriptStemSnapV", None)
            # comma-separated string for display
            stemSnapH_str = ", ".join(str(v) for v in stemSnapH) if stemSnapH else ""
            stemSnapV_str = ", ".join(str(v) for v in stemSnapV) if stemSnapV else ""
            items.append(
                dict(name=name, stemSnapH=stemSnapH_str, stemSnapV=stemSnapV_str)
            )
        self.w.getItem("fontTable").set(items=items)

    def saveFonts(self):
        for font in AllFonts():
            font.save()

    def fontDocumentDidOpen(self, info):
        self.refreshTable()

    def fontDocumentDidClose(self, info):
        self.refreshTable()

    def HStemButtonAddCallback(self, sender):
        f = CurrentFont()
        g = CurrentGlyph()
        y = []
        for c in g:
            for p in c.points:
                if p.selected:
                    y.append(p.y)
        h_stem = abs(y[1] - y[0])
        if len(f.info.postscriptStemSnapH) <= 11:
            f.info.postscriptStemSnapH.append(h_stem)
        else:
            print("Maximum of 12 values reached")
        self.refreshTable()

    def HStemButtonRemoveCallback(self, sender):
        f = CurrentFont()
        stem_snap_h = f.info.postscriptStemSnapH
        if stem_snap_h and len(stem_snap_h) > 0:
            stem_snap_h = stem_snap_h[:-1]
            f.info.postscriptStemSnapH = stem_snap_h
        self.refreshTable()

    def VStemButtonAddCallback(self, sender):
        f = CurrentFont()
        g = CurrentGlyph()
        x = []
        for c in g:
            for p in c.points:
                if p.selected:
                    x.append(p.x)
        v_stem = abs(x[1] - x[0])
        if len(f.info.postscriptStemSnapV) <= 11:
            f.info.postscriptStemSnapV.append(v_stem)
        else:
            print("Maximum of 12 values reached")
        self.refreshTable()

    def VStemButtonRemoveCallback(self, sender):
        f = CurrentFont()
        stem_snap_v = f.info.postscriptStemSnapV
        if stem_snap_v and len(stem_snap_v) > 0:
            stem_snap_v = stem_snap_v[:-1]
            f.info.postscriptStemSnapV = stem_snap_v
        self.refreshTable()

    def clearButtonCallback(self, sender):
        for font in AllFonts():
            font.info.postscriptStemSnapH = []
            font.info.postscriptStemSnapV = []
        self.refreshTable()
        print("Cleared all stem values.")


if __name__ == "__main__":
    StemTool()
