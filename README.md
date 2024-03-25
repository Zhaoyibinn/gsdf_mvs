# GSDF: 3DGS Meets SDF for Improved Rendering and Reconstruction

[Mulin Yu*](https://scholar.google.com/citations?user=w0Od3hQAAAAJ), [Tao Lu*](https://github.com/inspirelt), [Linning Xu](https://eveneveno.github.io/lnxu), [Lihan Jiang](https://jianglh-whu.github.io/), [Yuanbo Xiangli✉](https://kam1107.github.io/), [Bo Dai](https://daibo.info/) <br />


[[`Project Page`](https://city-super.github.io/GSDF/)][[`arxiv`](https://arxiv.org/abs/2312.00109)]

<!-- ## News

**[2024.02.27]**  Accepted to [CVPR 2024](https://cvpr.thecvf.com/).

**[2024.01.22]**  We add the appearance embedding to Scaffold-GS to handle wild scenes.

**[2024.01.22]** 🎈👀 The [viewer](https://github.com/city-super/Scaffold-GS/tree/main/SIBR_viewers) for Scaffold-GS is available now. 

**[2023.12.10]** We release the code. -->

## Overview

<p align="center">
<img src="assets/pipline.png" width=100% height=100% 
class="center">
</p>

Our dual-branch framework comprises a GS-branch dedicated to rendering and an SDF-branch focusing on learning neural surfaces. Our design effectively preserves the superiority of rendering with Gaussian primitives in terms of efficiency and fidelity, and also more accurately approximates scene surfaces from an SDF field adapted from NeuS. Concretely, (1) we leverage the efficiency and flexibility advantages of the GS-branch, to render depth maps and guide the ray sampling process of the SDF-branch. For each depth position, we query the SDF-branch to obtain its absolute SDF value |s|, and uniformly sample points within 2k|s| (e.g. k = 4). (2) The predicted SDF values from the SDF-branch are in turn used to guide the density control of the GS-branch to grow Gaussian primitives in near-surface regions and prune the ones that are far-away. (3) We further enforce mutual geometry consistency by comparing the depth and normal maps from each branch to encourage more coherent physical alignment between Gaussian primitives and surfaces.


### The code is coming soon.



<!-- ## Installation

We tested on a server configured with Ubuntu 18.04, cuda 11.6 and gcc 9.4.0. Other similar configurations should also work, but we have not verified each one individually.

1. Clone this repo:

```
git clone https://github.com/city-super/Scaffold-GS.git --recursive
cd Scaffold-GS
```

2. Install dependencies

```
SET DISTUTILS_USE_SDK=1 # Windows only
conda env create --file environment.yml
conda activate scaffold_gs
```

## Data

First, create a ```data/``` folder inside the project path by 

```
mkdir data
```

The data structure will be organised as follows:

```
data/
├── dataset_name
│   ├── scene1/
│   │   ├── images
│   │   │   ├── IMG_0.jpg
│   │   │   ├── IMG_1.jpg
│   │   │   ├── ...
│   │   ├── sparse/
│   │       └──0/
│   ├── scene2/
│   │   ├── images
│   │   │   ├── IMG_0.jpg
│   │   │   ├── IMG_1.jpg
│   │   │   ├── ...
│   │   ├── sparse/
│   │       └──0/
...
```


### Public Data

The BungeeNeRF dataset is available in [Google Drive](https://drive.google.com/file/d/1nBLcf9Jrr6sdxKa1Hbd47IArQQ_X8lww/view?usp=sharing)/[百度网盘[提取码:4whv]](https://pan.baidu.com/s/1AUYUJojhhICSKO2JrmOnCA). The MipNeRF360 scenes are provided by the paper author [here](https://jonbarron.info/mipnerf360/). And we test on scenes ```bicycle, bonsai, counter, garden, kitchen, room, stump```. The SfM data sets for Tanks&Temples and Deep Blending are hosted by 3D-Gaussian-Splatting [here](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/datasets/input/tandt_db.zip). Download and uncompress them into the ```data/``` folder.

### Custom Data

For custom data, you should process the image sequences with [Colmap](https://colmap.github.io/) to obtain the SfM points and camera poses. Then, place the results into ```data/``` folder.


## Training

### Training multiple scenes

To train multiple scenes in parallel, we provide batch training scripts: 

 - Tanks&Temples: ```train_tnt.sh```
 - MipNeRF360: ```train_mip360.sh```
 - BungeeNeRF: ```train_bungee.sh```
 - Deep Blending: ```train_db.sh```
 - Nerf Synthetic: base ->```train_nerfsynthetic.sh```; with warmup->```train_nerfsynthetic_withwarmup.sh```

 run them with 

 ```
bash train_xxx.sh
 ```

 > Notice 1: Make sure you have enough GPU cards and memories to run these scenes at the same time.

 > Notice 2: Each process occupies many cpu cores, which may slow down the training process. Set ```torch.set_num_threads(32)``` accordingly in the ```train.py``` to alleviate it.

### Training a single scene

For training a single scene, modify the path and configurations in ```single_train.sh``` accordingly and run it:

```
bash ./single_train.sh
```

- scene: scene name with a format of ```dataset_name/scene_name/``` or ```scene_name/```;
- exp_name: user-defined experiment name;
- gpu: specify the GPU id to run the code. '-1' denotes using the most idle GPU. 
- voxel_size: size for voxelizing the SfM points, smaller value denotes finer structure and higher overhead, '0' means using the median of each point's 1-NN distance as the voxel size.
- update_init_factor: initial resolution for growing new anchors. A larger one will start placing new anchor in a coarser resolution.

> For these public datasets, the configurations of 'voxel_size' and 'update_init_factor' can refer to the above batch training script. 


This script will store the log (with running-time code) into ```outputs/dataset_name/scene_name/exp_name/cur_time``` automatically.





## Evaluation

We've integrated the rendering and metrics calculation process into the training code. So, when completing training, the ```rendering results```, ```fps``` and ```quality metrics``` will be printed automatically. And the rendering results will be save in the log dir. Mind that the ```fps``` is roughly estimated by 

```
torch.cuda.synchronize();t_start=time.time()
rendering...
torch.cuda.synchronize();t_end=time.time()
```

which may differ somewhat from the original 3D-GS, but it does not affect the analysis.

Meanwhile, we keep the manual rendering function with a similar usage of the counterpart in [3D-GS](https://github.com/graphdeco-inria/gaussian-splatting), one can run it by 

```
python render.py -m <path to trained model> # Generate renderings
python metrics.py -m <path to trained model> # Compute error metrics on renderings
```

## Viewer

The [viewer](https://github.com/city-super/Scaffold-GS/tree/main/SIBR_viewers) for Scaffold-GS is available now. 



## Contact

- Tao Lu: taolu@smail.nju.edu.cn
- Mulin Yu: yumulin@pjlab.org.cn

## Citation

If you find our work helpful, please consider citing:

```bibtex
@misc{scaffoldgs,
      title={Scaffold-GS: Structured 3D Gaussians for View-Adaptive Rendering}, 
      author={Tao Lu and Mulin Yu and Linning Xu and Yuanbo Xiangli and Limin Wang and Dahua Lin and Bo Dai},
      year={2023},
      eprint={2312.00109},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

## LICENSE

Please follow the LICENSE of [3D-GS](https://github.com/graphdeco-inria/gaussian-splatting).

## Acknowledgement

We thank all authors from [3D-GS](https://github.com/graphdeco-inria/gaussian-splatting) for presenting such an excellent work. -->
