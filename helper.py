import subprocess
import os, re, math

env = os.environ.copy()

REGEX = r"HOOK: (\w+) requires (\d+\.\d+) seconds with (\d+) max # of threads"

def build(omp=True, dbg=True, opt=1):
    subprocess.run(["make","clean"])
    subprocess.run([
        "make",
        f"OMP={1 if omp else 0}",
        f"IS_DBG={1 if dbg else 0}",
        f"OPT={opt}",
        ], check=True)

def train(dataset, omp_threads=1, kernel=2, hooks = {}):
    env["OMP_NUM_THREADS"] = str(omp_threads)
    cmd = " ".join([
        "./svm-train",
        f"-t {kernel}",
        f"data/{dataset}",
        f"models/{dataset}"
        ])
    res = subprocess.run(
        cmd, shell=True,
        env=env, capture_output=True,
        check=True
    )

    stdout = str(res.stdout,"utf-8")
    for line in stdout.split("\n"):
        if line.startswith("HOOK:"):
            name, seconds, _  = [re.match(REGEX,line)[m] for m in range(1,4)]
            seconds = float(seconds)
            if name not in hooks:
                hooks[name] = []
            hooks[name].append(seconds)

    return hooks

def mean(l):
    s = sum(l)
    n = len(l)
    return s/n

def sd(l):
    m = mean(l)
    N = len(l)
    t = sum(((l[i]-m)**2 for i in range(N)))
    return math.sqrt(t/N)

def train_grid(dataset=[],nthreads=[],times=1):
    """
    returns:
        report: Dict[dataset,Dict[n_threads, Dict[hook_name,(total time, sd, count)]]]
    """
    report = {
        ds:{
            nt:{} for nt in nthreads
        }
        for ds in dataset
    }
    for ds in dataset:
        print(f"{ds} dataset:")
        for nt in nthreads:
            h = {}
            for i in range(times):
                print(f"\tUsing {nt} threads {i+1}/{times}", end="\r")
                h = train(ds,nt,hooks=h)
            for name in h:
                report[ds][nt][name] = sum(h[name])/times, sd(h[name]), len(h[name])//times
            print()
    return report

if __name__=="__main__":
    build(dbg=False,opt=2)
    N = 5
    N_THR = range(1,13)
    r = train_grid(["a9a"],N_THR,N)
    for ds in r:
        for nt in r[ds]:
            print(nt,r[ds][nt]['GET_Q'][0],r[ds][nt]['main'][0])