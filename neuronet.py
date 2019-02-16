
import numpy as np
import tensorflow as tf
from deeppavlov.core.data.simple_vocab import SimpleVocabulary
from deeppavlov.dataset_readers.conll2003_reader import Conll2003DatasetReader
from deeppavlov.metrics.fmeasure import precision_recall_f1
# The function precision_recall_f1 takes two lists: y_true and y_predicted
# the tag sequences for each sentences should be merged into one big list
from deeppavlov.core.data.utils import zero_pad
# zero_pad takes a batch of lists of token indices, pad it with zeros to the
# maximal length and convert it to numpy matrix
from itertools import chain
from deeppavlov.core.data.data_learning_iterator import DataLearningIterator
from deeppavlov.models.preprocessors.mask import Mask
from file_parser import loadData
from file_parser import repl
import re


def get_embeddings(indices, vocabulary_size, emb_dim):
    # Initialize the random gaussian matrix with dimensions [vocabulary_size, embedding_dimension]
    # The **VARIANCE** of the random samples must be 1 / embedding_dimension
    emb_mat = np.random.randn(vocabulary_size, emb_dim).astype(np.float32) / np.sqrt(emb_dim)
    emb_mat = tf.Variable(emb_mat, name='Embeddings', trainable=True)
    emb = tf.nn.embedding_lookup(emb_mat, indices)
    return emb


def conv_net(units, n_hidden_list, cnn_filter_width, activation=tf.nn.relu):
    # Use activation(units) to apply activation to units
    for n_hidden in n_hidden_list:
        units = tf.layers.conv1d(units,
                                 n_hidden,
                                 cnn_filter_width,
                                 padding='same')
        units = activation(units)
    return units


def masked_cross_entropy(logits, label_indices, number_of_tags, mask):
    ground_truth_labels = tf.one_hot(label_indices, depth=number_of_tags)
    loss_tensor = tf.nn.softmax_cross_entropy_with_logits_v2(labels=ground_truth_labels, logits=logits)
    loss_tensor *= mask
    loss = tf.reduce_mean(loss_tensor)
    return loss


def eval_valid(network, batch_generator):
    total_true = []
    total_pred = []
    for x, y_true in batch_generator:
        # Prepare token indices from tokens batch
        x_inds = token_vocab(x)

        # Pad the indices batch with zeros
        x_batch = zero_pad(x_inds)

        # Get the mask using get_mask
        mask = get_mask(x)

        # We call the instance of the NerNetwork because we have defined __call__ method
        y_inds = network(x_batch, mask)

        # For every sentence in the batch extract all tags up to paddings
        y_inds = [y_inds[n][:len(x[n])] for n, y in enumerate(y_inds)]
        y_pred = tag_vocab(y_inds)

        # Add fresh predictions
        total_true.extend(chain(*y_true))
        total_pred.extend(chain(*y_pred))
    res = precision_recall_f1(total_true, total_pred, print_results=True)
    return res


