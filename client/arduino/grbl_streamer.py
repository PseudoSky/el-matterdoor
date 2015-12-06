#!/usr/bin/env python
"""\
    Simple g-code streaming script for grbl

    Provided as an illustration of the basic communication interface
    for grbl. When grbl has finished parsing the g-code block, it will
    return an 'ok' or 'error' response. When the planner buffer is full,
    grbl will not send a response until the planner buffer clears space.

    G02/03 arcs are special exceptions, where they inject short line
    segments directly into the planner. So there may not be a response
    from grbl for the duration of the arc.

    ---------------------
    The MIT License (MIT)

    Copyright (c) 2012 Sungeun K. Jeon

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
    ---------------------
    """

import serial
import time
import subprocess
import sys
import re
import serial.tools.list_ports

RX_BUFFER_SIZE = 128
verbose=True
is_running=False

# Open grbl serial port
# serial.tools.list_ports;

serial_port = '/dev/tty.usbmodem1411'
for p in serial.tools.list_ports.comports():
    if 'usbmodem' in p[0]:
        serial_port=p[0].replace('cu','tty')
        print serial_port
s = serial.Serial(serial_port,115200)




# Stream g-code to grbl

print '\npopen2:'
def pp(s):
    print s+""
    # sys.stdout.write(s+'\n')

    return 1


def run_gcode(f):

    # print f
    l_count=0
    g_count = 0
    c_line = []


    for line in f:
        l_count += 1 # Iterate line counter
        l_block = re.sub('\s|\(.*?\)','',line).upper() # Strip comments/spaces/new line and capitalize

        l_block = line.strip()
        # pp(l_block)
        c_line.append(len(l_block)+1) # Track number of characters in grbl serial read buffer
        grbl_out = ''

        # While the arduino buffer is too full to accept the next command, wait
        while sum(c_line) >= RX_BUFFER_SIZE-1 | s.inWaiting() :
            out_temp = s.readline().strip() # Wait for grbl response
            if out_temp.find('ok') < 0 and out_temp.find('error') < 0 :
                print "  Debug: ",out_temp # Debug response
            else :
                grbl_out += out_temp;
                g_count += 1 # Iterate g-code counter
                grbl_out += str(g_count); # Add line finished indicator
                del c_line[0] # Delete the block character count corresponding to the last 'ok'
        # Then write the command


        if verbose: print "SND: " + str(l_count) + " : " + l_block,
        s.write(l_block + '\n') # Send g-code block to grbl
        if verbose : print "BUF:",str(sum(c_line)),"REC:",grbl_out



