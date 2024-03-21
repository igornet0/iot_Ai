import matplotlib.pyplot as  plt
X_0 = -19
X_1 = -16
X = [X_0, X_1]
a = 0
for n in range(7):
    n = -n
    X_n = ((2*(n+6)*X[abs(n+1)])/(n+7)) - (((n+5)*X[abs(n)])/(n+7))

    X.append(X_n)

    if X_n == 1:
        print(n)
    elif X_n > 1:
        break
plt.plot(X)
plt.show()