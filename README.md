# Automating Image Classification with Microsoft Azure Custom Vision Training and Prediction
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fatrox%2Fsync-dotenv%2Fbadge&style=flat)](https://github.com/marketplace/actions/automating-image-classification-with-microsoft-azure-custom-vision-training-and-prediction)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

This GitHub Action automates the entire process of
image classification with Microsoft Azure Custom Vision Service.

## How to use

### Step 1:

To use the Custom Vision Service you will need to create Custom Vision Training and Prediction resources in Azure. To do so in the Azure portal, fill out the dialog window on the [Create Custom Vision](https://customvision.ai/) page to create both a Training and Prediction resource.

### Step 2:

Get the **Endpoint, Training Key, Prediction Key and Prediction Resource ID** credentials andd save it as [Secrets](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets#creating-encrypted-secrets) in your GitHub repository settings. You can find the items at the [Custom Vision website](https://customvision.ai/) . Sign in with the account associated with the Azure account you used to create your Custom Vision resources. On the home page (the page with the option to add a new project), select the gear icon in the upper right.

![Image of above credentials](https://docs.microsoft.com/en-us/azure/cognitive-services/Custom-Vision-Service/media/csharp-tutorial/training-prediction-keys.png)

Save the above credentials with SECRET_NAME as: `AZURE_ENDPOINT`, `AZURE_TRAINING_KEY`, `AZURE_PREDICTION_KEY`, `AZURE_PREDICTION_RESOURCE_ID` respectively.

### Step 3:

Upload the image dataset and Test File in the Repository. Afte pushing the changes, Copy the below workflow file and push it:

```yaml
name: Auto Custom Vision Classifier
on:
  push:
    paths:
    - '**.yml'
jobs:
  build_model:
    runs-on: ubuntu-latest
    steps:
    - name: Automating Image Classification with Microsoft Azure Custom Vision Training and Prediction
      uses: mritunjaysharma394/autoCustomVision@v1.0
      with:
        tags: "[Hemlock,Japanese Cherry]" # Rename it according to the folder name under images/ which will also be our name to the tags
        tagsVar: "[hemlock_,japanese_cherry_]" # Rename it according to the symmetry of file names under images/tag/ 
        trainSize: "10" # Train Size of Each Tag
        endpoint: ${{ secrets.AZURE_ENDPOINT }}
        trainingKey: ${{ secrets.AZURE_TRAINING_KEY }}
        predictionKey: ${{ secrets.AZURE_PREDICTION_KEY }}
        predictionResourceid: ${{ secrets.AZURE_PREDICTION_RESOURCE_ID }}
```
