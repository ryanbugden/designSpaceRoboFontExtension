import AppKit
import ezui
from lib.cells.doubleClickCell import RFDoubleClickCell
from mojo.extensions import ExtensionBundle


BUNDLE = ExtensionBundle("DesignspaceEditor2")

numberFormatter = AppKit.NSNumberFormatter.alloc().init()
numberFormatter.setNumberStyle_(AppKit.NSNumberFormatterDecimalStyle)
numberFormatter.setAllowsFloats_(True)
numberFormatter.setLocalizesFormat_(False)
numberFormatter.setUsesGroupingSeparator_(False)


def makeTableImage(symbolName):
    return ezui.makeImage(
        symbolName=symbolName,
        template=True,
        symbolConfiguration=dict(
            weight="regular",
            scale="small",
        )
    )


INFO_IMAGE_COLUMN = makeTableImage("info.circle")
INFO_IMAGE_CELL = makeTableImage("info.circle.fill")
AXIS_REGISTERED_SYMBOL = makeTableImage("r.circle")  # 􀀦
AXIS_HAS_MAP_SYMBOL = makeTableImage("map")  # 􀙊
AXIS_HAS_LABELS_SYMBOL = makeTableImage("tag")  # 􀋡
SOURCE_HAS_PATH_SYMBOL = makeTableImage("opticaldiscdrive")  # 􀤄
SOURCE_IS_DEFAULT_SYMBOL = makeTableImage("mappin.and.ellipse")  # 􀎪
SOURCE_HAS_LOCALISED_FAMILY_NAMES_SYMBOL = makeTableImage("globe")  # 􀆪
SOURCE_HAS_MUTED_GLYPHS_SYMBOL = makeTableImage("speaker.slash")  # 􀋝
CHECKMARK = makeTableImage("checkmark")
# EMPTY_IMAGE = ezui.makeImage( 
#     symbolName="checkmark",
#     template=True,
#     symbolConfiguration=dict(
#         weight="regular",
#         scale="small",
#         colors=[(1,0,0,0)]
#     )
# )
REGISTERED_AXES = {
    # Name          Tag      Min   Def   Max    Discrete  Labels
    "Weight":       ("wght", 400,  400,  700,   [],       dict(en="Weight")),
    "Width":        ("wdth", 50,   100,  100,   [],       dict(en="Width")),
    "Optical Size": ("opsz", 10,   10,   72,    [],       dict(en="Optical Size")),
    "Slant":        ("slnt", -10,  0,    0,     [],       dict(en="Slant")),
    "Italic":       ("ital", None, None, None,  [0, 1],   dict(en="Italic")),
}


def doubleClickCell(callback, image=None):
    cell = RFDoubleClickCell.alloc().init()
    cell.setDoubleClickCallback_(callback)
    cell.setImage_(image)
    return cell


def checkmarkValueConverter(bool):
    return "✓" if bool else ""


# def discreteValueConverter(value):
#     if value is None:
#         return []
#     return value


