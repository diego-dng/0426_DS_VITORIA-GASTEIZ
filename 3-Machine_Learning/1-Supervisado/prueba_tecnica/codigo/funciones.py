from sklearn import metrics

def metricas(modelo, v_real, pred):
    print("----- METRICAS MODELO ------")
    print("Intercepto: ", modelo.intercept_)
    print("Lista coeficientes: ", modelo.coef_)
    
    print("----- METRICAS EVALUACIÓN------")
    
    print("MAE: ", metrics.mean_absolute_error(v_real, pred))
    print("MAPE: ", metrics.mean_absolute_percentage_error(v_real, pred))
    print("MSE: ", metrics.mean_squared_error(v_real, pred))
    print("RMSE: ", metrics.root_mean_squared_error(v_real, pred))