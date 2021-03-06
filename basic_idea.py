import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation, rc






def func(x):
    return 3 * x ** 3 - 5 * x ** 2

def func_der(x):
    return 9 * x ** 2 - 10 * x



x = np.linspace(0,2,200)
y = func(x)
xprime = np.linspace(1.1,1.9)
yprime = (xprime - 1.5) * func_der(1.5)  + func(1.5)
plt.text(0.5, 2, "$y=3x^3-5x^2$", fontsize=20)
plt.text(0.5,1, "$y_{line}=5.25x-9$", fontsize=16)
plt.axvline(1.5, color='k', linestyle='--',linewidth=1)
plt.plot(x,y, xprime, yprime, 'r--', [1.5], [func(1.5)], 'ro')
plt.show()







#Initial plot to setup the animation
fig, ax = plt.subplots()
ax.set_xlim(( 0, 2))
ax.set_ylim((-4, 4))
_,_,_, point, line = ax.plot(x,y, xprime, yprime, 'r--', [1.5], [func(1.5)], 'ro', [],[], 'ko', [], [], 'k-')
text = ax.text(0.5, 1, "")
ax.text(0.5, 0.65, "derivative 5.25", color="r")



def init():
    line.set_data([], [])
    point.set_data([], [])
    text.set_text("")
    return (point, line, text)
def animate(i):
    if (i < 45):
        pt = 1.495 - 0.495 * (60 - i) / 60
    elif (i < 75):
        pt = 1.495 - 0.495 * (16.25 - (i-45)/2 ) / 75
    elif (i<80):
        pt = 1.495
    elif (i < 125):
        pt = 1.495 + 0.495 * (140 - i) / 60
    elif (i < 155):
        pt = 1.495 + 0.495 * (16.25 - (i-125)/2 ) / 75
    else:
        pt = 1.505
    x = np.linspace(0.8, 1.99)
    text.set_text("slope of the arc {0:.4f}".format((func(1.5) - func(pt))/(1.5 - pt)))
    y = (x - 1.5) * (func(1.5) - func(pt))/(1.5 - pt) + func(1.5)
    line.set_data(x, y)
    point.set_data([pt], [func(pt)])
    return (point, line, text)


anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=160, repeat=True, blit=True)



# anim.save("slope.gif", writer='pillow')

plt.show()



class DualBasic(object):
    def __init__(self, val, eps):
        self.val = val
        self.eps = eps


class DualBasicEnhanced(object):
    def __init__(self, *args):
        if len(args) == 2:
            value, eps = args
        elif len(args) == 1:
            if isinstance(args[0], (float, int)):
                value, eps = args[0], 0
            else:
                value, eps = args[0].value, args[0].eps
        self.value = value
        self.eps = eps

    def __abs__(self):
        return abs(self.value)

    def __str__(self):
        return "Dual({}, {})".format(self.value, self.eps)

    def __repr__(self):
        return str(self)


# In code:
class DualArith(object):
    def __add__(self, other):
        other = Dual(other)
        return Dual(self.value + other.value, self.eps + other.eps)

    def __sub__(self, other):
        other = Dual(other)
        return Dual(self.value - other.value, self.eps - other.eps)

    def __mul__(self, other):
        other = Dual(other)
        return Dual(self.value * other.value, self.eps * other.value + self.value * other.eps)

class DualDiv(object):
    def __truediv__(self, other):
        other = Dual(other)
        if abs(other.value) == 0:
            raise ZeroDivisionError
        else:
            return Dual(self.value / other.value,
                        self.eps / other.value - self.value / (other.value) ** 2 * other.eps)

class Dual(DualBasicEnhanced, DualArith, DualDiv):
            pass

def square(x):
            return x * x

ans_1 = square(Dual(3, 1))

print(ans_1)