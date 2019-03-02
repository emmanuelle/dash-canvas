import numpy as np
from skimage import io, measure, feature
from scipy import ndimage

def autocrop(img):
    slices = ndimage.find_objects(img > 0)[0]
    return img[slices]


def register_tiles(imgs, n_rows, n_cols, overlap_global=None, 
                   overlap_local=None, pad=None):
    if pad is None:
        pad = 200
    l_r, l_c = imgs.shape[2:4]
    overlap = 0.15
    overlap_value = int(overlap * l_r)
    if imgs.ndim == 4:
        canvas = np.zeros((2 * pad + n_rows * l_r, 2 * pad + n_cols * l_c),
                      dtype=imgs.dtype)
    else:
        canvas = np.zeros((2 * pad + n_rows * l_r, 2 * pad + n_cols * l_c, 3),
                      dtype=imgs.dtype)
    init_r, init_c = pad, pad
    canvas[init_r:init_r + l_r, init_c:init_c + l_c] = imgs[0, 0]
    shifts = np.empty((n_rows, n_cols, 2), dtype=np.int)
    shifts[0, 0] = init_r, init_c
    counter = 0
    for i_rows in range(n_rows):
        if i_rows >= 1:
            index_target = np.ravel_multi_index((i_rows, 0), (n_rows, n_cols))
            index_orig = index_target - n_cols
            try:
                overlap = overlap_local[(index_orig, index_target)]
                print(index_orig, index_target, overlap_local[(index_orig, index_target)], overlap)
            except KeyError:
                overlap = np.array([overlap_value, 0])
                print(index_orig, index_target, overlap, "not found")
            init_r, init_c = shifts[i_rows - 1, 0]
            init_r += l_r
            shift_vert = feature.register_translation(
                    imgs[i_rows - 1, 0, -overlap[0]:, - (l_c - overlap[1]):],
                    imgs[i_rows, 0, :overlap[0], :(l_c - overlap[1])])[0]
            print("shift", shift_vert)
            init_r += int(shift_vert[0])  - overlap[0]
            init_c += int(shift_vert[1]) + overlap[1]
            shifts[i_rows, 0] = init_r, init_c
            canvas[init_r:init_r + l_r, init_c:init_c + l_c] = imgs[i_rows,
                                                                    0]
            counter += 1
        for j_cols in range(n_cols - 1):
            index_orig = np.ravel_multi_index((i_rows, j_cols),
                                              (n_rows, n_cols))
            index_target = index_orig + 1
            try:
                overlap = overlap_local[(index_orig, index_target)]
                print(index_orig, index_target, overlap_local[(index_orig, index_target)], overlap)
            except KeyError:
                overlap = np.array([0, overlap_value])
                print(index_orig, index_target, overlap, "not found")
            init_c += l_c
            shift_horiz = feature.register_translation(
                    imgs[i_rows, j_cols, - (l_r - overlap[0]):, -overlap[1]:], 
                imgs[i_rows, j_cols+1, : l_r - overlap[0], :overlap[1]])[0]
            print("shift", shift_horiz)
            init_r += int(shift_horiz[0]) + overlap[0]
            init_c += int(shift_horiz[1]) - overlap[1]
            shifts[i_rows, j_cols + 1] = init_r, init_c
            counter += 1
            canvas[init_r:init_r + l_r, init_c:init_c + l_c] = imgs[i_rows,
                                                                    j_cols+1]
    return autocrop(canvas)
