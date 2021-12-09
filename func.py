#!/usr/bin/env python
# coding: utf-8

# In[2]:


from keras.models import load_model


# In[3]:


from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd
import numpy as np
from keras.models import load_model



model = load_model('resnet50_100.h5')


# In[10]:


new_datagen = ImageDataGenerator(rescale =1/255.)

def load_data(path):

    train_generator = new_datagen.flow_from_directory(
        directory = path,
        target_size=(224, 224),
        class_mode = None,
        shuffle=False)
    
    return train_generator


# In[14]:



def pred_func(load_data):
    pred = model.predict(load_data, steps=len(load_data), verbose=1)
    
    #cl = np.round(pred)
    #filenames=load_data.filenames
    #How_old=pd.DataFrame({"file":filenames,"pr":pred[:,0], "class":cl[:,0]})
    
    return np.round(int(pred[0]))
    

    



# In[ ]:




