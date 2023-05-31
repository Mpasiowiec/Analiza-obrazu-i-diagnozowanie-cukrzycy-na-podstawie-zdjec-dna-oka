import splitfolders, sys, cv2 , glob , numpy, os, shutil
 
def scaleRadius(img, scale):
    x=img[int(img.shape[0]/2), :, :].sum(1)
    r=(x>x.mean()/10).sum()/2
    s=scale*1./r
    return cv2.resize(img, (0,0), fx=s, fy=s)


output = sys.argv[1]
rat = (.7, .2, .1)
scale = 500

if len(sys.argv) == 2 or sys.argv[2] == 'class':    

    os.makedirs("./data/segm/A_vessel/control",exist_ok = True)
    os.makedirs("./data/segm/A_vessel/retina",exist_ok = True)
    os.makedirs("./data/segm/F_vessel/control",exist_ok = True)
    os.makedirs("./data/segm/F_vessel/retina",exist_ok = True)
    os.makedirs("./data/segm/H_vessel/control",exist_ok = True)
    os.makedirs("./data/segm/H_vessel/retina",exist_ok = True)
    
    for f in glob.glob('./data/ARIA/aria_c_markup_vessel/*.tif'):
        shutil.copyfile(f, "./data/segm/A_vessel/control/"+f.split('\\')[-1])

    for f in glob.glob('./data/ARIA/aria_d_markup_vessel/*.tif'):
        shutil.copyfile(f, "./data/segm/A_vessel/retina/"+f.split('\\')[-1])

    for f in glob.glob('./data/FIVES/test/Ground truth/*.png')+glob.glob('./data/FIVES/train/Ground truth/*.png'):
        leb = f.split('\\')[-1].split('.')[0].split('_')[-1]
        if leb == 'N':
            shutil.copyfile(f, "./data/segm/F_vessel/control/"+f.split('\\')[-1])
        elif leb == 'D':
            shutil.copyfile(f, "./data/segm/F_vessel/retina/"+f.split('\\')[-1])
    
    for f in glob.glob('./data/HRF/manual1/*.tif'):
        leb = f.split('\\')[-1].split('.')[0].split('_')[-1]
        if leb == 'h':
            shutil.copyfile(f, "./data/segm/H_vessel/control/"+f.split('\\')[-1])
        if leb == 'dr':
            shutil.copyfile(f, "./data/segm/H_vessel/retina/"+f.split('\\')[-1])
            
    splitfolders.ratio('./data/segm/A_vessel', output="./"+output+"/data/data_m_vessel", seed=1337, ratio=rat)
    splitfolders.ratio('./data/segm/F_vessel', output="./"+output+"/data/data_m_vessel", seed=1337, ratio=rat)
    splitfolders.ratio('./data/segm/H_vessel', output="./"+output+"/data/data_m_vessel", seed=1337, ratio=rat)
    
    os.makedirs("./data/segm/A/control",exist_ok = True)
    os.makedirs("./data/segm/A/retina",exist_ok = True)
    os.makedirs("./data/segm/F/control",exist_ok = True)
    os.makedirs("./data/segm/F/retina",exist_ok = True)
    os.makedirs("./data/segm/H/control",exist_ok = True)
    os.makedirs("./data/segm/H/retina",exist_ok = True)
    
    for f in glob.glob('./data/ARIA/aria_c_markups/*.tif'):
        shutil.copyfile(f, "./data/segm/A/control/"+f.split('\\')[-1])

    for f in glob.glob('./data/ARIA/aria_d_markups/*.tif'):
        shutil.copyfile(f, "./data/segm/A/retina/"+f.split('\\')[-1])

    for f in glob.glob('./data/FIVES/test/Original/*.png')+glob.glob('./data/FIVES/train/Original/*.png'):
        leb = f.split('\\')[-1].split('.')[0].split('_')[-1]
        if leb == 'N':
            shutil.copyfile(f, "./data/segm/F/control/"+f.split('\\')[-1])
        elif leb == 'D':
            shutil.copyfile(f, "./data/segm/F/retina/"+f.split('\\')[-1])
    
    for f in glob.glob('./data/HRF/images/*.jpg'):
        leb = f.split('\\')[-1].split('.')[0].split('_')[-1]
        if leb == 'h':
            shutil.copyfile(f, "./data/segm/H/control/"+f.split('\\')[-1])
        if leb == 'dr':
            shutil.copyfile(f, "./data/segm/H/retina/"+f.split('\\')[-1])
            
    splitfolders.ratio('./data/segm/A', output="./"+output+"/data/data_m", seed=1337, ratio=rat)
    splitfolders.ratio('./data/segm/F', output="./"+output+"/data/data_m", seed=1337, ratio=rat)
    splitfolders.ratio('./data/segm/H', output="./"+output+"/data/data_m", seed=1337, ratio=rat)

    for i in ["test", "train", "val"]:
        for f in glob.glob("./"+output+"/data/data_m/" + i + "/control/*")+glob.glob("./"+output+"/data/data_m/" + i + "/retina/*"):
            a=cv2.imread(f)
            a=scaleRadius(a,scale)
            a=cv2.addWeighted(a,                                   4,
                              cv2.GaussianBlur(a,(0,0), scale/30),-4,
                              128)
            b=numpy.zeros(a.shape)
            cv2.circle(b,(int(a.shape[1]/2), int(a.shape[0]/2)),
                       int(scale*1.15), (1,1,1),-1,8,0)
            a=a*b+128*(1-b)
            os.makedirs(os.path.join(f[:14+len(output)]+"_prep", f.split('/')[4], f.split('/')[5].split('\\')[0]),exist_ok = True)
            cv2.imwrite(os.path.join(f[:14+len(output)]+"_prep", f.split('/')[4], f.split('/')[5][:-4]+'.png'),a)
    
    shutil.rmtree("./data/segm")
    


