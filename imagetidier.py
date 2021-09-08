import PIL.Image
import imagehash
import os
import matplotlib.pyplot as pyplot
from matplotlib.widgets import TextBox

dir = r' ' #ADD PATH OF DIRECTORY CONTAINING IMAGES
dir_files = os.listdir(dir)
working_imgs = []

class Images(object):

    instances = []

    def __init__(self, name):
        self.id = name
        #self.hash_avg = imagehash.average_hash(PIL.Image.open(r'%s\%s' %(dir,self.id) ))
        self.hash_p = imagehash.phash(PIL.Image.open((r'%s\%s' %(dir,self.id))))
        self.hash_d = imagehash.dhash(PIL.Image.open((r'%s\%s' %(dir,self.id))))
        self.sim_img = []
        Images.instances.append(self)


    def deleteInstance(self):
        if os.path.exists(r'%s/%s' %(dir,self.id)):
            os.remove(r'%s/%s' %(dir,self.id))
            Images.instances.remove(self)
            working_imgs.remove(self)
            print('Deleted image %s' %(self.id))
        else:
            print(r'Image at location %s\%s does not exist, file likely deleted during script operation...' %(dir,self.id))

    @classmethod
    def getImages(self, directory):
        dir_files = os.listdir(directory)
        print('%s total files' %(len(dir_files)))
        for img in dir_files:
            if img.endswith('.png') or img.endswith('jpg'):
                working_imgs.append(Images(img))
        print('Got %s images' %(len(working_imgs)))

    @classmethod
    def compareImages(self):
        pairs = 0
        print('Comparing images...')
        for i in range(len(Images.instances)):
            for x in range(i+1,len(Images.instances)):
                dif_p = Images.instances[i].hash_p - Images.instances[x].hash_p
                dif_d = Images.instances[i].hash_d - Images.instances[x].hash_d
                if (dif_p == 0) and (dif_d == 0):
                    Images.instances[i].sim_img.append(Images.instances[x])
                    Images.instances[x].sim_img.append(Images.instances[i])
                    pairs +=1
        print('Done comparing images, %s pair(s) found...' %(pairs))
        for img in Images.instances:
            if len(img.sim_img) > 0:
                print('%s has %s similar' %(img.id,len(img.sim_img)))

    @classmethod
    def tidyImages(self,info): #SET INFO TO TRUE IF IMAGE INFORMATION SHOULD BE PRINTED WITH EACH COMPARISON
        def deleteImage(response):
            print(response)
            if response.upper() == 'Y':
                comp.deleteInstance()
                pyplot.close()
            elif response.upper() == 'N':
                comp.sim_img.remove(img)
                pyplot.close()
            else:
                pass

        for img in Images.instances:
            if len(img.sim_img) > 0:
                for comp in img.sim_img:
                    if os.path.exists(r'%s\%s' %(dir,comp.id)):
                        if info:
                            print('%s (HASH_D:%s, HASH_P:%s) and %s (HASH_D:%s, HASH_P:%s) ' %(img.id, img.hash_d, img.hash_p, comp.id, comp.hash_d, comp.hash_p))
                        img1 = pyplot.imread(r'%s\%s' %(dir,img.id))
                        img2 = pyplot.imread(r'%s\%s' %(dir,comp.id))
                        fig = pyplot.figure()
                        fig.add_subplot(2,2,1)
                        pyplot.imshow(img1)
                        fig.add_subplot(2,2,2)
                        pyplot.imshow(img2)
                        textax = pyplot.axes([0.5,0.15,0.1,0.05])
                        inputbox = TextBox(textax,'Delete: Y/N')
                        inputbox.on_submit(deleteImage)
                        pyplot.show()
                    else:
                        print(r'Similar image at location %s/%s does not exist, file likely already deleted...' %(dir,sim.id))
                        img.sim_img.remove(comp)
                        working_imgs.remove(comp)

Images.getImages(dir)
Images.compareImages()
Images.tidyImages(True)
