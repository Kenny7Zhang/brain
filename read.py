import dfsio
import numpy as np
import nibabel as nib

def read_3d_img(path):
    '''
    
    :param path: (String) file path
    :return: (np.array) 3d matrix of img
    '''
    img = nib.load(path)
    return img.get_data()

def read_dfs_to_label(path, shape):
    '''
    read .dfs file and return 3d matrix of label
    :param path: (String) file path
    :param shape: (tuple) img shape
    :return: (np.array) 3d matrix of label
    '''
    reader = dfsio.readdfs(path)
    vertices = reader.vertices
    #print(vertices)
    #print('vertices shape {0}'.format(vertices.shape))
    vertices = vertices.astype(np.int32)
    #print(vertices.astype(np.int32))
    labels = np.zeros(shape)
    for vertix in vertices:
        labels[vertix[0]][vertix[1]][vertix[2]] = 1
    return labels

if __name__ == '__main__':
    img_path = 'data1/OAS1_0001_MR1_mpr_n4_anon_111_t88_gfc.bse.nii.gz'
    inner_cortex_path = 'data1/OAS1_0001_MR1_mpr_n4_anon_111_t88_gfc.inner.cortex.dfs'
    pial_cortex_path = 'data1/OAS1_0001_MR1_mpr_n4_anon_111_t88_gfc.pial.cortex.dfs'
    img = read_3d_img(img_path)
    inner_cortex_label = read_dfs_to_label(inner_cortex_path, img.shape)
    pial_cortex_path = read_dfs_to_label(pial_cortex_path, img.shape)
