
[TOCM]
#CLASIFICATION
##PLOTS
###Clasification based on raw image
#### Loss
![alt text](https://github.com/Mpasiowiec/Retinopatia/blob/main/densenet/models/densenet121_e50_s300_b14_loss_plot.jpg?raw=true)
#### Accuracy
![alt text](https://github.com/Mpasiowiec/Retinopatia/blob/main/densenet/models/densenet121_e50_s300_b14_accuracy_plot.jpg?raw=true)
###Clasification based on procesd image
#### Loss
![alt text](https://github.com/Mpasiowiec/Retinopatia/blob/main/densenet/models/densenet121_prep_e50_s300_b14_loss_plot.jpg?raw=true)
#### Accuracy
![alt text](https://github.com/Mpasiowiec/Retinopatia/blob/main/densenet/models/densenet121_prep_e50_s300_b14_accuracy_plot.jpg?raw=true)
###Clasification based on  binary vessel map
#### Loss
![alt text](https://github.com/Mpasiowiec/Retinopatia/blob/main/densenet/models/densenet121_vessel_e50_s300_b14_loss_plot.jpg?raw=true)
#### Accuracy
![alt text](https://github.com/Mpasiowiec/Retinopatia/blob/main/densenet/models/densenet121_vessel_e50_s300_b14_accuracy_plot.jpg?raw=true)
##TEST STATS
Model |  Loss | Accuracy
------------- | -------------
Clasification based on raw image  | 0.256 | 0.929
Clasification based on procesd image  |  |
Clasification based on  binary vessel map |  | 

#SEGMENTATION
##PLOTS
###Segmentation based on raw image
#### without augmentation
##### Loss
![alt text](https://github.com/Mpasiowiec/Retinopatia/blob/main/unet/models/UNet11_e35_s256_b9_loss_plot.jpg?raw=true)
##### F1 score
![alt text](https://github.com/Mpasiowiec/Retinopatia/blob/main/unet/models/UNet11_e35_s256_b9_f1_plot.jpg?raw=true)
#### with augmentation
##### Loss
![alt text](https://github.com/Mpasiowiec/Retinopatia/blob/main/unet/models/UNet11_e35_s256_b9_jit_loss_plot.jpg?raw=true)
##### F1 score
![alt text](https://github.com/Mpasiowiec/Retinopatia/blob/main/unet/models/UNet11_e35_s256_b9_jit_f1_plot.jpg?raw=true)
###Segmentation based on procesd image
#### without augmentation
##### Loss
![alt text](https://github.com/Mpasiowiec/Retinopatia/blob/main/unet/models/UNet11_prep_e35_s256_b9_loss_plot.jpg?raw=true)
##### F1 score
![alt text](https://github.com/Mpasiowiec/Retinopatia/blob/main/unet/models/UNet11_prep_e35_s256_b9_f1_plot.jpg?raw=true)
#### with augmentation
##### Loss
![alt text](https://github.com/Mpasiowiec/Retinopatia/blob/main/unet/models/UNet11_prep_e35_s256_b9_jit_loss_plot.jpg?raw=true)
##### F1 score
![alt text](https://github.com/Mpasiowiec/Retinopatia/blob/main/unet/models/UNet11_prep_e35_s256_b9_jit_f1_plot.jpg?raw=true)
##TEST STATS
Model | Loss | Iou score | F1 score | Accuracy | Recall | Precision | Specificity
------------- | -------------
Clasification based on raw image without augmentation |  |  |  |  |  |  |
Clasification based on raw image with augmentation |  |  |  |  |  |  |
Clasification based on procesd image  without augmentation |  |  |  |  |  |  |
Clasification based on procesd image with augmentation |  |  |  |  |  |  |
