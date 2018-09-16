from keras.models import load_model
from keras.callbacks import TensorBoard


class Network():
    def train(self, x, y, epochs, batch_size, tensorboard_modelname, validation_data=None, verbose=1,
              class_weight=None):

        tbCallBack = TensorBoard(log_dir='./models/tensorboard_logs/{}/'.format(tensorboard_modelname),
                                 histogram_freq=0, write_graph=True, write_images=True)

        return self.model.fit(x, y, batch_size=batch_size, epochs=epochs, validation_data=validation_data,
                              callbacks=[tbCallBack], verbose=verbose, class_weight=class_weight)

    def save(self, filename):
        self.model.save(filename)

    def load(self, filename):
        self.model = load_model(filename)

    def predict(self, x):
        return self.model.predict(x)

    def eval(self, x, y, verbose=1):
        return self.model.evaluate(x=x, y=y, verbose=verbose)