class Controller(ezui.WindowController):
    def build(self):
        content = """
        = ToolbarTabs

        * ToolbarTab: Axes                  @axesTab
        > |---|                             @axesTable
        > * HorizontalStack                 @axesStack
        >> (+-)                             @axesAddRemoveButton

        * ToolbarTab: Sources               @sourcesTab
        >|---|                              @sourcesTable
        > * HorizontalStack                 @sourcesStack
        >> (+-)
        >> (...)                            @sourcesActions

        * ToolbarTab: Instances             @instancesTab
        > |---|                             @instancesTable
        > * HorizontalStack                 @instancesStack
        >> (+-)
        >> ( Preview Instances )            @instancesPreview
        >> (...)                            @instancesActions

        * ToolbarTab: Rules                 @rulesTab
        > * CodeEditor                      @rulesEditor

        * ToolbarTab: Labels                @labelsTab
        > * CodeEditor                      @labelsEditor
        > * HorizontalStack                 @labelsStack
        >> ( Preview Labels )               @labelsPreviewButton

        * ToolbarTab: Variable Fonts        @vfsTab
        > * CodeEditor                      @vfsEditor
        > * HorizontalStack                 @vfsStack
        >> ( Preview Variable Fonts)        @vfsPreviewButton

        * ToolbarTab: Problems              @problemsTab
        > |---|                             @problemsTable
        > * HorizontalStack                 @problemsStack
        >> ( Validate Designspace )         @problemsValidateButton

        * ToolbarTab: Notes                 @notesTab
        > [[__]]                            @notesEditor
        """

        marginDescriptions = dict(margins=(10, 0, 10, 10))
        descriptionData = dict(
            axesTab=dict(
                image=BUNDLE.getResourceImage("toolbar_30_30_icon_axes")
            ),
            axesStack=marginDescriptions,
            axesTable=dict(
                width="fill",
                height="fill",
                allowsSorting=True,
                columnDescriptions=[
                    dict(title="ℹ️", identifier="genericInfoButton", width=20, cellDescription=dict(cellType="Image"), editable=False, cell=doubleClickCell(self.axisListDoubleClickCallback, INFO_IMAGE_CELL)),#, cell=axisDoubleClickCell),
                    dict(title="Ⓡ", identifier="axisIsRegistered", width=20, cellDescription=dict(valueToCellConverter=checkmarkValueConverter), allowsSorting=False, editable=False, sortable=True),
                    dict(title="Name", identifier="axisName", allowsSorting=False, editable=True, sortable=True),
                    dict(title="Tag", identifier="axisTag", width=70, allowsSorting=False, editable=True, sortable=True),
                    dict(title="Minimum", identifier="axisMinimum", width=70, allowsSorting=False, editable=True, formatter=numberFormatter, sortable=True),
                    dict(title="Default", identifier="axisDefault", width=70, allowsSorting=False, editable=True, formatter=numberFormatter, sortable=True),
                    dict(title="Maximum", identifier="axisMaximum", width=70, allowsSorting=False, editable=True, formatter=numberFormatter, sortable=True),
                    dict(title="Discrete Values", identifier="axisDiscreteValues", cellDescription=dict(valueType="integerList"), idth=100, allowsSorting=False, editable=True, sortable=True),
                    dict(title="Hidden", identifier="axisIsHidden", width=50, cellDescription=dict(cellType="Checkbox"), allowsSorting=False, editable=True, sortable=True),
                    dict(title="📈", identifier="axisHasMap", width=20, cellDescription=dict(valueToCellConverter=checkmarkValueConverter), allowsSorting=False, editable=False, sortable=True),
                    dict(title="🏷️", identifier="axisHasLabels", width=20, cellDescription=dict(valueToCellConverter=checkmarkValueConverter), allowsSorting=False, editable=False, sortable=True),
                ]
            ),

            sourcesTab=dict(
                image=BUNDLE.getResourceImage("toolbar_30_30_icon_sources")
            ),
            sourcesStack=marginDescriptions,
            sourcesTable=dict(
                width="fill",
                height="fill",
                allowsSorting=True,
                columnDescriptions=[
                    dict(title="ℹ️", identifier="genericInfoButton", width=20, cellDescription=dict(cellType="Image"), editable=False, cell=doubleClickCell(self.sourceListDoubleClickCallback, INFO_IMAGE_CELL)),
                    dict(title="💾", identifier="sourceHasPath", width=20, cellDescription=dict(cellType="Image"), editable=False, sortable=True),
                    dict(title="📍", identifier="sourceIsDefault", width=20, cellDescription=dict(cellType="Image"), editable=False, sortable=True),
                    dict(title="UFO", identifier="sourceUFOFileName", width=200, minWidth=100, maxWidth=350, editable=False, sortable=True),
                    dict(title="Family Name", identifier="sourceFamilyName", editable=True, width=130, minWidth=130, maxWidth=250, sortable=True),
                    dict(title="Style Name", identifier="sourceStyleName", editable=True, width=130, minWidth=130, maxWidth=250, sortable=True),
                    dict(title="Layer Name", identifier="sourceLayerName", editable=True, width=130, minWidth=130, maxWidth=250, sortable=True),
                    dict(title="🌐", identifier="sourceHasLocalisedFamilyNames", cellDescription=dict(cellType="Image"), width=20, allowsSorting=False, editable=False, sortable=True),
                    dict(title="🔕", identifier="sourceHasMutedGlyphs", cellDescription=dict(cellType="Image"), width=20, allowsSorting=False, editable=False, sortable=True),
                ]
            ),
            sourcesActions=dict(
                itemDescriptions=[
                    dict(identifier="basicItem", text="Open Source UFO"),
                    "----",
                    dict(identifier="basicItem", text="Add Open UFOs"),
                    dict(identifier="basicItem", text="Replace UFO"),
                ]
            ),

            instancesTab=dict(
                image=BUNDLE.getResourceImage("toolbar_30_30_icon_instances")
            ),
            instancesStack=marginDescriptions,
            instancesTable=dict(
                width="fill",
                height="fill",
                allowsSorting=True,
                columnDescriptions=[
                    dict(title="UFO", identifier="instanceUFOFileName", width=200, minWidth=100, maxWidth=350, editable=False, sortable=True),
                    dict(title="Family Name", identifier="instanceFamilyName", editable=True, width=130, minWidth=130, maxWidth=250, sortable=True),
                    dict(title="Style Name", identifier="instanceStyleName", editable=True, width=130, minWidth=130, maxWidth=250, sortable=True),
                ],
                items=[
                    dict(
                        instanceUFOFileName="c",
                        instanceFamilyName="c",
                        instanceStyleName="c",
                    ),
                    dict(
                        instanceUFOFileName="b",
                        instanceFamilyName="b",
                        instanceStyleName="b",
                    ),
                    dict(
                        instanceUFOFileName="a",
                        instanceFamilyName="a",
                        instanceStyleName="a",
                    ),
                ],
            ),
            instancesActions=dict(
                itemDescriptions=[
                    dict(identifier="basicItem", text="Duplicate Instance"),
                    dict(identifier="basicItem", text="Add Sources as Instances"),
                    "----",
                    dict(identifier="basicItem", text="Generate With MutatorMath"),
                    dict(identifier="basicItem", text="Generate With VarLib"),
                ]
            ),

            rulesTab=dict(
                image=BUNDLE.getResourceImage("toolbar_30_30_icon_rules")
            ),
            rulesEditor=dict(
                width="fill",
                height="fill",
                showLineNumbers=False
            ),

            labelsTab=dict(
                image=BUNDLE.getResourceImage("toolbar_30_30_icon_location_labels")
            ),
            labelsStack=marginDescriptions,
            labelsEditor=dict(
                width="fill",
                height="fill",
                showLineNumbers=False
            ),
            labelsActions=dict(
                itemDescriptions=[
                    dict(identifier="basicItem", text="Preview Labels"),
                ]
            ),

            vfsTab=dict(
                image=BUNDLE.getResourceImage("toolbar_30_30_icon_variable_fonts")
            ),
            vfsStack=marginDescriptions,
            vfsEditor=dict(
                width="fill",
                height="fill",
                showLineNumbers=False
            ),
            vfsActions=dict(
                itemDescriptions=[
                    dict(identifier="basicItem", text="Preview Variable Fonts"),
                ]
            ),

            problemsTab=dict(
                image=BUNDLE.getResourceImage("toolbar_30_30_icon_problems")
            ),
            problemsStack=marginDescriptions,
            problemsTable=dict(
                width="fill",
                height="fill",
                allowsSorting=True,
                columnDescriptions=[
                    dict(title="", identifier="problemIcon", width=20, sortable=True),
                    dict(title="Where", identifier="problemClass", width=130, sortable=True),
                    dict(title="What", identifier="problemDescription", minWidth=200, width=200, maxWidth=1000, sortable=True),
                    dict(title="Specifically", identifier="problemData", minWidth=200, width=200, maxWidth=1000, sortable=True),
                ]
            ),

            notesTab=dict(
                image=BUNDLE.getResourceImage("toolbar_30_30_icon_notes")
            ),
            notesEditor=dict(
                width="fill",
                height="fill",
            ),


        )
        self.w = ezui.EZWindow(
            title="Designspace Editor",
            content=content,
            descriptionData=descriptionData,
            size=(950, 325),
            minSize=(700, 200),
            controller=self,
            margins=0
        )
        self.w.addToolbarItem(dict(
            itemIdentifier="preview",
            label="Preview",
            imageObject=ezui.makeImage(
                symbolName="text.alignleft",
                symbolConfiguration=dict(
                    renderingMode="hierarchical",
                    weight="regular",
                    scale="small",
                    colors=[(1, 0, 1, 1), ]
                )
            ),
            callback=self.toolbarPreviewCallback
        ))
        self.w.addToolbarItem(dict(itemIdentifier=AppKit.NSToolbarSpaceItemIdentifier))
        self.w.addToolbarItem(dict(
            itemIdentifier="openIn",
            label="Open In...",
            imageObject=ezui.makeImage(
                symbolName="square.and.arrow.up",
                template=True,
                symbolConfiguration=dict(
                    renderingMode="hierarchical",
                    weight="regular",
                    scale="small"
                )
            ),
            callback=self.toolbarSaveCallback
        ))
        self.w.addToolbarItem(dict(
            itemIdentifier="save",
            label="Save",
            imageObject=ezui.makeImage(
                symbolName="square.and.arrow.down",
                template=True,
                symbolConfiguration=dict(
                    renderingMode="hierarchical",
                    weight="regular",
                    scale="small"
                )
            ),
            callback=self.toolbarSaveCallback
        ))
        self.w.addToolbarItem(dict(
            itemIdentifier="help",
            label="Help",
            imageObject=ezui.makeImage(
                symbolName="questionmark.circle",
                template=True,
                symbolConfiguration=dict(
                    renderingMode="hierarchical",
                    weight="regular",
                    scale="small"
                )
            ),
            callback=self.toolbarHelpCallback
        ))
        symbols = {
            "genericInfoButton": INFO_IMAGE_COLUMN,
            "axisIsRegistered": AXIS_REGISTERED_SYMBOL,
            "axisHasMap": AXIS_HAS_MAP_SYMBOL,
            "axisHasLabels": AXIS_HAS_LABELS_SYMBOL,
            "sourceHasPath": SOURCE_HAS_PATH_SYMBOL,
            "sourceIsDefault": SOURCE_IS_DEFAULT_SYMBOL,
            "sourceHasLocalisedFamilyNames": SOURCE_HAS_LOCALISED_FAMILY_NAMES_SYMBOL,
            "sourceHasMutedGlyphs": SOURCE_HAS_MUTED_GLYPHS_SYMBOL,
        }
        for table in ["axesTable", "sourcesTable"]:
            nsTableView = self.w.getItem(table)._table.getNSTableView()
            for columnID, nsTableColumn in enumerate(nsTableView.tableColumns()):
                headerImage = symbols.get(nsTableColumn.identifier())
                if headerImage:
                    nsTableHeaderCell = nsTableColumn.headerCell()
                    nsTableHeaderCell.setImage_(headerImage)
        self.w.getItem("axesTable")._table._menuCallback = self.axesTableMenuCallback
        self.w.getItem("sourcesTable")._table._menuCallback = self.sourcesTableMenuCallback
        self.w.getItem("instancesTable")._table._menuCallback = self.instancesTableMenuCallback

    def started(self):
        self.w.open()

    # Axes

    def axisListDoubleClickCallback(self, sender):
        print("axisListDoubleClickCallback")

    # def axisAddWeightAxisCallback(self, sender):
    #     print("axisAddWeightAxisCallback")

    # def axisAddWidthAxisCallback(self, sender):
    #     print("axisAddWidthAxisCallback")

    # def axisAddOpticalAxisCallback(self, sender):
    #     print("axisAddOpticalAxisCallback")

    def axesTableMenuCallback(self, sender):
        print("axesTableMenuCallback")

    def axesAddRemoveButtonAddCallback(self, sender):
        print("add")
        AddAxisSheetController(self.w)

    def axesAddRemoveButtonRemoveCallback(self, sender):
        print("remove")

    # Sources

    def sourceListDoubleClickCallback(self, sender):
        print("sourceListDoubleClickCallback")

    def sourcesTableMenuCallback(self, sender):
        print("sourcesTableMenuCallback")

    # Instances

    def instancesTableMenuCallback(self, sender):
        print("instancesTableMenuCallback")

    # Toolbar

    def toolbarPrepolatorCallback(self, sender):
        print("prepolator")

    def toolbarBatchCallback(self, sender):
        print("batch")

    def toolbarPreviewCallback(self, sender):
        print("preview")

    def toolbarSaveCallback(self, sender):
        print("save")

    def toolbarHelpCallback(self, sender):
        print("help")


