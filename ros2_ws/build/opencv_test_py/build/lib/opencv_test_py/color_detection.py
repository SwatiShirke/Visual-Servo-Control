import cv2 
import numpy as np


def detect_colors(img):
    # The order of the colors is blue, green, red  
    #img = cv2.cvtColor(cv2.imread('./image1.jpg'), cv2.COLOR_BGR2RGB)
    center_list = []
    #detect blue
    #define HSV range for blue color
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])
    result, mask_blue, num_pixels, center = detect_blue(img,lower_blue, upper_blue)
    center_list.append(center)
    # cv2.imshow('blue detected', result)
    # print("num blue pixels: ", num_pixels)
    # print("Center of blue circle: ", center)

    #detect Red
    #define HSV range for blue color
    print("")
    lower_red = np.array([0, 100, 100])
    upper_red = np.array( [10, 255, 255])
    result, mask_red, num_pixels, center = detect_blue(img,lower_red, upper_red)
    center_list.append(center)
    # cv2.imshow('red detected', result)
    # print("num red pixels: ", num_pixels)
    # print("Center of red circle: ", center)

    ##detect green
    #define HSV range for green color
    print("")
    lower_green = np.array([40, 100, 100])
    upper_green = np.array( [80, 255, 255])
    result, mask_green, num_pixels, center = detect_blue(img,lower_green, upper_green)
    center_list.append(center)
    # cv2.imshow('green detected', result)
    # print("num green pixels: ", num_pixels)
    # print("Center of green circle: ", center)

    ##detect pink
    #define HSV range for pink color
    print("")
    lower_pink = np.array([140, 100, 100])
    upper_pink = np.array( [170, 255, 255])
    result, mask_pink, num_pixels, center = detect_blue(img,lower_pink, upper_pink)
    center_list.append(center)
    # cv2.imshow('pink detected', result)
    # print("num pink pixels: ", num_pixels)
    # print("Center of pink circle: ", center)
   
    ##combine all masks
    # masks = [mask_blue,mask_red, mask_green, mask_pink]
    
    # common_mask = sum(masks)
    # result = cv2.bitwise_and(img, img, mask=common_mask)
    # cv2.imshow('all colors detected', result)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return center_list


def detect_blue(img, lower_value, upper_value):
    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)         
    # Create a mask for blue color
    mask = cv2.inRange(hsv, lower_value, upper_value)    
    # Apply the mask to get the blue regions in the original image
    result = cv2.bitwise_and(img, img, mask=mask)    
    # Calculate the number of pixels of the color
    num_pixels = cv2.countNonZero(mask)

    # Find contours of the detected color
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    center = None
    if contours:
        # Get the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        # Calculate the moments of the largest contour
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            # Calculate the center of the detected part
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    
    return result, mask, num_pixels, center


def main():
    path = '/home/swati/VBM/ros2_ws/src/opencv_test_py/opencv_test_py/image1.jpg'
    image = cv2.imread(path)  
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)      
    ref_feature_list = detect_colors(image)
    print(ref_feature_list)


if __name__ == "__main__":
    main()