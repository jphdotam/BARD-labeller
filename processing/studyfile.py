import pickle
import glob


class Studyfile:
    def __init__(self, filepath):
        self.filepath = filepath
        with open(self.filepath, 'rb') as f:
            self.pickle_data = pickle.load(f)
        self.procedure_type = self.pickle_data.get('proceduretype', None)


if __name__ == "__main__":
    filepath = glob.glob("../data/**/*.pickle", recursive=True)[0]
    studyfile = Studyfile(filepath=filepath)
    print(studyfile.pickle_data)
