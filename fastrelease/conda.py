# AUTOGENERATED! DO NOT EDIT! File to edit: 01_conda.ipynb (unless otherwise specified).

__all__ = ['pypi_json', 'latest_pypi', 'pypi_details', 'update_meta', 'as_posix', 'conda_output_path',
           'write_pip_conda_meta', 'write_conda_meta', 'anaconda_upload', 'fastrelease_conda_package', 'chk_conda_rel']

# Cell
from fastcore.script import *
from fastcore.all import *
from .core import find_config

import yaml,subprocess,glob,platform
from copy import deepcopy
try: from packaging.version import parse
except ImportError: from pip._vendor.packaging.version import parse

_PYPI_URL = 'https://pypi.org/pypi/'

# Cell
def pypi_json(s):
    "Dictionary decoded JSON for PYPI path `s`"
    return urljson(f'{_PYPI_URL}{s}/json')

# Cell
def latest_pypi(name):
    "Latest version of `name` on pypi"
    return max(parse(r) for r,o in pypi_json(name)['releases'].items()
               if not parse(r).is_prerelease and not o[0]['yanked'])

# Cell
def pypi_details(name):
    "Version, URL, and SHA256 for `name` from pypi"
    ver = str(latest_pypi(name))
    pypi = pypi_json(f'{name}/{ver}')
    info = pypi['info']
    rel = [o for o in pypi['urls'] if o['packagetype']=='sdist'][0]
    return ver,rel['url'],rel['digests']['sha256']

# Cell
def update_meta(name,src_path,dest_path):
    "Update VERSION and SHA256 in meta.yaml from pypi"
    src_path,dest_path = Path(src_path),Path(dest_path)
    txt = src_path.read_text()
    ver,url,sha = pypi_details(name)
    dest_path.write_text(txt.replace('VERSION',ver).replace('SHA256',sha))
    return ver

# Cell
def as_posix(p):
    "`Path(p).as_posix()`"
    return Path(p).as_posix()

# Cell
def conda_output_path(name,ver):
    "Output path for conda build"
    pre = run('conda info --root').strip()
    s = f"{as_posix(pre)}/conda-bld/*/{name}-{ver}-py"
    res = first(glob.glob(f"{s}_0.tar.bz2"))
    if not res:
        pyver = strcat(sys.version_info[:2])
        res = first(glob.glob(f"{s}{pyver}_0.tar.bz2"))
    if res: return as_posix(res)

# Cell
def _pip_conda_meta(name, path):
    ver = str(latest_pypi(name))
    pypi = pypi_json(f'{name}/{ver}')
    info = pypi['info']
    rel = [o for o in pypi['urls'] if o['packagetype']=='sdist'][0]
    reqs = ['pip', 'python', 'packaging']

    # Work around conda build bug - 'package' and 'source' must be first
    d1 = {
        'package': {'name': name, 'version': ver},
        'source': {'url':rel['url'], 'sha256':rel['digests']['sha256']}
    }
    d2 = {
        'build': {'number': '0', 'noarch': 'python',
                  'script': '{{ PYTHON }} -m pip install . -vv'},
        'test': {'imports': [name]},
        'requirements': {'host':reqs, 'run':reqs},
        'about': {'license': info['license'], 'home': info['project_url'], 'summary': info['summary']}
    }
    return d1,d2

# Cell
def _write_yaml(path, name, d1, d2):
    path = Path(path)
    p = path/name
    p.mkdir(exist_ok=True, parents=True)
    yaml.SafeDumper.ignore_aliases = lambda *args : True
    with (p/'meta.yaml').open('w') as f:
        yaml.safe_dump(d1, f)
        yaml.safe_dump(d2, f)

# Cell
def write_pip_conda_meta(name, path='conda'):
    "Writes a `meta.yaml` file for `name` to the `conda` directory of the current directory"
    _write_yaml(path, name, *_pip_conda_meta(name, path))

