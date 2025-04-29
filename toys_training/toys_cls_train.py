#importing the libraries
import pandas as pd
import torch
import cv2
from matplotlib import pyplot as  plt
import random
import os
random.seed(17)
from torch.utils.data import Dataset, Subset, DataLoader
import torchvision
from torchvision.models import resnet18, ResNet18_Weights
from torchvision import transforms
import torch.nn as nn
from PIL import Image
from torchvision.io import read_image
from sklearn.model_selection import train_test_split
import json
from tqdm import tqdm
import numpy as np
import warnings
warnings.simplefilter(action='ignore')
from sklearn.metrics import classification_report
from torch_lr_finder import LRFinder

#Loading the csv file for the data
df = pd.read_csv("PATH TO THE CSV FILE.")

#stratified split
def get_split_indices(df,column,stratify = True,val_split=0.2,test_split=0.1):
    if stratify:
        train, test_idxs = train_test_split(df.index, test_size=test_split, stratify=df[column])
        train_idxs,val_idxs = train_test_split(train, test_size=val_split, stratify=df.iloc[train,:][column])
    else:
        train, test_idxs = train_test_split(df.index, test_size=test_split, stratify=df[column])
        train_idxs,val_idxs = train_test_split(train, test_size=val_split, stratify=df.iloc[train,:][column])
    return train_idxs,val_idxs,test_idxs



#class for loading the images
#Give the path for the images
img_name_fn = lambda x: f"PATH FOR THE IMAGES/{x.split('/')[-1]}.jpg"

class ImageDataset(Dataset):

    def __init__(self,df,cat,class_type = "class_type",dt_type="train",img_size = (224,224),transforms_=False):
        mapper = {True:1,False:0}
        df["image_url"].apply(img_name_fn)
        self.dt_type = dt_type
        self.df = df[df[class_type] == self.dt_type]
        self.label = list(self.df[cat].map(mapper).values)
        self.df["img_name"] = self.df["image_url"].apply(img_name_fn)
        self.img_names = list(self.df["img_name"].values)
        self.default_transform = transforms.Compose([transforms.ToPILImage(), transforms.Resize(size=img_size),transforms.ToTensor()])
        self.transform = self.transforms(transforms_)


    def __len__(self):
        return len(self.img_names)

    def __getitem__(self,idx):
        image = read_image(self.img_names[idx])
        image = self.transform(image)
        label = self.label[idx]
        return image,label
    def transforms(self,transforms):
        if self.dt_type != "test":
            if not transforms:
                return  self.default_transform
            else:
                return transforms
        else:
            return self.default_transform


from torch.utils.data.sampler import WeightedRandomSampler
def img_dataloader(train_ds,val_ds,bs_train = 32,bs_val = 32,upsampling=False):
    
    if upsampling:
        labels_unq, counts = np.unique(train_ds.label,return_counts=True)
        class_weights = [sum(counts)/c for c in counts]
        example_wts = [class_weights[e] for e in train_ds.label]
        sampler = WeightedRandomSampler(example_wts,len(train_ds.label))
        train_dl = DataLoader(train_ds,batch_size=bs_train,sampler=sampler)

    else:
        train_dl = DataLoader(train_ds,batch_size=bs_train,shuffle = True)
    val_dl = DataLoader(val_ds,batch_size=bs_val,shuffle = True)

    return train_dl, val_dl


#setup the model function
def load_model(freeze_backbone,out_features,device,model_path=False):
    
    model = torchvision.models.resnet18(pretrained=True)
    if freeze_backbone:
        for param in model.parameters():
            param.requires_grad = False
    model.fc = nn.Sequential(
        nn.Linear(model.fc.in_features, out_features),
        nn.Sigmoid()           
        )
    if model_path:
        model.load_state_dict(torch.load(model_path,map_location=torch.device(device)))
    return model

#Train function
def fit_one_epoch(train_loader,model,criterion,device,optimizer, epoch, num_epochs,thresh = 0.5 ): 
    step_train = 0

    train_losses = list()
    train_acc = list()
    model.train()
    for i, (images, targets) in enumerate(tqdm(train_loader)):
        images = images.to(device)
        targets = targets.to(device)
        logits = model(images)
        targets = targets.unsqueeze(1).float()
        loss = criterion(logits, targets)

        loss.backward()
        optimizer.step()

        optimizer.zero_grad()

        train_losses.append(loss.item())

        preds = torch.Tensor(np.where(logits.detach().cpu() < thresh, 0, 1))

        num_correct = sum(preds.eq(targets.detach().cpu()))
        running_train_acc = float(num_correct) / float(images.shape[0])
        train_acc.append(running_train_acc)
        
    train_loss = torch.tensor(train_losses).mean()  
    train_accuracy = torch.tensor(train_acc).mean()   
    print(f'Epoch {epoch}/{num_epochs-1}')  
    print(f'Training loss: {train_loss:.2f}')
    print(f'Training accuracy: {train_accuracy*100:.2f} %') 
    return train_loss,train_accuracy

