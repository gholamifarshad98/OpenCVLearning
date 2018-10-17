import numpy as np
from PIL import Image

def MySSD( leftimage, rightimage, kernel, max_offset):
    leftimage = Image.open(leftimage).convert('L')
    left = np.asarray(leftimage)
    right_image = Image.open(rightimage).convert('L')
    right = np.asarray(right_image)
    w, h = right_image.size
    depth = np.zeros((w, h), np.uint8)
    depth.shape = h ,w
    kernel_half = int(kernel/2)
    offset_adjust = 255/ max_offset

    #print(int(left[0, 0]))


    for y in range(kernel_half, h-kernel_half):
        #print('.')
        for x in range(kernel_half, w-kernel_half):
            ssd_reserved = 65534
            best_offset = 0
            for offset in range(max_offset):
                ssd = 0
                ssd_temp=0
                for v in range(-kernel_half, kernel_half):
                    for u in range(-kernel_half, kernel_half):
                        #print(left[(y+v, x+u)])
                        #print(right[y+v, 5])
                        ssd_temp = int(left[(y+v), (x+u)])-int(right[(y+v), ((x+u)-offset)])
                        ssd += ssd_temp*ssd_temp
                if ssd < ssd_reserved:
                    ssd_reserved = ssd
                    best_offset = offset
            depth[y,x] = best_offset*offset_adjust

    Image.fromarray(depth).save('depth.png')


if __name__ == '__main__':
    MySSD("view0.png", "view1.png", 6, 30)
