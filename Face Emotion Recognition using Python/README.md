# Face Emotion Recognition using Python

[Original Paper](./JiangZhengLi_FaceRecognition.pdf) | [Presentation Video](./Option1_JiangZhengLi.mp4)

#### Team members (In order of last name):

- **Lanqi Li**

- **Lingyan Jiang**
- **Zhenghang Yin**

## Introduction

The presidential and vice-presidential debates are very interesting. The presidential candidates quickly turned into emotional arguments that we could clearly see on their faces. However, even for humans, identifying facial expressions is difficult. Therefore, we were trying to find and tune a model to predict presidential emotions.

Facial expressions are one of the most powerful ways for depicting specific patterns in human behavior and describing the human emotional states. Facial expression recognition has been a dynamic topic in computer vision in recent years. It will be interesting for us to use FER to quantify each candidate’s emotions. The machine learning model will be trained to classify the emotion shown on an image of a face. Thus, the computer program will tell us which kind of emotion on the face through images, like positive or negative.

However, it is difficult to identify facial expressions and the facial expressions recognition system often suffers from variations in expressions among individuals. The state-of-the-art methods in image-related tasks such as image classification and object detection are all based on Convolutional Neural Networks (CNNs)\[2]. These tasks require CNN architectures with millions of parameters. The best way to analyze what emotions each candidate wore on their face is to look at the distributions of detected expressions throughout videos. To do that, we first need to construct a dataset of images from the debate videos, process them with the expression recognition model, and then aggregate and visualize the results.

In this project, we installed FER through pip and used the `MTCNN` network to do facial recognition. For each full debate video, we sampled roughly one from every twenty frames resulting in a few thousand images per person. We then cropped the video frame to contain only the face, which allowed the expression recognition software to perform better. The expression recognition model was then run on every image in the dataset and the top emotion detected in each image was tallied.

In this work, our main objective was to understand better and improve the performance of emotion recognition models in the process. We also took some approaches from recent publications, including transfer learning and ensembling, to enhance our model’s accuracy. At the same time, we did not use any auxiliary data for my model other than the Dataset to train my models.

## Technology Methods

In the project, we used the FER package utility to perform the task of facial expression recognition. The package was available at PYPI\[8], and could be installed via `pip install FER`. In the remaining of the section, we will discuss the structures of FER, the details of models used inside FER and how the FER package can be applied to the project.

### Package structure

FER is a powerful and out-of-the-box tool which can be used to analyze and capture faces in images and videos, while predicting the gender and emotion of each face. Basically it provides two interfaces: **FER** (to process single-frame images) and **Video** (to process multiple-frame videos).

