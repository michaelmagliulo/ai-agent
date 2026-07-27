# %%
import sys
import platform

print(sys.executable)
print(platform.system())
print(platform.platform())

# %%
import pandas as pd

df = pd.DataFrame(
    {
        "name": ["Alice", "Bob", "Carol"],
        "score": [90, 85, 95],
    }
)

df

# %%
df.describe()
# %%


def add(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    print(add(2, 3))