class AddAxisSheetController(ezui.WindowController):
    def build(self, parent):
        content = """
        !!!!! Add Axis            @addAxisTitle

        !!!!!! Registered Axes    @registeredAxisTitle

        (Weight)                  @addWeightAxisButton
        (Width)                   @addWidthAxisButton
        (Optical Size)            @addOpticalAxisButton
        (Slant)                   @addSlantAxisButton
        (Italic)                  @addItalicAxisButton

        ---

        (Custom Continuous Axis)  @addCustomContAxisButton
        (Custom Discrete Axis)    @addCustomDiscAxisButton

        ---
        ===

        (Cancel)                  @cancelButton
        """
        descriptionData = dict(
            addAxisTitle=dict(
                width="fill",
                alignment="center",
            ),
            registeredAxisTitle=dict(
                width="fill",
                alignment="center",
            ),
            addWeightAxisButton=dict(
                width='fill',
            ),
            addWidthAxisButton=dict(
                width='fill',
            ),
            addOpticalAxisButton=dict(
                width='fill',
            ),
            addSlantAxisButton=dict(
                width='fill',
            ),
            addItalicAxisButton=dict(
                width='fill',
            ),
            addCustomContAxisButton=dict(
                width='fill',
            ),
            addCustomDiscAxisButton=dict(
                width='fill',
            ),
            cancelButton=dict(
                keyEquivalent=chr(27),
                width='fill',
            ),
        )
        self.w = ezui.EZSheet(
            content=content,
            size=(200, "auto"),
            descriptionData=descriptionData,
            parent=parent,
            controller=self
        )
        self.parent = parent

    def started(self):
        self.w.open()

    def cancelButtonCallback(self, sender):
        self.w.close()

    def okButtonCallback(self, sender):
        self.w.close()

    def makeAxisItem(self, axisName, axisTag=None, axisMinimum=None, axisDefault=None, axisMaximum=None, axisDiscreteValues=None):
        axisIsRegistered = False
        if axisName in REGISTERED_AXES:
            axisIsRegistered = True
            axisTag, axisMinimum, axisDefault, axisMaximum, axisDiscreteValues, axisLabel = REGISTERED_AXES[axisName]
            axisIsHidden = False
            axisHasMap = False
            axisHasLabels = True if axisLabel else False
        return dict(
            genericInfoButton=INFO_IMAGE_CELL,
            axisIsRegistered=axisIsRegistered,
            axisName=axisName,
            axisTag=axisTag,
            axisMinimum=axisMinimum,
            axisDefault=axisDefault,
            axisMaximum=axisMaximum,
            axisDiscreteValues=axisDiscreteValues,
            axisIsHidden=axisIsHidden,
            axisHasMap=axisHasMap,
            axisHasLabels=axisHasLabels,
        )

    def addWeightAxisButtonCallback(self, sender):
        items = [self.makeAxisItem(axisName="Weight")]
        self.parent.getItem("axesTable").appendItems(items)
        self.w.close()

    def addWidthAxisButtonCallback(self, sender):
        items = [self.makeAxisItem(axisName="Width")]
        self.parent.getItem("axesTable").appendItems(items)
        self.w.close()

    def addOpticalAxisButtonCallback(self, sender):
        items = [self.makeAxisItem(axisName="Optical Size")]
        self.parent.getItem("axesTable").appendItems(items)
        self.w.close()

    def addSlantAxisButtonCallback(self, sender):
        items = [self.makeAxisItem(axisName="Slant")]
        self.parent.getItem("axesTable").appendItems(items)
        self.w.close()

    def addItalicAxisButtonCallback(self, sender):
        items = [self.makeAxisItem(axisName="Italic")]
        self.parent.getItem("axesTable").appendItems(items)
        self.w.close()


Controller()