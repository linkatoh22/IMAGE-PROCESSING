import numpy as np
import PIL
from PIL import Image
import matplotlib.pyplot as plt
from timeit import default_timer as timer
def cut_characters_after(string, character):
    index = string.find(character) 
    if index != -1:
        new_string = string[:index]
        return new_string
    else:
        return string
def menu():
    print('-----Image Processing-----')
    print('0.   Run All')
    print('1.   Brightness Adjust')
    print('2.   Contrast Adjust')
    print('3.   Vertically/Horizontally Adjust')
    print('4.   GrayScale and Sepia Image')
    print('5.   Blurer and Sharper Image')
    print('6.   Image Cropping')
    print('7.   Circle Cropping Image')
    print('8.   Exit')
def open_img(filename):
    img=Image.open(filename)
    return img
def img_3d(img):
    return np.array(img)
def change_brightness(image,alpha):
    alpha=np.clip(float(alpha),-255,255)
    img=img_3d(image)
    bright_image=img+alpha
    bright_limited=np.clip(bright_image,0,255)
    return bright_limited.astype(np.uint8)
def change_contrast(image,alpha):
    alpha=np.clip(float(alpha),-255,255)
    img=img_3d(image)
    factor= (259*(255+alpha))/(255*(259-alpha))
    contrast=np.clip(img*float(factor)-128*float(factor)+128,0,255)
    return contrast.astype(np.uint8)
def flip_img(image,mode):
    img=img_3d(image)
    if(mode==1 or mode==0): # 1 ngang horizontally 0 dọc vertically
        flip_img=np.flip(img,mode)
    else:
        print('Invalid mode!')
    return flip_img.astype(np.uint8)
def gray_scale(image):
    img=img_3d(image)
    gray_img=np.mean(img,axis=2)
    return gray_img.astype(np.uint8)
def sepia(image):
    img = img_3d(image)
    sepia_img = img.astype(int)
    R,G,B=sepia_img[:,:,0],sepia_img[:,:,1],sepia_img[:,:,2]
    sepia_img[:, :, 0]=0.393*R+0.769*G+0.189*B
    sepia_img[:, :, 1]=0.349*R+0.686*G+0.168*B
    sepia_img[:, :, 2]=0.272*R+0.534*G+0.131*B
    sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
    return sepia_img.astype(np.uint8)
def convolve(img,filter,dim):
    if dim == 3:
        padding=np.zeros((img.shape[0]+2,img.shape[1]+2,img.shape[2]))
        padding= np.pad(img, ((1, 1), (1, 1), (0, 0)))
        for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    multiply=np.multiply(padding[i:i+3,j:j+3],filter)
                    column=np.sum(multiply,axis=1)
                    pixel=np.sum(column,axis=0)
                    img[i,j]=pixel
    if dim == 2:
        padding=np.zeros((img.shape[0]+2,img.shape[1]+2))
        padding[1:-1,1:-1]=img
        for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    multiply = np.sum(padding[i:i+3,j:j+3] * filter)
                    img[i,j]=multiply
    img=np.clip(img, 0, 255)
    return img
def blur(img):
    img=img_3d(img)
    img=img.astype(int)
    kernel=None
    if img.ndim==3:
        kernel = np.array([[[1], [2], [1]],
                        [[2], [4], [2]],
                        [[1], [2], [1]]]) / 16
    elif img.ndim==2:
            kernel = np.array([[1, 2, 1],
                            [2, 4, 2],
                            [1, 2, 1]]) / 16                 
    blur_img=convolve(img,kernel,img.ndim)
    return blur_img.astype(np.uint8)
def sharp(img):
    img=img_3d(img)
    img=img.astype(int)
    kernel=None
    if img.ndim==3:
        kernel = np.array([[[0], [-1], [0]],
                    [[-1],[5], [-1]],
                    [[0], [-1], [0]]])
    elif img.ndim==2:
            kernel = np.array([[0, -1, 0],
                    [-1,5, -1],
                    [0, -1, 0]])
    sharp_img=convolve(img,kernel,img.ndim)
    return sharp_img.astype(np.uint8)
def crop_center(img,cropX,cropY):
    img=img_3d(img)
    h,w,c=img.shape
    h1=h//2
    w1=w//2
    cropX=cropX//2
    cropY=cropY//2
    if(h1-cropY<=0 or h1+cropY>h or w1-cropX<=0 or w1+cropX>w):
        print("Out of size! Return original pic.")
        return img.astype(np.uint8)
    center_img=img[h1-cropY:h1+cropY,w1-cropX:w1+cropX,:]
    return center_img.astype(np.uint8)
def crop_circle(img):
    img=img_3d(img)
    h,w,c=img.shape
    y,x=np.ogrid[:h,:w]
    r=(h/2)**2 #Bán kính của hình tròn bằng cách lấy chiều cao ảnh chia hai và bình
    cen_h=h//2
    cen_w=w//2
    euclidean_dis=(y-cen_h)**2+(x-cen_w)**2 #Tính từng tâm đến X Y theo euclid
    circle=(euclidean_dis>=r) # Lấy những điểm ngoài bán kính
    img[circle]=0 #Những điểm ngoài bán kính =0
    return img.astype(np.uint8)
