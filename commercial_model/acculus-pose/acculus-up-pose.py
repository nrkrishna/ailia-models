import sys
import time

import cv2
import numpy as np

import ailia

sys.path.append('../../util')
from utils import get_base_parser, update_parser, get_savepath  # noqa: E402
from webcamera_utils import adjust_frame_size, get_capture  # noqa: E402
from image_utils import load_image  # noqa: E402
from model_utils import check_and_download_models  # noqa: E402

# logger
from logging import getLogger   # noqa: E402
logger = getLogger(__name__)


# ======================
# Parameters 1
# ======================
IMAGE_PATH = 'balloon.png'
SAVE_IMAGE_PATH = 'output.png'
IMAGE_HEIGHT = 240
IMAGE_WIDTH = 320


# ======================
# Arguemnt Parser Config
# ======================
parser = get_base_parser(
    'Acculus human up pose estimation.', IMAGE_PATH, SAVE_IMAGE_PATH
)
parser.add_argument(
    '-f', '--fpga', action='store_true',
    help=('By default, the gpu model is used, but with this option, '
          'you can switch to the fpga model')
)
args = update_parser(parser)


# ======================
# Parameters 2
# ======================
# NOTE: commercial model
logger.warning('The pre-trained model is not available freely')
MODEL_NAME = 'acculus-pose'
REMOTE_PATH = ''

if args.fpga:
    WEIGHT_PATH = 'uppose_fpga_1_obf.caffemodel'
    MODEL_PATH = 'uppose_fpga_obf.prototxt'
    ALGORITHM = ailia.POSE_ALGORITHM_ACCULUS_UPPOSE_FPGA
else:
    WEIGHT_PATH = 'uppose_obf.caffemodel'
    MODEL_PATH = 'uppose_obf.prototxt'
    ALGORITHM = ailia.POSE_ALGORITHM_ACCULUS_UPPOSE


# ======================
# Utils
# ======================
def hsv_to_rgb(h, s, v):
    bgr = cv2.cvtColor(
        np.array([[[h, s, v]]], dtype=np.uint8), cv2.COLOR_HSV2BGR
    )[0][0]
    return (int(bgr[2]), int(bgr[1]), int(bgr[0]))


def line(input_img, person, point1, point2):
    threshold = 0.3
    if person.points[point1].score > threshold and\
       person.points[point2].score > threshold:
        color = hsv_to_rgb(255*point1/ailia.POSE_UPPOSE_KEYPOINT_CNT, 255, 255)

        x1 = int(input_img.shape[1] * person.points[point1].x)
        y1 = int(input_img.shape[0] * person.points[point1].y)
        x2 = int(input_img.shape[1] * person.points[point2].x)
        y2 = int(input_img.shape[0] * person.points[point2].y)
        cv2.line(input_img, (x1, y1), (x2, y2), color, 5)


