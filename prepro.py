def preprocessing(df,method_remove="mean_std",norm_std="norm"):
    X_num = df.select_dtypes("number")
    if method_remove == "mean_std":
        min_val = X_num.mean() - 3*X_num.std()
        max_val = X_num.mean() + 3*X_num.std()
        df = df[~((X_num > max_val)|(X_num < min_val)).any(axis=1)]
    elif method_remove == "iqr":
        q1 = X_num.quantile(0.25)
        q3 = X_num.quantile(0.75)
        iqr = q3-q1
        min_ = q1-1.5*iqr
        max_ = q3+1.5*iqr
        df = df[~((X_num > max_)|(X_num < min_)).any(axis=1)]
    elif method_remove == "z_score":
        import numpy as np
        import scipy.stats as sts
        z = np.abs(sts.zscore(X_num))
        df = df[~(X_num < z).all(axis=1)]

    ## normalization/std
    if norm_std == "norm":
        df = (df-df.min())/(df.max()-df.min())
    elif norm_std == "std":
        df = (df-df.mean())/(df.std())
    
    import plotly.express as px
    featured = df.select_dtypes("number").columns.tolist()
    fig = px.box(df,y=featured)    
    
    return df,fig

