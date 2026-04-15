"""
fetch_dl_data.py
================
Descarga el dataset MNIST via torchvision (o genera datos sinteticos).

Uso:
    python src/fetch_dl_data.py

Dataset: MNIST — 60k imagenes de digitos escritos a mano (28x28 px, escala de grises)
Si la descarga falla, el script genera un dataset sintetico para que el notebook funcione.
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROC_DIR = Path(__file__).parent.parent / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)


def download_mnist():
    """Descarga MNIST usando torchvision y guarda como .npz."""
    try:
        from torchvision import datasets
        print("[INFO] Descargando MNIST via torchvision...")

        train_ds = datasets.MNIST(root=str(RAW_DIR), train=True, download=True)
        test_ds = datasets.MNIST(root=str(RAW_DIR), train=False, download=True)

        X_train = train_ds.data.numpy()
        y_train = train_ds.targets.numpy()
        X_test = test_ds.data.numpy()
        y_test = test_ds.targets.numpy()

        out_path = PROC_DIR / "mnist.npz"
        np.savez_compressed(
            out_path,
            X_train=X_train, y_train=y_train,
            X_test=X_test, y_test=y_test,
        )
        print(f"[OK] MNIST guardado: {out_path}")
        print(f"     Train: {X_train.shape} | Test: {X_test.shape}")
        return X_train, y_train, X_test, y_test

    except Exception as e:
        print(f"[ERROR] No se pudo descargar MNIST: {e}")
        return None


def generate_synthetic_mnist(n_train=10000, n_test=2000, seed=42):
    """
    Genera datos sinteticos que imitan MNIST: imagenes 28x28 con patrones
    simples por digito (circulos, lineas, etc.) para que el notebook funcione.
    """
    rng = np.random.default_rng(seed)
    print(f"[INFO] Generando dataset sintetico ({n_train} train, {n_test} test)...")

    def make_digit_image(digit, rng):
        """Genera una imagen 28x28 con un patron simple para cada digito."""
        img = np.zeros((28, 28), dtype=np.uint8)
        noise = rng.integers(0, 30, size=(28, 28), dtype=np.uint8)

        if digit == 0:  # circulo
            for i in range(28):
                for j in range(28):
                    dist = np.sqrt((i - 14)**2 + (j - 14)**2)
                    if 7 < dist < 11:
                        img[i, j] = rng.integers(180, 255)
        elif digit == 1:  # linea vertical
            col = rng.integers(12, 16)
            img[4:24, col-1:col+2] = rng.integers(180, 255, size=(20, 3))
        elif digit == 2:  # forma de 2 simplificada
            img[5:8, 8:20] = rng.integers(160, 240)
            img[8:14, 16:20] = rng.integers(160, 240)
            img[13:16, 8:20] = rng.integers(160, 240)
            img[15:22, 8:12] = rng.integers(160, 240)
            img[21:24, 8:20] = rng.integers(160, 240)
        elif digit == 3:  # forma de 3
            img[5:8, 8:20] = rng.integers(160, 240)
            img[12:15, 8:20] = rng.integers(160, 240)
            img[21:24, 8:20] = rng.integers(160, 240)
            img[5:24, 16:20] = rng.integers(160, 240)
        elif digit == 4:  # forma de 4
            img[5:15, 8:12] = rng.integers(160, 240)
            img[12:15, 8:20] = rng.integers(160, 240)
            img[5:24, 16:20] = rng.integers(160, 240)
        elif digit == 5:  # forma de 5
            img[5:8, 8:20] = rng.integers(160, 240)
            img[8:14, 8:12] = rng.integers(160, 240)
            img[13:16, 8:20] = rng.integers(160, 240)
            img[15:22, 16:20] = rng.integers(160, 240)
            img[21:24, 8:20] = rng.integers(160, 240)
        elif digit == 6:  # forma de 6
            img[5:8, 8:20] = rng.integers(160, 240)
            img[5:24, 8:12] = rng.integers(160, 240)
            img[13:16, 8:20] = rng.integers(160, 240)
            img[15:24, 16:20] = rng.integers(160, 240)
            img[21:24, 8:20] = rng.integers(160, 240)
        elif digit == 7:  # forma de 7
            img[5:8, 8:20] = rng.integers(160, 240)
            img[5:24, 16:20] = rng.integers(160, 240)
        elif digit == 8:  # forma de 8
            img[5:8, 8:20] = rng.integers(160, 240)
            img[12:15, 8:20] = rng.integers(160, 240)
            img[21:24, 8:20] = rng.integers(160, 240)
            img[5:24, 8:12] = rng.integers(160, 240)
            img[5:24, 16:20] = rng.integers(160, 240)
        elif digit == 9:  # forma de 9
            img[5:8, 8:20] = rng.integers(160, 240)
            img[5:15, 8:12] = rng.integers(160, 240)
            img[12:15, 8:20] = rng.integers(160, 240)
            img[5:24, 16:20] = rng.integers(160, 240)

        # Aplicar un poco de blur manual + ruido
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        # Desplazamiento aleatorio pequeno
        dx, dy = rng.integers(-2, 3, size=2)
        img = np.roll(np.roll(img, dx, axis=0), dy, axis=1)
        return img

    def make_dataset(n, rng):
        labels = rng.integers(0, 10, size=n)
        images = np.stack([make_digit_image(d, rng) for d in labels])
        return images, labels

    X_train, y_train = make_dataset(n_train, rng)
    X_test, y_test = make_dataset(n_test, rng)

    out_path = PROC_DIR / "mnist.npz"
    np.savez_compressed(
        out_path,
        X_train=X_train, y_train=y_train,
        X_test=X_test, y_test=y_test,
    )
    print(f"[OK] Dataset sintetico guardado: {out_path}")
    print(f"     Train: {X_train.shape} | Test: {X_test.shape}")
    return X_train, y_train, X_test, y_test


def load_or_generate():
    """Intenta cargar MNIST procesado, si no descarga, si no genera sintetico."""
    npz_path = PROC_DIR / "mnist.npz"

    if npz_path.exists():
        print(f"[OK] Cargando dataset: {npz_path}")
        data = np.load(npz_path)
        return data["X_train"], data["y_train"], data["X_test"], data["y_test"]

    # Intentar descarga
    result = download_mnist()
    if result is not None:
        return result

    # Fallback: sintetico
    print("[INFO] Generando dataset sintetico como fallback...")
    return generate_synthetic_mnist()


if __name__ == "__main__":
    X_train, y_train, X_test, y_test = load_or_generate()
    print(f"\nResumen:")
    print(f"  Train: {X_train.shape}, labels: {np.unique(y_train)}")
    print(f"  Test:  {X_test.shape}, labels: {np.unique(y_test)}")
    print(f"\nDistribucion de clases (train):")
    for d in range(10):
        count = (y_train == d).sum()
        bar = "#" * (count // 100)
        print(f"  {d}: {count:5d}  {bar}")
