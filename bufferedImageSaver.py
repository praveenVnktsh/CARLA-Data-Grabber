import numpy as np
import os

class BufferedImageSaver:
    def __init__(self, filename: str, size: int,
                 rows: int, cols: int, depth:int, sensorname: str):
        self.filename = filename + sensorname + '/'
        self.size = size
        self.sensorname = sensorname
        dtype = np.float32 if self.sensorname == 'CameraDepth' else np.uint8
        self.buffer = np.empty(shape=(size, rows, cols, depth),
                               dtype=dtype)
        self.index = 0
        self.reset_count = 0  # how many times this object has been reset

    def is_full(self):
        return self.index == self.size

    def reset(self):
        self.buffer = np.empty_like(self.buffer)
        self.index = 0
        self.reset_count += 1

    def save(self):
        save_name = self.filename + str(self.reset_count) + '.npy'
        
        # make the enclosing directories if not already present
        folder = os.path.dirname(save_name)
        if not os.path.isdir(folder):
            os.makedirs(folder)
        print("SAVING BUFFER!!!!!!", save_name)
        # save the buffer   
        np.save(save_name, self.buffer[:self.index + 1])

    @staticmethod
    def process_by_type(raw_img, name):
        if name == 'CameraRGB':
            return raw_img  # no need to do any processing

        elif name == 'CameraDepth':
            raw_img = raw_img.astype(np.float32)
            total = raw_img[:, :, 2:3] + 256*raw_img[:, :, 1:2] + 65536*raw_img[:, :, 0:1]
            total /= 16777215
            return total
        
        elif name == 'CameraSemSeg':
            return raw_img[:, :, 2: 3]  # only the red channel has information

    def add_image(self, img_bytes, name):

        if self.is_full():
            self.save()
            self.reset()
            self.add_image(img_bytes, name)
        else:
            raw_image = np.frombuffer(img_bytes, dtype=np.uint8)
            raw_image = raw_image.reshape(
                            self.buffer.shape[1], self.buffer.shape[2], -1)
            raw_image = self.process_by_type(raw_image[:, :, :3], name)
            self.buffer[self.index] = raw_image
            self.index += 1