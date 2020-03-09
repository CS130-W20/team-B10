import random
import numpy as np
# import matplotlib.pyplot as plts
from sklearn.cluster import KMeans
from collections import namedtuple
import json

Attraction = namedtuple('Attraction', ['places_id','lat','lon', 'score', 'is_restaurant'])
Hyperparameters = namedtuple('Hyperparameters', ['num_iter', 'neighborhood_frac', 'bias', 'random_max', 'random_min', 'decay'])

#####################################################################
# K-means Clustering
#####################################################################
def get_cluster_id_list(attraction_list, num_clusters):
    # use k-means clustering
    xy_list = np.array([(attraction.lat,attraction.lon) for attraction in attraction_list])
    kmeans = KMeans(n_clusters=num_clusters).fit(xy_list)
    centroids = kmeans.cluster_centers_
    cluster_id_list = kmeans.labels_
    return cluster_id_list, centroids

def cluster_attraction_list(cluster_id_list, attraction_list, num_clusters):
    # seperate by clusters
    attraction_list_clusters = [[] for _ in range(num_clusters)]
    for i, attraction in enumerate(attraction_list):
        k = int(cluster_id_list[i])
        attraction_list_clusters[k].append(attraction)
    return attraction_list_clusters

#####################################################################
# Score Filtering/Curation
#####################################################################
def attraction_popping(scores, attractions, num_attr, num_rest):
    #np2int = lambda x: [int(y) for y in x]
    # sort attractions by scores
    sorted_score_index = scores.argsort()[::-1]
    sorted_attractions = []
    for score_index in sorted_score_index:
        sorted_attractions.append(attractions[int(score_index)])
    top_k_attr_rest_idx = []
    # collect top k attractions and restaurants
    for a in sorted_attractions:
        idx = attractions.index(a)
        if a.is_restaurant == False and num_attr > 0:
            top_k_attr_rest_idx.append(idx)
            num_attr -= 1
        if a.is_restaurant == True and num_rest > 0:
            top_k_attr_rest_idx.append(idx)
            num_rest -= 1
    return top_k_attr_rest_idx

def filter_attraction_list(attraction_list, L, l_avg, k_attractions, k_restaurants, hyperparameters):
    # hyperparameters
    bias = hyperparameters.bias
    random_max = hyperparameters.random_max
    random_min = hyperparameters.random_min
    decay = hyperparameters.decay

    # get neighborhoods
    kna = k_attractions/hyperparameters.neighborhood_frac
    knr = k_restaurants/hyperparameters.neighborhood_frac

    # get scores
    S = np.array([attraction.score for attraction in attraction_list])
    S_original = S.copy()
    for i in range(hyperparameters.num_iter):
        S_idxs = attraction_popping(S, attraction_list, kna, knr)
        S_neighbors = ((l_avg-L)*S)[S_idxs]
        S_agg = np.sum(S_neighbors, axis=0)
        stdev = np.max((random_max-decay*i, random_min))
        S_tilde = S_agg + bias*S_original*S_original + np.random.normal(0,stdev)
        S = 10*S_tilde/np.max(S_tilde)

    return S

def get_dists(attraction_list):
    # get l2 distance between all node pairs
    # Note: this code can be optimized in future releases
    N = len(attraction_list)
    L = np.zeros(shape=(N,N))
    xy_list = [(attraction.lat,attraction.lon) for attraction in attraction_list]
    for i in range(N):
        for j in range(i, N):
            coord1 = np.array(xy_list[i])
            coord2 = np.array(xy_list[j])
            l = np.linalg.norm(coord1-coord2, ord=1)
            L[i][j] = l
            L[j][i] = l
    return L

def sigmoid(x):
    # sigmoid function
    return 1 / (1 + np.exp(-x))

#####################################################################
# Synthetic Dataset Generation
#####################################################################
Attraction = namedtuple('Attraction', ['places_id','lat','lon', 'score', 'is_restaurant'])
def gen_syn_loc(synthetic_params, restaurant_thresh):
    assert restaurant_thresh < 1

    xys_list = []
    for param in synthetic_params:
        # generate 2D gaussian
        num_samples, mu, sigma = param
        mu_x, mu_y = mu
        sigma_x, sigma_y = sigma
        for _ in range(num_samples):
            # sample data points
            x = random.gauss(mu_x, sigma_x)
            y = random.gauss(mu_y, sigma_y)
            s = 10*random.random()
            xys_list.append((x,y,s))
    random.shuffle(xys_list)

    attraction_list = []
    for xys in xys_list:
        x,y,s = xys
        is_restaurant = random.random() < restaurant_thresh
        locale_type = 'restaurant' if is_restaurant else 'other'
        attraction_list.append(Attraction('asdf',x,y,s,is_restaurant))

    return attraction_list