def main():
    
    filename=input('Enter picture\'s name:')
    img=open_img(filename)
    filename=cut_characters_after(filename,'.')
    output=input('Enter output format (jpg or png or pdf):')
    while output!='png' and output!='jpg' and output!='pdf':
        print('Invalid type!')
        output=input('Enter output format (jpg or png or pdf):')
    case=None
    while(case!='8'):
        menu()
        case=input('Enter one option in all option above: ')
        if case=='0':
            alpha=input('Enter alpha to change brightness and contrast(0 to 250):')
            if(int(alpha)<-255 or int(alpha) >255):
               alpha=input('Invalid! Enter alpha again(-255 to 255):')
            bright_img=change_brightness(img,int(alpha))
            bright_image = Image.fromarray(bright_img,'RGB')
            bright_image.save(filename+'_bright.'+output)

            contrast_img=change_contrast(img,int(alpha))
            contrast_image = Image.fromarray(contrast_img,'RGB')
            contrast_image.save(filename+'_contrast.'+output)

            
            horizon_image=flip_img(img,1)
            verical_image=flip_img(img,0)
            horizon_image = Image.fromarray(horizon_image,'RGB')
            verical_image = Image.fromarray(verical_image,'RGB')
            horizon_image.save(filename+'_horizontal.'+output)
            verical_image.save(filename+'_vertical.'+output)

            gray_image=gray_scale(img)
            sepia_image=sepia(img)
            gray_image=Image.fromarray(gray_image)
            gray_image.save(filename+'_gray.'+output)
            sepia_image = Image.fromarray(sepia_image,'RGB')
            sepia_image.save(filename+'_sephia.'+output)
            
            blur_img=blur(img)
            sharp_img=sharp(img)
            blur_img = Image.fromarray(blur_img,'RGB')
            blur_img.save(filename+'_blur.'+output)
            sharp_img = Image.fromarray(sharp_img,'RGB')
            sharp_img.save(filename+'_sharp.'+output)
            
            sizeX=input('Enter the size width you want to crop: ')
            sizeY=input('Enter the size height you want to crop: ')
            crop_img=crop_center(img,int(sizeX),int(sizeY))
            crop_img = Image.fromarray(crop_img,'RGB')
            crop_img.save(filename+'_crop.'+output)

            circle_img=crop_circle(img)
            circle_img = Image.fromarray(circle_img,'RGB')
            circle_img.save(filename+'_circle.'+output)
        if case=='1':
           alpha=input('Enter alpha (-255 to 255):')
           if(int(alpha)<-255 or int(alpha) >255):
               alpha=input('Invalid! Enter alpha again(-255 to 255):')
           bright_img=change_brightness(img,int(alpha))
           bright_image = Image.fromarray(bright_img,'RGB')
           bright_image.save(filename+'_bright.'+output)
        if case=='2':
           alpha=input('Enter alpha (0 to 250):')
           if(int(alpha)<-255 or int(alpha) >255):
               alpha=input('Invalid! Enter alpha again(-255 to 255):')
           contrast_img=change_contrast(img,int(alpha))
           contrast_image = Image.fromarray(contrast_img,'RGB')
           contrast_image.save(filename+'_contrast.'+output)
        if case=='3':
            mode=input('Enter 1 for horizontally or 0 for vertically:')
            while mode!='1' and mode !='0':
               mode=input('Invalid pls enter again!\nEnter 1 for horizontally or 0 for vertically:')
            flip_image=flip_img(img,int(mode))
            flip_image = Image.fromarray(flip_image,'RGB')
            if mode=='1':
                flip_image.save(filename+'_horizontal.'+output)
            elif mode=='0':
                flip_image.save(filename+'_vertical.'+output)
        if case=='4':
            gray_image=gray_scale(img)
            sepia_image=sepia(img)
            gray_image=Image.fromarray(gray_image) #Gray scale có 255 mức xám ta lưu theo giá trị xám của nó nên ko có RGB ()
            gray_image.save(filename+'_gray.'+output)
            sepia_image = Image.fromarray(sepia_image,'RGB')
            sepia_image.save(filename+'_sephia.'+output)
        if case=='5':
            blur_img=blur(img)
            sharp_img=sharp(img)
            img1=img_3d(img)
            if(img1.ndim==3):
                blur_img = Image.fromarray(blur_img,'RGB')
                blur_img.save(filename+'_blur.'+output)
                sharp_img = Image.fromarray(sharp_img,'RGB')
                sharp_img.save(filename+'_sharp.'+output)
            if(img1.ndim==2):
                blur_img = Image.fromarray(blur_img)
                blur_img.save(filename+'_blur.'+output)
                sharp_img = Image.fromarray(sharp_img)
                sharp_img.save(filename+'_sharp.'+output)
        if case=='6':
            sizeX=input('Enter the size width you want to crop: ')
            sizeY=input('Enter the size height you want to crop: ')
            crop_img=crop_center(img,int(sizeX),int(sizeY))
            crop_img = Image.fromarray(crop_img,'RGB')
            crop_img.save(filename+'_crop.'+output)
        if case=='7':
            circle_img=crop_circle(img)
            circle_img = Image.fromarray(circle_img,'RGB')
            circle_img.save(filename+'_circle.'+output)
        
main()