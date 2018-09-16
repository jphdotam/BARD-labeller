import pickle
import glob

class LabelFile:
    def __init__(self, filepath):
        self.filepath = filepath
        with open(self.filepath, 'rb') as f:
            self.pickle_data = pickle.load(f)
            self.ranges = self.pickle_data.get('ranges', None)
            self.markers = self.pickle_data.get('markers', None)

if __name__ == "__main__":
    filepath = glob.glob("../data/**/*.label", recursive=True)[0]
    labelfile = LabelFile(filepath=filepath)
    print(labelfile.pickle_data)