#####################################################################
# Plotting Utilities
#####################################################################
def plot(S, attraction_list, ax, k=None):
    color = 'grey'
    color_sel = 'red'
    if k is None:
        # setting up plottig parameters
        x_list = [attraction.lat for attraction in attraction_list]
        y_list = [attraction.lon for attraction in attraction_list]
        s_list = S
        plot_helper(x_list, y_list, s_list, ax, color)
    else:
        # setting up plottig parameters
        s_list = S
        s_list_topk = (np.array(s_list).argsort()[-k:][::-1]).tolist()
        x_list1, y_list1, s_list1 = [], [], []
        x_list2, y_list2, s_list2 = [], [], []
        for i, attraction in enumerate(attraction_list):
            x,y,s = attraction.lat,attraction.lon,attraction.score
            if i in s_list_topk:
                x_list2.append(x)
                y_list2.append(y)
                s_list2.append(s)
            else:
                x_list1.append(x)
                y_list1.append(y)
                s_list1.append(s)
        plot_helper(x_list1, y_list1, s_list1, ax, color)
        plot_helper(x_list2, y_list2, s_list2, ax, color_sel)

def plot_helper(x_list, y_list, s_list, ax, color):
    # actual plotting code
    ax.scatter(x_list, y_list, c=color)
    for i, s in enumerate(s_list):
        ax.annotate('{0:.2f}'.format(s), (x_list[i], y_list[i]))

#####################################################################
# Main Function
#####################################################################
def main():
    # TODO: |places| < |days|
    # generate synthetic datasets
    synthetic_params = [(35, (0,-10), (5,6)), (33, (12,8), (7,7))]
    random.seed(123)
    attraction_list = gen_syn_loc(synthetic_params, 0.1)
    # clustering configurations
    num_days = 2
    # topk configurations
    hours = (8,23)
    have_breakfast = False
    k_attractions = 10 # TODO: grab this from the maps API/ database
    k_restaurants = 3 if have_breakfast else 2 # TODO: grab this from the maps API/ database
    # filtering configurations
    num_iter = 5000
    neighborhood_frac = 1.5
    bias = 10
    random_max = 5
    random_min = 1
    decay = 5e-2
    hyperparameters = Hyperparameters(num_iter, neighborhood_frac, bias, random_max, random_min, decay)

    # generate cluster by number of days
    cluster_id_list, centroids = get_cluster_id_list(attraction_list, num_days)
    attraction_list_clusters = cluster_attraction_list(cluster_id_list, attraction_list, num_days)

    # plotting the clusters
    attraction_list_copy = attraction_list.copy()
    attraction_list_copy.extend([Attraction('aaa', centroid[0], centroid[1], float('inf'), False) for centroid in centroids])
    S = np.array([attraction.score for attraction in attraction_list] + [float('inf'),float('inf')])
    ax = plt.gca()
    ax.set_title('Input Scores and Cluster Centroids')
    ax.set_xlabel('X location')
    ax.set_ylabel('Y location')
    plot(S, attraction_list_copy, ax, k=num_days)
    plt.show()

    for i, attraction_list in enumerate(attraction_list_clusters):
        # get distance matrix
        L = get_dists(attraction_list)
        l_avg = np.mean(L)
        # curate the score list of each cluster
        S = filter_attraction_list(attraction_list, L, l_avg, k_attractions, k_restaurants, hyperparameters)

        # Show the pre- and post-filtering scores and selections
        ax1 = plt.subplot(121)
        ax1.set_title('Input Scores for Cluster {}'.format(i))
        ax1.set_xlabel('X location')
        ax1.set_ylabel('Y location')
        plot(S, attraction_list, ax1, k=5)
        ax2 = plt.subplot(111)
        ax2.set_title('Filtered Scores for Cluster {}'.format(i))
        ax2.set_xlabel('X location')
        ax2.set_ylabel('Y location')
        plot(S, attraction_list, ax2, k=5)
        plt.show()
        pass

    return S, L, attraction_list, k_attractions, k_restaurants, attraction_hotel, hours

if __name__ == '__main__':
    # main()
    pass
