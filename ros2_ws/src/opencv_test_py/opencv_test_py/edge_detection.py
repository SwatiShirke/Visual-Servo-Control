import cv2
import numpy as np





def edge_detection():
    img = cv2.imread('image1.jpg', cv2.IMREAD_GRAYSCALE)
    blur_img = cv2.GaussianBlur(img, (5, 5), 1.4)
    # Gradient in x direction
    sobel_x = cv2.Sobel(blur_img, cv2.CV_64F, 1, 0, ksize=3)  
    # Gradient in y direction
    sobel_y = cv2.Sobel(blur_img, cv2.CV_64F, 0, 1, ksize=3)   

    #find gradient magnitude
    G_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    G_magnitude = cv2.convertScaleAbs(G_magnitude)

    #NMS
    kernel = np.ones((3, 3), np.uint8)
    max_value = cv2.dilate(G_magnitude, kernel)
    nms_result = np.where(G_magnitude == max_value, G_magnitude, 0)

    #thresholding
    low_th = 30
    high_th = 100

    strong_edges = (nms_result >= high_th).astype(np.uint8)
    weak_edges = ((nms_result >= low_th) & (nms_result < high_th)).astype(np.uint8) 

    combined_edges = (strong_edges + weak_edges).astype(np.uint8)
    final_edges = np.zeros_like(combined_edges, dtype=np.uint8)
    num_labels, labels = cv2.connectedComponents(combined_edges)


    for label in range(1, num_labels):  # Start from 1 since 0 is the background
        if np.any(strong_edges[labels == label]):
            final_edges[labels == label] = 1
    

    cv2.imshow('input img', img)
    cv2.imshow('edge_detection', final_edges * 255)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return final_edges

if __name__ == "__main__":
    edge_detection()