*   **FER** is the core part of the tool. It uses TensorFlow\[9] as the main deep learning framework for prediction and uses a two-stage model prediction procedure: in the first stage, the model will try to find all rectangles in the image where exists a face, and in the second stage, another model will try to recognize the emotion of the face in above rectangles.
    In two stages, FER allows users to choose different pre-trained models. In the first stage, user can choose to use the default model or , which will be introduced briefly in the next subsection. In the second stage, it will use the model in to detect emotions.
    When using FER, it’s needed to call `FER.detect_emotions` function. The function will first preprocess the image, and then call `FER.find_faces` function to return a list of rectangle data representing the faces detected in the image. Next, it will crop the corresponding faces into small picture clips and passing them to the second model to predict the emotions.
    In FER, there are 7 builtin emotion labels: (**0**: “angry", **1**: “disgust", **2**: “fear", **3**: “happy", **4**: “sad", **5**: “surprise", **6**: “neutral"). They’re overlapping with the labels defined in the task, so they can be used directly.

*   **Video** is an encapsulation of the interface FER. In general, it first divides the video into multiple frames at a certain frequency, and then calls `FER.detect_emotions` for each frame. Then for each frame, video will draw rectangles on the video, and recompresses frames into a new video.

### Application

In this project, We exploited the FER package to do face emotion recognition in the presidential campaign videos. First the videos were passing into the **Video** class to analyze emotions one by one. Then, in each video, We selected the label with the highest probability for each frame as the predicted results. Each video was divided into equal parts according to a fixed interval (every 1000 frames, with time interval equals to $\frac{1000}{\mathrm{fps}}$). Finally, We counted and chose the label with the maximum sum for each video.

The pseduo-code of the project is similar to the following:

<img src="./assets/algorithm.svg" alt="pseduo-code algorithm" style="zoom:150%;" />

Here are some of the emotional analysis we made using this model.

![Emotional Test 1](./assets/test_1.gif)

![Emotional Test 2](./assets/test_2.gif)

# Experiments and Results

In this section, we will introduce how we run the code, how to process the data results, and the final prediction results.

## Experiments Steps

Considering the programs part that relies heavily on GPU can having problems of long-time running, we divided the task into two stages:

1.  The first step was to take screenshots of each video file at a fixed frame rate, and use a pre-trained model to detect face rectangles and recognize emotions. This step required the use of GPU and was quite time-consuming. During the step, we three team members used the deep learning platform on BU SCC, trained 2019 (1,320 videos) and 2020 (1,506 videos) datasets for up to 24 hours.
    Two face detection algorithms are used in FER: the method in (marked **MTCNN=False**) or (marked **MTCNN=True**). We ran all data sets separately in two methods, by specifying python command `detector = FER(MTCNN=True or False)`.
    The following was a partial sample of the raw data generated by FER. The content within each braces indicated a frame. Then within a frame, there was multiple fields, `box` means the rectangle data about the faces, and the other fields `angry`, `happy`, etc. were scores of different emotions. For each faces, because the facial recognition models used in FER did softmax computation in the last step, the total score of all emotions is 1.0.

    ```纯文本
    [
        {
            "box0": [430, 110, 84, 84],
            "angry0":0.43, "disgust0":0.0,
            "fear0":0.07, "happy0":0.02,
            "sad0":0.31, "surprise0":0.01,
            "neutral0": 0.17
        },
        {
            "box0": [429, 109, 85, 85],
            "angry0":0.53, "disgust0":0.0,
            "fear0":0.07, "happy0":0.01,
            "sad0":0.28, "surprise0":0.01,
            "neutral0": 0.1
        },
        ...
    ]
    ```

    Because both models were pretrained to find multiple faces in one frame. In this project, we simply discarded the extra faces except the default box$_0$ face.

2.  The second step was to analyze intermediate raw data files, produce prediction results, and then compared them with golden labels.
    Because the difference between our project and the pretrained model: there were 7 labels in the model, but only 3 labels in our project. So we did the following mapping:

    | ​**labels in pretrained model** |               | ​**our project** |
    | ------------------------------- | ------------- | ---------------- |
    | happy                           | $\rightarrow$ | Positive         |
    | surprise                        | $\rightarrow$ | Positive         |
    | neutral                         | $\rightarrow$ | Neutral          |
    | fear                            | $\rightarrow$ | Neutral          |
    | sad                             | $\rightarrow$ | Neutral          |
    | disgust                         | $\rightarrow$ | Negative         |
    | angry                           | $\rightarrow$ | Negative         |

In order to balance the Positive, Neutral, and Negative 3 class labels, we sorted the results of FER and then converted them into new class labels.

## Results

The results of the project are as the following:

| Datasets | Counts | Use MTCNN? | accuracy |
| -------- | ------ | ---------- | -------- |
| 2019     | 1320   | √          | 60.05%   |
|          |        |            | 53.94%   |
| 2020     | 1506   | √          | 55.35%   |
|          |        |            | 57.75%   |

The result is in the following format:

| filename | predict | golden | pos | neg | neut |
| :-: | :-: | :-: | :-: | :-: | :-: |
| biden_58_0  | Neut | Neg | 77 | 67 | 187 |
| biden_124_0 | Neut | Neut | 13 | 5 | 42 |
| biden_138_0 | Neut | Neut | 0 | 0 | 4 |
| biden_139_2 | Neut | Neut | 0 | 3 | 120 |
| biden_143_0 | Neut | Neg | 23 | 42 | 139 |
| biden_143_2 | Neut | Neut | 14 | 88 | 179 |
| biden_274_0 | Pos | Neg | 31 | 0 | 25 |
| biden_308_0 | Pos | Neg | 55 | 1 | 20 |
| biden_411_0 | Neut | Neg | 0 | 0 | 112 |
|  |  | ... |  |  |  |

# Discussion

First, the results of this task have been described above. We can see that the results for two different data sets: the 2019 and 2020 presidential candidate data sets are not very satisfactory. In this paragraph, we focus on discussing its causes and our thinking.

## Algorithm Bias

The FER (MTCNN=False or True) algorithm we found has a certain emotion recognition bias when its pretrain and labels are selected. In the Fer algorithm, it divides people’s facial emotions into seven categories: angry, disgust, fear, happy, sad, surprise, and neutral.

Besides, we matched the given labels in the later stage. we mapped into three categories of emotions: Positive, Neutral, and Negative. As you can see in Fer’s algorithm, there are more than half of the negative emotions in the labels. If it is a simple classification or detection of different emotions without any label constraints, there is surely no problem. But when only three types of emotions are needed, it is obvious that negative emotions account for the vast majority. This has brought the deviation and bias of the algorithm, which is one of the reasons why our team believes that the accuracy rate is kind of low.

## Model Difference

In the process of our training model, our group unexpectedly found that for the 2019 data set, we use the `FER(MTCNN=True)` algorithm to achieve higher accuracy. For the 2020 data set, we use the `FER(MTCNN=False)` algorithm for better results.

When we observed the original raw data, we found that many faces of the 2019 mp4 data were very clear in the video, and many of them were directly shot videos instead of secondary videos selected from the news. But in 2020 mp4 data, many secondary videos selected from the news have relatively small faces. And some of them were videos of profile faces. It can be inferred that when the face recognition degree is higher and the video face is clearer, the effect of using `FER(MTCNN=True)` will be better. When the face situation in the video is in the opposite situation, the effect of using `FER(MTCNN=False)` will be better.

# References

\[1] [https://www.bu.edu/tech/support/research/computing-resources/scc](https://www.bu.edu/tech/support/research/computing-resources/scc/ "https://www.bu.edu/tech/support/research/computing-resources/scc")

\[2] [https://en.wikipedia.org/wiki/Convolutional\_neural\_network](https://en.wikipedia.org/wiki/Convolutional_neural_network "https://en.wikipedia.org/wiki/Convolutional_neural_network")

\[3] [https://en.wikipedia.org/wiki/Recurrent\_neural\_network](https://en.wikipedia.org/wiki/Recurrent_neural_network "https://en.wikipedia.org/wiki/Recurrent_neural_network")

\[4] [https://en.wikipedia.org/wiki/Facial\_Action\_Coding\_System](https://en.wikipedia.org/wiki/Facial_Action_Coding_System "https://en.wikipedia.org/wiki/Facial_Action_Coding_System")

\[5] [https://github.com/microsoft/FERPlus](https://github.com/microsoft/FERPlus "https://github.com/microsoft/FERPlus")

\[6] [https://en.wikipedia.org/wiki/AlexNet](https://en.wikipedia.org/wiki/AlexNet "https://en.wikipedia.org/wiki/AlexNet")

\[7] [https://github.com/rcmalli/keras-vggface](https://github.com/rcmalli/keras-vggface "https://github.com/rcmalli/keras-vggface")

\[8] [https://github.com/justinshenk/fer](https://github.com/justinshenk/fer "https://github.com/justinshenk/fer")

\[9] [https://pypi.org/project/tensorflow/](https://pypi.org/project/tensorflow/ "https://pypi.org/project/tensorflow/")
