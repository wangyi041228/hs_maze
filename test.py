from time import perf_counter


line = r'                Info[0] = [entityName=移动 id=7 zone=PLAY zonePos=0 cardId=AV_760 player=1]'

time_a = perf_counter()
for _ in range(1000000):
    len(line) - len(line.lstrip())
time_b = perf_counter()
print(time_b - time_a, len(line) - len(line.lstrip()))


time_a = perf_counter()
for _ in range(1000000):
    len(line) - len(line.replace('    ', ''))
time_b = perf_counter()
print(time_b - time_a, len(line) - len(line.lstrip()))
