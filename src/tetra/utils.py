import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
import numpy as np
from IPython.display import HTML

def create_animation(rgb_images, figsize = (3, 6), fps=10):
    fig, ax = plt.subplots(figsize=figsize)
    plt.close()  # Don't show

    im = ax.imshow(rgb_images[0])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(color='white', linewidth=0.5, alpha=0.5)

    def update(frame):
        im.set_array(rgb_images[frame])
        return [im]

    anim = FuncAnimation(fig, update, frames=len(rgb_images), interval=1000//fps, blit=True)
    html = anim.to_html5_video()    

    return HTML(html)