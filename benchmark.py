#! python3

import subprocess
import time


def runClientBench(client_concurrency=2,
                   client_target_rps=20000,
                   client_duration=60,
                   request_body_size=128,
                   response_body_size=128,
                   request_header_num=5,
                   header_value_size=32,
                   target="http://localhost:80"):
    args = [
        "/usr/local/bin/nighthawk_client", "--concurrency",
        str(client_concurrency), "--rps",
        str(client_target_rps), "--duration",
        str(client_duration), "--request-header",
        "x-nighthawk-test-server-config:{response_body_size:%s}" %
        response_body_size
    ]

    if (request_body_size > 0):
        args.append("--request-method")
        args.append("POST")
        args.append("--request-body-size")
        args.append(str(request_body_size))

    request_header_value = header_value_size * "c"
    for i in range(request_header_num):
        args.append("--request-header")
        args.append("x-bench-test-key-{}:{}".format(i, request_header_value))

    args.append(target)

    out = subprocess.run(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    if (out != None):
        if (out.stdout != None):
            print(out.stdout.decode('utf'))
        if (out.stderr != None):
            print(out.stderr.decode('utf'))


print("sleep 20s to wait server and proxy ready...")
time.sleep(20)

runClientBench(request_header_num=5,
               header_value_size=32,
               target="http://proxy:9090")
runClientBench(request_header_num=10,
               header_value_size=32,
               target="http://proxy:9090")
runClientBench(request_header_num=20,
               header_value_size=32,
               target="http://proxy:9090")
runClientBench(request_header_num=30,
               header_value_size=32,
               target="http://proxy:9090")

runClientBench(request_header_num=5,
               header_value_size=256,
               target="http://proxy:9090")
runClientBench(request_header_num=10,
               header_value_size=256,
               target="http://proxy:9090")
runClientBench(request_header_num=20,
               header_value_size=256,
               target="http://proxy:9090")
runClientBench(request_header_num=30,
               header_value_size=256,
               target="http://proxy:9090")
