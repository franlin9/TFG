#!/usr/bin/env python3

import sys
import argparse

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log

import time
from jetracer.nvidia_racecar import NvidiaRacecar

# Crear una instancia del robot
car = NvidiaRacecar()

car.steering = 0.1

def avanzar(tiempo, velocidad=0.32):
    print("Avanzar")
    car.steering = 0.1
    car.throttle = velocidad
    time.sleep(tiempo)
    car.throttle = 0

def girar_derecha(tiempo, angulo=0.6):
    print("Girar a la derecha")
    car.steering = angulo
    car.throttle = 0.32  # Mantener algo de velocidad para el giro
    time.sleep(tiempo)
    car.steering = -0.1  # Enderezar
    car.throttle = 0  # Detener después del giro

def esquivar_obstaculo():
    avanzar(4)             # Avanzar por 2 segundos
    girar_derecha(2)       # Girar a la derecha por 1 segundo
    avanzar(3)             # Avanzar por 2 segundos después del giro
    print("Maniobra de esquivar completada")

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=detectNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage())

parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

try:
	args = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# create video sources and outputs
input = videoSource(args.input, argv=sys.argv)
#output = videoOutput(args.output, argv=sys.argv)
	
# load the object detection network
net = detectNet(args.network, sys.argv, args.threshold)

# note: to hard-code the paths to load a model, the following API can be used:
#
# net = detectNet(model="model/ssd-mobilenet.onnx", labels="model/labels.txt", 
#                 input_blob="input_0", output_cvg="scores", output_bbox="boxes", 
#                 threshold=args.threshold)

# Etiquetas de interés
desired_labels = ["car"]
n = 0;
# process frames until EOS or the user exits
while True:
    # capture the next image
    img = input.Capture()

    if img is None: # timeout
        continue  
        
    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay=args.overlay)
    
    # Filtrar y mostrar solo detecciones de interés
    filtered_detections = []
    for detection in detections:
        class_id = detection.ClassID
        label = net.GetClassDesc(class_id)
        print(f"Detected label: {label}")  # Línea de depuración
        if label in desired_labels:
            filtered_detections.append(detection)
            print("Se ha encontrado un coche")
            n = n + 1 ;
    if n == 1:
        print("Iniciandooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
        esquivar_obstaculo()
        print("Finalizandoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
        break
    # print the detections
    print("detected {:d} objects in image".format(len(filtered_detections)))

    for detection in filtered_detections:
        print(detection)

    # render the image
    #output.Render(img)

    # update the title bar
    #output.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    # exit on input/output EOS
    #if not input.IsStreaming() or not output.IsStreaming():
    if not input.IsStreaming():
        break
