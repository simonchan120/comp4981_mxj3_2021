from transformers import BertTokenizer
from .model import BertForMultiLabelClassification
from .multilabel_pipeline import MultiLabelPipeline
from pprint import pprint
import os

_file_path = os.path.dirname(os.path.realpath(__file__))
_models_file_path= os.path.join(_file_path,'models')
_tokenizer_path=os.path.join(_models_file_path,"tokenizer")
_classifier_model_path=os.path.join(_models_file_path,"classifier")

_tokenizer = BertTokenizer.from_pretrained(_tokenizer_path)
_classifier_model = BertForMultiLabelClassification.from_pretrained(_classifier_model_path)

_tag_file_name=os.path.join(_file_path,'data','ekman','labels.txt')
emotion_tags=[]
with open(_tag_file_name) as file:
    emotion_tags = [line.rstrip() for line in file]

goemotions = MultiLabelPipeline(
    model=_classifier_model,
    tokenizer=_tokenizer,
    threshold=0.3
)

__all__=['goemotions','emotion_tags']