class NerNetwork:
    def __init__(self,
                 n_tokens,
                 n_tags,
                 token_emb_dim=100,
                 n_hidden_list=(128,),
                 cnn_filter_width=7,
                 use_batch_norm=False,
                 embeddings_dropout=False,
                 top_dropout=False,
                 **kwargs):
        # ================ Building inputs =================

        self.learning_rate_ph = tf.placeholder(tf.float32, [])
        self.dropout_keep_ph = tf.placeholder(tf.float32, [])
        self.token_ph = tf.placeholder(tf.int32, [None, None], name='token_ind_ph')
        self.mask_ph = tf.placeholder(tf.float32, [None, None], name='Mask_ph')
        self.y_ph = tf.placeholder(tf.int32, [None, None], name='y_ph')

        # ================== Building the network ==================

        # Now embedd the indices of tokens using token_emb_dim function
        emb = get_embeddings(self.token_ph, n_tokens, token_emb_dim)
        ######################################

        emb = tf.nn.dropout(emb, self.dropout_keep_ph, (tf.shape(emb)[0], 1, tf.shape(emb)[2]))

        # Build a multilayer CNN on top of the embeddings.
        # The number of units in the each layer must match
        # corresponding number from n_hidden_list.
        # Use ReLU activation

        units = conv_net(emb, n_hidden_list, cnn_filter_width)
        units = tf.nn.dropout(units, self.dropout_keep_ph, (tf.shape(units)[0], 1, tf.shape(units)[2]))
        logits = tf.layers.dense(units, n_tags, activation=None)
        self.predictions = tf.argmax(logits, 2)

        # ================= Loss and train ops =================
        # Use cross-entropy loss. check the tf.nn.softmax_cross_entropy_with_logits_v2 function

        self.loss = masked_cross_entropy(logits, self.y_ph, n_tags, self.mask_ph)


        # Create a training operation to update the network parameters.
        # We purpose to use the Adam optimizer as it work fine for the
        # most of the cases. Check tf.train to find an implementation.
        # Put the train operation to the attribute self.train_op


        optimizer = tf.train.AdamOptimizer(self.learning_rate_ph)
        self.train_op = optimizer.minimize(self.loss)
        ######################################

        # ================= Initialize the session =================
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    def __call__(self, tok_batch, mask_batch):
        feed_dict = {self.token_ph: tok_batch,
                     self.mask_ph: mask_batch,
                     self.dropout_keep_ph: 1.0}
        return self.sess.run(self.predictions, feed_dict)

    def train_on_batch(self, tok_batch, tag_batch, mask_batch, dropout_keep_prob, learning_rate):
        feed_dict = {self.token_ph: tok_batch,
                     self.y_ph: tag_batch,
                     self.mask_ph: mask_batch,
                     self.dropout_keep_ph: dropout_keep_prob,
                     self.learning_rate_ph: learning_rate}
        self.sess.run(self.train_op, feed_dict)


#здесь я указывала абсолютный путь к директории data
dataset = Conll2003DatasetReader().read('C:\\Users\\stron\\PycharmProjects\\word2vec\\data')
get_mask = Mask()
data_iterator = DataLearningIterator(dataset)

special_tokens = ['<UNK>']
token_vocab = SimpleVocabulary(special_tokens, save_path='model/token.dict')
tag_vocab = SimpleVocabulary(save_path='model/tag.dict')

all_tokens_by_sentences = [tokens for tokens, tags in dataset['train']]
all_tags_by_sentences = [tags for tokens, tags in dataset['train']]

token_vocab.fit(all_tokens_by_sentences)
tag_vocab.fit(all_tags_by_sentences)

nernet = NerNetwork(len(token_vocab),
                    len(tag_vocab),
                    n_hidden_list=[50, 50, 50, 50],
                    cnn_filter_width=9)

batch_size = 2
n_epochs = 3
learning_rate = 0.001
dropout_keep_prob = 0.5

# train network:
for k in range(n_epochs):
    for x, y in data_iterator.gen_batches(batch_size, 'train'):
        # Convert tokens to indices via Vocab
        x_inds = token_vocab(x)
        # Convert tags to indices via Vocab
        y_inds = tag_vocab(y)

        # Pad every sample with zeros to the maximal length
        x_batch = zero_pad(x_inds)
        y_batch = zero_pad(y_inds)

        mask = get_mask(x)
        nernet.train_on_batch(x_batch, y_batch, mask, dropout_keep_prob, learning_rate)
    print(k, " epoch ended")
    print('Evaluating the model on valid part of the dataset')
    f1 = eval_valid(nernet, data_iterator.gen_batches(300, 'valid', shuffle=False))

#example of using neuronet to extract entityties
# sentence = 'о разъяснении Определения Конституционного Суда Российской Федерации от 24 марта 2015 года № 720-О город Санкт-Петербург'
# x = [sentence.split()]
# x_inds = token_vocab(x)
# x_batch = zero_pad(x_inds)
# mask = get_mask(x)
# y_inds = nernet(x_batch, mask)
# for token,tag in zip(x[0],tag_vocab(y_inds)[0]):
#     print(token + " : " + tag)