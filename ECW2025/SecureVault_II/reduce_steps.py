## reduce steps base on cycle found using brent alg
def reduce_steps(steps, mu, lam):
    if steps < mu:
        return steps
    else:
        return mu + ((steps - mu) % lam)

steps = 306210010937948737844847939557021440793
mu = 6984369
lam = 5779304

steps_reduced = reduce_steps(steps, mu, lam)
print("Reduced steps :", steps_reduced)	
