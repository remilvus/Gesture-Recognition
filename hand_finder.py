import math as m
from skin_finder import SkinFinder
import numpy as np
import cv2 as cv


def find_hand(img): #zwraca wspolrzedne x,y i szerokosc kwadratu z najwieksza iloscia bialych pikseli
    height = img.shape[0]
    width = img.shape[1]
    s = m.ceil(1.5*(np.sqrt(np.sum(img)/255)))

    max_s = 0
    max_i = 0
    max_j = 0
    for i in range(0, height - s+1, 5):
        for j in range(0, width - s+1, 5):
            val = img[i:i+s, j:j+s].sum()
            if val > max_s:
                max_s, max_i, max_j = val, i, j
    return max_j, max_i, s

def cut_img(img, i, j, s):
    ans = img[i:i+s, j:j+s]
    return ans



if __name__== "__main__":
    cam = cv.VideoCapture(0)

    width = int(cam.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv.CAP_PROP_FRAME_HEIGHT))

    finder = SkinFinder(width, height)
    finder.show_trackbars()
    while True:
        ret, frame = cam.read()
        key_input = cv.waitKey(1)
        if key_input == ord('b'):
            finder.add_background(frame)

        frame = finder.repair_brightness(frame)

        if key_input == ord('p'):
            finder.get_skin_color(frame)

        if key_input == ord('q'):
            break

        if key_input == ord('a'):
            x = int(input("x: "))
            y = int(input("y: "))
            finder.add_probing_point((x, y))

        masks_merged = finder.get_important_area(frame)
        #print(masks_merged)

        frame = cv.drawMarker(frame, tuple(finder.probing_points[finder.probe_idx]), (0, 0, 255))
#       frame = cv.drawMarker(frame, find_hand(masks_merged)[:2], (0, 255, 0))

        skin_mask = finder.get_skin_mask(frame)
        foreground = finder.get_foreground_mask(frame)
        #cv.imshow("skin_mask", skin_mask)
        #cv.imshow("foreground_no_noise", foreground)
        cv.imshow("masks_merged", masks_merged)
        cv.imshow("frame", frame)

    print(find_hand(masks_merged))

    x1, x2, s = find_hand(masks_merged)
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    frame = cv.drawMarker(frame, (x1, x2), (0, 255, 0))
    frame = cv.drawMarker(frame, (x1+s, x2+s), (0, 255, 0))
    cv.imshow('image', frame)
    cv.waitKey(0)

    ready = cut_img(frame, x2, x1, s)
    cv.namedWindow('ready', cv.WINDOW_NORMAL)
    cv.imshow('ready', ready)
    cv.waitKey(0)



    # ready2 = cut_img(masks_merged, x2, x1, s)
    # cv.namedWindow('ready2', cv.WINDOW_NORMAL)
    # cv.imshow('ready2', masks_merged)
    # cv.waitKey(0)

    print(find_hand(masks_merged))
    cam.release()
    cv.destroyAllWindows()

