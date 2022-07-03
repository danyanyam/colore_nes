import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def show(path_to_img: str) -> None:
    plt.imshow(mpimg.imread(path_to_img))
