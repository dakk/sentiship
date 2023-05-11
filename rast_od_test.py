from os.path import join, dirname

from rastervision.core.rv_pipeline import (ObjectDetectionConfig,
                                           ObjectDetectionChipOptions,
                                           ObjectDetectionPredictOptions)
from rastervision.core.data import (
    ClassConfig, ObjectDetectionLabelSourceConfig, GeoJSONVectorSourceConfig,
    RasterioSourceConfig, SceneConfig, DatasetConfig, ClassInferenceTransformerConfig)
from rastervision.pytorch_backend import PyTorchObjectDetectionConfig
from rastervision.pytorch_learner import (
    Backbone, SolverConfig, ObjectDetectionModelConfig,
    ObjectDetectionImageDataConfig, ObjectDetectionGeoDataConfig,
    ObjectDetectionGeoDataWindowConfig, GeoDataWindowMethod)

import os

# CUDA OPTIONS
#os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = 'max_split_size_mb:128'


def get_config(runner, data_uri='./dataset', full_train=True, nochip=False):
    def get_path(part):
        return join(data_uri, part)

    class_config = ClassConfig(
        names=['ship'], colors=['red'])

    def make_scene(scene_id, img_path, label_path):
        raster_source = RasterioSourceConfig(
            channel_order=[0, 1, 2], uris=[img_path])
        label_source = ObjectDetectionLabelSourceConfig(
            vector_source=GeoJSONVectorSourceConfig( 
                uri=label_path, 
                ignore_crs_field=True,
                transformers=[
                    ClassInferenceTransformerConfig(default_class_id=0)
                ])
        )
        return SceneConfig(
            id=scene_id,
            raster_source=raster_source,
            label_source=label_source)

    chip_sz = 300
    img_sz = chip_sz

    scenes = [
        make_scene('od_test', get_path('anno2_sard.jp2'),
                   get_path('anno2.geojson')),
        make_scene('od_test-2', get_path('anno1_lampe.jp2'),
                   get_path('anno1.geojson'))
                   
    ]
    scene_dataset = DatasetConfig(
        class_config=class_config,
        train_scenes=scenes,
        validation_scenes=scenes)

    chip_options = ObjectDetectionChipOptions(neg_ratio=1.0, ioa_thresh=1.0)

    if nochip:
        window_opts = ObjectDetectionGeoDataWindowConfig(
            method=GeoDataWindowMethod.sliding,
            stride=chip_sz,
            size=chip_sz,
            neg_ratio=chip_options.neg_ratio,
            ioa_thresh=chip_options.ioa_thresh)

        data = ObjectDetectionGeoDataConfig(
            scene_dataset=scene_dataset,
            window_opts=window_opts,
            img_sz=img_sz,
            augmentors=[])
    else:
        data = ObjectDetectionImageDataConfig(img_sz=img_sz, augmentors=[])

    if full_train:
        model = ObjectDetectionModelConfig(backbone=Backbone.resnet18)
        solver = SolverConfig(
            lr=1e-4,
            num_epochs=12,
            batch_sz=8,
            one_cycle=True,
            sync_interval=300)
    else:
        pretrained_uri = (
            'https://github.com/azavea/raster-vision-data/releases/download/v0.12/'
            'object-detection.pth')
        model = ObjectDetectionModelConfig(
            backbone=Backbone.resnet18, init_weights=pretrained_uri)
        solver = SolverConfig(
            lr=1e-9,
            num_epochs=1,
            batch_sz=2,
            one_cycle=True,
            sync_interval=200)
    backend = PyTorchObjectDetectionConfig(
        data=data,
        model=model,
        solver=solver,
        log_tensorboard=True,
        run_tensorboard=True)

    predict_options = ObjectDetectionPredictOptions(
        merge_thresh=0.1, score_thresh=0.5)

    return ObjectDetectionConfig(
        root_uri='.',
        dataset=scene_dataset,
        backend=backend,
        train_chip_sz=chip_sz,
        predict_chip_sz=chip_sz,
        chip_options=chip_options,
        predict_options=predict_options)
