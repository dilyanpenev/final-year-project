
# Credits:
#
# Project: Colorful Image Colorization PyTorch https://github.com/Time0o/colorful-colorization

import os
import torch
import numpy as np
import sklearn.neighbors as snn

from torch.autograd import Function


class SoftEncoder():
    def __init__(self, NN=5, sigma=5):
        self.sigma = sigma
        q_ab = np.load(
            os.getcwd() + "\model_components\pts_in_hull.npy")
        self.nb_q = q_ab.shape[0]
        self.nn_finder = snn.NearestNeighbors(
            n_neighbors=NN, algorithm='ball_tree').fit(q_ab)

    def __call__(self, image_ab):
        h, w = image_ab.shape[:2]
        a = np.ravel(image_ab[:, :, 0])
        b = np.ravel(image_ab[:, :, 1])
        ab = np.vstack((a, b)).T
        # Get the distance to and the idx of the nearest neighbors
        dist_neighb, idx_neigh = self.nn_finder.kneighbors(ab)
        # Smooth the weights with a gaussian kernel
        wts = np.exp(-dist_neighb ** 2 / (2 * self.sigma ** 2))
        wts = wts / np.sum(wts, axis=1)[:, np.newaxis]
        # format the target
        y = np.zeros((ab.shape[0], self.nb_q))
        idx_pts = np.arange(ab.shape[0])[:, np.newaxis]
        y[idx_pts, idx_neigh] = wts
        y = y.reshape(h, w, self.nb_q)
        return y


class GetClassWeights():
    def __init__(self, lambda_=0.5):
        prior = torch.from_numpy(
            np.load(os.getcwd() + "\model_components\prior_probs.npy"))

        uniform = torch.zeros_like(prior)
        uniform[prior > 0] = 1 / (prior > 0).sum().type_as(uniform)

        self.weights = 1 / ((1 - lambda_) * prior + lambda_ * uniform)
        self.weights /= torch.sum(prior * self.weights)

    def __call__(self, ab_actual):
        return self.weights[ab_actual.argmax(dim=1, keepdim=True)]


class RebalanceLoss(Function):
    @staticmethod
    def forward(ctx, data_input, weights):
        ctx.save_for_backward(weights)

        return data_input.clone()

    @staticmethod
    def backward(ctx, grad_output):
        weights, = ctx.saved_tensors

        # reweigh gradient pixelwise so that rare colors get a chance to
        # contribute
        grad_input = grad_output * weights

        # second return value is None since we are not interested in the
        # gradient with respect to the weights
        return grad_input, None


class ABGamut:
    DTYPE = np.float32
    EXPECTED_SIZE = 313

    def __init__(self):
        self.points = np.load(
            os.getcwd() + "\model_components\pts_in_hull.npy").astype(self.DTYPE)
        self.prior = np.load(
            os.getcwd() + "\model_components\prior_probs.npy").astype(self.DTYPE)

        assert self.points.shape == (self.EXPECTED_SIZE, 2)
        assert self.prior.shape == (self.EXPECTED_SIZE,)


class CIELAB:
    L_MEAN = 50

    AB_BINSIZE = 10
    AB_RANGE = [-110 - AB_BINSIZE // 2, 110 + AB_BINSIZE // 2, AB_BINSIZE]
    AB_DTYPE = np.float32

    Q_DTYPE = np.int64

    RGB_RESOLUTION = 101
    RGB_RANGE = [0, 1, RGB_RESOLUTION]
    RGB_DTYPE = np.float64

    def __init__(self, gamut=None):
        self.gamut = gamut if gamut is not None else ABGamut()

        a, b, self.ab = self._get_ab()

        self.ab_gamut_mask = self._get_ab_gamut_mask(
            a, b, self.ab, self.gamut)

        self.q_to_ab = self._get_q_to_ab(self.ab, self.ab_gamut_mask)

    @classmethod
    def _get_ab(cls):
        a = np.arange(*cls.AB_RANGE, dtype=cls.AB_DTYPE)
        b = np.arange(*cls.AB_RANGE, dtype=cls.AB_DTYPE)

        b_, a_ = np.meshgrid(a, b)
        ab = np.dstack((a_, b_))

        return a, b, ab

    @classmethod
    def _get_ab_gamut_mask(cls, a, b, ab, gamut):
        ab_gamut_mask = np.full(ab.shape[:-1], False, dtype=bool)

        a = np.digitize(gamut.points[:, 0], a) - 1
        b = np.digitize(gamut.points[:, 1], b) - 1

        for a_, b_ in zip(a, b):
            ab_gamut_mask[a_, b_] = True

        return ab_gamut_mask

    @classmethod
    def _get_q_to_ab(cls, ab, ab_gamut_mask):
        return ab[ab_gamut_mask] + cls.AB_BINSIZE / 2


class AnnealedMeanDecodeQ:
    def __init__(self, cielab, T, device='cpu'):
        self.q_to_ab = torch.from_numpy(cielab.q_to_ab).to(device)

        self.T = T

    def __call__(self, q):
        if self.T == 0:
            # making this a special case is somewhat ugly but I have found
            # no way to make this a special case of the branch below (in
            # NumPy that would be trivial)
            ab = self._unbin(self._mode(q))
        else:
            q = self._annealed_softmax(q)

            a = self._annealed_mean(q, 0)
            b = self._annealed_mean(q, 1)
            ab = torch.cat((a, b), dim=1)

        return ab.type(q.dtype)

    def _mode(self, q):
        return q.max(dim=1, keepdim=True)[1]

    def _unbin(self, q):
        _, _, h, w = q.shape

        ab = torch.stack([
            self.q_to_ab.index_select(
                0, q_.flatten()
            ).reshape(h, w, 2).permute(2, 0, 1)

            for q_ in q
        ])

        return ab

    def _annealed_softmax(self, q):
        q = torch.exp(q / self.T)
        q /= q.sum(dim=1, keepdim=True)

        return q

    def _annealed_mean(self, q, d):
        am = torch.tensordot(q, self.q_to_ab[:, d], dims=((1,), (0,)))

        return am.unsqueeze(dim=1)
