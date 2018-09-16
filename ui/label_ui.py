from PyQt5 import QtCore, QtWidgets, QtGui
from ui.label_layout import Ui_MainWindow
import os
import pickle
import glob
from settings.settings import settings
from processing.txtfile import TxtFile
import datetime
import pyqtgraph as pg
from settings.protocol import Protocol
import numpy as np
import traceback
import sys

if QtCore.QT_VERSION >= 0x50501:
    def excepthook(type_, value, traceback_):
        traceback.print_exception(type_, value, traceback_)
        QtCore.qFatal('')


    sys.excepthook = excepthook


class LabelledLinearRegionItem(pg.LinearRegionItem):
    def __init__(self, values, movable, label):
        super(LabelledLinearRegionItem, self).__init__(values=values, movable=movable)
        self.label = pg.InfLineLabel(self.lines[1], label, position=0.80, rotateAxis=(1, 0), anchor=(1, 1))


class LabelUI(Ui_MainWindow):
    def __init__(self, mainwindow):
        super(LabelUI, self).__init__()
        self.setupUi(mainwindow)
        self.actionLoad_patient.triggered.connect(self.load_patient)
        self.comboBox_ProcedureType.addItem("")
        self.lineEdit_PatientID.editingFinished.connect(self.save_patient_data)
        self.dateEdit_ProcedureDate.editingFinished.connect(self.save_patient_data)
        self.comboBox_ProcedureType.activated.connect(self.save_patient_data)
        self.comboBox_txtFiles.activated.connect(self.load_txtFile)
        self.pushButton_SeparationInc.clicked.connect(self.increase_separation)
        self.pushButton_SeparationDec.clicked.connect(self.decrease_separation)
        self.tableWidget_Markers.cellDoubleClicked.connect(lambda row, column: self.delete_marker_or_range(marker=row))
        self.tableWidget_Ranges.cellDoubleClicked.connect(lambda row, column: self.delete_marker_or_range(range=row))
        self.protocol = None
        self.range_buttons = {}
        self.marker_buttons = {}
        self.ranges = []
        self.markers = []
        self.offset = 10000
        for setting in settings.keys():
            self.comboBox_ProcedureType.addItem(setting)

    def load_patient(self):
        self.patientfolder_path = QtWidgets.QFileDialog.getExistingDirectory(None, "Select a folder", "./data/",
                                                                             QtWidgets.QFileDialog.ShowDirsOnly)
        self.patient_data = self.load_patient_data_pickle()
        self.refresh_ui()
        self.load_protocol()

    def load_txtFile(self):
        filepath = self.comboBox_txtFiles.currentText().rsplit(' ', 3)[0]
        try:
            self.TxtFile = TxtFile(filepath=filepath)
        except FileNotFoundError:
            print("!!!UNABLE TO FIND FILE {}!!!".format(filepath))
        self.plot_txtFile()
        labels = self.TxtFile.load_labels()
        self.ranges, self.markers = self.create_sliders_from_labels(labels)
        self.draw_protocol_labels_and_buttons()
        self.update_label_list_and_save()

    def plot_txtFile(self):
        pg.setConfigOptions(antialias=True)
        self.ranges = []
        self.markers = []

        self.GraphicsLayout = pg.GraphicsLayout()
        self.graphicsView_.setCentralItem(self.GraphicsLayout)
        self.graphicsView_.show()

        self.plot = self.GraphicsLayout.addPlot(title=self.TxtFile.filepath)
        self.lead_plots = []
        self.plot.addLegend()
        for i in range(len(self.TxtFile.channels)):
            if i % 2 == 0:
                colour = 'g'
            else:
                colour = 'y'
            offset = i * -self.offset
            data = self.TxtFile.data.iloc[:, i].values + offset
            data = TxtFile.filter_data(data, type='wavelet', sample_freq=self.TxtFile.sample_freq)
            self.plot.plot(y=data, name=self.TxtFile.channels[i], pen=colour)

        self.GraphicsLayout.setSpacing(0)
        self.GraphicsLayout.setContentsMargins(0., 0., 0., 0.)

    def refresh_ui(self):
        if self.patient_loaded:
            self.lineEdit_PatientID.setEnabled(True)
            self.dateEdit_ProcedureDate.setEnabled(True)
            self.comboBox_ProcedureType.setEnabled(True)
            self.comboBox_txtFiles.setEnabled(True)
            self.lineEdit_PatientID.setText(self.patient_data.get('id', "NA"))
            self.dateEdit_ProcedureDate.setDate(self.patient_data.get('date', datetime.date(2001, 1, 1)))
            self.pushButton_SeparationInc.setEnabled(True)
            self.pushButton_SeparationDec.setEnabled(True)
            index = self.comboBox_ProcedureType.findText(self.patient_data.get('proceduretype', ""),
                                                         QtCore.Qt.MatchFixedString)

            # Get rid of the old files list and add the new ones
            self.comboBox_txtFiles.clear()
            self.comboBox_txtFiles.addItem("Please select a file")
            if index >= 0:
                self.comboBox_ProcedureType.setCurrentIndex(index)

            txtfiles = glob.glob(os.path.join(self.patientfolder_path, "*.txt"))
            for txtfile in txtfiles:

                labels = TxtFile.get_labels_from_textfile(txtfile)
                if len(labels) == 2:
                    n_labels = len(labels['ranges']) + len(labels['markers'])
                else:
                    n_labels = 0
                self.comboBox_txtFiles.addItem("{} - {} labels".format(txtfile, n_labels))

            # Clear the plot window
            self.GraphicsLayout = pg.GraphicsLayout()
            self.graphicsView_.setCentralItem(self.GraphicsLayout)
            self.graphicsView_.show()
        else:
            self.actionLoad_txt_file.setEnabled(False)
            self.lineEdit_PatientID.setEnabled(False)
            self.dateEdit_ProcedureDate.setEnabled(False)
            self.comboBox_ProcedureType.setEnabled(False)
            self.comboBox_txtFiles.setEnabled(False)

    def load_patient_data_pickle(self):
        filename = "patientdata.pickle"
        try:
            with open(os.path.join(self.patientfolder_path, filename), 'rb') as f:
                patient_data = pickle.load(f)
                print("Opened {}".format(patient_data))
        except FileNotFoundError:
            print("Patient data not found, creating new file")
            patient_data = {}
        self.patient_loaded = True
        return patient_data

    def load_protocol(self):
        if 'proceduretype' in self.patient_data:
            try:
                self.protocol = Protocol(self.patient_data['proceduretype'])
                self.draw_protocol_labels_and_buttons()

            except KeyError:
                print("Protocol {} not found".format(self.patient_data['proceduretype']))

    def draw_protocol_labels_and_buttons(self):
        def clear_layout(layout):
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)

        clear_layout(self.verticalLayout_ProtocolButtons)
        font24 = QtGui.QFont()
        font24.setPointSize(24)

        #### RANGES ####

        self.label_Buttons_Ranges = QtWidgets.QLabel(self.centralwidget)
        self.label_Buttons_Ranges.setFont(font24)
        self.label_Buttons_Ranges.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Buttons_Ranges.setObjectName("label_Buttons")
        self.verticalLayout_ProtocolButtons.addWidget(self.label_Buttons_Ranges)
        self.label_Buttons_Ranges.setText("Ranges")

        try:
            for range_key in self.protocol.ranges.keys():
                self.range_buttons[range_key] = QtWidgets.QPushButton(self.centralwidget)
                self.range_buttons[range_key].setStyleSheet("background-color: orange")
                self.range_buttons[range_key].setText(range_key)
                if self.protocol.ranges[range_key].get('mandatory', False) == True:
                    self.range_buttons[range_key].setStyleSheet("background-color: red")
                self.range_buttons[range_key].clicked.connect(
                    lambda state, key=range_key: self.create_label_range_or_marker(range_key=key))
                self.verticalLayout_ProtocolButtons.addWidget(self.range_buttons[range_key])
            for range_slider in self.ranges:
                range_type = range_slider.label.format
                try:
                    self.range_buttons[range_type].setStyleSheet("background-color: green")
                except KeyError:
                    print("Couldn't find a button for {}; likely label under a different protocol".format(range_type))
        except AttributeError:
            pass
        #### MARKERS ####

        # Labels
        self.label_Buttons_Markers = QtWidgets.QLabel(self.centralwidget)
        self.label_Buttons_Markers.setFont(font24)
        self.label_Buttons_Markers.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Buttons_Markers.setObjectName("label_Buttons")
        self.verticalLayout_ProtocolButtons.addWidget(self.label_Buttons_Markers)
        self.label_Buttons_Markers.setText("Markers")

        # Buttons
        try:
            for marker_key in self.protocol.markers.keys():
                self.marker_buttons[marker_key] = QtWidgets.QPushButton(self.centralwidget)
                self.marker_buttons[marker_key].setStyleSheet("background-color: orange")
                self.marker_buttons[marker_key].setText(marker_key)
                if self.protocol.markers[marker_key].get('mandatory', False) == True:
                    self.marker_buttons[marker_key].setStyleSheet("background-color: red")
                self.marker_buttons[marker_key].clicked.connect(
                    lambda state, key=marker_key: self.create_label_range_or_marker(marker_key=key))
                self.verticalLayout_ProtocolButtons.addWidget(self.marker_buttons[marker_key])
            for marker_slider in self.markers:
                marker_type = marker_slider.label.format
                self.marker_buttons[marker_type].setStyleSheet("background-color: green")
        except AttributeError:
            pass

    def create_label_range_or_marker(self, range_key=None, marker_key=None):
        if not range_key and not marker_key:
            print("ERROR: No range key or marker key received")
            return 0
        if range_key:
            x_lower, x_upper = self.plot.getAxis('bottom').range
            x_min = (x_lower + x_lower + x_upper) / 3
            x_max = (x_lower + x_upper + x_upper) / 3
            self.create_range_slider_and_add_to_plot(x_min, x_max, range_key)
            self.draw_protocol_labels_and_buttons()
        if marker_key:
            x = np.mean(self.plot.getAxis('bottom').range)
            self.create_marker_slider_and_add_to_plot(x, marker_key)
            self.draw_protocol_labels_and_buttons()

    def create_range_slider_and_add_to_plot(self, range_from, range_to, range_type):
        range = LabelledLinearRegionItem(values=(range_from, range_to), movable=True, label=range_type)
        range.sigRegionChangeFinished.connect(self.update_label_list_and_save)
        self.ranges.append(range)
        self.plot.addItem(range, ignoreBounds=True)
        self.draw_protocol_labels_and_buttons()
        return range

    def create_marker_slider_and_add_to_plot(self, location, range_type):
        marker = pg.InfiniteLine(pos=location, movable=True, label=range_type,
                                 labelOpts={'position': 0.2, 'rotateAxis': (1, 0), 'anchor': (1, 1)})
        marker.sigPositionChangeFinished.connect(self.update_label_list_and_save)
        self.markers.append(marker)
        self.plot.addItem(marker, ignoreBounds=True)
        return marker

    def create_sliders_from_labels(self, labels):
        range_labels = labels.get('ranges', [])
        marker_labels = labels.get('markers', [])
        range_sliders = []
        marker_sliders = []
        for range_label in range_labels:
            range_slider = LabelledLinearRegionItem(values=(range_label['from'], range_label['to']),
                                                    movable=True, label=range_label['type'])
            range_sliders.append(range_slider)
            range_slider.sigRegionChangeFinished.connect(self.update_label_list_and_save)
            self.plot.addItem(range_slider, ignoreBounds=True)
        for marker_label in marker_labels:
            marker_slider = pg.InfiniteLine(pos=marker_label['location'], movable=True, label=marker_label['type'],
                                            labelOpts={'position': 0.2, 'rotateAxis': (1, 0), 'anchor': (1, 1)})
            marker_sliders.append(marker_slider)
            marker_slider.sigPositionChangeFinished.connect(self.update_label_list_and_save)
            self.plot.addItem(marker_slider, ignoreBounds=True)
        self.draw_protocol_labels_and_buttons()
        return range_sliders, marker_sliders

    def update_label_list_and_save(self):

        # Add RANGES to list
        self.tableWidget_Ranges.setRowCount(len(self.ranges))
        self.tableWidget_Ranges.setColumnCount(4)
        self.tableWidget_Ranges.setHorizontalHeaderLabels(("ID", "Type", "From", "To"))
        for i, range_slider in enumerate(self.ranges):
            self.tableWidget_Ranges.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i)))
            self.tableWidget_Ranges.setItem(i, 1, QtWidgets.QTableWidgetItem(str(range_slider.label.format)))
            self.tableWidget_Ranges.setItem(i, 2, QtWidgets.QTableWidgetItem(str(range_slider.getRegion()[0])))
            self.tableWidget_Ranges.setItem(i, 3, QtWidgets.QTableWidgetItem(str(range_slider.getRegion()[1])))

        # Add MARKERS to list
        self.tableWidget_Markers.setRowCount(len(self.markers))
        self.tableWidget_Markers.setColumnCount(3)
        self.tableWidget_Markers.setHorizontalHeaderLabels(("ID", "Type", "Location"))
        for i, marker_slider in enumerate(self.markers):
            self.tableWidget_Markers.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i)))
            self.tableWidget_Markers.setItem(i, 1, QtWidgets.QTableWidgetItem(str(marker_slider.label.format)))
            self.tableWidget_Markers.setItem(i, 2, QtWidgets.QTableWidgetItem(str(marker_slider.value())))

        # Write to file
        self.TxtFile.labels = {'ranges': self.ranges_to_dictionary(),
                               'markers': self.markers_to_dictionary()}
        self.TxtFile.save_labels()

    def ranges_to_dictionary(self):
        ranges = []
        for range_slider in self.ranges:
            range_dict = {}
            range_dict['type'] = range_slider.label.format
            range_dict['from'] = range_slider.getRegion()[0]
            range_dict['to'] = range_slider.getRegion()[1]
            ranges.append(range_dict)
        return ranges

    def markers_to_dictionary(self):
        markers = []
        for marker_slider in self.markers:
            marker_dict = {}
            marker_dict['type'] = marker_slider.label.format
            marker_dict['location'] = marker_slider.value()
            markers.append(marker_dict)
        return markers

    def delete_marker_or_range(self, marker=None, range=None):
        if marker != None:
            print("Deleting marker {}".format(marker))
            self.plot.removeItem(self.markers[marker])
            del self.markers[marker]
        if range != None:
            print("Deleting range {}".format(range))
            self.plot.removeItem(self.ranges[range])
            del self.ranges[range]
        self.update_label_list_and_save()
        self.draw_protocol_labels_and_buttons()

    def save_patient_data(self):
        patient_id = self.lineEdit_PatientID.text()
        procedure_date = self.dateEdit_ProcedureDate.date()
        procedure_type = self.comboBox_ProcedureType.currentText()
        self.patient_data = {"id": patient_id, "date": procedure_date, "proceduretype": procedure_type}
        self.load_protocol()
        filename = "patientdata.pickle"
        print("Saving {}".format(self.patient_data))
        with open(os.path.join(self.patientfolder_path, filename), 'wb') as f:
            pickle.dump(self.patient_data, f)

    def get_procedure_types(self):
        settings_files = glob.glob("../settings/*.py")
        settings_names = [os.path.splitext(file)[0] for file in settings_files]
        settings = dict(zip(settings_names, settings_files))
        return settings

    def increase_separation(self):
        x_range = self.plot.getAxis('bottom').range
        y_range = self.plot.getAxis('left').range
        self.offset *= 1.2
        self.plot_txtFile()
        print("Setting to {}, {}".format(x_range, y_range))
        self.plot.setRange(xRange=x_range, yRange=y_range)
        labels = self.TxtFile.load_labels()
        self.ranges, self.markers = self.create_sliders_from_labels(labels)
        self.draw_protocol_labels_and_buttons()
        self.update_label_list_and_save()

    def decrease_separation(self):
        x_range = self.plot.getAxis('bottom').range
        y_range = self.plot.getAxis('left').range
        self.offset /= 1.2
        self.plot_txtFile()
        print("Setting to {}, {}".format(x_range, y_range))
        self.plot.setRange(xRange=x_range, yRange=y_range)
        labels = self.TxtFile.load_labels()
        self.ranges, self.markers = self.create_sliders_from_labels(labels)
        self.draw_protocol_labels_and_buttons()
        self.update_label_list_and_save()
