import click, os, subprocess, time
import constants as constant
from sys import platform, stderr
from getpass import getpass, getuser
from progress.spinner import Spinner
from progress.bar import IncrementalBar
from subprocess import Popen, PIPE, DEVNULL, run
from constants import applications_windows, devpackages_windows, applications_linux, devpackages_linux, apt_script, apt_remove, snap_script, snap_remove, display_list_linux, display_list_windows, hyperpkgs
from miscellaneous import show_progress, is_password_valid
from HyperPack import HyperPack
from Debugger import Debugger
from Install import Installer
from Uninstall import Uninstaller
from Update import Updater


@click.group()
def cli():
    pass


@cli.command()
def version():
    '''
    Current Turbocharged Version You Have
    '''
    print('Version: 3.0.6 \nDistribution: Stable x86-64')


@cli.command()
@click.argument('package_list', required=True)
def install(package_list):
    '''
    Install A Specified Package(s)
    '''
    if platform == 'linux':
        password = getpass('Enter your password: ')
    else:
        password = ''
        # otherwise the variable would be undefined..

    packages = package_list.split(',')
    turbocharge = Installer()

    click.echo('\n')

    os_bar = IncrementalBar('Getting Operating System...', max=1)
    os_bar.next()

    for package_name in packages:
        package_name = package_name.strip(' ')

        if platform == 'linux':
            click.echo('\n')
            finding_bar = IncrementalBar(
                'Finding Requested Packages...', max=1)

            if package_name in devpackages_linux:
                show_progress(finding_bar)
                turbocharge.install_task(
                    devpackages_linux[package_name],
                    f'{constant.apt_script} {package_name}',
                    password,
                    f'{package_name} --version',
                    [f'{devpackages_linux[package_name]} Version'])

            if package_name in applications_linux:
                show_progress(finding_bar)
                turbocharge.install_task(
                    applications_linux[package_name],
                    f'{constant.snap_script} {package_name}',
                    password,
                    '',
                    [])

            if package_name == 'chrome':
                show_progress(finding_bar)
                try:
                    click.echo('\n')

                    password = getpass("Enter your password: ")

                    installer_progress = Spinner(
                        message='Installing Chrome...', max=100)

                    for _ in range(1, 75):
                        time.sleep(0.03)
                        installer_progress.next()

                    click.echo(
                        click.style(
                            '\n Chrome Will Take 2 to 4 Minutes To Download... \n',
                            fg='yellow'))

                    
                    os.system(constant.chrome_link)

                    os.system(constant.chrome_move)

                    second = Popen(
                        constant.chrome_setup.split(),
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE)
                    # Popen only accepts byte-arrays so you must encode the
                    # string
                    second.communicate(password.encode())

                    # stdoutput = (output)[0].decode('utf-8')
                    click.echo(
                        click.style('\n\n 🎉 Successfully Installed Chrome! 🎉 \n'))
                    # Testing the successful installation of the package
                    testing_bar = IncrementalBar('Testing package...', max=100)
                    for _ in range(1, 21):
                        time.sleep(0.045)
                        testing_bar.next()
                    
                    for _ in range(21, 60):
                        time.sleep(0.045)
                        testing_bar.next()
                    for _ in range(60, 101):
                        time.sleep(0.03)
                        testing_bar.next()
                    click.echo('\n')
                    click.echo(
                        click.style(
                            'Test Passed: Chrome Launch ✅\n',
                            fg='green'))
                except subprocess.CalledProcessError as e:
                    click.echo(e.output)
                    click.echo(
                        'An Error Occurred During Installation...', err=True)

            if package_name == 'anaconda':
                show_progress(finding_bar)

                try:
                    installer_progress = Spinner(
                        message=f'Installing {package_name}...', max=100)
                    # sudo requires the flag '-S' in order to take input from
                    # stdin
                    for _ in range(1, 35):
                        time.sleep(0.01)
                        installer_progress.next()
                    os.system(constant.anaconda_download)
                    for _ in range(35, 61):
                        time.sleep(0.01)
                        installer_progress.next()

                    os.system(constant.anaconda_setup)

                    for _ in range(61, 91):
                        time.sleep(0.01)
                        installer_progress.next()

                    os.system(constant.anaconda_PATH)

                    for _ in range(90, 101):
                        time.sleep(0.01)
                        installer_progress.next()
                    # stdoutput = (output)[0].decode('utf-8')
                    click.echo(
                        click.style(f'\n\n 🎉 Successfully Installed {package_name}! 🎉 \n'))
                except subprocess.CalledProcessError as e:
                    click.echo(e.output)
                    click.echo(
                        'An Error Occurred During Installation...', err=True)

            if package_name == 'miniconda':
                show_progress(finding_bar)
                try:
                    installer_progress = Spinner(
                        message=f'Installing {package_name}...', max=100)
                    # sudo requires the flag '-S' in order to take input from
                    # stdin
                    for _ in range(1, 35):
                        time.sleep(0.01)
                        installer_progress.next()
                    os.system(constant.miniconda_download)
                    for _ in range(35, 61):
                        time.sleep(0.01)
                        installer_progress.next()
                    os.system(constant.miniconda_setup)
                    for _ in range(61, 91):
                        time.sleep(0.01)
                        installer_progress.next()
                    os.system(constant.miniconda_PATH)
                    for _ in range(90, 101):
                        time.sleep(0.01)
                        installer_progress.next()
                    # stdoutput = (output)[0].decode('utf-8')
                    click.echo(
                        click.style(f'\n\n 🎉 Successfully Installed {package_name}! 🎉 \n'))
                except subprocess.CalledProcessError as e:
                    click.echo(e.output)
                    click.echo(
                        'An Error Occurred During Installation...', err=True)

            elif package_name not in devpackages_linux and package_name not in applications_linux and package_name != 'chrome' and package_name != 'anaconda' and package_name != 'miniconda':
                click.echo('\n')
                click.echo(click.style(':( Package Not Found! :(', fg='red'))
        

        elif platform == 'win32':
            click.echo('\n')
            finding_bar = IncrementalBar('Finding Requested Packages...', max = 1)

            if package_name in devpackages_windows:
                show_progress(finding_bar)
                turbocharge.install_task(
                    package_name=devpackages_windows[package_name],
                    script=f"choco install {package_name} -y",
                    password="",
                    test_script=f"{package_name} --version",
                    tests_passed=[f'{devpackages_windows[package_name]} Version']
                )
                # test _scirpt is just a string here..


            elif package_name in applications_windows:
                show_progress(finding_bar)
                turbocharge.install_task(
                    package_name=applications_windows[package_name],
                    script=f"choco install {package_name} -y",
                    password="",
                    test_script="",
                    tests_passed=[]
                )
            
            elif package_name not in devpackages_windows and package_name not in applications_windows:
                click.echo('\n')
                click.echo(click.style(':( Package Not Found! :(', fg='red'))
            



