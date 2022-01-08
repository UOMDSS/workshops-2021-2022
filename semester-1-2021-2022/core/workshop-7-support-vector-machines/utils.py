import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def plot_iris(class1, class1_name: str, class2, class2_name: str, feature1: str, feature2: str):
    plt.title('Plot two classes of features')
    sns.scatterplot(data=class1, x=class1[:,0], y=class1[:,1], label=class1_name, color='orange')
    sns.scatterplot(data=class2, x=class2[:,0], y=class2[:,1], label=class2_name, color='#9966cc')
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.legend()


def plot_dataset(axis, class1, class1_name: str, class2, class2_name: str, class3, class3_name: str, feature1: str, feature2: str):
    axis.set_title('Plot total dataset')
    sns.scatterplot(data=class1, x=class1[:,0], y=class1[:,1], label=class1_name, color='orange', ax=axis)
    sns.scatterplot(data=class2, x=class2[:,0], y=class2[:,1], label=class2_name, color='#9966cc', ax=axis)
    sns.scatterplot(data=class3, x=class3[:,0], y=class3[:,1], label=class3_name, ax=axis)
    axis.set_xlabel(feature1)
    axis.set_ylabel(feature2)
    plt.legend()


def get_idx_from_features(feature1: int, feature2: int):
    features = ['sepal length (cm)',
                'sepal width (cm)',
                'petal length (cm)',
                'petal width (cm)']
    return features.index(feature1), features.index(feature2)


def make_meshgrid(x, y, h=.02):
    x_min, x_max = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1, y.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    return xx, yy


def plot_contours(ax, clf, xx, yy, **params):
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    out = ax.contourf(xx, yy, Z, **params)
    return out


def plot_nonlinear(X, y):
    plt.plot(X[:, 0][y == 0], X[:, 1][y == 0], 'b^')
    plt.plot(X[:, 0][y == 1], X[:, 1][y == 1], 'ys')
