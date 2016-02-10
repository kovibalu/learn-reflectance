import os
import shutil
import sys
import tempfile

from django.conf import settings

from util import decompose_single_image


def run(image, device_id, **kwargs):
    tmpdir = tempfile.mkdtemp()
    try:
        image_file = os.path.join(tmpdir, 'input.png')
        image.save(image_file)

        algo_dir = os.path.join(
            settings.SRC_DIR, 'intrinsic', 'algorithm', 'zhou2015release',
        )
        os.chdir(algo_dir)
        caffe_python_dir = os.path.join('caffe', 'python')

        sys.path.append(caffe_python_dir)
        # Silence Caffe
        from os import environ
        environ['GLOG_minloglevel'] = '2'
        import caffe
        caffe.set_mode_gpu()
        caffe.set_device(device_id)
        fnet = caffe.Net('net/feat.prototxt', 'net/rref.caffemodel', 1)
        rnet = caffe.Net('net/rref.prototxt', 'net/rref.caffemodel', 1)

        return decompose_single_image(image_file, fnet, rnet, srgb=True)
    finally:
        shutil.rmtree(tmpdir)
