# Data Efficient Masked Language Modeling for Vision and Language
Repository for the paper "Data Efficient Masked Language Modeling for Vision and Language".

![](fig1.png)
The baseline MLM masks a random token with 15\% probability (where ~50\% of the masked tokens are stop-words or punctuation). Our method masks words that require the image in order to be predicted (e.g., physical objects).
Our experiments show that our pretrain masking strategy consistently improves over the baseline strategy in two evaluation setups. 

## Intro

The code for pretraining is based on the great LXMERT repository: https://github.com/airsplay/lxmert  

This repository includes:    

### Data:  

The `data_directory` is available here: https://drive.google.com/drive/folders/1smFCIwNbIm4QhNHf4gn5RKRfcvGh4_Vl?usp=sharing

- Pretrained models and fine-tuned models are available here: `data_directory/models`.  

- Sets of annotated Objects, Attributes, Relationships from GQA and Visual Genome `data_directory/all_objects_attributes_relationships.pickle`.  

- Aggregated data, where we extracted _Δ Validation loss_ (loss without the image, minus the loss with the image) for LXMERT validation set. This is used to define the necessity of the image for a masked word prediction during MLM. Available in `data_directory/aggregated_data_detla_val_loss.csv`.    
The structure of the csv is as follows: ![](fig_delta_validation_loss.png)  
-  We can see the sentence, the image, and the masked token (motorcycle).  
- `ind_loss_with_img` is the loss with the image, `ind_loss_false_img` is the loss without the image, and `loss_gap` is the _Δ Validation loss_.  
- Similar for `conf_gap_of_label_with_img`, `conf_gap_of_label_false_img`, and 'conf_gap' - it is the confidence of the model (logits at location of the masked word).  
- `top_5_preds_token_with_img`, `top_5_preds_token_false_img` - predictions of the model, with and without the image.  
- `tagged_pos` - there is also the spacy pos tag for the sentence.
- `label_in_top_5_with_img`, `label_in_top_5_false_img` - A boolean value for whether the label is among the top 5 predictions. In this example, without the image, the label is not among the top 5 predictions, but with the image, it is.      


### Code:  
- Code for the alternative masking strategies, available in `src/alternative_masking_strategies.py`
  
- Semantic classes information, including functions to detect _Objects_, _Attributes_, and _Relationships_, available in `src/semantic_types_information.py`   
