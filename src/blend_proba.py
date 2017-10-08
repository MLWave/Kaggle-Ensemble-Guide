from sklearn import cross_validation
from sklearn.metrics import log_loss, accuracy_score
import numpy as np
import pandas as pd
import random
import md5
import json

def blend_proba(clf, X_train, y, X_test, nfolds=5, save_preds="",
                save_test_only="", seed=300373, save_params="",
                clf_name="XX", generalizers_params=[], minimal_loss=0,
                return_score=False, minimizer="log_loss"):
  print("\nBlending with classifier:\n\t%s"%(clf))
  folds = list(cross_validation.StratifiedKFold(y, nfolds,shuffle=True,random_state=seed))
  print(X_train.shape)
  dataset_blend_train = np.zeros((X_train.shape[0],np.unique(y).shape[0]))

  #iterate through train set and train - predict folds
  loss = 0
  for i, (train_index, test_index) in enumerate( folds ):
    print("Train Fold %s/%s"%(i+1,nfolds))
    fold_X_train = X_train[train_index]
    fold_y_train = y[train_index]
    fold_X_test = X_train[test_index]
    fold_y_test = y[test_index]
    clf.fit(fold_X_train, fold_y_train)

    fold_preds = clf.predict_proba(fold_X_test)
    print("Logistic loss: %s"%log_loss(fold_y_test,fold_preds))
    dataset_blend_train[test_index] = fold_preds
    if minimizer == "log_loss":
      loss += log_loss(fold_y_test,fold_preds)
    if minimizer == "accuracy":
      fold_preds_a = np.argmax(fold_preds, axis=1)
      loss += accuracy_score(fold_y_test,fold_preds_a)
    #fold_preds = clf.predict(fold_X_test)

    #loss += accuracy_score(fold_y_test,fold_preds)

    if minimal_loss > 0 and loss > minimal_loss and i == 0:
      return False, False
    fold_preds = np.argmax(fold_preds, axis=1)
    print("Accuracy:      %s"%accuracy_score(fold_y_test,fold_preds))
  avg_loss = loss / float(i+1)
  print("\nAverage:\t%s\n"%avg_loss)
  #predict test set (better to take average on all folds, but this is quicker)
  print("Test Fold 1/1")
  clf.fit(X_train, y)
  dataset_blend_test = clf.predict_proba(X_test)

  if clf_name == "XX":
    clf_name = str(clf)[1:3]

  if len(save_preds)>0:
    id = md5.new("%s"%str(clf.get_params())).hexdigest()
    print("storing meta predictions at: %s"%save_preds)
    np.save("%s%s_%s_%s_train.npy"%(save_preds,clf_name,avg_loss,id),dataset_blend_train)
    np.save("%s%s_%s_%s_test.npy"%(save_preds,clf_name,avg_loss,id),dataset_blend_test)

  if len(save_test_only)>0:
    id = md5.new("%s"%str(clf.get_params())).hexdigest()
    print("storing meta predictions at: %s"%save_test_only)

    dataset_blend_test = clf.predict(X_test)
    np.savetxt("%s%s_%s_%s_test.txt"%(save_test_only,clf_name,avg_loss,id),dataset_blend_test)
    d = {}
    d["stacker"] = clf.get_params()
    d["generalizers"] = generalizers_params
    with open("%s%s_%s_%s_params.json"%(save_test_only,clf_name,avg_loss, id), 'wb') as f:
      json.dump(d, f)

  if len(save_params)>0:
    id = md5.new("%s"%str(clf.get_params())).hexdigest()
    d = {}
    d["name"] = clf_name
    d["params"] = { k:(v.get_params() if "\n" in str(v) or "<" in str(v) else v) for k,v in clf.get_params().items()}
    d["generalizers"] = generalizers_params
    with open("%s%s_%s_%s_params.json"%(save_params,clf_name,avg_loss, id), 'wb') as f:
      json.dump(d, f)

  if np.unique(y).shape[0] == 2: # when binary classification only return positive class proba
    if return_score:
      return dataset_blend_train[:,1], dataset_blend_test[:,1], avg_loss
    else:
      return dataset_blend_train[:,1], dataset_blend_test[:,1]
  else:
    if return_score:
      return dataset_blend_train, dataset_blend_test, avg_loss
    else:
      return dataset_blend_train, dataset_blend_test