cmd=['G21 G90 G17 G94 G54','G0 X0.000','G1 X0.500 F149.944','G1 X0.972 F141.747','G1 X1.385 F123.957','G1 X1.710 F97.309','G1 X1.921 F63.218','G1 X2.000 F23.731','G1 X1.938 F20.000','G1 X1.735 F60.719','G1 X1.404 F99.564','G1 X0.964 F132.001','G1 X0.446 F155.225','G1 X-0.111 F166.986','G1 X-0.663 F165.822','G1 X-1.167 F151.246','G1 X-1.580 F123.866','G1 X-1.865 F85.422','G1 X-1.994 F38.723','G1 X-1.952 F20.000','G1 X-1.739 F63.976','G1 X-1.369 F111.010','G1 X-0.872 F149.137','G1 X-0.291 F174.439','G1 X0.323 F183.991','G1 X0.910 F176.228','G1 X1.414 F151.198','G1 X1.783 F110.682','G1 X1.977 F58.132','G1 X1.972 F20.000','G1 X1.763 F62.494','G1 X1.369 F118.291','G1 X0.826 F162.789','G1 X0.191 F190.723','G1 X-0.471 F198.382','G1 X-1.084 F184.140','G1 X-1.580 F148.786','G1 X-1.899 F95.602','G1 X-1.999 F30.134','G1 X-1.865 F40.314','G1 X-1.507 F107.460','G1 X-0.964 F163.003','G1 X-0.298 F199.662','G1 X0.409 F212.169','G1 X1.070 F198.080','G1 X1.597 F158.272','G1 X1.921 F97.045','G1 X1.993 F21.761','G1 X1.800 F57.965','G1 X1.362 F131.448','G1 X0.734 F188.351','G1 X0.000 F220.174','G1 X-0.739 F221.576','G1 X-1.376 F191.346','G1 X-1.819 F132.829','G1 X-1.998 F53.702','G1 X-1.882 F34.924','G1 X-1.482 F119.989','G1 X-0.854 F188.389','G1 X-0.090 F229.015','G1 X0.692 F234.627','G1 X1.369 F203.235','G1 X1.831 F138.720','G1 X2.000 F50.535','G1 X1.841 F47.549','G1 X1.376 F139.512','G1 X0.677 F209.679','G1 X-0.141 F245.431','G1 X-0.939 F239.569','G1 X-1.579 F191.874','G1 X-1.944 F109.526','G1 X-1.965 F20.000','G1 X-1.631 F100.005','G1 X-0.999 F189.803','G1 X-0.178 F246.103','G1 X0.680 F257.414','G1 X1.414 F220.312','G1 X1.883 F140.519','G1 X1.990 F32.262','G1 X1.710 F84.088','G1 X1.091 F185.753','G1 X0.251 F252.005','G1 X-0.644 F268.480','G1 X-1.412 F230.450','G1 X-1.893 F144.286','G1 X-1.982 F26.668','G1 X-1.654 F98.437','G1 X-0.972 F204.557','G1 X-0.078 F268.324','G1 X0.838 F274.735','G1 X1.574 F220.872','G1 X1.965 F117.134','G1 X1.916 F20.000','G1 X1.434 F144.810','G1 X0.620 F243.961','G1 X-0.340 F288.170','G1 X-1.226 F265.701','G1 X-1.826 F180.178','G1 X-1.995 F50.429','G1 X-1.683 F93.377','G1 X-0.961 F216.583','G1 X-0.000 F288.391','G1 X0.966 F289.713','G1 X1.694 F218.494','G1 X1.997 F90.997','G1 X1.792 F61.553','G1 X1.124 F200.400','G1 X0.161 F289.047','G1 X-0.849 F302.988','G1 X-1.638 F236.754','G1 X-1.992 F106.207','G1 X-1.810 F54.850','G1 X-1.132 F203.156','G1 X-0.141 F297.552','G1 X0.895 F310.544','G1 X1.683 F236.619','G1 X1.999 F94.730','G1 X1.745 F76.114','G1 X0.988 F227.297','G1 X-0.060 F314.385','G1 X-1.095 F310.375','G1 X-1.810 F214.428','G1 X-1.987 F53.185','G1 X-1.566 F126.178','G1 X-0.668 F269.501','G1 X0.439 F332.024','G1 X1.414 F292.642','G1 X1.952 F161.450','G1 X1.878 F22.214','G1 X1.208 F201.141','G1 X0.148 F317.915','G1 X-0.964 F333.496','G1 X-1.766 F240.677','G1 X-1.991 F67.678','G1 X-1.559 F129.857','G1 X-0.604 F286.448','G1 X0.558 F348.497','G1 X1.535 F292.985','G1 X1.990 F136.515','G1 X1.760 F68.946','G1 X0.917 F252.870','G1 X-0.251 F350.278','G1 X-1.334 F324.969','G1 X-1.946 F183.516','G1 X-1.860 F25.542','G1 X-1.101 F227.785','G1 X0.063 F349.205','G1 X1.208 F343.513','G1 X1.909 F210.335','G1 X1.899 F20.000','G1 X1.174 F217.634','G1 X0.000 F352.061','G1 X-1.178 F353.281','G1 X-1.905 F218.278','G1 X-1.895 F20.000','G1 X-1.143 F225.660','G1 X0.063 F361.687','G1 X1.248 F355.416','G1 X1.937 F206.700','G1 X1.846 F27.068','G1 X1.005 F252.372','G1 X-0.251 F376.722','G1 X-1.407 F346.926','G1 X-1.982 F172.559','G1 X-1.729 F75.952','G1 X-0.746 F295.057','G1 X0.558 F391.071','G1 X1.627 F320.661','G1 X1.998 F111.224','G1 X1.502 F148.715','G1 X0.348 F346.293','G1 X-0.964 F393.324','G1 X-1.851 F266.280','G1 X-1.914 F20.000','G1 X-1.116 F239.495','G1 X0.191 F391.967','G1 X1.414 F367.048','G1 X1.991 F173.144','G1 X1.648 F102.861','G1 X0.536 F333.679','G1 X-0.831 F410.179','G1 X-1.810 F293.585','G1 X-1.930 F36.136','G1 X-1.126 F241.158','G1 X0.223 F404.838','G1 X1.468 F373.501','G1 X1.999 F159.238','G1 X1.547 F135.479','G1 X0.328 F365.898','G1 X-1.059 F415.993','G1 X-1.918 F257.660','G1 X-1.810 F32.431','G1 X-0.780 F308.766','G1 X0.651 F429.550','G1 X1.751 F330.000','G1 X1.946 F58.265','G1 X1.124 F246.435','G1 X-0.291 F424.403','G1 X-1.555 F379.451','G1 X-1.995 F132.015','G1 X-1.367 F188.441','G1 X0.000 F410.178','G1 X1.371 F411.278','G1 X1.997 F187.720','G1 X1.527 F141.045','G1 X0.211 F394.736','G1 X-1.226 F430.961','G1 X-1.980 F226.110','G1 X-1.620 F108.001','G1 X-0.340 F383.810','G1 X1.137 F443.025','G1 X1.965 F248.390','G1 X1.660 F91.435','G1 X0.390 F381.068','G1 X-1.112 F450.368','G1 X-1.963 F255.301','G1 X-1.654 F92.551','G1 X-0.360 F388.266','G1 X1.153 F453.910','G1 X1.975 F246.567','G1 X1.602 F112.006','G1 X0.251 F405.289','G1 X-1.257 F452.401','G1 X-1.993 F220.736','G1 X-1.494 F149.871','G1 X-0.060 F429.974','G1 X1.414 F442.357','G1 X1.999 F175.416','G1 X1.315 F205.160','G1 X-0.211 F457.737','G1 X-1.605 F418.174','G1 X-1.965 F107.982','G1 X-1.048 F274.909','G1 X0.556 F481.133','G1 X1.798 F372.643','G1 X1.854 F20.000','G1 X0.677 F352.942','G1 X-0.955 F489.648','G1 X-1.948 F298.141','G1 X-1.627 F96.491','G1 X-0.198 F428.589','G1 X1.369 F470.195','G1 X1.998 F188.817','G1 X1.248 F225.283','G1 X-0.372 F485.950','G1 X-1.735 F408.930','G1 X-1.882 F43.911','G1 X-0.699 F354.914','G1 X0.983 F504.594','G1 X1.966 F294.950','G1 X1.539 F128.103','G1 X-0.000 F461.827','G1 X-1.543 F462.788','G1 X-1.963 F126.012','G1 X-0.944 F305.712','G1 X0.773 F515.133','G1 X1.921 F344.130','G1 X1.638 F84.637','G1 X0.128 F453.112','G1 X-1.482 F482.966','G1 X-1.973 F147.349','G1 X-0.964 F302.836','G1 X0.785 F524.570','G1 X1.933 F344.490','G1 X1.590 F103.156','G1 X0.010 F473.836','G1 X-1.580 F477.109','G1 X-1.933 F105.915','G1 X-0.762 F351.444','G1 X1.016 F533.340','G1 X1.988 F291.476','G1 X1.369 F185.523','G1 X-0.353 F516.484','G1 X-1.792 F431.894','G1 X-1.777 F20.000','G1 X-0.310 F440.112','G1 X1.414 F517.380','G1 X1.975 F168.231','G1 X0.899 F322.791','G1 X-0.928 F548.127','G1 X-1.981 F315.957','G1 X-1.369 F183.652','G1 X0.402 F531.293','G1 X1.835 F429.788','G1 X1.703 F39.361','G1 X0.111 F477.834','G1 X-1.580 F507.251','G1 X-1.905 F97.466','G1 X-0.572 F399.825','G1 X1.263 F550.692','G1 X1.992 F218.656','G1 X0.964 F308.561','G1 X-0.921 F565.470','G1 X-1.988 F320.082','G1 X-1.277 F213.465','G1 X0.584 F558.378','G1 X1.921 F400.833','G1 X1.515 F121.651','G1 X-0.273 F536.453','G1 X-1.814 F462.246','G1 X-1.687 F37.981','G1 X0.000 F506.192']
cmd=['G21 G90 G17 G94 G54','G0 X0.000','G1 X0.500 F149.944','G1 X0.972 F141.747','G1 X1.385 F123.957','G1 X1.710 F97.309','G1 X1.921 F63.218','G1 X2.000 F23.731','G1 X1.938 F20.000','G1 X1.735 F60.719','G1 X1.404 F99.564','G1 X0.964 F132.001','G1 X0.446 F155.225','G1 X-0.111 F166.986','G1 X-0.663 F165.822','G1 X-1.167 F151.246','G1 X-1.580 F123.866','G1 X-1.865 F85.422','G1 X-1.994 F38.723','G1 X-1.952 F20.000','G1 X-1.739 F63.976','G1 X-1.369 F111.010','G1 X-0.872 F149.137','G1 X-0.291 F174.439','G1 X0.323 F183.991','G1 X0.910 F176.228','G1 X1.414 F151.198','G1 X1.783 F110.682']
# sys.stderr.write('grbl_streamer.py: starting\n')
print 'grbl_streamer.py: starting\n'
# sys.stderr.flush()

try:

    # Wake up grbl
    s.write("\r\n\r\n")
    time.sleep(2)   # Wait for grbl to initialize
    s.flushInput()  # Flush startup text in serial input
    count=0
    run_gcode(['G21 G90 G17 G94 G54','G0 X0.000'])
    cmd_buffer=[]
    while True:

        next_line = sys.stdin.readline().strip()

        if "kill" in next_line:
            s.close()
            sys.stdout.write("Actually killed\n")
            # print "Actually killed"
            break
        elif "is_running" in next_line:
            sys.stdout.write(is_running and "Is Running" or "Is Not Running")
            print is_running and "Is Running" or "Is Not Running"

        else:
            print next_line
            output=run_gcode([next_line])

except KeyboardInterrupt:
    print "\n\n"+("*"*50)
    print "\nKilling Motor Control And Closing Connection..."
    s.close()
    print "\nConnection Closed"
    print "\n"+("*"*50)
    print "\n\nGoodbye"

s.close()