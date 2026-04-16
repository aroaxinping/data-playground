# Intro a Deep Learning

De Random Forest a redes neuronales convolucionales: usando MNIST como campo de pruebas para entender por que deep learning funciona y cuando tiene sentido usarlo.

## Por que este proyecto

Deep learning no es magia — es una extension natural del machine learning clasico. Pero para entenderlo hay que verlo en accion: por que un perceptron no basta, que cambia cuando apilamos capas, por que las convoluciones son mejores que aplanar una imagen, y como el dropout evita que el modelo memorice en vez de aprender.

Este notebook construye 4 modelos de menor a mayor complejidad sobre el mismo dataset para que la comparacion sea directa.

## Que se aprende

| Seccion | Concepto | Por que importa |
|---|---|---|
| Baseline | Random Forest sobre pixeles aplanados (784 features) | Referencia: que tan lejos llega ML clasico en vision |
| Perceptron | Neurona, activaciones (sigmoid, ReLU, softmax) | El bloque basico de toda red neuronal |
| MLP | Red 784->128->64->10 con PyTorch | Primera red neuronal: como se entrena con backpropagation |
| CNN | Conv2d + MaxPool + dense layers | Las convoluciones detectan patrones espaciales que el MLP no puede |
| Overfitting | CNN sin vs con Dropout | Como detectar y reducir el sobreajuste con regularizacion |
| Comparacion | Accuracy, parametros, tiempo de entrenamiento | Trade-offs reales: mas complejo no siempre es mejor |

## Progresion de modelos

```
Random Forest (~97%)  →  MLP (~98%)  →  CNN (~99%)  →  CNN + Dropout (~99%+)
     ML clasico          primera NN       convoluciones     regularizacion
```

## Datos

- **MNIST**: 60k imagenes de entrenamiento + 10k de test (digitos escritos a mano, 28x28 pixeles)
- **Fuente**: torchvision (descarga automatica)
- **Fallback**: Generador sintetico con patrones geometricos por digito si no hay conexion

## Uso

```bash
pip install -r requirements.txt
python src/fetch_dl_data.py
jupyter lab notebooks/01_deep_learning_intro.ipynb
```

## Stack

Python · PyTorch · scikit-learn · pandas · matplotlib · seaborn
