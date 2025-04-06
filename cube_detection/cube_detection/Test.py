
import cv2
def cube_location(frame, model):
    

    results = model(frame, save=False, conf=0.25) #confidence can be changes here
    annotated_frame = results[0].plot()
    cv2.imshow("Rubix detection", annotated_frame)

   
    return(results)