config = {
  "dataset_reader": {
    "class_name": "faq_reader",
    "x_col_name": "Question",
    "y_col_name": "Answer",
    "data_path": "data_csv4.csv"
  },
  "dataset_iterator": {
    "class_name": "data_learning_iterator"
  },
  "chainer": {
    "in": "q",
    "in_y": "y",
    "pipe": [
      {
        "class_name": "stream_spacy_tokenizer",
        "in": "q",
        "id": "my_tokenizer",
        "lemmas": True,
        "out": "q_token_lemmas"
      },
      {
        "ref": "my_tokenizer",
        "in": "q_token_lemmas",
        "out": "q_lem"
      },
      {
        "in": [
          "q_lem"
        ],
        "out": [
          "q_vect"
        ],
        "fit_on": [
          "q_lem"
        ],
        "id": "tfidf_vec",
        "class_name": "sklearn_component",
        "save_path": "{MODELS_PATH}/faq/mipt/my_model/tfidf.pkl",
        "load_path": "{MODELS_PATH}/faq/mipt/my_model/tfidf.pkl",
        "model_class": "sklearn.feature_extraction.text:TfidfVectorizer",
        "infer_method": "transform"
      },
      {
        "id": "answers_vocab",
        "class_name": "simple_vocab",
        "fit_on": [
          "y"
        ],
        "save_path": "{MODELS_PATH}/faq/mipt/my_model/en_mipt_answers.dict",
        "load_path": "{MODELS_PATH}/faq/mipt/my_model/en_mipt_answers.dict",
        "in": "y",
        "out": "y_ids"
      },
      {
        "in": "q_vect",
        "fit_on": [
          "q_vect",
          "y_ids"
        ],
        "out": [
          "y_pred_proba"
        ],
        "class_name": "sklearn_component",
        "main": True,
        "save_path": "{MODELS_PATH}/faq/mipt/my_model/logreg.pkl",
        "load_path": "{MODELS_PATH}/faq/mipt/my_model/logreg.pkl",
        "model_class": "sklearn.linear_model:LogisticRegression",
        "infer_method": "predict_proba",
        "C": 1000,
        "penalty": "l2"
      },
      {
        "in": "y_pred_proba",
        "out": "y_pred_ids",
        "class_name": "proba2labels",
        "max_proba": True,
        "confident_threshold": 0.8
      },
      {
        "in": "y_pred_ids",
        "out": "y_pred_answers",
        "ref": "answers_vocab"
      }
    ],
    "out": [
      "y_pred_answers",
      "y_pred_proba",
      "y_pred_ids"
    ]
  },
  "train": {
    "evaluation_targets": [],
    "class_name": "fit_trainer"
  },
  "metadata": {
    "variables": {
      "ROOT_PATH": "./deep",
      "DOWNLOADS_PATH": "{ROOT_PATH}/downloads",
      "MODELS_PATH": "{ROOT_PATH}/models"
    },
    "requirements": [
      "{DEEPPAVLOV_PATH}/requirements/spacy.txt",
      "{DEEPPAVLOV_PATH}/requirements/en_core_web_sm.txt"
    ],
    "download": [
      {
        "url": "http://files.deeppavlov.ai/faq/mipt/en_mipt_faq_v4.tar.gz",
        "subdir": "{MODELS_PATH}/faq/mipt"
      }
    ]
  }
}
