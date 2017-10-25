import tensorflow as tf
import tensorflow.contrib.slim as slim
import pprint
import os

from dcgan import *

flags = tf.app.flags

flags.DEFINE_integer('batch_size', 128, 'The size of minibatch when training [128]')
flags.DEFINE_float('learning_rate', 1e-3, 'Learning rate of optimizer [1e-3]')
flags.DEFINE_string('optimizer', 'Adam', 'Optimizer used when training [Adam]')
flags.DEFINE_string('dataset_name', 'mnist', 'Image dataset used when trainging [mnist]')
flags.DEFINE_string('dataset_dir', '', 'Path to dataset directory []')
flags.DEFINE_string('checkpoint_path', None, 'Path to checkpoint path [None]')
flags.DEFIEN_string('train_dir', '', 'Path to save new training result')

def main(*args):
    FLAGS = flags.FLAGS
    FLAGS.dataset_dir = os.path.join(os.getcwd(), FLAGS.dataset_dir)
    FLAGS.checkpoint_dir = os.path.join(os.getcwd(), FLAGS.checkpoint_dir)

    pp = pprint.PrettyPrinter(indent=4)
    print('Running flags:')
    pp.pprint(FLAGS.__dict__['__flags'])
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    z = tf.placeholder(tf.float32, shape=(z_dim), name='z')
    t = tf.placeholder(tf.float32, shape=(FLAGS.batch_size, 64, 64, 1), name='t')
    generator_result = dcgan_generator(z, 'DCGAN', reuse=True, output_height=64, fc1_c=1024, greyscale=True)
    discriminator_g = dcgan_discriminator(generator_result, 'DCGAN', reuse=True, conv2d1_c=128, greyscale=True)
    discriminator_t = dcgan_discriminator(t, 'DCGAN', reuse=True, conv2d1_c=128, greyscale=True)
    g_loss = tf.losses.sigmoid_cross_entropy=(multi_class_labels=tf.ones(FLAGS.batch_size), logits=discriminator_g)
    d_loss = tf.losses.sigmoid_cross_entropy=(multi_class_labels=tf.zeros(FLAGS.batch_size), logits=discriminator_g) + \
             tf.losses.sigmoid_cross_entropy=(multi_class_labels=tf.ones(FLAGS.batch_szie), logits=discriminator_t)
    g_optimizer = tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate,
                                         beta1=FLAGS.beta1,
                                         beta2=FLAGS.beta2,
                                         epsilon=FLAGS.epsilon,
                                         name='g_adam')
    d_optimizer = tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate,
                                         beta1=FLAGS.beta1,
                                         beta2=FLAGS.beta2,
                                         epsilon=FLAGS.epsilon,
                                         name='d-adam')
    saver = tf.train.Saver()
    provider = slim.DatasetDataProvider(FLAGS.dataset_name, 
                                        common_queue_capacity=2*FLAGS.batch_size,
                                        common_queue_min=FLAGS.batch_size)
    with tf.Session(config=config) as sess:
      if FLAGS.checkpoint_path:
        if not tf.train.checkpoint_exists(FLAGS.checkpoint_path):
          raise ValueError('Checkpoint not exist in path ', FLAGS.checkpoint_path)
        else:
          saver.restore(sess, FLAGS.checkpoint_path)
      else:
        
   return

if __name__ == '__main__':
    tf.app.run(main=main)

