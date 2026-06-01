import pandas as pd
import seaborn as sns

df = pd.read_csv("../data/coches-de-segunda-mano-sample.csv")

df = df.drop(columns= ["url", "company", "publish_date", "insert_date", "province", "country", "dealer", "price_financed"])

df.dropna(inplace= True)

df.to_csv("../data/coches_proc.csv", index= False)