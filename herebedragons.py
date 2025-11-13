import os
import pyemu
import platform
import shutil
import numpy as np


def get_bins(local_dir):
    #figure out if mac,lilnux or windows
    if platform.system() == "Windows":
        bin_dir = "win"
    elif platform.system() == "Darwin":
        bin_dir = "mac"
    else:
        bin_dir = "linux"
    bindir = os.path.join("bin", bin_dir)

    # copy all the exes to a local bin dir
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    for fname in os.listdir(bindir):
        src = os.path.join(bindir, fname)
        dst = os.path.join(local_dir, fname)
        if os.path.isfile(dst):
            os.remove(dst)
        shutil.copy(src, dst)
    return bindir


def tidy_array(fpath):
    # read unordered txt file
    with open(fpath, 'r') as f:
        data = f.read().split()
    data = [float(x) for x in data]
    arr = np.array(data)
    arr = arr.flatten()
    #arr = arr.reshape(sr.ncpl)
    np.savetxt(fpath, arr, fmt='%1.6e')
    return


def get_lst_budget(ws='.',start_datetime=None, casename='gwf',mfversion='mf6'):
    """get the inc and cum dataframes from a MODFLOW-6 list file
    Parameters
    ----------
    ws : str
        path to the model workspace
    start_datetime : str
        a string that can be parsed by pandas.to_datetime
    Returns
    -------
    inc : pandas.DataFrame
        the incremental budget
    cum : pandas.DataFrame
        the cumulative budget
        """
    print("postprocessing lst obs...")
    import flopy
    if mfversion == 'mf6':
        lst = flopy.utils.Mf6ListBudget(os.path.join(ws,f"{casename}.lst"))
    else:
        lst = flopy.utils.MfListBudget(os.path.join(ws,f"{casename}.lst"))
    inc,cum = lst.get_dataframes(diff=True,start_datetime=start_datetime)
    inc.columns = inc.columns.map(lambda x: x.lower().replace("_","-"))
    cum.columns = cum.columns.map(lambda x: x.lower().replace("_", "-"))
    inc.index.name = "time"
    cum.index.name = "time"
    inc.to_csv(os.path.join(ws,"inc.csv"))
    cum.to_csv(os.path.join(ws,"cum.csv"))
    return inc, cum

def get_obs_cellids(t_d='.'):
    import pandas as pd
    import flopy

    sim = flopy.mf6.MFSimulation.load(sim_ws=t_d,load_only=['oc','obs'],verbosity_level=0)
    gwf = sim.get_model('gwf')

    df = pd.DataFrame(columns=['icpl','group'])
    a = gwf.obs.continuous

    for k,v in a.data.items():
        _ = pd.DataFrame(v)
        _['icpl'] = _['id'].apply(lambda x: x[1])
        obsgp = k.split(".")[0].replace("gwf_","")
        if "_" in obsgp:
            obsgp = obsgp.split("_")[1]
        else:
            obsgp = "calib"
        _['group'] = obsgp
        _ = _[['icpl','group']]
        df = pd.concat([df, _], ignore_index=True)
    return df


def post_model_outputs(template_ws="."):
    import flopy
    import pandas as pd
    sim = flopy.mf6.MFSimulation.load(sim_ws=template_ws,load_only=['oc'], verbosity_level=0)
    gwf = sim.get_model("gwf")
    gwe = sim.get_model("gwe")

    heads = gwf.output.head().get_alldata()
    np.savetxt(os.path.join(template_ws,"heads.0.txt"),heads[0,:,:,:].flatten())
    print(f"saving heads in kper0 to: {os.path.join(template_ws,'heads.0.txt')}")
    np.savetxt(os.path.join(template_ws,"heads.1.txt"),heads[1,:,:,:].flatten())
    print(f"saving heads in kper1 to: {os.path.join(template_ws,'heads.1.txt')}")

    temp = gwe.output.temperature().get_alldata()
    max_temp = temp.max(axis=0).flatten()
    np.savetxt(os.path.join(template_ws,"temp.max.txt"),max_temp)
    print(f"saving max temps to: {os.path.join(template_ws,'temp.max.txt')}")

    # calib riv obs
    df = pd.read_csv(os.path.join(template_ws,"rivobs.csv"),index_col=0)
    np.savetxt(os.path.join(template_ws,"riv.0.txt"),df.iloc[0].values)
    print(f"saving riv obs to: {os.path.join(template_ws,'riv.0.txt')}")
    return 