#Validation Function
def val_one_epoch(val_loader,model,criterion,device,thresh = 0.5):
    val_losses = list()
    val_accs = list()
    model.eval()
    step_val = 0
    with torch.no_grad():
        for (images, targets) in val_loader:
            images = images.to(device)
            targets = targets.to(device)
            logits = model(images)
            targets = targets.unsqueeze(1).float()
            loss = criterion(logits, targets)
            val_losses.append(loss.item())      

            preds = torch.Tensor(np.where(logits.detach().cpu() < thresh, 0, 1))
            num_correct = sum(preds.eq(targets.detach().cpu()))
            running_val_acc = float(num_correct) / float(images.shape[0])

            val_accs.append(running_val_acc)
      

    val_loss = torch.tensor(val_losses).mean()
    val_acc = torch.tensor(val_accs).mean() 
  
    print(f'Validation loss: {val_loss:.2f}')  
    print(f'Validation accuracy: {val_acc*100:.2f} %') 
    return val_loss,val_acc

#Plotting loss history
def plot_loss_history(train_history):
    train_history = json.load(open(train_history))
    val_loss = [a['val_loss'] for a in train_history]
    train_loss = [a['train_loss'] for a in train_history]
    train_acc = [a['train_acc'] for a in train_history]
    val_acc = [a['val_acc'] for a in train_history]
    epochs = [a['epoch'] for a in train_history]
    plt.figure(figsize = (8,6))
    plt.plot(epochs, train_loss, label = "train_loss", linestyle="--")
    plt.plot(epochs, val_loss, label = "val_loss", linestyle="--")
    plt.plot(epochs, train_acc, label = "train_acc", linestyle="--")
    plt.plot(epochs, val_acc, label = "val_acc", linestyle="--")
    plt.legend()
    plt.show()

#Engine
def engine(model,num_epochs,criterion,optim,train_dl,val_dl,device,model_save_folder = "model_checkpoints",start_epoch= 0 ,lr=None):

    loss_history=[]
    
    model = model.to(device)
    
    if not os.path.exists(model_save_folder):
        os.mkdir(model_save_folder)
    torch.save(model.state_dict(),f"{model_save_folder}/start.pth")
    
    best_loss = float('inf')    
    
    for epoch in range(num_epochs):
        loss_history_ =  {
          "epoch":start_epoch + epoch,
          "train": None,
          "val": None,
        }        
        print('Epoch {}/{}'.format(epoch + 1, num_epochs ))   

        train_loss,train_accuracy=fit_one_epoch(train_dl,model,criterion,device,optim,epoch,num_epochs)

        loss_history_["train_loss"] = train_loss.item()
        loss_history_["train_acc"] = train_accuracy.item()
        val_loss,val_accuracy = val_one_epoch(val_dl,model,criterion,device)
       
        loss_history_["val_loss"]= val_loss.item()
        loss_history_["val_acc"] = val_accuracy.item()
        if lr:
            loss_history_["lr"] = lr
        loss_history.append(loss_history_)
        if val_loss.item() < best_loss:
            best_loss = val_loss.item()
            torch.save(model.state_dict(),f'{model_save_folder}/best_model_till_epoch_no_{epoch}.pth')
            try:
                torch.save(model.state_dict(),f'GIVE THE PATH TO SAVE THE MODEL/best_model_scale.pth')
            except:
                print("failed to copy to drive")
        
        
        print("train loss: %.6f " %(train_loss.item()))
        print("val loss: %.6f " %(val_loss.item()))
        print("-"*15)
        with open(f"train_details.json","w") as fp:
            json.dump(loss_history,fp,indent=2)

    plot_loss_history("train_details.json")
    return  model, loss_history


#Load the data
df["target"] = df["updated_shows_scale"] == True
print(df["target"].value_counts())
train_idxs,val_idxs,test_idxs = get_split_indices(df,"target")
df["ds_type"] = df["target"]
df.iloc[train_idxs,-1] = "train"
df.iloc[val_idxs,-1]= "val"
df.iloc[test_idxs,-1] = "test"
#print(df["ds_type"].value_counts())

train_ds = ImageDataset(df,"target","ds_type")
val_ds = ImageDataset(df,"target","ds_type",dt_type="val")
train_dl,val_dl =  img_dataloader(train_ds,val_ds,bs_train = 32,bs_val = 32,upsampling=False)

#Load the model
device= "cuda" if torch.cuda.is_available() else "cpu"
model  = load_model(True,1,device = device)
print(device)
model = model.to(device)
model
optimizer = torch.optim.Adam(model.parameters()) 
criterion = torch.nn.BCELoss()
pass

#setup the optimizer, loss function and get the learning rate
optimizer = torch.optim.Adam(model.parameters(),lr=1e-7,weight_decay = 1e-2) 
criterion = torch.nn.BCELoss()
lr_finder = LRFinder(model, optimizer, criterion, device="cuda")
#lr_finder = LRFinder(model, optimizer, criterion)
lr_finder.range_test(train_dl, end_lr=100, num_iter=100)
#lr_finder.plot() 
lr_finder.reset()

#load the optimizer, loss function and engine function to train the model.
optimizer = torch.optim.Adam(model.parameters(),lr=1e-3,weight_decay = 1e-2) 
criterion = torch.nn.BCELoss()
engine(model,15,criterion,optimizer,val_dl,val_dl,device,model_save_folder = "model_checkpoints")
