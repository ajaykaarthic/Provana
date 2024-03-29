import argparse
import logging
import time
import cv2
import numpy as np
import imutils

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

logger = logging.getLogger('TfPoseEstimator-Video')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
writer = None
fps_time = 0

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='tf-pose-estimation Video')
    parser.add_argument('--video', type=str, default='')
    parser.add_argument('--resolution', type=str, default='432x368', help='network input resolution. default=432x368')
    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    parser.add_argument('--showBG', type=bool, default=True, help='False to show skeleton only.')
    parser.add_argument('--ex', type =str)
    args = parser.parse_args()

    logger.debug('initialization %s : %s' % (args.model, get_graph_path(args.model)))
    w, h = model_wh(args.resolution)
    e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    cap = cv2.VideoCapture(args.video)
    count =0	
    if cap.isOpened() is False:
        print("Error opening video stream or file")
    while cap.isOpened():
        ret_val, image = cap.read()
        count += 6
        cap.set(1,count)
        image = imutils.resize(image,width=1500)
        humans = e.inference(image, resize_to_default=True, upsample_size=4.0)
        if not args.showBG:
            image = np.zeros(image.shape)
            
        if args.ex == 'lunges':
            from tf_pose.lunges import TfPoseEstimator
            image= TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
            cv2.putText(image, "FPS: %f" % (1.0 / (time.time() - fps_time)), (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.imshow('tf-pose-estimation result', image)
            fps_time = time.time()
            if writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                writer = cv2.VideoWriter('output/lunges.mp4', fourcc, 20,(image.shape[1], image.shape[0]), True)
        
            writer.write(image)
			
            if cv2.waitKey(1) == 27:
                break

        if args.ex == 'halfsquats':
            from tf_pose.halfsquats import TfPoseEstimator
            image= TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
            cv2.putText(image, "FPS: %f" % (1.0 / (time.time() - fps_time)), (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.imshow('tf-pose-estimation result', image)
            fps_time = time.time()
            if writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                writer = cv2.VideoWriter('output/halfsquats.mp4', fourcc, 20,(image.shape[1], image.shape[0]), True)
        
            writer.write(image)
			
            if cv2.waitKey(1) == 27:
                break

        if args.ex == 'dumbbell':
            from tf_pose.dumbbell import TfPoseEstimator
            image= TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
            cv2.putText(image, "FPS: %f" % (1.0 / (time.time() - fps_time)), (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.imshow('tf-pose-estimation result', image)
            fps_time = time.time()
            if writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                writer = cv2.VideoWriter('output/dumbbell.mp4', fourcc, 20,(image.shape[1], image.shape[0]), True)
        
            writer.write(image)
			
            if cv2.waitKey(1) == 27:
                break

    cv2.destroyAllWindows()
logger.debug('finished+')
