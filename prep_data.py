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
    splitfolders.ratio('./ARIA\\raw', output="./"+output+"/raw_data", seed=1337, ratio=rat)
    for f in glob.glob("./"+output+"/raw_data/train/control/*.tif")+glob.glob("./"+output+"/raw_data/test/control/*.tif")+glob.glob("./"+output+"/raw_data/val/control/*.tif")+glob.glob("./"+output+"/raw_data/train/diabetic/*.tif")+glob.glob("./"+output+"/raw_data/test/diabetic/*.tif")+glob.glob("./"+output+"/raw_data/val/diabetic/*.tif"):
        a=cv2.imread(f)
        a=scaleRadius(a,scale)
        a=cv2.addWeighted(a,                                   4,
                          cv2.GaussianBlur(a,(0,0), scale/30),-4,
                          128)
        b=numpy.zeros(a.shape)
        cv2.circle(b,(int(a.shape[1]/2), int(a.shape[0]/2)),
                   int(scale*0.93), (1,1,1),-1,8,0)
        a=a*b+128*(1-b)
        os.makedirs(os.path.join(f[:3+len(output)]+f[7+len(output):]).split('\\')[0],exist_ok = True)
        cv2.imwrite(os.path.join(f[:3+len(output)]+f[7+len(output):-4]+'.png'),a)


elif sys.argv[2] == 'segm':
    if os.path.exists("./ARIA/segm") == 0:
        os.makedirs("./ARIA/segm/raw_img",exist_ok = True)
    
        for f in glob.glob('./ARIA/raw/control/*.tif')+glob.glob('./ARIA/raw/diabetic/*.tif'):
            shutil.copyfile(f, "./ARIA/segm/raw_img/"+f.split('\\')[-1])
                
    splitfolders.ratio('./ARIA/segm', output="./"+output+"/data", seed=42, ratio=rat, group_prefix=True)
    
    shutil.rmtree('./ARIA/segm')
    
    for i in ['train', 'val', 'test']:
        for j in ['img', 'mask', 'raw_mask', 'segm_BDP', 'segm_BSS']:
            os.makedirs("./"+output+f"/data/{i}/{j}/",exist_ok = True)
    
    for f in glob.glob("./"+output+"/data/train/raw_img/*.tif")+glob.glob("./"+output+"/data/test/raw_img/*.tif")+glob.glob("./"+output+"/data/val/raw_img/*.tif"):
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
        cv2.imwrite(os.path.join(f.split('\\')[0][:-7]+'raw_mask/'+f.split('\\')[1][:-4]+'.png'),bb * 255)
        
        for p in glob.glob(f"./ARIA/vessel/control/*.tif")+glob.glob(f"./ARIA/vessel/diabetic/*.tif"):
            if p.split('\\')[-1].split('.')[0][:-4] == f.split('\\')[1][:-4]:
                if p.split('\\')[-1].split('.')[0].split('_')[-1] == 'BDP': 
                    shutil.copyfile(p, f.split('\\')[0][:-7]+'segm_BDP/'+p.split('\\')[1])
                if p.split('\\')[-1].split('.')[0].split('_')[-1] == 'BSS':
                    shutil.copyfile(p, f.split('\\')[0][:-7]+'segm_BSS/'+p.split('\\')[1])
        
        
        