def display_result(input_img, pose):
    count = pose.get_object_count()
    for idx in range(count):
        person = pose.get_object_up_pose(idx)

        line(input_img, person, ailia.POSE_UPPOSE_KEYPOINT_NOSE,
             ailia.POSE_UPPOSE_KEYPOINT_SHOULDER_CENTER)
        line(input_img, person, ailia.POSE_UPPOSE_KEYPOINT_SHOULDER_LEFT,
             ailia.POSE_UPPOSE_KEYPOINT_SHOULDER_CENTER)
        line(input_img, person, ailia.POSE_UPPOSE_KEYPOINT_SHOULDER_RIGHT,
             ailia.POSE_UPPOSE_KEYPOINT_SHOULDER_CENTER)

        line(input_img, person, ailia.POSE_UPPOSE_KEYPOINT_EYE_LEFT,
             ailia.POSE_UPPOSE_KEYPOINT_NOSE)
        line(input_img, person, ailia.POSE_UPPOSE_KEYPOINT_EYE_RIGHT,
             ailia.POSE_UPPOSE_KEYPOINT_NOSE)
        line(input_img, person, ailia.POSE_UPPOSE_KEYPOINT_EAR_LEFT,
             ailia.POSE_UPPOSE_KEYPOINT_EYE_LEFT)
        line(input_img, person, ailia.POSE_UPPOSE_KEYPOINT_EAR_RIGHT,
             ailia.POSE_UPPOSE_KEYPOINT_EYE_RIGHT)

        line(input_img, person, ailia.POSE_UPPOSE_KEYPOINT_ELBOW_LEFT,
             ailia.POSE_UPPOSE_KEYPOINT_SHOULDER_LEFT)
        line(input_img, person, ailia.POSE_UPPOSE_KEYPOINT_ELBOW_RIGHT,
             ailia.POSE_UPPOSE_KEYPOINT_SHOULDER_RIGHT)
        line(input_img, person, ailia.POSE_UPPOSE_KEYPOINT_WRIST_LEFT,
             ailia.POSE_UPPOSE_KEYPOINT_ELBOW_LEFT)
        line(input_img, person, ailia.POSE_UPPOSE_KEYPOINT_WRIST_RIGHT,
             ailia.POSE_UPPOSE_KEYPOINT_ELBOW_RIGHT)

        line(input_img, person, ailia.POSE_UPPOSE_KEYPOINT_BODY_CENTER,
             ailia.POSE_UPPOSE_KEYPOINT_SHOULDER_CENTER)
        line(input_img, person, ailia.POSE_UPPOSE_KEYPOINT_HIP_LEFT,
             ailia.POSE_UPPOSE_KEYPOINT_BODY_CENTER)
        line(input_img, person, ailia.POSE_UPPOSE_KEYPOINT_HIP_RIGHT,
             ailia.POSE_UPPOSE_KEYPOINT_BODY_CENTER)


# ======================
# Main functions
# ======================
def recognize_from_image():
    # net initialize
    pose = ailia.PoseEstimator(
        MODEL_PATH, WEIGHT_PATH, env_id=args.env_id, debug_log=args.debug, algorithm=ALGORITHM
    )

    # input image loop
    for image_path in args.input:
        # prepare input data
        logger.info(image_path)
        src_img = cv2.imread(image_path)
        input_image = load_image(
            image_path,
            (IMAGE_HEIGHT, IMAGE_WIDTH),
            normalize_type='None'
        )
        input_data = cv2.cvtColor(input_image, cv2.COLOR_RGB2BGRA)

        # inference
        logger.info('Start inference...')
        if args.benchmark:
            logger.info('BENCHMARK mode')
            for i in range(5):
                start = int(round(time.time() * 1000))
                _ = pose.compute(input_data)
                end = int(round(time.time() * 1000))
                logger.info(f'\tailia processing time {end - start} ms')
        else:
            _ = pose.compute(input_data)

        # postprocessing
        count = pose.get_object_count()
        logger.info(f'person_count={count}')
        display_result(src_img, pose)
        # TODO: deprecate next line
        # cv2.imwrite(args.savepath, src_img)
        cv2.imwrite(get_savepath(args.savepath, image_path), src_img)
    logger.info('Script finished successfully.')


def recognize_from_video():
    # net initialize
    pose = ailia.PoseEstimator(
        MODEL_PATH, WEIGHT_PATH, env_id=args.env_id, debug_log=args.debug, algorithm=ALGORITHM
    )
    shape = pose.get_input_shape()
    logger.info(shape)
    IMAGE_WIDTH = shape[3]
    IMAGE_HEIGHT = shape[2]

    capture = get_capture(args.video)

    while(True):
        ret, frame = capture.read()
        if (cv2.waitKey(1) & 0xFF == ord('q')) or not ret:
            break

        input_image, input_data = adjust_frame_size(
            frame, IMAGE_HEIGHT, IMAGE_WIDTH,
        )
        input_data = cv2.cvtColor(input_data, cv2.COLOR_BGR2BGRA)

        # inference
        _ = pose.compute(input_data)

        # postprocessing
        display_result(input_image, pose)
        cv2.imshow('frame', input_image)

    capture.release()
    cv2.destroyAllWindows()
    logger.info('Script finished successfully.')


def main():
    # model files check and download
    check_and_download_models(WEIGHT_PATH, MODEL_PATH, REMOTE_PATH)

    if args.video is not None:
        # video mode
        recognize_from_video()
    else:
        # image mode
        recognize_from_image()


if __name__ == '__main__':
    main()
