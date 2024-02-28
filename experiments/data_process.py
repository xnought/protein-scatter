import pandas as pd
from to3Di import to3Di
import torch

# from 5.ipynb

START_TOKEN = "["
END_TOKEN = "]"
ALPHABET_3Di = [
    "A",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "W",
    "Y",
]
assert len(ALPHABET_3Di) == 20
TOKENS = [
    *ALPHABET_3Di,
    START_TOKEN,
    END_TOKEN,
]

to_index = {letter: i for i, letter in enumerate(TOKENS)}
to_3Di = {i: letter for i, letter in enumerate(TOKENS)}


def encode(repr_3Di: str):
    return [to_index[letter] for letter in repr_3Di]


def decode(encoded: list):
    return "".join([to_3Di[i] for i in encoded])


def pdb_to_3Di_csv(dir, out_file="default.csv"):
    parsed = to3Di(dir)
    with_start_and_stop_tokens = [
        f"{START_TOKEN}{_repr}{END_TOKEN}" for _repr in parsed.repr_3Di
    ]
    pd.DataFrame({"name": parsed.names, "3Di": with_start_and_stop_tokens}).to_csv(
        out_file, index=False
    )


def get_block_xy(repr_3Di, block_size):
    protein_idx = torch.randint(len(repr_3Di), (1,)).item()
    protein_3Di = repr_3Di[protein_idx]
    block_idx = torch.randint(len(protein_3Di) - block_size, (1,)).item()
    X = protein_3Di[block_idx : block_idx + block_size]
    Y = protein_3Di[block_idx + 1 : block_idx + block_size + 1]
    return X, Y


def get_train_val_split(repr_3Di, ratio=0.9):
    split = int(ratio * len(repr_3Di))
    train = repr_3Di[:split]
    val = repr_3Di[split:]
    return train, val


def get_batch(split, batch_size=8, block_size=64):
    xs = []
    ys = []
    for b in range(batch_size):
        x, y = get_block_xy(split, block_size)
        xs.append(encode(x))
        ys.append(encode(y))
    xs = torch.tensor(xs, dtype=torch.long)
    ys = torch.tensor(ys, dtype=torch.long)
    return xs, ys
