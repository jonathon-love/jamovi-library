
from oyaml import load
from oyaml import dump
from oyaml import SafeLoader

from collections import OrderedDict
from zipfile import ZipFile
from os import scandir
from os.path import basename

import os
import sys
import asyncio
import platform
from asyncio import create_subprocess_shell

R_VERSION = '3.6.1'

if os.name == 'nt':
    OS = 'win64'
elif platform.system() == 'Darwin':
    OS = 'macos'
else:
    OS = 'linux'

platform = '{}/R{}'.format(OS, R_VERSION)


async def generate_modules():

    PREP_COMMANDS = [
        'git init',
        'git remote add origin {url}',
        'git pull origin master',
        'git checkout {commit}',
        ('RD build /Q /S & echo ""' if os.name == 'nt' else 'rm -rf build'),
        # { 'cmd': 'git fetch origin {commit}', 'cwd': '{name}' },
        # { 'cmd': 'git reset --hard FETCH_HEAD', 'cwd': '{name}' },
    ]

    BUILD_COMMANDS = [
        'node jamovi-compiler/index.js --build "{name}/{subdir}" --home "{jamovi_home}" --jmo {name}.jmo',
        'appveyor PushArtifact {name}.jmo -FileName "{outdir}/{name}-{version}.jmo" -DeploymentName Modules',
    ]

    ZIP_COMMANDS = [
        ('7z a -tzip -r {name}.jmo {name} -xr!.git' if os.name == 'nt' else 'zip -r {name}.jmo {name} -x "*/.git*"'),
        'appveyor PushArtifact {name}.jmo -FileName "{outdir}/{name}-{version}.jmo" -DeploymentName Modules',
    ]

    with open('modules.yaml', 'r') as stream:
        library = load(stream, Loader=SafeLoader)

    for module in library['modules']:
        dir = module['name']
        os.makedirs(dir, exist_ok=True)

        for cmd in PREP_COMMANDS:
            cmd = cmd.format(outdir=platform, **module)
            proc = await create_subprocess_shell(cmd, cwd=dir)
            rc = await proc.wait()
            if rc != 0:
                raise RuntimeError('Command failed: "{}"'.format(cmd))

        if not module.get('precompiled', False):

            commands = BUILD_COMMANDS

            sub_dir = module.get('subdir', False)
            if sub_dir:
                path = '{}/{}/jamovi/0000.yaml'.format(dir, sub_dir)
            else:
                path = '{}/jamovi/0000.yaml'.format(dir)

            with open(path, 'r') as stream:
                defn = load(stream, Loader=SafeLoader)

            module['version'] = defn['version']
            if 'subdir' not in module:
                module['subdir'] = ''

            module['jamovi_home'] = os.environ['JAMOVI_HOME']

        else:
            commands = ZIP_COMMANDS

            path = '{}/jamovi.yaml'.format(dir)

            with open(path, 'r') as stream:
                defn = load(stream, Loader=SafeLoader)

            module['version'] = defn['version']

        for cmd in commands:
            cmd = cmd.format(outdir=platform, **module)
            proc = await create_subprocess_shell(cmd)
            rc = await proc.wait()
            if rc != 0:
                raise RuntimeError('Command failed: "{}"'.format(cmd))

async def generate_index():

    keep_info = [
        'name',
        'title',
        'version',
        'authors',
        'description',
        'website',
    ]

    with open('modules.yaml', 'r') as stream:
        library = load(stream, Loader=SafeLoader)

    modules = [ ]

    for module in library['modules']:
        name = module['name']
        jmo = '{}.jmo'.format(name)
        zip = ZipFile(jmo)
        with zip.open('{}/jamovi.yaml'.format(name)) as stream:
            content = stream.read()
            data = load(content, Loader=SafeLoader)
            version = data['version']
            final = OrderedDict()
            for key in keep_info:
                try:
                    final[key] = data[key]
                except KeyError:
                    pass
            final['architectures'] = [ { 'name': '*', 'path': '{}-{}.jmo'.format(name, version) } ]
            modules.append(final)

    index = {
        'jds': '1.4',
        'modules': modules,
    }

    with open('index', 'w', encoding='utf-8') as file:
        dump(index, file)

    proc = await create_subprocess_shell('appveyor PushArtifact index -FileName {}/index -DeploymentName Index'.format(platform))
    rc = await proc.wait()
    if rc != 0:
        raise RuntimeError('Command failed: "{}"'.format(cmd))

asyncio.run(generate_modules())
asyncio.run(generate_index())
