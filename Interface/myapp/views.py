from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import docker
import os
import time
import re


# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request, '../templates/index.html')
    if request.method == 'POST':
        lang = request.POST['lang']
        code = request.POST['code']
        res = {'lang': lang, 'code': code, 'run': 'none'}
        return HttpResponse("Hello")


# @name = save_file
# @Description: This function is used to generate temporary files like code, input and executable file
# @Parameter:
#   - code : file content
#   - lang : file type, for example, '.c', '.txt', '.cpp', '.py'
#   - directory : absolute path of the directory where file is saved
#   - filename : filename to be generated, but PROBABLY NOT THE FINAL NAME of the file
#   due to existed name created by other user
# @Return: filename : the final filename


def save_file(code, lang, directory, filename):
    path = directory + filename

    while os.path.exists(path+lang):
        time_suffix = str(time.time()).replace('.', '')
        path = path + time_suffix
        filename = filename + time_suffix

    path = path + lang
    filename = filename + lang

    file_handler = open(path, 'w', encoding='utf-8')
    file_handler.write(code)
    file_handler.close()
    return filename


def result(request):
    if request.method == 'POST':
        lang = request.POST['lang']
        code = request.POST['code']
        data_input = request.POST['input']
        time_limit = request.POST['time_limit']

        # TODO: Change the parameters as you want
        # RUN_DIR - directory in the host to save code as temporary file posted from web,
        # now the directory is set as current directory.
        # when you change the RUN_DIR, DO REMEMBER TO GIVE PERMISSION TO THE DIRECTORY
        # TIME_LIMIT - time limit for the program, unit (s)
        RUN_DIR = os.getcwd().replace('\\', '/') + '/.temp/'
        # replace aimed to change windows style into linux style
        TIME_LIMIT_C = str(time_limit * 0.001) + 's'
        TIME_LIMIT_PY = str(time_limit * 0.001) + 's'

        message_dict = {
            0: 'Run Success',
            1: 'Time Limit Exceed',
            2: 'Compile Error',
            3: 'Runtime Error',
            4: 'System Error'
        }

        # create a docker container and bind current directory to the container
        try:
            client = docker.from_env()
            container = client.containers.run('ubuntugccpy:v2.0', '/bin/bash -c "tail -f /dev/null"', name=str(time.time()).replace('.', ''),
                                              detach=True, volumes={RUN_DIR: {'bind': '/home/code', 'mode': 'rw'}},
                                              )
        except RuntimeError:
            error_code = 4

        # filename is generated current time
        # For Example
        # >>> time.time()
        # 1596857839.850112
        # >>> '-' + str(time.time()).replace('.', '')
        # 1596857839850112
        code_filename = str(time.time()).replace('.', '')
        input_filename = code_filename + '_input'
        input_filename = save_file(data_input, '.txt', RUN_DIR, input_filename)

        if lang == 'c':
            code_filename = save_file(code, '.c', RUN_DIR, code_filename)
            exec_filename = code_filename[:-2]
            compile_command = 'gcc ' + code_filename + ' -o ' + exec_filename + ' -w'
            run_command = 'timeout ' + TIME_LIMIT_C + ' ./' + exec_filename + ' < ' + input_filename
            # compile with gcc
            exit_code, out = container.exec_run(compile_command)
            if exit_code == 0:
                os.remove(RUN_DIR + code_filename)
                exit_code, out = container.exec_run(run_command)
                if exit_code == 124:
                    # Time Limit Exceed
                    error_code = 1
                elif exit_code != 0:
                    # Runtime Error
                    error_code = 3
                else:
                    # No problem
                    error_code = 0
                    output = out.decode()
                os.remove(RUN_DIR + exec_filename)
            else:
                # Compile Error
                error_code = 2
                print(out.decode())
                os.remove(RUN_DIR + code_filename)

        elif lang == 'cpp':
            code_filename = save_file(code, '.cpp', RUN_DIR, code_filename)
            exec_filename = code_filename[:-2]
            compile_command = 'g++ ' + code_filename + ' -o ' + exec_filename + ' -w'
            run_command = 'timeout ' + TIME_LIMIT_C + ' ./' + exec_filename + ' < ' + input_filename
            # compile with g++
            exit_code, out = container.exec_run(compile_command)
            if exit_code == 0:
                os.remove(RUN_DIR + code_filename)
                exit_code, out = container.exec_run(run_command)
                #     TODO: 如何判断程序超时被停止
                if exit_code == 124:
                    # Time Limit Exceed
                    error_code = 1
                elif exit_code != 0:
                    # Runtime Error
                    error_code = 3
                else:
                    # No problem
                    error_code = 0
                    output = out.decode()
                os.remove(RUN_DIR + exec_filename)
            else:
                os.remove(RUN_DIR + code_filename)
                # Compile Error
                error_code = 2

        else:
            code_filename = save_file(code, '.py', RUN_DIR, code_filename)
            run_command = 'timeout ' + TIME_LIMIT_PY + ' python3 ' + code_filename + ' < ' + input_filename
            exit_code, out = container.exec_run(run_command)
            out = out.decode()
            if exit_code == 0:
                # no problem
                error_code = 0
                output = out
            elif exit_code == 124:
                # Time Limit Exceed
                error_code = 1
            else:
                # Complie Error
                error_code = 2

            os.remove(RUN_DIR + code_filename)

        os.remove(RUN_DIR + input_filename)

        container.stop()
        container.remove()

        if error_code == 0:
            result = output
        else:
            result = 'Error'
        res = {'result': result, 'message': message_dict[error_code]}
        return JsonResponse(res)
