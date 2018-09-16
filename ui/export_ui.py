from PyQt5 import QtCore, QtWidgets, QtGui
import traceback
import sys
from ui.export_layout import Ui_MainWindow
import glob
import os
from processing.labelfile import LabelFile
from processing.studyfile import Studyfile
from processing.txtfile import TxtFile
import math
from settings.settings import settings
from settings.protocol import Protocol
import numpy as np

LEADS = ['I','II','III','aVR','aVL','aVF','V1','V2','V3','V4','V5','V6']

if QtCore.QT_VERSION >= 0x50501:
    def excepthook(type_, value, traceback_):
        traceback.print_exception(type_, value, traceback_)
        QtCore.qFatal('')


    sys.excepthook = excepthook


class ExportUI(Ui_MainWindow):
    def __init__(self, mainwindow):
        def load_data():
            self.load_data()

        def load_dir():
            self.load_directory()

        def change_protocol():
            self.change_protocol()

        def export():
            self.export()

        super(ExportUI, self).__init__()
        self.setupUi(mainwindow)

        self.protocol = None
        self.comboBox_Protocol.addItem("")
        for setting in settings.keys():
            self.comboBox_Protocol.addItem(setting)
        self.comboBox_ExportRange.addItem("ALL")
        self.comboBox_ExportRange.addItem("95%")
        self.comboBox_ExportRange.addItem("99%")

        self.data_dir = None
        self.label_list = None
        self.studyfolder_list = None
        self.treeView_model = None
        self.valid_studies = None
        self.valid_labels_by_study, self.n_valid_labels = None, None
        self.durations = None

        self.load_directory()
        print("Directory loaded")

        self.actionLoad.triggered.connect(load_dir)
        self.pushButton_Filter.clicked.connect(load_data)
        self.pushButton_Export.clicked.connect(export)
        self.comboBox_Protocol.activated.connect(change_protocol)

    def export(self):

        def get_min_max_duration(proportion=0.95):
            mn = self.durations[int(len(self.durations) * (1 - proportion))]
            mx = self.durations[int(len(self.durations) * proportion)]
            return mn, mx

        minduration, maxduration = 0, max(self.durations)
        prepostbuffer = self.spinBox_exportBuffer.value()

        exportrange = self.comboBox_ExportRange.currentText()
        if exportrange != 'ALL':
            if exportrange == '95%':
                minduration, maxduration = get_min_max_duration(0.95)
            elif exportrange == '99%':
                minduration, maxduration = get_min_max_duration(0.99)
            else:
                print(f"Unknown range {exportrange}; using all samples")

        for i, studyfilepath in enumerate(self.valid_labels_by_study.keys()):
            self.progressBar.setValue(i / len(self.valid_labels_by_study) * 100)
            studyname = os.path.basename(os.path.dirname(studyfilepath))
            studyfolder = os.path.join("./exports/", studyname)
            if not os.path.exists(studyfolder):
                os.mkdir(studyfolder)
            for studylabel in self.valid_labels_by_study[studyfilepath]:
                start = studylabel.start
                stop = studylabel.stop
                if minduration <= stop - start <= maxduration:
                    # print(f"Loading {studylabel.filepath}")
                    txtfile = TxtFile(filepath=studylabel.filepath.rsplit(".label", 1)[0])
                    # print(f"Going to cut {txtfile.data.shape} by [{start}:{stop},:]")
                    try:
                        txtfile_filtered = txtfile.data[LEADS].loc[start - prepostbuffer:stop + prepostbuffer]
                        np.save(os.path.join(studyfolder, os.path.basename(txtfile.filepath)), txtfile_filtered)
                    except KeyError as e:
                        print(f"Skipping {studylabel.filepath} as missing ECG lead :{e}")
                else:
                    print(f"Skipping {studylabel.filepath} as length {stop - start} exceeds {exportrange} of data")
        self.progressBar.setValue(0)

    def change_protocol(self):
        self.protocol = Protocol(self.comboBox_Protocol.currentText())
        self.comboBox_StartSegment.clear()
        self.comboBox_StopSegment.clear()

        for range_key in self.protocol.ranges.keys():
            self.comboBox_StartSegment.addItem(range_key + " START")
            self.comboBox_StartSegment.addItem(range_key + " STOP")
            self.comboBox_StopSegment.addItem(range_key + " START")
            self.comboBox_StopSegment.addItem(range_key + " STOP")
        for marker_key in self.protocol.markers.keys():
            self.comboBox_StartSegment.addItem(marker_key + " MARKER")
            self.comboBox_StopSegment.addItem(marker_key + " MARKER")

    def load_directory(self):
        print("Loading dir")
        self.data_dir = QtWidgets.QFileDialog.getExistingDirectory(None, "Select a folder", "./",
                                                                   QtWidgets.QFileDialog.ShowDirsOnly)
        self.label_list = glob.glob(os.path.join(self.data_dir, "**/*.label"), recursive=True)
        self.studyfolder_list = set([os.path.dirname(labelfile) for labelfile in self.label_list])
        print(
            f"In folder {self.data_dir} I found {len(self.label_list)} labels in {len(self.studyfolder_list)} studies")

    def load_data(self):
        if not self.comboBox_Protocol.currentText() or not self.comboBox_StartSegment or not self.comboBox_StopSegment:
            print("Unable to filter without protocol, start and stop position chosen")
        self.valid_studies = self.get_valid_studies()
        self.valid_labels_by_study, self.n_valid_labels = self.get_valid_labels_by_study()
        self.display_valid_labels_by_study()

    def get_valid_studies(self):
        studies = []
        for studyfolder in self.studyfolder_list:
            try:
                study = Studyfile(filepath=os.path.join(studyfolder, "patientdata.pickle"))
                if study.pickle_data.get('proceduretype') == self.comboBox_Protocol.currentText():
                    studies.append(study)
            except FileNotFoundError:
                print(f"Strange error finding the picklefile for {studyfolder}")
        return studies

    def get_valid_labels_by_study(self):
        valid_labels_by_study = {}
        n_valid_labels = 0
        for i, study in enumerate(self.valid_studies):
            self.progressBar.setValue(i / len(self.valid_studies) * 100)
            unfiltered_study_labels = [LabelFile(filepath=labelfile) for labelfile in self.label_list if
                                       os.path.dirname(study.filepath) in labelfile]
            filtered_study_labels = []
            for label in unfiltered_study_labels:
                # 'start' and 'stop' will contain a range/marker name e.g. 'ectopic qrst'
                # 'start_startstopmarker' and 'stop_startstopmarker' will contain either 'START', 'STOP' or 'MARKER'
                start, start_startstopmarker = self.comboBox_StartSegment.currentText().rsplit(" ", 1)
                stop, stop_startstopmarker = self.comboBox_StopSegment.currentText().rsplit(" ", 1)

                # Start
                starttime = None
                if start_startstopmarker == 'MARKER':
                    for marker in label.markers:
                        if marker['type'] == start:
                            starttime = marker['location']
                elif start_startstopmarker == 'START' or start_startstopmarker == 'STOP':
                    for rnge in label.ranges:
                        if rnge['type'] == start:
                            if start_startstopmarker == 'START':
                                starttime = rnge['from']
                            else:
                                starttime = rnge['to']
                else:
                    raise ValueError(f"Could not parse start_startstopmarker of {start_startstopmarker}")

                # Stop
                stoptime = None
                if stop_startstopmarker == 'MARKER':
                    for marker in label.markers:
                        if marker['type'] == stop:
                            stoptime = marker['location']
                elif stop_startstopmarker == 'START' or stop_startstopmarker == 'STOP':
                    for rnge in label.ranges:
                        if rnge['type'] == stop:
                            if stop_startstopmarker == 'START':
                                stoptime = rnge['from']
                            else:
                                stoptime = rnge['to']
                else:
                    raise ValueError(f"Could not parse start_startstopmarker of {start_startstopmarker}")

                if not starttime or not stoptime:
                    print(f"Unable to find valid start and stop times in label {label.filepath}")
                else:
                    if starttime >= stoptime:
                        print(
                            f"The stop time {stoptime} precedes the start time {starttime} for label {label.filepath}")
                    else:
                        label.start = int(starttime)
                        label.stop = math.ceil(stoptime)
                        filtered_study_labels.append(label)
                        n_valid_labels += 1
            valid_labels_by_study[study.filepath] = filtered_study_labels
        self.progressBar.setValue(0)
        return valid_labels_by_study, n_valid_labels

    def display_valid_labels_by_study(self):
        print(f"Valid studies: {self.valid_studies}")
        print(f"Valid labels by study: {self.valid_labels_by_study}")

        self.label_ValidCasesValue.setText(str(len(self.valid_studies)))
        self.label_ValidValue.setText(str(self.n_valid_labels))

        self.treeView_model = QtGui.QStandardItemModel()
        self.treeView_model.setHorizontalHeaderLabels(['Label type', 'Start', 'End', 'Length'])
        self.treeView.setModel(self.treeView_model)
        self.treeView.setUniformRowHeights(True)

        durations = []

        for studyrow, studypath in enumerate(self.valid_labels_by_study.keys()):
            studyrelpath = os.path.relpath(os.path.dirname(studypath), self.data_dir)
            item_study = QtGui.QStandardItem(f"{studyrelpath}")

            for labelfile in self.valid_labels_by_study[studypath]:
                duration = labelfile.stop - labelfile.start
                durations.append(duration)
                item_labelfile = QtGui.QStandardItem(
                    f"{os.path.basename(labelfile.filepath)} - {duration}")
                ranges = labelfile.ranges
                markers = labelfile.markers

                for rnge in ranges:
                    item_range_col1 = QtGui.QStandardItem(rnge['type'])
                    item_range_col2 = QtGui.QStandardItem(str(int(rnge['from'])))
                    item_range_col3 = QtGui.QStandardItem(str(math.ceil(rnge['to'])))
                    item_labelfile.appendRow([item_range_col1, item_range_col2, item_range_col3])
                for marker in markers:
                    item_marker_col1 = QtGui.QStandardItem(marker['type'])
                    item_marker_col2 = QtGui.QStandardItem(str(int(marker['location'])))
                    item_labelfile.appendRow([item_marker_col1, item_marker_col2])
                item_study.appendRow(item_labelfile)
            self.treeView_model.appendRow(item_study)
            self.treeView.setFirstColumnSpanned(studyrow, self.treeView.rootIndex(), True)
        self.treeView.expandAll()
        for columnid in range(3):
            self.treeView.resizeColumnToContents(columnid)

        durations = sorted(durations)
        range95 = f"{durations[int(len(durations)*0.05)]} to {durations[int(len(durations)*0.95)]} (n={len(durations[int(len(durations)*0.05):int(len(durations)*0.95)])})"
        range99 = f"{durations[int(len(durations)*0.01)]} to {durations[int(len(durations)*0.99)]} (n={len(durations[int(len(durations)*0.01):int(len(durations)*0.99)])})"

        self.durations = durations
        self.label_sampleLengthsValue.setText(
            f"{np.mean(durations):.0f}\n{np.min(durations)}\n{np.max(durations)}\n{np.std(durations):.1f}\n{range95}\n{range99}")