elif sys.argv[2] == 'segm':
    
    os.makedirs("./data/segm/img",exist_ok = True)
         
    for i in glob.glob('./data/ARIA/*'):
        if i.split('\\')[-1].split('_')[-1] == 'markups':
            for f in glob.glob(i+'/*'):
                shutil.copyfile(f, "./data/segm/img/"+f.split('\\')[-1])
 
    nr=1
    for f in glob.glob('./data/FIVES/test/Original/*.png')+glob.glob('./data/FIVES/train/Original/*.png'):
        shutil.copyfile(f, "./data/segm/img/"+"f_"+str(nr)+"_"+f.split('\\')[-1].split('_')[-1])
        nr+=1
    
    for f in glob.glob('./data/HRF/images/*.jpg'):
        shutil.copyfile(f, "./data/segm/img/"+f.split('\\')[-1])
  
    splitfolders.ratio('./data/segm', output="./"+output+"/data", seed=42, ratio=rat, group_prefix=True)
    shutil.rmtree('./data/segm')
    
    for i in ['train', 'val', 'test']:
        for j in ['img_prep', 'mask_prep', 'mask', 'segm']:
            os.makedirs("./"+output+f"/data/{i}/{j}/",exist_ok = True)
    
    for f in glob.glob("./"+output+"/data/train/img/*")+glob.glob("./"+output+"/data/test/img/*")+glob.glob("./"+output+"/data/val/img/*"):
        
        for p in glob.glob(f"./data/ARIA/aria_a_markup_vessel/*.tif")+glob.glob(f"./data/ARIA/aria_d_markup_vessel/*.tif")+glob.glob(f"./data/ARIA/aria_c_markup_vessel/*.tif")+glob.glob("./data/HRF/manual1/*.tif"):
            if p.split('\\')[-1].split('.')[0][:-4] == f.split('\\')[-1][:-4]:
                if p.split('\\')[-1].split('.')[0].split('_')[-1] == 'BDP':
                    shutil.copyfile(p, f.split('\\')[0][:-3]+'segm/'+p.split('\\')[1])
                if p.split('\\')[-1].split('.')[0].split('_')[-1] == 'BSS':
                    shutil.copyfile(p, f.split('\\')[0][:-3]+'segm/'+p.split('\\')[1])
                    shutil.copyfile(f, f.split('\\')[0]+'\\'+p.split('\\')[1])
            elif p.split('\\')[-1].split('.')[0] == f.split('\\')[-1].split('.')[0]:
                shutil.copyfile(p, f.split('\\')[0][:-3]+'segm/'+p.split('\\')[1])

    
    for d in glob.glob("./"+output+"/data/train/img/*.png")+glob.glob("./"+output+"/data/test/img/*.png")+glob.glob("./"+output+"/data/val/img/*.png"):
        nr=1
        for f in glob.glob('./data/FIVES/test/Original/*.png')+glob.glob('./data/FIVES/train/Original/*.png'):
            if d.split('\\')[-1] == "f_"+str(nr)+"_"+f.split('\\')[-1].split('_')[-1]:
                for p in glob.glob('./data/FIVES/test/Ground truth/*.png')+glob.glob('./data/FIVES/train/Ground truth/*.png'):
                    if p.split('\\')[-1] == f.split('\\')[-1]:
                        shutil.copyfile(p, d.split('\\')[0][:-3]+'segm/'+"f_"+str(nr)+"_"+f.split('\\')[-1].split('_')[-1])
            nr+=1
                    
    for f in glob.glob("./"+output+"/data/train/img/*")+glob.glob("./"+output+"/data/test/img/*")+glob.glob("./"+output+"/data/val/img/*"):
                                    
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
                   int(scale*1.15), (1,1,1),-1,8,0)
        a=a*b+128*(1-b)
        
        cv2.imwrite(os.path.join(f.split("\\")[0][:-3]+'img_prep/'+f.split('\\')[1][:-4]+'.png'),a)
        cv2.imwrite(os.path.join(f.split("\\")[0][:-3]+'mask_prep/'+f.split('\\')[1][:-4]+'.png'),b * 255)
        cv2.imwrite(os.path.join(f.split("\\")[0][:-3]+'mask/'+f.split('\\')[1][:-4]+'.png'),bb * 255)
        

