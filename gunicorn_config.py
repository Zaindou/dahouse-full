import os

loglevel = "debug"
accesslog = "-"  # '-' significa salida estándar
errorlog = "-"  # '-' significa salida estándar

bind = "0.0.0.0:8080"
workers = 6
threads = 5
timeout = 120
