import splitfolders, sys
import cv2 , glob , numpy, os

def scaleRadius(img, scale):
    x=img[int(img.shape[0]/2), :, :].sum(1)
    r=(x>x.mean()/10).sum()/2
    s=scale*1./r
    return cv2.resize(img, (0,0), fx=s, fy=s)


output = sys.argv[1]
rat = (.7, .2, .1)
scale = 300

# if len(sys.argv) == 3:
    # rat = (.7, .2, .1)
    
for folder in glob.glob("./ARIA/*"):
    if folder == "./ARIA\\readme.txt" or  folder == './ARIA\\vessel': continue
    
    if folder == './ARIA\\raw': 
        dil = "/raw_data" 
        splitfolders.ratio(folder, output="./"+output+dil, seed=1337, ratio=rat)

        for f in glob.glob("./"+output+"/raw_data/train/control/*.tif")+glob.glob("./"+output+"/raw_data/test/control/*.tif")+glob.glob("./"+output+"/raw_data/val/control/*.tif")+glob.glob("./"+output+"/raw_data/train/diabetic/*.tif")+glob.glob("./"+output+"/raw_data/test/diabetic/*.tif")+glob.glob("./"+output+"/raw_data/val/diabetic/*.tif"):

            a=cv2.imread(f)
            a=scaleRadius(a,scale)
            a=cv2.addWeighted(a,                                   4,
                              cv2.GaussianBlur(a,(0,0), scale/30),-4,
                              128)
            b=numpy.zeros(a.shape)
            cv2.circle(b,(int(a.shape[1]/2), int(a.shape[0]/2)),
                       int(scale*0.9), (1,1,1),-1,8,0)
 
            a=a*b+128*(1-b)
            # print(os.path.join(f[:3+len(output)]+f[7+len(output):-4]+'.png'))
            os.makedirs(os.path.join(f[:3+len(output)]+f[7+len(output):]).split('\\')[0],exist_ok = True)
            cv2.imwrite(os.path.join(f[:3+len(output)]+f[7+len(output):-4]+'.png'),a)
    else:
        dil = "/data_vessel"
    