from mnist import MNIST

mndata = MNIST("/path_to_mnist_data_folder/")
tr_images, tr_labels = mndata.load.training()
test_images, test_labels = mndata.load_testing()