@cli.command()
@click.argument('package_list', required=True)
def remove(package_list):
    '''
    Uninstall Applications And Packages
    '''
    uninstaller = Uninstaller()
    
    if platform == 'linux':
        password = getpass('Enter your password: ')
    else:
        password = ''

    packages = package_list.split(',')

    for package in packages:
        if platform == 'linux':
            if package in devpackages_linux:
                uninstaller.uninstall(
                    f'{apt_remove} {package}',
                    password,
                    package_name=devpackages_linux[package])

            if package in applications_linux:
                uninstaller.uninstall(
                    f'{snap_remove} {package}',
                    password,
                    package_name=applications_linux[package])

            if package == 'anaconda':
                try:
                    installer_progress = Spinner(
                        message=f'Uninstalling Anaconda...', max=100)
                    # sudo requires the flag '-S' in order to take input from
                    # stdin
                    for _ in range(1, 75):
                        time.sleep(0.007)
                        installer_progress.next()

                    os.system(constant.anaconda_remove_folder)
                    os.system(constant.anaconda_remove_file)

                    with open('.bashrc', 'r') as file:
                        lines = file.read()

                    with open('.bashrc', 'w') as file:
                        for line in lines:
                            if 'anaconda' in line or 'miniconda' in line:
                                continue
                            else:
                                file.write(line)

                    # stdoutput = (output)[0].decode('utf-8')
                    for _ in range(75, 101):
                        time.sleep(0.01)
                        installer_progress.next()
                    click.echo(click.style(
                        f'\n\n 🎉 Successfully Uninstalled Anaconda! 🎉 \n', fg='green'))
                except subprocess.CalledProcessError as e:
                    click.echo(e.output)
                    click.echo('An Error Occurred During Uninstallation...', err=True)

            if package == 'miniconda':
                try:
                    installer_progress = Spinner(
                        message=f'Uninstalling Miniconda...', max=100)

                    # sudo requires the flag '-S' in order to take input from
                    # stdin
                    for _ in range(1, 75):
                        time.sleep(0.007)
                        installer_progress.next()

                    os.system(constant.miniconda_remove_folder)
                    os.system(constant.miniconda_remove_file)

                    with open('.bashrc', 'r') as file:
                        lines = file.read()

                    with open('.bashrc', 'w') as file:
                        for line in lines:
                            if 'anaconda' in line or 'miniconda' in line:
                                continue
                            else:
                                file.write(line)

                    # stdoutput = (output)[0].decode('utf-8')
                    for _ in range(1, 101):
                        time.sleep(0.01)
                        installer_progress.next()
                    click.echo(click.style(
                        f'\n\n 🎉 Successfully Uninstalled Miniconda! 🎉 \n', fg='green'))
                except subprocess.CalledProcessError as e:
                    click.echo(e.output)
                    click.echo(
                        'An Error Occurred During Uninstallation...', err=True)

        elif platform == 'win32':
            if package in devpackages_windows:
                uninstaller.uninstall(
                    f'choco uninstall {package} -y',
                    password="",
                    package_name=devpackages_windows[package]
                )
            elif package in applications_windows:
                uninstaller.uninstall(
                    f'choco uninstall {package}',
                    password="",
                    package_name=applications_windows[package]
                )

