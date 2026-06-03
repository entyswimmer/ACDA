from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItem,
    QAbstractItemView,
)


class FormulaTree(QTreeWidget):

    formula_selected = Signal(str)

    def __init__(
        self,
        registry
    ):
        super().__init__()

        self.registry = registry

        self.setHeaderHidden(True)
        self.setMinimumHeight(240)
        self.setVerticalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.setAnimated(True)
        self.setIndentation(16)

        self._build_tree()

        self.itemClicked.connect(
            self._on_item_clicked
        )

    def _build_tree(self):

        categories = {}

        for key in self.registry.list_keys():

            meta = self.registry.get(key)

            category = meta.get(
                "category",
                "Other"
            )

            if category not in categories:

                category_item = QTreeWidgetItem(
                    [category]
                )
                category_item.setFlags(
                    Qt.ItemFlag.ItemIsEnabled
                )

                categories[category] = (
                    category_item
                )

                self.addTopLevelItem(
                    categories[category]
                )

            item = QTreeWidgetItem(
                [meta["name"]]
            )

            item.setData(
                0,
                Qt.ItemDataRole.UserRole,
                key
            )

            categories[category].addChild(
                item
            )

        self.expandAll()

    def _on_item_clicked(
        self,
        item,
        column
    ):

        key = item.data(
            0,
            Qt.ItemDataRole.UserRole
        )

        if key:

            self.formula_selected.emit(
                key
            )