import os

from PIL import Image
from kp import KandinskyUniverse, RandomKandinskyFigure, SimpleObjectAndShape, ShapeOnShapes, NumbersKandinskyFigure,  KandinskyCaptions
import cv2
import json

u = KandinskyUniverse.SimpleUniverse()
cg = KandinskyCaptions.CaptionGenerator(u)


def generateImagesAndCaptions(basedir, kfgen, n=50, width=200):
    os.makedirs(basedir, exist_ok=True)
    capt_color_shape_size_file = open(basedir + "/color_shape_size.cap", "w")
    capt_numbers = open(basedir + "/numbers.cap", "w")
    for (i, kf) in enumerate(kfgen.true_kf(n)):
        image = KandinskyUniverse.kandinskyFigureAsImage(kf, width)
        image.save(basedir + "/%06d" % i + ".png")
        capt_color_shape_size_file.write(
            str(i) + '\t' + cg.colorShapesSize(kf, 'one ')+'\n')
        capt_numbers.write(str(i) + '\t' + cg.numbers(kf) + '\n')
    capt_color_shape_size_file.close()
    capt_numbers.close()


def generateSimpleNumbersCaptions(basedir, kfgen, n=50, width=200):
    os.makedirs(basedir, exist_ok=True)
    capt_numbers_file = open(basedir + "/numbers.cap", "w")
    for (i, kf) in enumerate(kfgen.true_kf(n)):
        image = KandinskyUniverse.kandinskyFigureAsImage(kf, width)
        image.save(basedir + "/%06d" % i + ".png")
        # imagePIL = KandinskyUniverse.kandinskyFigureAsImagePIL (kf, width)
        # image.save (basedir + "/%06d" % i + "_PIL.png")
        capt_numbers_file.write(str(i) + '\t' + cg.simpleNumbers(kf)+'\n')
    capt_numbers_file.close()


def generateClasses(basedir, kfgen, n=50,  width=200, counterfactual=False):
    os.makedirs(basedir + "/true", exist_ok=True)
    os.makedirs(basedir + "/false", exist_ok=True)
    for (i, kf) in enumerate(kfgen.true_kf(n)):
        image = KandinskyUniverse.kandinskyFigureAsImage(kf, width)
        image.save(basedir + "/true/%06d" % i + ".png")

    for (i, kf) in enumerate(kfgen.false_kf(n)):
        image = KandinskyUniverse.kandinskyFigureAsImage(kf, width)
        image.save(basedir + "/false/%06d" % i + ".png")
    if (counterfactual):
        os.makedirs(basedir + "/counterfactual", exist_ok=True)
        for (i, kf) in enumerate(kfgen.almost_true_kf(n)):
            image = KandinskyUniverse.kandinskyFigureAsImage(kf, width)
            image.save(basedir + "/counterfactual/%06d" % i + ".png")


def generateWithJson(basedir, kfgen, n=50, width=200):
    os.makedirs(basedir, exist_ok=True)
    capt_numbers_file = open(basedir + "/numbers.cap", "w")
    scene_json = {}

    scene_list = []

    for (i, kf) in enumerate(kfgen.true_kf(n)):
        image = KandinskyUniverse.kandinskyFigureAsImage(kf, width)
        image.save(basedir + "/%06d" % i + ".png")
        # imagePIL = KandinskyUniverse.kandinskyFigureAsImagePIL (kf, width)
        # image.save (basedir + "/%06d" % i + "_PIL.png")
        capt_numbers_file.write(str(i) + '\t' + cg.simpleNumbers(kf)+'\n')

        # json
        print(kf)

        img_dic = {'img_id': i, 'scene': []}
        for j, obj in enumerate(kf):
            obj_dic = kf[j].__dict__
            obj_dic['object_id'] = j
            img_dic['scene'].append(obj_dic)
        print('img_dic: ', img_dic)
        scene_list.append(img_dic)

    with open(basedir+'/scene.json', 'w') as f:
        json.dump(scene_list, f)

    capt_numbers_file.close()


if (__name__ == '__main__'):

    print('Welcome to the Kandinsky Figure Generator')

    train_path = 'data/pattern_free/train'
    val_path = 'data/pattern_free/val'
    test_path = 'data/pattern_free/test'
    os.makedirs(train_path, exist_ok=True)
    os.makedirs(val_path, exist_ok=True)
    os.makedirs(test_path, exist_ok=True)

    # generate kandinsky figures
    # n is the number of figures to be generated
    randomkf = RandomKandinskyFigure.Random(u, 2, 10)
    generateWithJson(train_path, randomkf, n=15, width=640)
    generateWithJson(val_path, randomkf, n=5, width=640)
    generateWithJson(test_path, randomkf, n=5, width=640)

    # randomkf = RandomKandinskyFigure.Random(u, 2, 10)
    # generateWithJson(train_path, randomkf, n=15000, width=640)
    # generateWithJson(val_path, randomkf, n=5000, width=640)
    # generateWithJson(test_path, randomkf, n=5000, width=640)