# Cell
def _get_conda_meta():
    cfg = find_config()
    name,ver = cfg.lib_name,cfg.version
    url = cfg.doc_host or cfg.git_url

    reqs = ['pip', 'python', 'packaging']
    if cfg.get('requirements'): reqs += cfg.requirements.split()
    if cfg.get('conda_requirements'): reqs += cfg.conda_requirements.split()

    pypi = pypi_json(f'{name}/{ver}')
    rel = [o for o in pypi['urls'] if o['packagetype']=='sdist'][0]

    # Work around conda build bug - 'package' and 'source' must be first
    d1 = {
        'package': {'name': name, 'version': ver},
        'source': {'url':rel['url'], 'sha256':rel['digests']['sha256']}
    }

    d2 = {
        'build': {'number': '0', 'noarch': 'python',
                  'script': '{{ PYTHON }} -m pip install . -vv'},
        'requirements': {'host':reqs, 'run':reqs},
        'test': {'imports': [cfg.get('lib_path')]},
        'about': {
            'license': 'Apache Software',
            'license_family': 'APACHE',
            'home': url, 'doc_url': url, 'dev_url': url,
            'summary': cfg.get('description')
        },
        'extra': {'recipe-maintainers': [cfg.get('user')]}
    }
    return name,d1,d2

# Cell
def write_conda_meta(path='conda'):
    "Writes a `meta.yaml` file to the `conda` directory of the current directory"
    _write_yaml(path, *_get_conda_meta())

# Cell
def anaconda_upload(name, version, user=None, token=None, env_token=None):
    "Update `name` `version` to anaconda"
    user = f'-u {user} ' if user else ''
    if env_token: token = os.getenv(env_token)
    token = f'-t {token} ' if token else ''
    loc = conda_output_path(name,version)
    if not loc: raise Exception("Failed to find output")
    return run(f'anaconda {token} upload {user} {loc} --skip-existing', stderr=True)

# Cell
@call_parse
def fastrelease_conda_package(
    path:str='conda', # Path where package will be created
    do_build:bool_arg=True,  # Run `conda build` step
    build_args:str='',  # Additional args (as str) to send to `conda build`
    skip_upload:store_true=False,  # Skip `anaconda upload` step
    mambabuild:store_true=False,  # Use `mambabuild` (requires `boa`)
    upload_user:None=None  # Optional user to upload package to
):
    "Create a `meta.yaml` file ready to be built into a package, and optionally build and upload it"
    write_conda_meta(path)
    cfg = find_config()
    out = f"Done. Next steps:\n```\`cd {path}\n"""
    name,lib_path = cfg.lib_name,cfg.lib_path
#     out_upl = f"anaconda upload {loc}"
    build = 'mambabuild' if mambabuild else 'build'
    if not do_build: return #print(f"{out}conda {build} .\n{out_upl}\n```")

    os.chdir(path)
    print(f"conda {build} --no-anaconda-upload {build_args} {name}")
    res = run(f"conda {build} --no-anaconda-upload {build_args} {name}")
    if 'anaconda upload' not in res: return print(f"{res}\n\Failed. Check auto-upload not set in .condarc. Try `--do_build False`.")
    loc = conda_output_path(lib_path, cfg.version)
    return anaconda_upload(lib_path, cfg.version)

# Cell
@call_parse
def chk_conda_rel(
    nm:str,  # Package name on pypi
    apkg:str=None,  # Anaconda Package (defaults to {nm})
    channel:str='fastai',  # Anaconda Channel
    force:store_true=False  # Always return github tag
):
    "Prints GitHub tag only if a newer release exists on Pypi compared to an Anaconda Repo."
    if not apkg: apkg=nm
    condavs = L(loads(run(f'mamba repoquery search {apkg} -c {channel} --json'))['result']['pkgs'])
    condatag = condavs.attrgot('version').map(parse)
    pypitag = latest_pypi(nm)
    if force or not condatag or pypitag > max(condatag): return f'{pypitag}'
