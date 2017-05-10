import tensorflow as tf
import os


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


class Checkpoint():
    pass


class SaveCheckpoint:
    def __init__(self, session):
        self.session = session
        with tf.Session() as sess:
            self.saver = tf.train.Saver()

    def save_model(self, experiment):
        path = "sessions/" + experiment.get_save_path()
        ensure_dir(path)
        path += experiment.get_save_name()
        saved_path = self.saver.save(experiment.session, path)
        print("Session from " + experiment.name + " saved to " + saved_path + ".")


class LoadCheckpoint:
    def __init__(self, path, name):
        sess = tf.Session()
        meta_path = path + "\\" + name + ".session.meta"
        self.saver = tf.train.import_meta_graph(meta_path,clear_devices=True)
        self.saver.restore(sess, tf.train.latest_checkpoint(path))
        self.session = sess
        print("Loaded Checkpoint: " + name)


if __name__ == "__main__":
    exit(-1)
