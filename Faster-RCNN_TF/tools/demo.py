import _init_paths
import tensorflow as tf
import matplotlib
matplotlib.use('Agg')
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from utils.timer import Timer
import matplotlib.pyplot as plt
import numpy as np
import os, sys, cv2
import argparse
from networks.factory import get_network


CLASSES = ('__background__',
           'rust', 'grey_spot', 'mosaic', 'brown_spot',
           'alternaria_boltch')


#CLASSES = ('__background__','person','bike','motorbike','car','bus')

def vis_detections(im, class_name, dets,ax, thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return

    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]

        ax.add_patch(
            plt.Rectangle((bbox[0], bbox[1]),
                          bbox[2] - bbox[0],
                          bbox[3] - bbox[1], fill=False,
                          edgecolor='red', linewidth=3.5)
            )
        ax.text(bbox[0], bbox[1] - 2,
                '{:s} {:.3f}'.format(class_name, score),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=14, color='white')

    ax.set_title(('{} detections with '
                  'p({} | box) >= {:.1f}').format(class_name, class_name,
                                                  thresh),
                  fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.draw()


def demo(sess, net, image_name):
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the demo image
    im_file = os.path.join(cfg.DATA_DIR, 'demo', image_name)
    #im_file = os.path.join('/home/corgi/Lab/label/pos_frame/ACCV/training/000001/',image_name)
    im = cv2.imread(im_file)

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(sess, net, im)
    timer.toc()
    print ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    im = im[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(im, aspect='equal')

    CONF_THRESH = 0.8
    NMS_THRESH = 0.3
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        vis_detections(im, cls, dets, ax, thresh=CONF_THRESH)

    save_dir = 'plot_images'
    if not os.path.exists(save_dir):
       os.makedirs(save_dir)
    plt.savefig(os.path.join(save_dir,image_name))
def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Faster R-CNN demo')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]',
                        default=0, type=int)
    parser.add_argument('--cpu', dest='cpu_mode',
                        help='Use CPU mode (overrides --gpu)',
                        action='store_true')
    parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16]',
                        default='VGGnet_test')
    parser.add_argument('--model', dest='model', help='Model path',
                        default=' ')

    args = parser.parse_args()

    return args
if __name__ == '__main__':
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals

    args = parse_args()

    if args.model == ' ':
        raise IOError(('Error: Model not found.\n'))
        
    # init session
    sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
    # load network
    net = get_network(args.demo_net)
    # load model
    saver = tf.train.Saver(write_version=tf.train.SaverDef.V1)
    saver.restore(sess, args.model)
   
    #sess.run(tf.initialize_all_variables())

    print '\n\nLoaded network {:s}'.format(args.model)

    # Warmup on a dummy image
    im = 128 * np.ones((300, 300, 3), dtype=np.uint8)
    for i in xrange(2):
        _, _= im_detect(sess, net, im)

   # im_names = ['024373.jpg']
    im_names = ['000000.jpg', '000600.jpg', '001231.jpg', '005373.jpg', '005636.jpg', '006554.jpg', '011317.jpg', '012261.jpg', '016115.jpg', '016524.jpg', '016621.jpg', '023085.jpg', '023434.jpg',
                '024368.jpg', '000001.jpg', '000763.jpg', '001252.jpg', '005419.jpg', '005644.jpg', '006635.jpg', '011327.jpg', '012316.jpg', '016116.jpg', '016525.jpg', '016622.jpg', '023155.jpg', 
                '023500.jpg', '024370.jpg', '000002.jpg', '000782.jpg', '001265.jpg', '005433.jpg', '005706.jpg', '006643.jpg', '011364.jpg', '012317.jpg', '016117.jpg', '016526.jpg', '016650.jpg', 
                '000008.jpg', '000783.jpg', '001266.jpg', '005434.jpg', '005763.jpg', '006645.jpg', '011367.jpg', '012318.jpg', '016170.jpg', '016527.jpg', '016651.jpg', '023157.jpg', '023858.jpg', 
                '000009.jpg', '000787.jpg', '001593.jpg', '005470.jpg', '005771.jpg', '006668.jpg', '011378.jpg', '012339.jpg', '016171.jpg', '016528.jpg', '016659.jpg', '023158.jpg', '023859.jpg', 
                '000010.jpg', '000793.jpg', '001594.jpg', '005504.jpg', '005899.jpg', '010998.jpg', '011443.jpg', '012365.jpg', '016194.jpg', '016529.jpg', '016660.jpg', '023159.jpg', '023878.jpg',
                '000014.jpg', '000949.jpg', '001595.jpg', '005507.jpg', '006044.jpg', '011012.jpg', '011444.jpg', '012427.jpg', '016195.jpg', '016530.jpg', '016738.jpg', '023299.jpg', '024158.jpg',
                '000017.jpg', '000950.jpg', '001874.jpg', '005529.jpg', '006052.jpg', '011013.jpg', '011445.jpg', '012435.jpg', '016196.jpg', '016531.jpg', '016739.jpg', '023300.jpg', '024159.jpg',
                '000026.jpg', '000951.jpg', '001877.jpg', '005538.jpg', '006063.jpg', '011018.jpg', '011522.jpg', '012436.jpg', '016275.jpg', '016532.jpg', '016740.jpg', '023301.jpg', '024163.jpg',
                '000048.jpg', '000988.jpg', '001887.jpg', '005551.jpg', '006333.jpg', '011070.jpg', '011523.jpg', '012510.jpg', '016276.jpg', '016533.jpg', '016802.jpg', '023332.jpg', '024164.jpg',
                '000064.jpg', '000989.jpg', '005343.jpg', '005569.jpg', '006339.jpg', '011075.jpg', '011524.jpg', '012562.jpg', '016277.jpg', '016534.jpg', '023075.jpg', '023333.jpg', '024291.jpg',
                '000082.jpg', '001116.jpg', '005344.jpg', '005570.jpg', '006340.jpg', '011118.jpg', '012204.jpg', '012564.jpg', '016395.jpg', '016535.jpg', '023076.jpg', '023374.jpg', '024292.jpg',
                '000085.jpg', '001154.jpg', '005345.jpg', '005579.jpg', '006468.jpg', '011157.jpg', '012222.jpg', '012565.jpg', '016396.jpg', '016547.jpg', '023077.jpg', '023410.jpg', '024362.jpg',
                '000121.jpg', '001172.jpg', '005371.jpg', '005605.jpg', '006469.jpg', '011159.jpg', '012231.jpg', '012612.jpg', '016397.jpg', '016587.jpg', '023078.jpg', '023411.jpg', '024363.jpg',
                '000190.jpg', '001204.jpg', '005372.jpg', '005613.jpg', '006548.jpg', '011188.jpg', '012259.jpg', '012894.jpg', '016523.jpg', '016588.jpg', '023079.jpg', '023433.jpg', '024364.jpg',
                '023156.jpg', '023501.jpg', '024371.jpg', '024372.jpg', '024373.jpg']
    for im_name in im_names:
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'Demo for data/demo/{}'.format(im_name)
        demo(sess, net, im_name)
       # plt.savefig(cfg.FLAGS2["data_dir"]+'/test_result/'+ im_name, format = 'jpg',transparent = True,pad_inches = 0,dpi = 300,bbox_inches = 'tight') 
    plt.savefig(im_name)
       #plt.show()

