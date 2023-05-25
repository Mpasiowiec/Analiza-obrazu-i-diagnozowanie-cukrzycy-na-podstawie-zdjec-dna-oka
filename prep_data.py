import splitfolders, sys, cv2 , glob , numpy, os, shutil
 
def scaleRadius(img, scale):
    x=img[int(img.shape[0]/2), :, :].sum(1)
    r=(x>x.mean()/10).sum()/2
    s=scale*1./r
    return cv2.resize(img, (0,0), fx=s, fy=s)


output = sys.argv[1]
rat = (.7, .2, .1)
scale = 300

if len(sys.argv) == 2 or sys.argv[2] == 'class':    
    splitfolders.ratio('./data/ARIA\\raw', output="./"+output+"/data/data_A_raw", seed=1337, ratio=rat)
    for f in glob.glob("./"+output+"/data/data_A_raw/train/control/*.tif")+glob.glob("./"+output+"/data/data_A_raw/test/control/*.tif")+glob.glob("./"+output+"/data/data_A_raw/val/control/*.tif")+glob.glob("./"+output+"/data/data_A_raw/train/diabetic/*.tif")+glob.glob("./"+output+"/data/data_A_raw/test/diabetic/*.tif")+glob.glob("./"+output+"/data/data_A_raw/val/diabetic/*.tif"):
        a=cv2.imread(f)
        a=scaleRadius(a,scale)
        a=cv2.addWeighted(a,                                   4,
                          cv2.GaussianBlur(a,(0,0), scale/30),-4,
                          128)
        b=numpy.zeros(a.shape)
        cv2.circle(b,(int(a.shape[1]/2), int(a.shape[0]/2)),
                   int(scale*0.93), (1,1,1),-1,8,0)
        a=a*b+128*(1-b)
        os.makedirs(os.path.join(f[:14+len(output)]+f[18+len(output):]).split('\\')[0],exist_ok = True)
        cv2.imwrite(os.path.join(f[:14+len(output)]+f[18+len(output):-4]+'.png'),a)

    splitfolders.ratio('./data/ARIA\\vessel', output="./"+output+"/data/data_A_vessel", seed=1337, ratio=rat)
       
    splitfolders.ratio('./data/HRF\\raw', output="./"+output+"/data/data_H_raw", seed=1337, ratio=rat)
    for f in glob.glob("./"+output+"/data/data_H_raw/train/control/*.jpg")+glob.glob("./"+output+"/data/data_H_raw/test/control/*.jpg")+glob.glob("./"+output+"/data/data_H_raw/val/control/*.jpg")+glob.glob("./"+output+"/data/data_H_raw/train/diabetic/*.jpg")+glob.glob("./"+output+"/data/data_H_raw/test/diabetic/*.jpg")+glob.glob("./"+output+"/data/data_H_raw/val/diabetic/*.jpg"):
        a=cv2.imread(f)
        a=scaleRadius(a,scale)
        a=cv2.addWeighted(a,                                   4,
                          cv2.GaussianBlur(a,(0,0), scale/30),-4,
                          128)
        b=numpy.zeros(a.shape)
        cv2.circle(b,(int(a.shape[1]/2), int(a.shape[0]/2)),
                   int(scale*0.93), (1,1,1),-1,8,0)
        a=a*b+128*(1-b)
        os.makedirs(os.path.join(f[:14+len(output)]+f[18+len(output):]).split('\\')[0],exist_ok = True)
        cv2.imwrite(os.path.join(f[:14+len(output)]+f[18+len(output):-4]+'.png'),a)
        
    splitfolders.ratio('./data/HRF\\vessel', output="./"+output+"/data/data_H_vessel", seed=1337, ratio=rat)
    
    shutil.copytree("./"+output+"/data/data_A", "./"+output+"/data/data_m", dirs_exist_ok=True)
    shutil.copytree("./"+output+"/data/data_H", "./"+output+"/data/data_m", dirs_exist_ok=True)
    shutil.copytree("./"+output+"/data/data_A_raw", "./"+output+"/data/data_m_raw", dirs_exist_ok=True)
    shutil.copytree("./"+output+"/data/data_H_raw", "./"+output+"/data/data_m_raw", dirs_exist_ok=True)
    shutil.copytree("./"+output+"/data/data_A_vessel", "./"+output+"/data/data_m_vessel", dirs_exist_ok=True)
    shutil.copytree("./"+output+"/data/data_H_vessel", "./"+output+"/data/data_m_vessel", dirs_exist_ok=True)
    


elif sys.argv[2] == 'segm':
    if os.path.exists("./ARIA/segm") == False:
        os.makedirs("./ARIA/segm/img_raw",exist_ok = True)
    
        for f in glob.glob('./ARIA/raw/control/*.tif')+glob.glob('./ARIA/raw/diabetic/*.tif'):
            shutil.copyfile(f, "./ARIA/segm/img_raw/"+f.split('\\')[-1])
                
    splitfolders.ratio('./ARIA/segm', output="./"+output+"/data", seed=42, ratio=rat, group_prefix=True)
    
    shutil.rmtree('./ARIA/segm')
    
    for i in ['train', 'val', 'test']:
        for j in ['img', 'mask', 'mask_raw', 'segm_BDP', 'segm_BSS']:
            os.makedirs("./"+output+f"/data/{i}/{j}/",exist_ok = True)
    
    for f in glob.glob("./"+output+"/data/train/img_raw/*.tif")+glob.glob("./"+output+"/data/test/img_raw/*.tif")+glob.glob("./"+output+"/data/val/img_raw/*.tif"):
        a=cv2.imread(f)
        bb=numpy.zeros(a.shape)
        cv2.circle(bb,(int(a.shape[1]/2), int(a.shape[0]/2)),
                   int(a.shape[1]/2*0.93), (1,1,1),-1,8,0) 
        a=scaleRadius(a,scale)
        a=cv2.addWeighted(a,                                   4,
                          cv2.GaussianBlur(a,(0,0), scale/30),-4,
                          128)
        b=numpy.zeros(a.shape)
        cv2.circle(b,(int(a.shape[1]/2), int(a.shape[0]/2)),
                   int(scale*0.93), (1,1,1),-1,8,0)
        a=a*b+128*(1-b)
        cv2.imwrite(os.path.join(f.split('\\')[0][:-7]+'img/'+f.split('\\')[1][:-4]+'.png'),a)
        cv2.imwrite(os.path.join(f.split('\\')[0][:-7]+'mask/'+f.split('\\')[1][:-4]+'.png'),b * 255)
        cv2.imwrite(os.path.join(f.split('\\')[0][:-7]+'mask_raw/'+f.split('\\')[1][:-4]+'.png'),bb * 255)
        
        for p in glob.glob(f"./ARIA/vessel/control/*.tif")+glob.glob(f"./ARIA/vessel/diabetic/*.tif"):
            if p.split('\\')[-1].split('.')[0][:-4] == f.split('\\')[1][:-4]:
                if p.split('\\')[-1].split('.')[0].split('_')[-1] == 'BDP': 
                    shutil.copyfile(p, f.split('\\')[0][:-7]+'segm_BDP/'+p.split('\\')[1])
                if p.split('\\')[-1].split('.')[0].split('_')[-1] == 'BSS':
                    shutil.copyfile(p, f.split('\\')[0][:-7]+'segm_BSS/'+p.split('\\')[1])
        
        
        

