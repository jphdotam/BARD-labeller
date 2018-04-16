# BARD-labeller
Python app for labelling ECG text files exported from the BARD EP system

## About

This program is at its VERY early infancy. It can currently label text files but I haven't yet coded the ability to export the data in batches.

## Requirements

* PyQt5
* Pandas
* SciPy
* pywt (conda install pywavelets)
* Statsmodels (conda install -c statsmodels statsmodels)

## Reporting cases

First, place all the exported *.txt files for specific case in specific subfolder within the "./data/" directory, e.g. "./data/case1/", then select that folder using the 'load patient' icon in the top left corner.

Second, fill in the procedure ID, procedure date and procedure type (protocol) on the left side. These parameters are associated with the patient (the active folder) rather than individual text files.
This program comes with labelling protocols for 3 types of studies:
1) Accessory pathway ablations
2) Ventricular ectopy ablations
3) AVNRT ablations
To add more protocols, edit the "./settings/settings.py" file, which should be fairly self-explanatory.

Third, select the text file you wish to label using the 'file selector' drop down box.

The plot can be moved by holding left mouse and dragging. The plot can be stretched vertically or horizontally by holding mouse 2 and dragging. Zooming/unzooming is performed by scrolling.

Use the buttons on the left to add either range sliders. Labelled segments appear green. Red buttons are those which are marked as 'mandatory' in the protocol settings.

A labelled plot might look like the following:

![label example](http://i.imgur.com/VwRGp4F.jpg)

To delete labels, double-click their entry in the labels tables visible on the right hand side.

## Exporting cases

This doesn't work yet!

However, the data are easily accessible. The patient-level data (ID, procedure date and type) are stored in a pickle file "patientdata.pickle" in the case directory as a dictionary of format `{"id": patient_id, "date": procedure_date, "proceduretype": procedure_type}`.

Labels of files as similarly stored as pickles, and the example from the file above would be stored as <filename>.label and when read would yield:
`{'ranges': [{'type': 'sinus qrs', 'from': 7740.997212822703, 'to': 7824.136764773928}, {'type': 'sinus pwave', 'from': 7619.853033131245, 'to': 7704.575151408585}, {'type': 'rr', 'from': 6022.301053574819, 'to': 6850.871178542038}], 'markers': [{'type': 'deltawave end', 'location': 7755.115319117976}]}`
