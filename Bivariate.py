import pandas as pd

class Bivariate():
    def QuanQual(dataset):
        quan = []
        qual = []
        for columnName in dataset.columns:
            if(dataset[columnName].dtypes == 'O'):
                qual.append(columnName)
            else:
                quan.append(columnName)
            converted = pd.to_numeric(dataset[columnName],errors="coerce")

        return quan,qual
    def descriptiveTable(dataset,quan):
        
        descriptive = pd.DataFrame(index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","Q4:100%","IQR","1.5rule","Lesser","Greater","Min","Max","Skewness","Kurtosis","Var","Std"],columns=quan)
        for columnName in quan:
            descriptive[columnName]["Mean"] = dataset[columnName].mean().item()
            descriptive[columnName]["Median"] = dataset[columnName].median().item()
            descriptive[columnName]["Mode"] = dataset[columnName].mode()[0]
            descriptive[columnName]["Q1:25%"] = dataset.describe()[columnName]["25%"].item() 
            descriptive[columnName]["Q2:50%"] = dataset.describe()[columnName]["50%"].item() 
            descriptive[columnName]["Q3:75%"] = dataset.describe()[columnName]["75%"].item() 
            descriptive[columnName]["Q4:100%"] =dataset.describe()[columnName]["max"].item()
            descriptive[columnName]["IQR"] = descriptive[columnName]["Q3:75%"] - descriptive[columnName]["Q1:25%"]
            descriptive[columnName]["1.5rule"] =1.5 * descriptive[columnName]["IQR"]
            descriptive[columnName]["Lesser"] =descriptive[columnName]["Q1:25%"] - descriptive[columnName]["1.5rule"]
            descriptive[columnName]["Greater"] =descriptive[columnName]["Q3:75%"] + descriptive[columnName]["1.5rule"]
            descriptive[columnName]["Min"] = dataset[columnName].min()
            descriptive[columnName]["Max"] = dataset[columnName].max()
            descriptive[columnName]["Skewness"] = dataset[columnName].skew()
            descriptive[columnName]["Kurtosis"] = dataset[columnName].kurtosis()
            descriptive[columnName]["Var"] = dataset[columnName].var()
            descriptive[columnName]["Std"] = dataset[columnName].std()
        return descriptive
    def checkOutliers(quan,descriptive):
            Lesser = []
            Greater = []
            for columnName in quan:
                if(descriptive[columnName]["Lesser"]>descriptive[columnName]["Min"]):
                    Lesser.append(columnName)
                if(descriptive[columnName]["Greater"]<descriptive[columnName]["Max"]):
                    Greater.append(columnName)
            print(Lesser)
            print(Greater)
            return Lesser,Greater
    
    def replaceOutliers(dataset,descriptive,Lesser,Greater):
        for columnName in Lesser:
            dataset[columnName][dataset[columnName]<descriptive[columnName]["Lesser"]] = descriptive[columnName]["Lesser"]
        for columnName in Greater:
            dataset[columnName][dataset[columnName]>descriptive[columnName]["Greater"]] = descriptive[columnName]["Greater"]
        return dataset
    
    def stdNBgraph(dataset):
        import seaborn as sns
        mean = dataset.mean()
        std = dataset.std()
        #converting dataset to list
        values  = [value for value in dataset]
        #finding z_score value by applying in x-mean/std
        z_score = [((j-mean)/std) for j in values]
        #distributed plot derived using z_score
        sns.distplot(z_score,kde=True)

    def get_pdf_Probability(dataset,startRange,endrange):
        import seaborn as sns
        from matplotlib import pyplot
        from scipy.stats import norm
        ax= sns.distplot(dataset,kde=True,kde_kws={'color':'blue'},color='Green')
        pyplot.axvline(startRange,color='Red')
        pyplot.axvline(endrange,color='Red')
        #generate a sample
        sample = dataset
        #calculate parameter
        sample_mean = sample.mean()
        sample_std = sample.std()
        print("Mean=%.3f,Standard Deaviation=%.3f" % (sample_mean,sample_std))
        dist = norm(sample_mean,sample_std)

        values = [value for value in range(startRange,endrange)]
        probabilities = [dist.pdf(value) for value in values]
        prob = sum(probabilities)
        print("The area between range ({},{}):{}".format(startRange,endrange,prob))
        return prob