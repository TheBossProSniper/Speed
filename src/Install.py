from sys import platform
import click
from progress.spinner import Spinner
from progress.bar import IncrementalBar
import time
from subprocess import Popen, PIPE, DEVNULL, run
from getpass import getuser
from Debugger import Debugger
import subprocess
from constants import applications, devpackages
from os.path import isfile

class Installer:
    def install_task(self, package_name: str, script: str,
                     password: str, test_script: str, tests_passed):
        if platform == 'linux':
            try:
                installer_progress = Spinner(
                    message=f'Installing {package_name}...', max=100)

                # sudo requires the flag '-S' in order to take input from stdin
                for _ in range(1, 75):
                    time.sleep(0.01)
                    installer_progress.next()

                proc = Popen(
                    script.split(),
                    stdin=PIPE,
                    stdout=PIPE,
                    stderr=PIPE)

                # Popen only accepts byte-arrays so you must encode the string
                output, error = proc.communicate(password.encode())

                if proc.returncode != 0:
                    click.echo(
                        click.style(
                            '❎ Installation Failed... ❎',
                            fg='red',
                            blink=True,
                            bold=True))

                    debug = click.prompt(
                        'Would you like us to debug the failed installation?[y/n]')

                    if debug == 'y':
                        debugger = Debugger()
                        debugger.debug(password, error)

                        logs = click.prompt(
                            'Would you like to see the logs?[y/n]', type=str)

                        if logs == 'y':
                            final_output = error.decode('utf-8')

                            if final_output == '':
                                click.echo('There were no logs found...')

                                return
                            else:
                                click.echo(final_output)

                                return
                        return
                    else:
                        logs = click.prompt(
                            'Would you like to see the logs?[y/n]', type=str)

                        if logs == 'y':
                            final_output = output.decode('utf-8')

                            if final_output == '':
                                click.echo('There were no logs found...')

                                return
                            else:
                                click.echo(final_output)

                                return
                        return

                click.echo(
                    click.style(
                        f'\n\n 🎉 Successfully Installed {package_name}! 🎉 \n',
                        fg='green',
                        bold=True))

                def get_key(val, dictionary):
                        for key, value in dictionary.items():
                            if val == value:
                                return key

                def subprocess_cmd(command):
                    process = subprocess.Popen(
                        command, stdout=subprocess.PIPE, stdin=PIPE, stderr=PIPE)
                    proc_stdout = process.communicate()[0].strip()
                    decoded = proc_stdout.decode("utf-8")
                    version_tag = decoded.split("\n")[1]
                    # using [1:] might be useful in some scenario where the
                    # version has multiple colons in it.
                    cleaned_version = version_tag.split(": ")[1]
                    return cleaned_version

                package_type = None
                
                if 'sudo -S apt-get' in script:
                    package_type = 'p'
                elif 'sudo -S snap' in script:
                    package_type = 'a'

                

                # Testing the successful installation of the package
                testing_bar = IncrementalBar('Testing package...', max=100)

                if tests_passed == [] and test_script == '':
                    if package_type == 'a':
                        file_exists = False
                        if isfile(f'/home/{getuser()}/config.tcc'):
                            file_exists = True
            
                        if file_exists:
                            with open(f'/home/{getuser()}/config.tcc', 'r') as file:
                                lines = file.readlines()

                            line_exists = False

                            for line in lines:
                                if get_key(package_name, applications) in line:
                                    line_exists = True

                            with open(f'/home/{getuser()}/config.tcc', 'a+') as file:
                                if line_exists == False:
                                    file.write(
                                        f'{get_key(package_name, applications)} None {package_type} \n')
                        elif file_exists == False:
                            with open(f'/home/{getuser()}/config.tcc', 'w+') as file:
                                lines = file.readlines()

                            line_exists = False

                            for line in lines:
                                if get_key(package_name, applications) in line:
                                    line_exists = True

                            with open(f'/home/{getuser()}/config.tcc', 'a+') as file:
                                if line_exists == False:
                                    file.write(
                                        f'{get_key(package_name, applications)} None {package_type} \n')

                    click.echo('\n')
                    click.echo(
                        click.style(
                            f'Test Passed: {package_name} Launch ✅\n',
                            fg='green'))

                    return

                for _ in range(1, 21):
                    time.sleep(0.002)
                    testing_bar.next()

                

                for _ in range(21, 60):
                    time.sleep(0.002)
                    testing_bar.next()

                proc = Popen(
                    test_script.split(),
                    stdin=PIPE,
                    stdout=PIPE,
                    stderr=PIPE)

                

                package_type = None
                if 'sudo -S apt-get' in script:
                    package_type = 'p'
                elif 'sudo -S snap' in script:
                    package_type = 'a'

                

                    return 'Key doesn\'t exist'

                if package_type == 'p':

                    file_exists = False
                    if isfile(f'/home/{getuser()}/config.tcc'):
                        file_exists = True
                                        
                    package_version = subprocess_cmd(
                        f'apt show {get_key(package_name, devpackages)}'.split())
                    

                    if file_exists:
                        with open(f'/home/{getuser()}/config.tcc', 'r') as file:
                            lines = file.readlines()

                        line_exists = False

                        for line in lines:
                            if get_key(package_name, devpackages) in line:
                                line_exists = True

                        with open(f'/home/{getuser()}/config.tcc', 'a+') as file:
                            if line_exists == False:
                                file.write(
                                    f'{get_key(package_name, devpackages)} {package_version} {package_type} \n')
                    
                    elif file_exists == False:

                        with open(f'/home/{getuser()}/config.tcc', 'w+') as file:
                            lines = file.readlines()

                        line_exists = False

                        for line in lines:
                            if get_key(package_name, devpackages) in line:
                                line_exists = True

                        with open(f'/home/{getuser()}/config.tcc', 'a+') as file:
                            if line_exists == False:
                                file.write(
                                    f'{get_key(package_name, devpackages)} {package_version} {package_type} \n')


                for _ in range(60, 101):
                    time.sleep(0.002)
                    testing_bar.next()

                click.echo('\n')

                for test in tests_passed:
                    click.echo(
                        click.style(
                            f'Test Passed: {test} ✅\n',
                            fg='green'))

            except subprocess.CalledProcessError as e:
                click.echo(e.output)
                click.echo('An Error Occured During Installation...', err=True)

        elif platform == 'win32':
            try:
                installer_progress = Spinner(
                    message=f'Installing {package_name}...', max=100)

                for _ in range(1, 75):
                    time.sleep(0.01)
                    installer_progress.next()

                run(script, stdout=PIPE, stderr=PIPE)

                for _ in range(1, 25):
                    time.sleep(0.01)
                    installer_progress.next()

                # Haven't implemented debug because .run() doesn't offer
                # communicate() function

                click.echo(
                    click.style(
                        f'\n\n 🎉 Successfully Installed {package_name}! 🎉 \n',
                        fg='green',
                        bold=True))

                testing_bar = IncrementalBar('Testing package...', max=100)

                if tests_passed == [] and test_script == '':
                    click.echo('\n')
                    click.echo(
                        click.style(
                            f'Test Passed: {package_name} Launch ✅\n',
                            fg='green'))

                    return

                for _ in range(1, 64):
                    time.sleep(0.002)
                    testing_bar.next()

                run(test_script, stdout=PIPE, stderr=PIPE)

                for _ in range(1, 36):
                    time.sleep(0.002)
                    testing_bar.next()

                click.echo('\n')

                for test in tests_passed:
                    click.echo(
                        click.style(
                            f'Test Passed: {test} ✅\n',
                            fg='green'))

                return

            except Exception as e:
                click.echo(e)
                click.echo('An Error Occured During Installation...', err=True)
