import tensorflow as tf
import os


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


class Checkpointer:
    def __init__(self, session=tf.Session()):
        self.session = session
        with tf.Session() as sess:
            self.saver = tf.train.Saver()

    def save_model(self, experiment):
        path = "sessions/" + experiment.get_save_path()
        ensure_dir(path)
        path += experiment.get_save_name()
        saved_path = self.saver.save(experiment.session, path)
        print("Session from " + experiment.name + " saved to " + saved_path + ".")

    def load_model(self, path):
        with tf.Session() as sess:
            self.saver.restore(sess, path)
            print("Session from " + path + " restored to session.")
            return sess


if __name__ == "__main__":
    exit(-1)
