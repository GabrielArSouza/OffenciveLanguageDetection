def print_results (tp, tn, fp, fn):
    accuracy = (tp+tn)/(tp+fp+tn+fn)
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f1_score = 2*(recall*precision)/(recall+precision)

    print ("tp = " + str(tp))
    print ("tn = " + str(tn))
    print ("fp = " + str(fp))
    print ("fn = " + str(fn))
    print ("accuracy = " + str(accuracy))
    print ("precision = " + str(precision))
    print ("recall = " + str(recall))
    print ("F1-score = " + str(f1_score))