@cli.command()
@click.argument('package_list', required=True)
def update(package_list):
    '''
    Updates Applications And Packages
    '''
    updater = Updater()

    if platform == 'linux':
        password = getpass('Enter your password: ')
    else:
        password = ''

    packages = package_list.split(',')

    for package in packages:
        if platform == "linux":
            if package in devpackages_linux:
                updater.updatepack(package, password)

            if package in applications_linux:
                updater.updateapp(package, password)

            else:
                return

        elif platform == "win32":
            if package in devpackages_windows:
                updater.updatepack(package, "")

            if package in applications_windows:
                updater.updateapp(package, "")

            else:
                return


@cli.command()
@click.argument('hyperpack_list', required=True)
def hyperpack(hyperpack_list):
    '''
    Install Large Packs Of Applications And Packages
    '''
    os_bar = IncrementalBar('Getting Operating System...', max=1)
    os_bar.next()

    installer = Installer()
    updater = Updater()
    cleaner = Uninstaller()

    hyperpacks = hyperpack_list.split(',')

    if platform == 'linux':
        password = getpass('Enter your password: ')
        click.echo('\n')

        password_bar = IncrementalBar('Verifying Password...', max=1)

        exitcode = is_password_valid(password)

        if exitcode == 1:
            click.echo('Wrong Password Entered... Aborting Installation!')
            return

        password_bar.next()

        click.echo('\n')

        for hyperpack in hyperpacks:
            hyper_pack = hyperpkgs[hyperpack]

            packages = hyper_pack.packages.split(',')
            apps = hyper_pack.applications.split(',')

            # Installing Required Packages
            for package in packages:
                installer.install_task(
                    devpackages_linux[package],
                    f'sudo -S apt-get install -y {package}',
                    password,
                    f'{package} --version',
                    [f'{devpackages_linux[package]} Version'])

            # Installing Required Applications
            for app in apps:
                installer.install_task(
                    applications_linux[app],
                    f'sudo -S snap install --classic {app}',
                    password,
                    '',
                    [])

            # Updating Required Packages
            for package in packages:
                updater.updatepack(package, password)

            for app in apps:
                updater.updateapp(app, password)

            cleaner.clean(password)
    
    elif platform == 'win32':
        for hyperpack in hyperpacks:
            hyper_pack = hyperpkgs[hyperpack]

            packages = hyper_pack.packages.split(',')
            apps = hyper_pack.applications.split(',')

            for package in packages:
                installer.install_task(
                    package_name=devpackages_windows[package],
                    script=f'choco install {package} -y',
                    password="",
                    test_script=f'{package} --version',
                    tests_passed=[f'{devpackages_windows[package]} Version']
                )

            for package in packages:
                updater.updatepack(package, password="")
            
            for app in apps:
                installer.install_task(
                    package_name=applications_windows[app],
                    script=f'choco install {app} -y',
                    password="",
                    test_script='',
                    tests_passed=[]
                )
            
            for app in apps:
                updater.updateapp(app, password="")


@cli.command()
def clean():
    '''
    Remove Junk Packages Which Are Not Needed
    '''
    if platform == 'linux':
        uninstaller = Uninstaller()
        password = getpass('Enter your password: ')
        uninstaller.clean(password)
    elif platform == 'win32':
        arr = ['|',"/","-","\\"]
        slen = len(arr)
        print('.....Getting your PC cleaned .........')
        for i in range(1, 60):
            time.sleep(0.04)
            print(arr[i%slen], end='\r')


@cli.command()
def list():
    '''
    Applications And Packages TurboCharge Supports
    '''
    if platform == 'linux':
        click.echo(click.style(display_list_linux, fg='white'))
    elif platform == 'win32':
        
        click.echo(click.style(display_list_windows, fg='white'))