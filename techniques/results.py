def print_results (tp, tn, fp, fn):
    accuracy = (tp+tn)/(tp+fp+tn+fn)
    
    try:
        precision = tp/(tp+fp)
    except:
        precision = 0
    
    try:
        recall = tp/(tp+fn)
    except: 
        recall = 0
    
    try:
        f1_score = 2*(recall*precision)/(recall+precision)
    except:
        f1_score = 0

    print ("tp = " + str(tp))
    print ("tn = " + str(tn))
    print ("fp = " + str(fp))
    print ("fn = " + str(fn))
    print ("accuracy = " + str(accuracy))
    print ("precision = " + str(precision))
    print ("recall = " + str(recall))
    print ("F1-score = " + str(f1_score))

    return accuracy, precision